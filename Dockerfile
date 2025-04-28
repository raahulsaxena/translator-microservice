# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 5001

# Run app using gunicorn for better scalability
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "run:app"]