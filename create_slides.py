import re
import os
import math
import io
from googleapiclient.http import MediaIoBaseUpload
import diagram_generator
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import json
import tempfile

OAUTH_CLIENT_FILE = None
TOKEN_FILE = os.path.join(tempfile.gettempdir(), 'token.json')

_oauth_data = os.environ.get('GOOGLE_OAUTH_CLIENT')
if _oauth_data:
    _tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    _tmp.write(_oauth_data)
    _tmp.close()
    OAUTH_CLIENT_FILE = _tmp.name
else:
    OAUTH_CLIENT_FILE = r'C:\Users\murra\OneDrive\Desktop\MonProf-Slides\oauth_client.json'
    TOKEN_FILE = r'C:\Users\murra\OneDrive\Desktop\MonProf-Slides\token.json'

SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
OUTPUT_FOLDER_ID = '13qSBTeNOaAEpdxEsDwF7vGj-9MJx2zxE'

CLAUDE_OUTPUT = """NOMBRE DE DIAPOSITIVES : 12 | MATIÈRE : Études sociales | ATTENTE : Décrire diverses situations qui engendraient des relations de coopération ou des conflits dans les sociétés anciennes

---DIAPOSITIVE 1---
TYPE: TITRE
TITRE: Le troc et les routes commerciales : coopération et conflits dans les sociétés anciennes
CONTENU:
- Objectifs d'aujourd'hui :
- Comprendre ce qu'est le troc et son importance
- Découvrir la célèbre Route de la Soie
- Explorer comment le commerce créait coopération et conflits
- Analyser les innovations qui facilitaient les échanges
NOTE_ENSEIGNANT: Présenter les objectifs en adaptant le vocabulaire selon les besoins.
---FIN DIAPOSITIVE 1---
"""

def emu(pt):
    return int(pt * 12700)

def auto_font_size(text):
    length = len(text)
    if length < 200:
        return 24
    elif length < 400:
        return 20
    else:
        return 18

def get_credentials():
    import json
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    # First try: use OAuth token (personal Gmail account)
    token_data = os.environ.get('GOOGLE_TOKEN')
    if token_data:
        token_dict = json.loads(token_data)
        creds = Credentials(
            token=token_dict.get('token'),
            refresh_token=token_dict.get('refresh_token'),
            token_uri=token_dict.get('token_uri'),
            client_id=token_dict.get('client_id'),
            client_secret=token_dict.get('client_secret'),
            scopes=token_dict.get('scopes')
        )
        if creds.expired or not creds.valid:
            creds.refresh(Request())
        return creds

    # Second try: use service account
    service_account_data = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
    if service_account_data:
        from google.oauth2 import service_account
        info = json.loads(service_account_data)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES)
        return creds

    # Local fallback
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def extract_defis(text):
    defi1 = defi2 = defi3 = None
    d1 = re.search(r'\*{0,2}DÉFI 1\*{0,2}[^\n]*\n([\s\S]*?)(?=\*{0,2}DÉFI 2|$)', text)
    d2 = re.search(r'\*{0,2}DÉFI 2\*{0,2}[^\n]*\n([\s\S]*?)(?=\*{0,2}DÉFI 3|$)', text)
    d3 = re.search(r'\*{0,2}DÉFI 3\*{0,2}[^\n]*\n([\s\S]*?)(?=---FIN|$)', text)
    if d1: defi1 = d1.group(1).strip()
    if d2: defi2 = d2.group(1).strip()
    if d3: defi3 = d3.group(1).strip()
    return defi1, defi2, defi3

def parse_slides(text):
    slides = []
    defi1, defi2, defi3 = extract_defis(text)

    blocks = re.split(r'---DIAPOSITIVE \d+---', text)
    for block in blocks:
        if len(block.strip()) < 10:
            continue
        if 'TYPE:' not in block:
            continue
        titre_check = re.search(r'TITRE:\s*(.+)', block)
        if not titre_check:
            continue
        type_m    = re.search(r'TYPE:\s*(.+)', block)
        titre_m   = re.search(r'TITRE:\s*(.+)', block)
        contenu_m = re.search(r'CONTENU:\s*([\s\S]*?)(?=VISUEL:|NOTE_ENSEIGNANT:|\Z)', block)
        visuel_m  = re.search(r'VISUEL:\s*(.+)', block)
        note_m    = re.search(r'NOTE_ENSEIGNANT:\s*([\s\S]*?)(?=---FIN|\Z)', block)

        contenu = contenu_m.group(1).strip() if contenu_m else ''
        contenu = re.sub(
            r'\[FRACTION:(\d+)/(\d+)\]',
            lambda m: f'{m.group(1)}\n—\n{m.group(2)}',
            contenu
        )
        note   = note_m.group(1).strip()   if note_m   else ''
        visuel = visuel_m.group(1).strip() if visuel_m else 'aucun'

        for pattern in [r'DÉFI \d+[^:]*:[\s\S]*']:
            contenu = re.sub(pattern, '', contenu).strip()
            note    = re.sub(pattern, '', note).strip()

        slides.append({
            'type':    type_m.group(1).strip() if type_m else 'CONTENU',
            'titre':   titre_m.group(1).strip() if titre_m else '',
            'contenu': contenu,
            'note':    note,
            'visuel':  visuel,
        })

    if any([defi1, defi2, defi3]):
        slides.append({
            'type':    'DEFIS',
            'titre':   'Choisis ton défi ! 🎯',
            'contenu': '',
            'note':    '',
            'visuel':  'aucun',
            'defi1':   defi1 or '',
            'defi2':   defi2 or '',
            'defi3':   defi3 or '',
        })

    return slides

# ── DIAGRAM BUILDERS ─────────────────────────────────────────────────────────

def draw_angle(requests, slide_id, idx, angle_deg, label, ox, oy, length=120):
    rad = math.radians(angle_deg)
    x2 = ox + int(length * math.cos(rad))
    y2 = oy - int(length * math.sin(rad))
    line1_id = f'line_base_{idx}_{angle_deg}'
    line2_id = f'line_arm_{idx}_{angle_deg}'
    label_id = f'label_{idx}_{angle_deg}'
    requests.append({'createLine': {
        'objectId': line1_id, 'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(length), 'unit': 'EMU'},
                     'height': {'magnitude': 1, 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(ox), 'translateY': emu(oy),
                          'unit': 'EMU'}}}})
    arm_w = abs(x2 - ox) if x2 != ox else 1
    arm_h = abs(y2 - oy) if y2 != oy else 1
    requests.append({'createLine': {
        'objectId': line2_id, 'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(arm_w), 'unit': 'EMU'},
                     'height': {'magnitude': emu(arm_h), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(min(ox, x2)),
                          'translateY': emu(min(oy, y2)),
                          'unit': 'EMU'}}}})
    requests.append({'createShape': {
        'objectId': label_id, 'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(100), 'unit': 'EMU'},
                     'height': {'magnitude': emu(25), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(ox), 'translateY': emu(oy + 10),
                          'unit': 'EMU'}}}})
    requests.append({'insertText': {'objectId': label_id, 'text': label}})
    requests.append({'updateTextStyle': {
        'objectId': label_id,
        'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 11, 'unit': 'PT'},
                  'bold': True,
                  'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.8}}}},
        'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

def add_diagram(requests, slide_id, visuel, i):
    base_x = 370
    base_y = 80
    if visuel == 'types_angles':
        configs = [
            (30,  'Aigu\n< 90°',   base_x + 10,  base_y + 20),
            (90,  'Droit\n= 90°',  base_x + 90,  base_y + 20),
            (120, 'Obtus\n> 90°',  base_x + 170, base_y + 20),
            (180, 'Plat\n= 180°',  base_x + 250, base_y + 20),
        ]
        for deg, lbl, ox, oy in configs:
            draw_angle(requests, slide_id, i, deg, lbl, ox, oy, length=60)
    elif visuel == 'angle_aigu':
        draw_angle(requests, slide_id, i, 45, 'Angle aigu\n45°', base_x + 80, base_y + 120, length=100)
    elif visuel == 'angle_droit':
        draw_angle(requests, slide_id, i, 90, 'Angle droit\n90°', base_x + 80, base_y + 120, length=100)
    elif visuel == 'angle_obtus':
        draw_angle(requests, slide_id, i, 120, 'Angle obtus\n120°', base_x + 80, base_y + 120, length=100)
    elif visuel == 'angle_plat':
        draw_angle(requests, slide_id, i, 180, 'Angle plat\n180°', base_x + 40, base_y + 120, length=160)

def upload_image_to_drive(drive_service, image_path):
    """Upload a PNG file to Drive and return a publicly accessible URL."""
    file_metadata = {
        'name': os.path.basename(image_path),
        'parents': [OUTPUT_FOLDER_ID]
    }
    with open(image_path, 'rb') as f:
        media = MediaIoBaseUpload(io.BytesIO(f.read()), mimetype='image/png')
    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    file_id = uploaded['id']
    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    return f'https://drive.google.com/uc?export=download&id={file_id}'

def render_inline_fractions(text):
    """Replace [FRACTION:num/den] tokens with num/den plain text."""
    return re.sub(
        r'\[FRACTION:(\d+)/(\d+)\]',
        lambda m: f'{m.group(1)}/{m.group(2)}',
        text
    )

# ── MAIN ─────────────────────────────────────────────────────────────────────

def create_presentation(slide_data, title):
    creds = get_credentials()
    slides_service = build('slides', 'v1', credentials=creds)
    drive_service  = build('drive',  'v3', credentials=creds)

    file_metadata = {
        'name': title,
        'mimeType': 'application/vnd.google-apps.presentation',
        'parents': [OUTPUT_FOLDER_ID]
    }
    pres_file = drive_service.files().create(body=file_metadata, fields='id').execute()
    pres_id   = pres_file['id']

    pres = slides_service.presentations().get(presentationId=pres_id).execute()
    default_slide_id = pres['slides'][0]['objectId']
    requests = [{'deleteObject': {'objectId': default_slide_id}}]

    for i, slide in enumerate(slide_data):
        slide_id   = f'slide_{i}'
        is_title   = slide['type'] == 'TITRE'
        is_defis   = slide['type'] == 'DEFIS'
        has_visuel = slide.get('visuel', 'aucun') not in ('aucun', '', None)
        font_size  = auto_font_size(slide['contenu'])

        requests.append({'createSlide': {
            'objectId': slide_id,
            'insertionIndex': i,
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})

        requests.append({'updatePageProperties': {
            'objectId': slide_id,
            'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}}},
            'fields': 'pageBackgroundFill'}})

        titre_id = f'titre_{i}'
        requests.append({'createShape': {
            'objectId': titre_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': emu(680), 'unit': 'EMU'},
                         'height': {'magnitude': emu(55), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1,
                              'translateX': emu(20), 'translateY': emu(12),
                              'unit': 'EMU'}}}})
        requests.append({'insertText': {'objectId': titre_id, 'text': slide['titre']}})
        requests.append({'updateTextStyle': {
            'objectId': titre_id,
            'style': {
                'fontFamily': 'Arial',
                'fontSize': {'magnitude': 28 if is_title else 20, 'unit': 'PT'},
                'bold': True,
                'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
            'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

        if is_defis:
            col_width  = emu(210)
            col_height = emu(280)
            col_top    = emu(80)
            cols = [
                (f'defi1_{i}', emu(20),  '⭐ Défi 1\n\n'    + slide.get('defi1', '')),
                (f'defi2_{i}', emu(245), '⭐⭐ Défi 2\n\n'  + slide.get('defi2', '')),
                (f'defi3_{i}', emu(470), '⭐⭐⭐ Défi 3\n\n' + slide.get('defi3', '')),
            ]
            for col_id, col_x, col_text in cols:
                requests.append({'createShape': {
                    'objectId': col_id, 'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': col_width, 'unit': 'EMU'},
                                 'height': {'magnitude': col_height, 'unit': 'EMU'}},
                        'transform': {'scaleX': 1, 'scaleY': 1,
                                      'translateX': col_x, 'translateY': col_top,
                                      'unit': 'EMU'}}}})
                requests.append({'insertText': {'objectId': col_id, 'text': col_text}})
                requests.append({'updateTextStyle': {
                    'objectId': col_id,
                    'style': {
                        'fontFamily': 'Arial', 'fontSize': {'magnitude': 14, 'unit': 'PT'},
                        'bold': False,
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
                    'fields': 'fontFamily,fontSize,bold,foregroundColor'}})
        else:
            content_width = 340 if has_visuel else 680
            if slide['contenu']:
                contenu_id = f'contenu_{i}'
                requests.append({'createShape': {
                    'objectId': contenu_id, 'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {'width': {'magnitude': emu(content_width), 'unit': 'EMU'},
                                 'height': {'magnitude': emu(270), 'unit': 'EMU'}},
                        'transform': {'scaleX': 1, 'scaleY': 1,
                                      'translateX': emu(20), 'translateY': emu(80),
                                      'unit': 'EMU'}}}})
                requests.append({'insertText': {'objectId': contenu_id, 'text': slide['contenu']}})
                requests.append({'updateTextStyle': {
                    'objectId': contenu_id,
                    'style': {
                        'fontFamily': 'Arial', 'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                        'bold': False,
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
                    'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

            if has_visuel:
                visuel_key = slide['visuel']
                diagram_path = diagram_generator.generate_diagram(visuel_key)
                if diagram_path:
                    image_url = upload_image_to_drive(drive_service, diagram_path)
                    img_id = f'img_{i}'
                    requests.append({'createImage': {
                        'objectId': img_id,
                        'url': image_url,
                        'elementProperties': {
                            'pageObjectId': slide_id,
                            'size': {
                                'width':  {'magnitude': emu(300), 'unit': 'EMU'},
                                'height': {'magnitude': emu(220), 'unit': 'EMU'}},
                            'transform': {
                                'scaleX': 1, 'scaleY': 1,
                                'translateX': emu(370), 'translateY': emu(90),
                                'unit': 'EMU'}}}})

    slides_service.presentations().batchUpdate(
        presentationId=pres_id,
        body={'requests': requests}
    ).execute()

    pres = slides_service.presentations().get(presentationId=pres_id).execute()
    notes_requests = []
    for i, slide in enumerate(slide_data):
        if slide.get('note'):
            notes_page_id = pres['slides'][i]['slideProperties']['notesPage']['notesProperties']['speakerNotesObjectId']
            notes_requests.append({'insertText': {
                'objectId': notes_page_id,
                'text': slide['note']}})
    if notes_requests:
        slides_service.presentations().batchUpdate(
            presentationId=pres_id,
            body={'requests': notes_requests}
        ).execute()

    print(f'Done: https://docs.google.com/presentation/d/{pres_id}/edit')

if __name__ == '__main__':
    slides = parse_slides(CLAUDE_OUTPUT)
    create_presentation(slides, 'Test')
