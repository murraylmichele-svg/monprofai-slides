import os
import json
from flask import Flask, request, jsonify
from create_slides import parse_slides, create_presentation

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'MonProf.ai Slides Generator'})

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
