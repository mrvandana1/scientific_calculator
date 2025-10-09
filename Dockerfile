# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY app/ ./app
# WORKDIR /app/app

# EXPOSE 5000

# # Use gunicorn for production
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
WORKDIR /app/app
EXPOSE 5000
CMD ["python", "app.py"]
