import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact,
)
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_object, save_numpy_arry_data, read_yaml_file


class DataTransformation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys) from e

    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates a complete preprocessing pipeline:
        - OneHotEncoding for categorical columns (with fixed categories)
        - StandardScaler & MinMaxScaler for numerical columns
        - Fully consistent across train/test
        """
        logging.info("Creating complete data transformation pipeline")

        try:
            num_features = self._schema_config["num_features"]
            mm_columns = self._schema_config["mm_columns"]

            vehicle_age_categories = ["< 1 Year", "1-2 Year", "> 2 Years"]
            gender_categories = ["Female", "Male"]
            damage_categories = ["No", "Yes"]

            preprocessor = ColumnTransformer(
                transformers=[
                    ("vehicle_age_ohe",
                    OneHotEncoder(categories=[vehicle_age_categories],
                                drop="first", sparse_output=False, handle_unknown="ignore"),
                    ["Vehicle_Age"]),

                    ("gender_ohe",
                    OneHotEncoder(categories=[gender_categories],
                                drop="first", sparse_output=False, handle_unknown="ignore"),
                    ["Gender"]),

                    ("damage_ohe",
                    OneHotEncoder(categories=[damage_categories],
                                drop="first", sparse_output=False, handle_unknown="ignore"),
                    ["Vehicle_Damage"]),

                    ("standard_scaler", StandardScaler(), num_features),
                    ("minmax_scaler", MinMaxScaler(), mm_columns),
                ],
                remainder="drop"   # <---- IMPORTANT: prevents duplicate columns
            )

            final_pipeline = Pipeline(steps=[("preprocessor", preprocessor)])
            return final_pipeline

           

        except Exception as e:
            logging.exception("Error occurred while creating data transformer object")
            raise MyException(e, sys) from e

    def _drop_id_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop the id column as per schema"""
        logging.info("Dropping 'id' column")
        drop_col = self._schema_config["drop_columns"]
        if drop_col in df.columns:
            df = df.drop(columns=[drop_col])
        return df

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Main method to execute the full data transformation pipeline
        """
        try:
            logging.info("Starting Data Transformation")

            if not self.data_validation_artifact.validation_status:
                raise Exception(f"Data validation failed: {self.data_validation_artifact.message}")

            # Read train and test data
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            logging.info("Train and test data loaded successfully")

            # Separate features and target
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Only drop id — everything else is handled by the pipeline
            input_feature_train_df = self._drop_id_column(input_feature_train_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)

            # Get the complete preprocessing pipeline
            preprocessor = self.get_data_transformer_object()
            logging.info("Preprocessing pipeline created")

            # Fit on train, transform both
            logging.info("Fitting preprocessor on training data")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

            logging.info(f"[TRAINED MODEL] x_test columns BEFORE transform: {input_feature_train_df.columns.tolist()}")
            logging.info(f"[TRAINED MODEL] x_test shape BEFORE transform: {input_feature_train_df.shape}")


            logging.info("Transforming test data")
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # Apply SMOTEENN for class imbalance
            logging.info("Applying SMOTEENN for handling class imbalance")
            smt = SMOTEENN(sampling_strategy="minority", random_state=42)

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            # Concatenate features and target
            train_arr = np.c_[
                input_feature_train_final, np.array(target_feature_train_final)
            ]
            test_arr = np.c_[
                input_feature_test_final, np.array(target_feature_test_final)
            ]

            # Save preprocessor object and transformed arrays
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )
            save_numpy_arry_data(
                self.data_transformation_config.transformed_train_file_path, train_arr
            )
            save_numpy_arry_data(
                self.data_transformation_config.transformed_test_file_path, test_arr
            )

            logging.info("Transformed data and preprocessor saved successfully")

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

        except Exception as e:
            logging.exception("Error in initiate_data_transformation")
            raise MyException(e, sys) from e