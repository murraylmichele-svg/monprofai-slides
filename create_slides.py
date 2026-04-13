
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

OAUTH_CLIENT_FILE = r'C:\Users\murra\OneDrive\Desktop\MonProf-Slides\client_secret_683032921562-bt2e92mvt6lse0j1l5if8hcs6ao1qd3g.apps.googleusercontent.com.json'
TOKEN_FILE = r'C:\Users\murra\OneDrive\Desktop\MonProf-Slides\token.json'
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
OUTPUT_FOLDER_ID = '13qSBTeNOaAEpdxEsDwF7vGj-9MJx2zxE'

CLAUDE_OUTPUT = """
NOMBRE DE DIAPOSITIVES : 18 | MATIÈRE : Études sociales | ATTENTE : Analyser l'information recueillie pour en faire l'interprétation en utilisant divers outils organisationnels

---DIAPOSITIVE 1---
TYPE: TITRE
TITRE: Analyser l'information historique avec des outils organisationnels
CONTENU:
• Apprendre à organiser et analyser l'information historique
• Utiliser différents outils : lignes de temps, tableaux comparatifs, cartes, œuvres d'art
• Exemple principal : l'histoire des Acadiens
• Objectifs différenciés selon ton choix de défi !

NOTE_ENSEIGNANT: Expliquez aux élèves qu'ils pourront choisir leur niveau de défi à la fin selon leur confiance et leurs préférences. Tous les défis sont valorisés également - c'est une question de choix personnel, pas de niveau.

---DIAPOSITIVE 2---
TYPE: AMORCE
TITRE: Que savez-vous déjà ?
CONTENU:
• Quand vous voulez comprendre une histoire, comment organisez-vous les informations ?
• Avez-vous déjà entendu parler des Acadiens ?
• Quels outils utilisez-vous pour organiser vos idées ? (dessins, listes, calendriers...)
• Discussion en équipes de 2 minutes

NOTE_ENSEIGNANT: Circulez et écoutez les réponses. Notez les outils mentionnés au tableau. Cela servira de pont vers les outils organisationnels formels. Encouragez toutes les réponses sans jugement.

---DIAPOSITIVE 3---
TYPE: CONTENU
TITRE: Qu'est-ce qu'un outil organisationnel ?
CONTENU:
• Un outil qui aide à classer, comparer et comprendre l'information
• Exemples : ligne de temps, tableau comparatif, carte annotée, analyse d'œuvre d'art
• Chaque outil a un but spécifique
• Ils nous aident à devenir de meilleurs historiens !

NOTE_ENSEIGNANT: Reliez aux exemples donnés par les élèves à l'amorce. Expliquez que ces outils aident non seulement à organiser mais aussi à analyser - c'est-à-dire à comprendre les causes, conséquences et liens entre les événements.

---DIAPOSITIVE 4---
TYPE: CONTENU
TITRE: Qui étaient les Acadiens ?
CONTENU:
• Premiers colons français en Amérique du Nord (1604)
• Installés en Acadie (actuelle Nouvelle-Écosse, Nouveau-Brunswick)
• Agriculteurs et pêcheurs pacifiques
• Neutres dans les conflits entre France et Angleterre
• Population d'environ 18 000 personnes vers 1750

NOTE_ENSEIGNANT: Montrez la région de l'Acadie sur une carte du Canada. Insistez sur leur neutralité - concept important pour comprendre l'injustice de la déportation qui suivra.

---DIAPOSITIVE 5---
TYPE: CONTENU
TITRE: Outil 1 : La ligne de temps - La Grande Déportation
CONTENU:
• 1755 : Début de la déportation des Acadiens
• 1755-1764 : Dispersion forcée de 11 500 Acadiens
• 1764 : Fin officielle de la déportation
• 1764-1800 : Retour graduel de certains Acadiens
• Utilité : voir l'ordre chronologique des événements

NOTE_ENSEIGNANT: Dessinez cette ligne de temps au tableau ou affichez-la. Expliquez que la ligne de temps aide à visualiser la durée des événements et leur séquence. Soulignez que la déportation a duré près de 10 ans.

---DIAPOSITIVE 6---
TYPE: CONTENU
TITRE: Pourquoi utiliser une ligne de temps ?
CONTENU:
• Montre l'ordre chronologique des événements
• Aide à voir la durée des périodes importantes
• Permet de comprendre les causes et conséquences
• Facilite la comparaison entre différentes époques
• Exemple : comprendre que la déportation n'était pas un événement d'une journée

NOTE_ENSEIGNANT: Demandez aux élèves de réfléchir à ce qu'ils ressentiraient si leur famille était séparée pendant 10 ans. Cela aide à comprendre l'impact humain révélé par la ligne de temps.

---DIAPOSITIVE 7---
TYPE: CONTENU
TITRE: Outil 2 : Le tableau comparatif - Points de vue sur la déportation
CONTENU:
• Compare différentes perspectives sur le même événement
• Colonne 1 : Point de vue britannique
• Colonne 2 : Point de vue acadien
• Permet de voir que l'histoire a plusieurs versions
• Aide à développer l'esprit critique

NOTE_ENSEIGNANT: Préparez un tableau à deux colonnes au tableau. Dans les prochaines diapositives, vous le remplirez avec les élèves. Insistez sur l'importance de comprendre différents points de vue.

---DIAPOSITIVE 8---
TYPE: CONTENU
TITRE: Remplissons notre tableau comparatif
CONTENU:
• Point de vue britannique : "Les Acadiens refusent de prêter serment à la Couronne britannique"
• Point de vue acadien : "Nous voulons rester neutres et garder notre religion"
• Point de vue britannique : "C'est une mesure de sécurité militaire"
• Point de vue acadien : "C'est une injustice - nous sommes pacifiques"

NOTE_ENSEIGNANT: Remplissez le tableau avec les élèves. Expliquez que les deux points de vue peuvent contenir des vérités partielles. L'important est de comprendre pourquoi chaque groupe pensait ainsi selon leur situation.

---DIAPOSITIVE 9---
TYPE: CONTENU
TITRE: Outil 3 : L'analyse de cartes - Dispersion des Acadiens
CONTENU:
• Les cartes montrent où les Acadiens ont été envoyés
• Colonies américaines, Louisiane, France, Antilles
• Distance géographique = séparation des familles
• Certaines régions plus accueillantes que d'autres
• Les cartes révèlent l'ampleur géographique de la tragédie

NOTE_ENSEIGNANT: Utilisez une carte de l'Amérique du Nord pour montrer les différentes destinations. Calculez avec les élèves les distances approximatives. Cela concrétise l'ampleur de la dispersion.

---DIAPOSITIVE 10---
TYPE: CONTENU
TITRE: Que nous apprend l'analyse de cartes ?
CONTENU:
• Information géographique : où, distances, frontières
• Impact humain : séparation, adaptation, voyage difficile
• Contexte politique : quels territoires étaient disponibles
• Conséquences à long terme : nouvelles communautés acadiennes
• Les cartes racontent une histoire de mouvement et de survie

NOTE_ENSEIGNANT: Encouragez les élèves à réfléchir à ce que représentaient ces déplacements pour des familles entières. Reliez à leurs propres expériences de déménagement si pertinent.

---DIAPOSITIVE 11---
TYPE: CONTENU
TITRE: Outil 4 : L'analyse d'œuvres d'art - "Le Grand Dérangement"
CONTENU:
• Les peintures et sculptures racontent aussi l'histoire
• Émotions représentées : tristesse, séparation, espoir
• Détails importants : vêtements, objets, expressions
• Perspective de l'artiste : comment il voit l'événement
• L'art aide à comprendre l'impact émotionnel

NOTE_ENSEIGNANT: Si possible, montrez des reproductions d'œuvres sur la déportation acadienne (ex: tableaux de Claude Picard). Guidez l'observation : que voyez-vous ? Que ressentent les personnages ? Que veut nous dire l'artiste ?

---DIAPOSITIVE 12---
TYPE: CONTENU
TITRE: Comment analyser une œuvre d'art historique ?
CONTENU:
• Observer : que voit-on exactement ?
• Interpréter : que nous dit l'artiste ?
• Contextualiser : quand et pourquoi l'œuvre fut créée ?
• Comparer : avec d'autres sources sur le même événement
• Questionner : quelle émotion l'artiste veut-il transmettre ?

NOTE_ENSEIGNANT: Modelez cette démarche avec une œuvre sur les Acadiens. Posez les questions à voix haute et répondez-y partiellement, laissant les élèves compléter vos observations.

---DIAPOSITIVE 13---
TYPE: PRATIQUE_GUIDÉE
TITRE: À votre tour - Créons ensemble une ligne de temps
CONTENU:
• Sujet : le retour des Acadiens après 1764
• 1764 : Permission de revenir
• 1765-1785 : Premières vagues de retour
• 1785 : Fondation de nouvelles communautés
• En équipes : placez ces événements sur votre ligne de temps

NOTE_ENSEIGNANT: Distribuez du papier et des crayons. Circulez pour aider. Certains élèves peuvent avoir besoin d'aide pour l'espacement proportionnel des dates. Valorisez les efforts de tous.

---DIAPOSITIVE 14---
TYPE: PRATIQUE_GUIDÉE
TITRE: Pratiquons le tableau comparatif
CONTENU:
• Nouveau sujet : l'adaptation des Acadiens dans leurs nouveaux territoires
• Comparez : défis rencontrés vs opportunités trouvées
• En équipes, remplissez votre tableau
• Pensez aux aspects : langue, religion, travail, communauté

NOTE_ENSEIGNANT: Laissez 8-10 minutes pour cette activité. Passez d'équipe en équipe pour guider sans donner les réponses. Encouragez la réflexion et l'utilisation de leurs connaissances antérieures.

---DIAPOSITIVE 15---
TYPE: DISCUSSION
TITRE: Partageons nos découvertes
CONTENU:
• Présentez vos lignes de temps et tableaux
• Qu'avez-vous appris de nouveau sur les Acadiens ?
• Quel outil vous a le mieux aidé à comprendre ?
• Comment ces outils changent-ils notre compréhension de l'histoire ?

NOTE_ENSEIGNANT: Animez un partage de 10-12 minutes. Valorisez chaque contribution. Aidez les élèves à articuler comment chaque outil révèle des aspects différents de la même histoire.

---DIAPOSITIVE 16---
TYPE: DISCUSSION
TITRE: Réflexion sur nos apprentissages
CONTENU:
• Dans quelles autres situations pourriez-vous utiliser ces outils ?
• Ligne de temps : votre vie familiale, l'histoire de l'école
• Tableau comparatif : comparer des options, des personnages
• Analyse de cartes : comprendre l'actualité, la géographie
• Analyse d'art : comprendre d'autres cultures, époques

NOTE_ENSEIGNANT: Guidez vers des applications concrètes dans leur vie. Ces outils ne servent pas qu'en histoire ! Encouragez la créativité dans leurs suggestions d'utilisation.

---DIAPOSITIVE 17---
TYPE: RÉSUMÉ
TITRE: Ce que nous avons appris aujourd'hui
CONTENU:
• Les outils organisationnels nous aident à analyser l'information
• Ligne de temps : ordre chronologique et durée
• Tableau comparatif : différents points de vue
• Analyse de cartes : information géographique et déplacements
• Analyse d'art : émotions et perspectives artistiques
• L'exemple des Acadiens montre l'importance de ces outils

NOTE_ENSEIGNANT: Récapitulez en montrant comment chaque outil a révélé des aspects différents de l'histoire acadienne. Préparez-vous à présenter les choix de billets de sortie de manière positive et encourageante.

---DIAPOSITIVE 18---
TYPE: RÉSUMÉ
TITRE: Choisis ton défi - Billet de sortie !
CONTENU:
• Trois défis disponibles - choisis selon ta confiance !
• Défi 1 : Questions de reconnaissance avec choix multiples
• Défi 2 : Questions d'explication avec phrases complètes
• Défi 3 : Questions d'analyse avec justifications détaillées
• Tous les défis sont valorisés - c'est TON choix !

NOTE_ENSEIGNANT: Présentez les trois défis comme des choix équivalents. Insistez : "Choisis le défi qui te permet de mieux montrer ce que tu as appris." Distribuez les trois versions. Aucun élève ne devrait se sentir obligé de choisir un défi particulier.

**BILLET DE SORTIE - DÉFI 1**

**Choisis la meilleure réponse :**

1. Quel outil aide à voir l'ordre des événements ?
   a) Tableau comparatif  b) Ligne de temps  c) Carte

2. Les Acadiens vivaient principalement en :
   a) Ontario  b) Québec  c) Nouvelle-Écosse

3. Une ligne de temps sert à :
   a) Comparer des opinions  b) Montrer des lieux  c) Organiser des dates

4. Encercle VRAI ou FAUX : Un tableau comparatif montre différents points de vue.
   VRAI     FAUX

5. Nomme UN outil organisationnel appris aujourd'hui : ________________

**BILLET DE SORTIE - DÉFI 2**

1. Explique en une phrase comment une ligne de temps nous aide à comprendre l'histoire des Acadiens.

2. Pourquoi est-il important de comparer différents points de vue sur la déportation acadienne ?

3. Que peut nous apprendre une carte sur la dispersion des Acadiens que les autres outils ne montrent pas ?

4. Donne un exemple de situation dans ta vie où tu pourrais utiliser un tableau comparatif.

5. Complete : L'analyse d'œuvres d'art nous aide à comprendre _____________ des événements historiques.

**BILLET DE SORTIE - DÉFI 3**

1. Analyse comment l'utilisation combinée d'une ligne de temps et d'un tableau comparatif enrichit notre compréhension de la déportation acadienne. Justifie ta réponse avec des exemples précis.

2. Évalue l'efficacité des quatre outils organisationnels présentés. Lequel considères-tu le plus révélateur pour comprendre l'expérience acadienne ? Explique ton raisonnement en comparant au moins deux outils.

3. Synthétise ce que l'exemple acadien nous enseigne sur l'importance d'utiliser plusieurs outils d'analyse historique. Comment cette approche change-t-elle notre perspective d'historien ?




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

slides = parse_slides(CLAUDE_OUTPUT)
create_presentation(slides, 'Les Acadiens')