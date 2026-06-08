FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure the vulnerable flag ships inside the container in the working directory
COPY flag.txt .

EXPOSE 8000

CMD ["python", "app.py"]

