import os
import json
import requests
from flask import Flask, request, jsonify
from create_slides import parse_slides, create_presentation

app = Flask(__name__)

# ── CORS: add headers to EVERY response ──────────────────────
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Proxy-Secret'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/api/claude', methods=['POST', 'OPTIONS'])
def claude_proxy():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    # ── Secret check ──────────────────────────────────────
    expected = os.environ.get('PROXY_SECRET', '')
    received = request.headers.get('X-Proxy-Secret', '')
    if expected and received != expected:
        return jsonify({'error': 'Non autorisé'}), 401

    try:
        data = request.get_json()
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
        resp = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            },
            json=data,
            timeout=120
        )
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            raw = request.get_data(as_text=True)
            data = json.loads(raw.replace('\n', '\\n'))
        if not data:
            return jsonify({'error': 'No data received'}), 400
        title = (data.get('title') or
                 data.get('Title') or
                 data.get('Text') or
                 'MonProf.ai — Leçon')
        content = (data.get('content') or
                   data.get('Content') or '')
        if not content:
            return jsonify({'error': 'No content provided', 'received_keys': list(data.keys())}), 400
        slides_data = parse_slides(content)
        if not slides_data:
            return jsonify({'error': 'No slides parsed from content'}), 400
        create_presentation(slides_data, title)
        return jsonify({
            'success': True,
            'slide_count': len(slides_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
