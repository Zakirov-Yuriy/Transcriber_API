FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*


# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import whisper; whisper.load_model('tiny')"

# Копируем код
COPY . /app
WORKDIR /app

# Запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
