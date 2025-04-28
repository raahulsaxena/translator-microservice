from langdetect import detect
from transformers import pipeline
import redis
import hashlib
import os 


# translator_pipeline = pipeline("translation_en_to_fr")  # Example: English to French


LANGUAGE_TO_MODEL = {
    'fr': "Helsinki-NLP/opus-mt-fr-en",
    'de': "Helsinki-NLP/opus-mt-de-en",
    'es': "Helsinki-NLP/opus-mt-es-en",
    'hi': "Helsinki-NLP/opus-mt-hi-en",
    'it': "Helsinki-NLP/opus-mt-it-en",
    # 'pt': "Helsinki-NLP/opus-mt-pt-en",
    'ru': "Helsinki-NLP/opus-mt-ru-en",
    'zh': "Helsinki-NLP/opus-mt-zh-en",
    'ja': "Helsinki-NLP/opus-mt-ja-en",
    'ar': "Helsinki-NLP/opus-mt-ar-en",
}

# Preload common translation models at startup - global dictionary - code executed once per server process (per each worker process)
# PRELOADED_MODELS = {}
# for lang_code, model_name in LANGUAGE_TO_MODEL.items():
#     PRELOADED_MODELS[lang_code] = pipeline("translation", model=model_name)



# Global dictionary for loaded models
PRELOADED_MODELS = {}

def get_translator_pipeline(lang_code):
    # If model already loaded, reuse
    if lang_code in PRELOADED_MODELS:
        return PRELOADED_MODELS[lang_code]
    
    # Else, load it on demand
    model_name = LANGUAGE_TO_MODEL.get(lang_code)
    if not model_name:
        raise ValueError(f"No model available for detected language: {lang_code}")
    
    pipeline_model = pipeline("translation", model=model_name)
    PRELOADED_MODELS[lang_code] = pipeline_model
    
    return pipeline_model

def detect_language(text):
    return detect(text)

def translate_text(text):
    detected_lang = detect_language(text)

    # If already English, no translation needed
    if detected_lang == 'en':
        return text

    cache_key = generate_cache_key(text, 'en')
    cached_translation = r.get(cache_key)
    if cached_translation:
        return cached_translation.decode('utf-8')

    # Lazy-load pipeline
    translator_pipeline = get_translator_pipeline(detected_lang)
    
    result = translator_pipeline(text)
    translated_text = result[0]['translation_text']

    r.set(cache_key, translated_text)

    return translated_text



# Connect to Redis server
r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'), 
    port=int(os.getenv('REDIS_PORT', 6379)), 
    db=0
)

# Function to generate a cache key based on input text and target language
def generate_cache_key(text, target_lang):
    key = f"{text}:{target_lang}"
    return hashlib.sha256(key.encode()).hexdigest()