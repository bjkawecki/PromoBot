FROM python:3.11-slim

WORKDIR /app

# Zuerst nur requirements kopieren und installieren (wenn requirements.txt im Root liegt)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Den gesamten Code kopieren: sowohl 'src/' als auch 'dev_runner.py'
COPY src ./src
COPY .env .

# Optional: PYTHONPATH, falls deine Module in src sind
ENV PYTHONPATH=/app/src

# Default CMD (kann angepasst werden, z.B. "python dev_runner.py")
CMD ["python", "src/main.py"]
