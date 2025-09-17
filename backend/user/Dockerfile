FROM python:3.13-slim

WORKDIR /app/user

COPY backend/requirements.txt /app/requirements.txt
COPY backend/core /app/core
COPY backend/user /app/user

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]