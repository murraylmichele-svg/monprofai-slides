import os
import re
import json
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

def parse_slides(content):
    """Parse Claude's output into individual slide blocks."""
    slides = []
    blocks = re.split(r'---DIAPOSITIVE \d+---', content)
    blocks = [b for b in blocks if b.strip() and '---FIN DIAPOSITIVE' in b]
    
    for block in blocks:
        slide = {}
        
        # Extract TYPE
        type_match = re.search(r'TYPE:\s*(.+)', block)
        slide['type'] = type_match.group(1).strip() if type_match else 'CONTENU'
        
        # Extract TITRE
        titre_match = re.search(r'TITRE:\s*(.+)', block)
        slide['titre'] = titre_match.group(1).strip() if titre_match else ''
        
        # Extract CONTENU
        contenu_match = re.search(r'CONTENU:\s*([\s\S]*?)NOTE_ENSEIGNANT:', block)
        if contenu_match:
            contenu = contenu_match.group(1).strip()
            contenu = re.sub(r'\*\*', '', contenu)
            contenu = re.sub(r'\\', '', contenu)
            slide['contenu'] = contenu
        else:
            slide['contenu'] = ''
        
        # Extract NOTE_ENSEIGNANT
        note_match = re.search(r'NOTE_ENSEIGNANT:\s*([\s\S]*?)---FIN DIAPOSITIVE', block)
        if note_match:
            note = note_match.group(1).strip()
            note = re.sub(r'\*\*', '', note)
            note = re.sub(r'\\', '', note)
            slide['note'] = note
        else:
            slide['note'] = ''
        
        if slide['titre']:
            slides.append(slide)
    
    return slides

def get_slides_service():
    """Create Google Slides API service using service account."""
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS environment variable not set")
    
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            'https://www.googleapis.com/auth/presentations',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    return build('slides', 'v1', credentials=creds), build('drive', 'v3', credentials=creds)

def create_presentation(title, slides_data, folder_id):
    """Create a Google Slides presentation from parsed slide data."""
    slides_service, drive_service = get_slides_service()
    
    # Create blank presentation
    presentation = slides_service.presentations().create(
        body={'title': title}
    ).execute()
    
    presentation_id = presentation['presentationId']
    
    # Delete the default blank slide
    default_slide_id = presentation['slides'][0]['objectId']
    
    requests = [{'deleteObject': {'objectId': default_slide_id}}]
    
    # Build all slide requests in one batch
    for i, slide in enumerate(slides_data):
        slide_id = f'slide_{i}'
        title_id = f'title_{i}'
        body_id = f'body_{i}'
        notes_id = f'notes_{i}'
        
        is_title_slide = slide['type'] == 'TITRE'
        
        # Create slide
        requests.append({
            'createSlide': {
                'objectId': slide_id,
                'insertionIndex': i,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                },
                'placeholderIdMappings': [
                    {
                        'layoutPlaceholder': {'type': 'TITLE', 'index': 0},
                        'objectId': title_id
                    },
                    {
                        'layoutPlaceholder': {'type': 'BODY', 'index': 0},
                        'objectId': body_id
                    }
                ]
            }
        })
        
        # Insert title text
        if slide['titre']:
            requests.append({
                'insertText': {
                    'objectId': title_id,
                    'text': slide['titre']
                }
            })
            
            # Style title
            requests.append({
                'updateTextStyle': {
                    'objectId': title_id,
                    'style': {
                        'fontSize': {'magnitude': 28 if is_title_slide else 22, 'unit': 'PT'},
                        'bold': True,
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize,bold,foregroundColor'
                }
            })
        
        # Insert body text
        if slide['contenu']:
            requests.append({
                'insertText': {
                    'objectId': body_id,
                    'text': slide['contenu']
                }
            })
            
            # Style body
            requests.append({
                'updateTextStyle': {
                    'objectId': body_id,
                    'style': {
                        'fontSize': {'magnitude': 16, 'unit': 'PT'},
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}
                    },
                    'textRange': {'type': 'ALL'},
                    'fields': 'fontSize,foregroundColor'
                }
            })
        
        # Set white background
        requests.append({
            'updateSlideProperties': {
                'objectId': slide_id,
                'slideProperties': {
                    'background': {
                        'solidFill': {
                            'color': {
                                'rgbColor': {'red': 1, 'green': 1, 'blue': 1}
                            }
                        }
                    }
                },
                'fields': 'background'
            }
        })
        
        # Add speaker notes
        if slide['note']:
            requests.append({
                'createShape': {
                    'objectId': notes_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': 100, 'unit': 'PT'}, 'height': {'magnitude': 100, 'unit': 'PT'}},
                        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 0, 'translateY': 0, 'unit': 'PT'}
                    }
                }
            })
    
    # Execute all requests in one batch
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()
    
    # Move to shared folder
    if folder_id:
        drive_service.files().update(
            fileId=presentation_id,
            addParents=folder_id,
            removeParents='root',
            fields='id, parents'
        ).execute()
    
    # Make it accessible
    drive_service.permissions().create(
        fileId=presentation_id,
        body={'type': 'anyone', 'role': 'writer'}
    ).execute()
    
    return f"https://docs.google.com/presentation/d/{presentation_id}/edit"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'MonProf.ai Slides Generator'})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        title = data.get('title', 'MonProf.ai — Leçon')
        content = data.get('content', '')
        folder_id = data.get('folder_id', os.environ.get('DRIVE_FOLDER_ID', ''))
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        # Parse slides
        slides_data = parse_slides(content)
        
        if not slides_data:
            return jsonify({'error': 'No slides parsed from content'}), 400
        
        # Create presentation
        slides_url = create_presentation(title, slides_data, folder_id)
        
        return jsonify({
            'success': True,
            'slides_url': slides_url,
            'slide_count': len(slides_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
