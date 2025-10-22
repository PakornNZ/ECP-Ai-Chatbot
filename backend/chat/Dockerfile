FROM python:3.13-slim

WORKDIR /app/chat

COPY backend/chat/requirements.txt /app/requirements.txt
COPY backend/core /app/core
COPY backend/response /app/response
COPY backend/chat .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8020"]