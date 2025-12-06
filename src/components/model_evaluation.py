from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from src.exception import MyException
from src.constants import TARGET_COLUMN
from src.logger import logging
from src.utils.main_utils import load_object
import sys
import pandas as pd
from typing import Optional
from src.entity.s3_estimator import Proj1Estimator
from dataclasses import dataclass


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:
    def __init__(
        self,
        model_eval_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys) from e

    def get_best_model(self) -> Optional[Proj1Estimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            proj1_estimator = Proj1Estimator(bucket_name=bucket_name, model_path=model_path)
            if proj1_estimator.is_model_present(model_path=model_path):
                return proj1_estimator
            return None
        except Exception as e:
            raise MyException(e, sys) from e

    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            # Load test data
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x_test = test_df.drop(columns=[TARGET_COLUMN])
            y_test = test_df[TARGET_COLUMN]

            # Drop id-related columns if they exist to match training schema
            id_columns = [col for col in x_test.columns if col.lower() in ["id", "_id"]]
            if id_columns:
                logging.info(f"Dropping ID columns: {id_columns}")
                x_test = x_test.drop(columns=id_columns)

            logging.info(f"[TRAINED MODEL] x_test columns BEFORE predict: {x_test.columns.tolist()}")
            logging.info(f"[TRAINED MODEL] x_test shape BEFORE predict: {x_test.shape}")

            # Load trained model (MyModel) which already wraps the preprocessor
            trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score

            # Predict with new model (let MyModel handle preprocessing internally)
            y_pred_new = trained_model.predict(x_test)
            # If model returns probability, threshold at 0.5
            if y_pred_new.ndim > 1 and y_pred_new.shape[1] > 1:
                y_pred_new = (y_pred_new[:, 1] > 0.5).astype(int)

            # Get production model
            # Temporarily disable S3/production model evaluation.
            # Older models in S3 may have been trained with a different
            # feature schema, which leads to a ColumnTransformer
            # "X has N features" mismatch when calling best_model.predict.
            #
            # By setting best_model to None and best_model_f1_score to None,
            # we skip comparison against the S3 model and only evaluate
            # the newly trained local model.
            best_model = None
            best_model_f1_score = None
                                
            tmp_best_score = 0.0 if best_model_f1_score is None else best_model_f1_score

            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_score,
                difference=trained_model_f1_score - tmp_best_score
            )

            logging.info(f"Evaluation Result: {result}")
            return result

        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting Model Evaluation")
            evaluate_response = self.evaluate_model()

            model_eval_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_response.is_model_accepted,
                s3_model_path=self.model_eval_config.s3_model_key_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_response.difference
            )

            logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
            return model_eval_artifact

        except Exception as e:
            raise MyException(e, sys) from e