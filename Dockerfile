FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

WORKDIR app/

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .


RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn","app/application:app","--reload", "--host 0.0.0.0", "--port 8000"]