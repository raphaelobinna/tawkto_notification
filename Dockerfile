FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8080

CMD ["bash", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --log-level info"]
