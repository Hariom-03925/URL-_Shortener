# app/main.py

from flask import Flask, request, jsonify, redirect
from app.utils import generate_short_code, is_valid_url
from app.models import save_url, get_url, increment_click, get_stats

app = Flask(__name__)

@app.route("/")
def health_check():
    return jsonify({"status": "healthy", "service": "URL Shortener API"})

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400

    original_url = data["url"]
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    save_url(short_code, original_url)

    short_url = f"{request.host_url}{short_code}"
    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@app.route("/<short_code>")
def redirect_to_url(short_code):
    entry = get_url(short_code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    increment_click(short_code)
    return redirect(entry["original_url"])

@app.route("/api/stats/<short_code>")
def get_url_stats(short_code):
    stats = get_stats(short_code)
    if not stats:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": stats["original_url"],
        "created_at": stats["created_at"],
        "clicks": stats["click_count"]
    })
