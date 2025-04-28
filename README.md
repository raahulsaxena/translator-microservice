# Translator Microservice

A lightweight and scalable microservice that automatically translates text into English from multiple supported languages using pre-trained NLP models.

## Features
- Detects input text language automatically (using langdetect).
- Translates to English using Hugging Face models (Helsinki-NLP/opus-mt-XX-en).
- Supports 10+ major languages (French, Spanish, Hindi, German, etc).
- Caches translations using Redis for faster subsequent retrieval.
- Containerized with Docker, scalable with Gunicorn.
- Lightweight and optimized for minimal memory overhead.


 ## Tech Stack
 - Python 3.11 (slim image)
 - Flask (for REST API)
 - Gunicorn (for scalable WSGI server)
 - Transformers (for translation pipelines)
 - Redis (for caching translations)
 - Docker & Docker Compose


## API Endpoints

| Method | Endpoint       | Description                                |
|:-------|:---------------|:-------------------------------------------|
| POST   | `/translate`    | Translate given text to English            |
| GET    | `/health`       | Check if the service and models are healthy|
| GET    | `/cache-keys`   | (Optional) View all keys in Redis cache    |
| GET    | `/cache/<key>`  | (Optional) Get specific cached translation |

## Setup and Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/translator-microservice.git
cd translator-microservice
```
2. Create .env file (optional)
Set environment variables if needed, e.g., Redis host/port.

3. Build and run with Docker Compose
```bash
docker-compose up --build
```
This will spin up:
	•	translator-service (Flask + Gunicorn app)
	•	redis (for caching)

Service will be available at:
👉 http://localhost:5001


## Example Request
- Translate Text
```bash
curl -X POST http://localhost:5001/translate -H "Content-Type: application/json" -d '{"text": "Bonjour tout le monde"}'
```
- Response
```json
{
  "translated_text": "Hello everyone"
}
```

## 🧠 Development Notes
- Models are lazily loaded on first request to optimize memory and startup time.
- Redis cache uses generated keys based on original text to speed up translations.

## Useful Commands
1. See all keys in Redis
```bash
docker-compose exec redis redis-cli
> KEYS *
```

2. Flush all REDIS data (use carefully)

```bash
docker-compose exec redis redis-cli FLUSHALL
```


## Future Improvements
- Add API authentication (e.g., API keys).
- Support batch translation for multiple texts in one request.
- Auto-scale with Kubernetes readiness probes (/health endpoint ready).
- Handle fallback when a model isn’t available.



## 👨‍💻 Author
Made with ❤️ by Rahul Saxena
