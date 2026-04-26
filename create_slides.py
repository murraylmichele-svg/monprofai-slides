
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
NOTE_ENSEIGNANT: Présenter les objectifs en adaptant le vocabulaire selon les besoins. Expliquer que nous allons voyager dans le temps pour découvrir comment nos ancêtres faisaient du commerce bien avant l'invention de l'argent moderne.
---FIN DIAPOSITIVE 1---

---DIAPOSITIVE 2---
TYPE: AMORCE
TITRE: Que savez-vous déjà ?
CONTENU:
- Réflexion : Comment obtenez-vous ce dont vous avez besoin aujourd'hui ?
- Dans le passé, il n'y avait pas de magasins comme maintenant
- Les peuples devaient échanger pour survivre
- Question : Avez-vous déjà échangé quelque chose avec un ami ?
NOTE_ENSEIGNANT: Encourager les élèves à partager leurs expériences d'échange (cartes, jouets, collations). Faire le lien avec le concept de troc. Activer leurs connaissances sur les moyens d'obtenir des biens aujourd'hui versus dans le passé.
---FIN DIAPOSITIVE 2---

---DIAPOSITIVE 3---
TYPE: CONTENU
TITRE: Qu'est-ce que le troc ?
CONTENU:
- Le troc : échanger des biens ou services sans utiliser d'argent
- Exemple : échanger des fourrures contre des outils
- Pratiqué par toutes les sociétés anciennes du monde
- Les Premières Nations échangeaient des produits de la chasse
- Les Inuit troquaient de l'huile de phoque et de l'ivoire
NOTE_ENSEIGNANT: Utiliser des exemples concrets et visuels. Expliquer que chaque société avait des ressources différentes selon son environnement. Montrer des images d'objets échangés si possible. Souligner l'ingéniosité de ce système.
---FIN DIAPOSITIVE 3---

---DIAPOSITIVE 4---
TYPE: CONTENU
TITRE: Pourquoi faire du commerce ?
CONTENU:
- Obtenir des ressources non disponibles dans sa région
- Améliorer sa qualité de vie
- Créer des liens avec d'autres peuples
- Partager des connaissances et des innovations
- Exemples : épices d'Asie, fourrures du Nord, métaux précieux
NOTE_ENSEIGNANT: Utiliser une carte pour montrer comment différentes régions produisaient différentes ressources. Expliquer le concept de spécialisation géographique. Faire comprendre que le commerce était une nécessité, pas un luxe.
---FIN DIAPOSITIVE 4---

---DIAPOSITIVE 5---
TYPE: CONTENU
TITRE: La Route de la Soie : une route commerciale légendaire
CONTENU:
- Réseau de routes commerciales entre l'Europe et l'Asie
- Longue de plus de 6 000 kilomètres
- Active pendant plus de 1 500 ans
- Nom vient de la soie chinoise, produit très prisé
- Permettait d'échanger soie, épices, métaux, idées
NOTE_ENSEIGNANT: Utiliser une carte pour tracer la Route de la Soie. Expliquer que ce n'était pas une seule route mais un réseau. Insister sur la durée exceptionnelle de cette route commerciale et son impact sur le développement des civilisations.
---FIN DIAPOSITIVE 5---

---DIAPOSITIVE 6---
TYPE: CONTENU
TITRE: Les innovations qui facilitaient le commerce
CONTENU:
- Développement de moyens de transport : chameaux, navires
- Création de cartes plus précises
- Invention de la boussole pour la navigation
- Construction de routes et de ponts
- Développement de systèmes de mesure standardisés
NOTE_ENSEIGNANT: Expliquer comment chaque innovation résolvait un problème spécifique du commerce. Montrer des exemples visuels des innovations. Faire le lien avec les attentes sur les innovations scientifiques et technologiques des sociétés anciennes.
---FIN DIAPOSITIVE 6---

---DIAPOSITIVE 7---
TYPE: CONTENU
TITRE: Le commerce créait de la coopération
CONTENU:
- Formation d'alliances entre peuples commerçants
- Négociations pacifiques pour établir les prix
- Partage de connaissances et de technologies
- Création de langues commerciales communes
- Établissement de règles commerciales acceptées par tous
NOTE_ENSEIGNANT: Donner des exemples concrets de coopération. Expliquer comment les intérêts commerciaux mutuels encourageaient la paix. Souligner que le commerce était souvent plus profitable que la guerre.
---FIN DIAPOSITIVE 7---

---DIAPOSITIVE 8---
TYPE: CONTENU
TITRE: Mais le commerce causait aussi des conflits
CONTENU:
- Disputes sur les prix et la qualité des marchandises
- Conflits pour contrôler les routes commerciales importantes
- Jalousie entre peuples riches et pauvres
- Attaques de bandits sur les caravanes
- Guerres pour s'emparer des ressources précieuses
NOTE_ENSEIGNANT: Expliquer que les mêmes routes qui apportaient la richesse pouvaient causer des problèmes. Donner des exemples historiques de conflits liés au commerce. Faire comprendre que la richesse attirait aussi les convoitises.
---FIN DIAPOSITIVE 8---

---DIAPOSITIVE 9---
TYPE: CONTENU
TITRE: Le commerce chez les Premières Nations et les Inuit
CONTENU:
- Vastes réseaux d'échange à travers l'Amérique du Nord
- Les Premières Nations échangeaient fourrures, cuivre, coquillages
- Les Inuit troquaient huile de phoque, ivoire, fourrures d'ours
- Routes commerciales suivaient les rivières et côtes
- Rencontres commerciales lors de grandes assemblées
NOTE_ENSEIGNANT: Utiliser une carte de l'Amérique du Nord pour montrer les routes commerciales autochtones. Expliquer l'ingéniosité de ces systèmes bien avant l'arrivée des Européens. Valoriser ces connaissances ancestrales.
---FIN DIAPOSITIVE 9---

---DIAPOSITIVE 10---
TYPE: PRATIQUE_GUIDÉE
TITRE: Analysons ensemble une situation commerciale
CONTENU:
- Scénario : Des marchands veulent traverser le territoire d'un autre peuple
- Questions à explorer :
- Quels avantages chaque groupe peut-il tirer de cet échange ?
- Quels problèmes pourraient survenir ?
- Comment éviter les conflits ?
NOTE_ENSEIGNANT: Présenter le scénario et guider l'analyse collective. Encourager les élèves à proposer des solutions. Faire ressortir les principes de négociation et de respect mutuel. Lier aux situations historiques réelles.
---FIN DIAPOSITIVE 10---

---DIAPOSITIVE 11---
TYPE: DISCUSSION
TITRE: Le commerce aujourd'hui et autrefois
CONTENU:
- En équipes, comparez :
- Comment obtenait-on des biens autrefois vs aujourd'hui ?
- Quels avantages et défis dans chaque époque ?
- Le commerce cause-t-il encore des conflits aujourd'hui ?
- Que peut-on apprendre du passé ?
NOTE_ENSEIGNANT: Former des équipes hétérogènes. Circuler pour soutenir les discussions. Encourager les liens entre passé et présent. Préparer les équipes à partager une idée principale en plénière.
---FIN DIAPOSITIVE 11---

---DIAPOSITIVE 12---
TYPE: RÉSUMÉ
TITRE: Ce que nous avons appris aujourd'hui
CONTENU:
- Le troc était essentiel à la survie des sociétés anciennes
- La Route de la Soie montre l'importance du commerce international
- Les innovations technologiques facilitaient les échanges
- Le commerce créait à la fois coopération et conflits
- Les peuples autochtones avaient des systèmes commerciaux sophistiqués
NOTE_ENSEIGNANT: Récapituler les apprentissages en sollicitant la participation des élèves. Valoriser leurs contributions. Présenter les billets de sortie comme des choix équivalents : "Choisissez le défi qui vous intéresse le plus aujourd'hui !" Aucun défi n'est plus facile ou difficile, ils explorent simplement le sujet de façons différentes.

DÉFI 1
1. Qu'est-ce que le troc ?
2. Nomme deux choses que les Inuit échangeaient.
3. Vrai ou faux : La Route de la Soie était une seule route.
4. Donne un exemple de coopération dans le commerce ancien.

DÉFI 2
1. Explique pourquoi les peuples anciens faisaient du commerce avec d'autres régions.
2. Décris deux innovations qui aidaient les marchands sur la Route de la Soie.
3. Comment le commerce pouvait-il créer des conflits entre les peuples ?
4. Compare le système d'échange des Premières Nations avec celui d'aujourd'hui.

DÉFI 3
1. Analyse pourquoi la Route de la Soie a été active pendant plus de 1500 ans.
2. Justifie cette affirmation : "Le commerce était plus profitable que la guerre."
3. Évalue l'impact des innovations technologiques sur le développement du commerce ancien.
4. Propose des stratégies que les peuples anciens auraient pu utiliser pour éviter les conflits commerciaux.
---FIN DIAPOSITIVE 12---


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
    service_account_data = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
    if service_account_data:
        from google.oauth2 import service_account
        info = json.loads(service_account_data)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES)
        return creds
    # Local fallback — uses OAuth for desktop use
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
        note_m = re.search(r'NOTE_ENSEIGNANT:\s*([\s\S]*?)(?=---FIN|\Z)', block)

        contenu = contenu_m.group(1).strip() if contenu_m else ''
        # Render inline fraction tokens
        import re
        contenu = re.sub(
            r'\[FRACTION:(\d+)/(\d+)\]',
            lambda m: f'{m.group(1)}\n—\n{m.group(2)}',
            contenu
        )
        note    = note_m.group(1).strip()    if note_m    else ''
        visuel  = visuel_m.group(1).strip()  if visuel_m  else 'aucun'

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

# ── DIAGRAM BUILDERS ────────────────────────────────────────────────────────

def draw_angle(requests, slide_id, idx, angle_deg, label, ox, oy, length=120):
    """Draw a single angle with two arms and a label."""
    rad = math.radians(angle_deg)
    x2 = ox + int(length * math.cos(rad))
    y2 = oy - int(length * math.sin(rad))

    line1_id = f'line_base_{idx}_{angle_deg}'
    line2_id = f'line_arm_{idx}_{angle_deg}'
    label_id = f'label_{idx}_{angle_deg}'

    # Base arm (horizontal)
    requests.append({'createLine': {
        'objectId': line1_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(length), 'unit': 'EMU'},
                     'height': {'magnitude': 1, 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(ox), 'translateY': emu(oy),
                          'unit': 'EMU'}}}})

    # Second arm
    arm_w = abs(x2 - ox) if x2 != ox else 1
    arm_h = abs(y2 - oy) if y2 != oy else 1
    requests.append({'createLine': {
        'objectId': line2_id,
        'lineCategory': 'STRAIGHT',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(arm_w), 'unit': 'EMU'},
                     'height': {'magnitude': emu(arm_h), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(min(ox, x2)),
                          'translateY': emu(min(oy, y2)),
                          'unit': 'EMU'}}}})

    # Label
    requests.append({'createShape': {
        'objectId': label_id,
        'shapeType': 'TEXT_BOX',
        'elementProperties': {
            'pageObjectId': slide_id,
            'size': {'width': {'magnitude': emu(100), 'unit': 'EMU'},
                     'height': {'magnitude': emu(25), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1,
                          'translateX': emu(ox),
                          'translateY': emu(oy + 10),
                          'unit': 'EMU'}}}})
    requests.append({'insertText': {'objectId': label_id, 'text': label}})
    requests.append({'updateTextStyle': {
        'objectId': label_id,
        'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 11, 'unit': 'PT'},
                  'bold': True,
                  'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.2, 'blue': 0.8}}}},
        'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

def add_diagram(requests, slide_id, visuel, i):
    """Route to the correct diagram builder based on visuel tag."""

    # Diagram area: right half of slide
    # x starts at ~370pt, y from 80pt, width ~310pt, height ~270pt
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

    elif visuel == 'rapporteur':
        # Draw a simple semicircle representation as text label
        box_id = f'rapporteur_{i}'
        requests.append({'createShape': {
            'objectId': box_id,
            'shapeType': 'ARC',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': emu(200), 'unit': 'EMU'},
                         'height': {'magnitude': emu(100), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1,
                              'translateX': emu(base_x + 50),
                              'translateY': emu(base_y + 80),
                              'unit': 'EMU'}}}})
        requests.append({'updateShapeProperties': {
            'objectId': box_id,
            'shapeProperties': {
                'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 0.9, 'green': 0.95, 'blue': 1}}}},
                'outline': {'outlineFill': {'solidFill': {'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0.8}}}},
                            'weight': {'magnitude': 2, 'unit': 'PT'}}},
            'fields': 'shapeBackgroundFill,outline'}})

        lbl_id = f'rapporteur_lbl_{i}'
        requests.append({'createShape': {
            'objectId': lbl_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': emu(200), 'unit': 'EMU'},
                         'height': {'magnitude': emu(30), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1,
                              'translateX': emu(base_x + 50),
                              'translateY': emu(base_y + 185),
                              'unit': 'EMU'}}}})
        requests.append({'insertText': {'objectId': lbl_id, 'text': 'Rapporteur — 0° à 180°'}})
        requests.append({'updateTextStyle': {
            'objectId': lbl_id,
            'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 12, 'unit': 'PT'}, 'bold': True,
                      'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0.8}}}},
            'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

    elif visuel == 'droite_numerique':
        line_id = f'numline_{i}'
        requests.append({'createLine': {
            'objectId': line_id,
            'lineCategory': 'STRAIGHT',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': emu(260), 'unit': 'EMU'},
                         'height': {'magnitude': 1, 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1,
                              'translateX': emu(base_x + 20),
                              'translateY': emu(base_y + 130),
                              'unit': 'EMU'}}}})
        for n in range(11):
            tick_id = f'tick_{i}_{n}'
            lbl_id  = f'ticklbl_{i}_{n}'
            x = base_x + 20 + n * 26
            requests.append({'createLine': {
                'objectId': tick_id,
                'lineCategory': 'STRAIGHT',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': 1, 'unit': 'EMU'},
                             'height': {'magnitude': emu(10), 'unit': 'EMU'}},
                    'transform': {'scaleX': 1, 'scaleY': 1,
                                  'translateX': emu(x),
                                  'translateY': emu(base_y + 125),
                                  'unit': 'EMU'}}}})
            requests.append({'createShape': {
                'objectId': lbl_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': emu(24), 'unit': 'EMU'},
                             'height': {'magnitude': emu(18), 'unit': 'EMU'}},
                    'transform': {'scaleX': 1, 'scaleY': 1,
                                  'translateX': emu(x - 8),
                                  'translateY': emu(base_y + 138),
                                  'unit': 'EMU'}}}})
            requests.append({'insertText': {'objectId': lbl_id, 'text': str(n)}})
            requests.append({'updateTextStyle': {
                'objectId': lbl_id,
                'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 10, 'unit': 'PT'}},
                'fields': 'fontFamily,fontSize'}})

    elif visuel.startswith('fraction_'):
        parts = visuel.split('_')
        num = parts[1] if len(parts) > 1 else '1'
        den = parts[2] if len(parts) > 2 else '2'
        frac_id = f'frac_{i}'
        requests.append({'createShape': {
            'objectId': frac_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {'width': {'magnitude': emu(150), 'unit': 'EMU'},
                         'height': {'magnitude': emu(100), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1,
                              'translateX': emu(base_x + 80),
                              'translateY': emu(base_y + 80),
                              'unit': 'EMU'}}}})
        requests.append({'insertText': {'objectId': frac_id, 'text': f'{num}\n—\n{den}'}})
        requests.append({'updateTextStyle': {
            'objectId': frac_id,
            'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 48, 'unit': 'PT'}, 'bold': True,
                      'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0.1, 'green': 0.1, 'blue': 0.5}}}},
            'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

    elif visuel == 'plan_cartesien':
        cx = base_x + 150
        cy = base_y + 150
        axis_len = 120
        for axis_id, w, h, tx, ty in [
            (f'xaxis_{i}', axis_len * 2, 1, cx - axis_len, cy),
            (f'yaxis_{i}', 1, axis_len * 2, cx, cy - axis_len),
        ]:
            requests.append({'createLine': {
                'objectId': axis_id,
                'lineCategory': 'STRAIGHT',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': emu(w), 'unit': 'EMU'},
                             'height': {'magnitude': emu(h), 'unit': 'EMU'}},
                    'transform': {'scaleX': 1, 'scaleY': 1,
                                  'translateX': emu(tx), 'translateY': emu(ty),
                                  'unit': 'EMU'}}}})
        for lbl, lx, ly in [('x', cx + axis_len + 5, cy - 8), ('y', cx + 5, cy - axis_len - 20)]:
            lbl_id = f'axislbl_{i}_{lbl}'
            requests.append({'createShape': {
                'objectId': lbl_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {'width': {'magnitude': emu(20), 'unit': 'EMU'},
                             'height': {'magnitude': emu(20), 'unit': 'EMU'}},
                    'transform': {'scaleX': 1, 'scaleY': 1,
                                  'translateX': emu(lx), 'translateY': emu(ly),
                                  'unit': 'EMU'}}}})
            requests.append({'insertText': {'objectId': lbl_id, 'text': lbl}})
            requests.append({'updateTextStyle': {
                'objectId': lbl_id,
                'style': {'fontFamily': 'Arial', 'fontSize': {'magnitude': 14, 'unit': 'PT'}, 'bold': True},
                'fields': 'fontFamily,fontSize,bold'}})

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
    # Make it publicly readable so Slides API can fetch it
    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    return f'https://drive.google.com/uc?export=download&id={file_id}'
    def render_inline_fractions(drive_service, text, slide_requests, slide_id, box_id, font_size):
    """
    Parse [FRACTION:num/den] tokens in text and build a sequence of
    text boxes + inline fraction images to replace them.
    Renders the text as segments separated by fraction images.
    """
    import re
    pattern = r'\[FRACTION:(\d+)/(\d+)\]'
    parts = re.split(pattern, text)
    
    x_cursor = 20  # starting x position in points
    y_pos = 80     # y position in points
    segment_width = 320
    
    # Just render the text with fraction tokens replaced by unicode approximation
    # for now - full inline rendering requires complex positioning
    clean_text = re.sub(pattern, lambda m: f'{m.group(1)}/{m.group(2)}', text)
    return clean_text
# ── MAIN ────────────────────────────────────────────────────────────────────

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
        slide_id  = f'slide_{i}'
        is_title  = slide['type'] == 'TITRE'
        is_defis  = slide['type'] == 'DEFIS'
        has_visuel = slide.get('visuel', 'aucun') not in ('aucun', '', None)
        font_size = auto_font_size(slide['contenu'])

        requests.append({'createSlide': {
            'objectId': slide_id,
            'insertionIndex': i,
            'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})

        requests.append({'updatePageProperties': {
            'objectId': slide_id,
            'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}}},
            'fields': 'pageBackgroundFill'}})

        # Title box — full width always
        titre_id = f'titre_{i}'
        requests.append({'createShape': {
            'objectId': titre_id,
            'shapeType': 'TEXT_BOX',
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
                (f'defi1_{i}', emu(20),  '⭐ Défi 1\n\n'    + slide.get('defi1', ''), ),
                (f'defi2_{i}', emu(245), '⭐⭐ Défi 2\n\n'  + slide.get('defi2', ''), ),
                (f'defi3_{i}', emu(470), '⭐⭐⭐ Défi 3\n\n' + slide.get('defi3', ''), ),
            ]
            for col_id, col_x, col_text in cols:
                requests.append({'createShape': {
                    'objectId': col_id,
                    'shapeType': 'TEXT_BOX',
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
                        'fontFamily': 'Arial',
                        'fontSize': {'magnitude': 14, 'unit': 'PT'},
                        'bold': False,
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
                    'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

        else:
            # Content box — left half if visual, full width otherwise
            content_width = 340 if has_visuel else 680
            if slide['contenu']:
                contenu_id = f'contenu_{i}'
                requests.append({'createShape': {
                    'objectId': contenu_id,
                    'shapeType': 'TEXT_BOX',
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
                        'fontFamily': 'Arial',
                        'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                        'bold': False,
                        'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
                    'fields': 'fontFamily,fontSize,bold,foregroundColor'}})

            # Draw diagram on right half if visuel tag present
            if has_visuel:
                diagram_paths = diagram_generator.generate_all()
                visuel_key = slide['visuel']
                if visuel_key in diagram_paths:
                    image_url = upload_image_to_drive(drive_service, diagram_paths[visuel_key])
                    img_id = f'img_{i}'
                    requests.append({'createImage': {
                        'objectId': img_id,
                        'url': image_url,
                        'elementProperties': {
                            'pageObjectId': slide_id,
                            'size': {
                                'width':  {'magnitude': emu(300), 'unit': 'EMU'},
                                'height': {'magnitude': emu(220), 'unit': 'EMU'}
                            },
                            'transform': {
                                'scaleX': 1, 'scaleY': 1,
                                'translateX': emu(370),
                                'translateY': emu(90),
                                'unit': 'EMU'
                            }
                        }
                    }})

    slides_service.presentations().batchUpdate(
        presentationId=pres_id,
        body={'requests': requests}
    ).execute()

    # Speaker notes
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

TEST_MATH = """
---DIAPOSITIVE 1---
TYPE: CONTENU
TITRE: Les types d'angles
CONTENU:
- Un angle se forme quand deux droites se rencontrent
- On mesure les angles en degrés (°)
- Il existe quatre types d'angles principaux
VISUEL: types_angles
NOTE_ENSEIGNANT: Montrez chaque type d'angle avec le rapporteur.
---DIAPOSITIVE 2---
TYPE: CONTENU
TITRE: L'angle droit
CONTENU:
- L'angle droit mesure exactement 90°
- On le reconnaît par son symbole carré
- Exemples : coins d'une feuille, murs d'une pièce
VISUEL: angle_droit
NOTE_ENSEIGNANT: Faites trouver des angles droits dans la classe.
"""

if __name__ == '__main__':
    slides = parse_slides(CLAUDE_OUTPUT)
    create_presentation(slides, 'Les Acadiens')
