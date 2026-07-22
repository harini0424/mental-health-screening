FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='j-hartmann/emotion-english-distilroberta-base', local_dir='./emotion_model')"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]