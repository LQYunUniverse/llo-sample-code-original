# Dockerfile for chat_completion.py
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r Real-Time-Latent-Consistency-Model/server/requirements.txt
RUN pip install --no-cache-dir openai websockets python-dotenv pyserial

CMD ["python", "chat_completion.py"]