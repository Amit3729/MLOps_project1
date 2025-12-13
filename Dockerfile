# DEBUG LINES – remove them after it works
RUN echo "=== LISTING ALL FILES IN /app ==="  
RUN ls -la /app  
RUN echo "=== TRYING TO SHOW requirements.txt ===" && cat /app/requirements.txt || echo "FILE NOT FOUND"