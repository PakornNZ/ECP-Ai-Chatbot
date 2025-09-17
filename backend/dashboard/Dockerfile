FROM python:3.13-slim

WORKDIR /app/dashboard

RUN apt-get update && apt-get install -y poppler-utils

COPY backend/dashboard/requirements.txt /app/requirements.txt
COPY backend/core /app/core
COPY backend/dashboard /app/dashboard

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8030

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8030"]