FROM python:3.13-slim

WORKDIR /app/data

COPY backend/requirements.txt /app/requirements.txt
COPY backend/core /app/core
COPY backend/data .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]