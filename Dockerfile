FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# System packages required for audio, image and PDF processing
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        espeak \
        espeak-ng \
        libespeak1 \
        libsndfile1 \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Temporary working directory
RUN mkdir -p /tmp/telegram_bot

# Start bot
CMD ["python", "bot.py"]
