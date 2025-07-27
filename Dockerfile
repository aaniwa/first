FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Render will detect port from this dummy server
CMD ["python", "bot.py"]
