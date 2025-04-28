
from flask import Blueprint, request, jsonify
from .translator import detect_language, translate_text

bp = Blueprint('routes', __name__)

@bp.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400
    language = detect_language(text)
    return jsonify({"language": language})


@bp.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400
    translated = translate_text(text)
    return jsonify({"translated_text": translated})