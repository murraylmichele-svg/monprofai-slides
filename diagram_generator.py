import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os
import tempfile

OUTPUT_DIR = tempfile.gettempdir()

def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, f'{name}.png')
    fig.savefig(path, bbox_inches='tight', dpi=150, transparent=False,
                facecolor='white')
    plt.close(fig)
    return path

# ── FRACTION DISPLAY (large centred) ────────────────────────────────────────

def fraction_affichage(num, den):
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.axis('off')
    ax.text(0.5, 0.72, str(num), ha='center', va='center',
            fontsize=72, fontweight='bold', color='#1a1a8c')
    ax.plot([0.2, 0.8], [0.5, 0.5], color='#1a1a8c', linewidth=4,
            transform=ax.transAxes)
    ax.text(0.5, 0.28, str(den), ha='center', va='center',
            fontsize=72, fontweight='bold', color='#1a1a8c')
    return save_fig(fig, f'fraction_affichage_{num}_{den}')

# ── INLINE FRACTION (small, for text embedding) ──────────────────────────────

def fraction_inline(num, den):
    fig, ax = plt.subplots(figsize=(0.6, 0.8))
    ax.axis('off')
    ax.text(0.5, 0.75, str(num), ha='center', va='center',
            fontsize=28, fontweight='bold', color='#1a1a8c')
    ax.plot([0.1, 0.9], [0.5, 0.5], color='#1a1a8c', linewidth=2,
            transform=ax.transAxes)
    ax.text(0.5, 0.25, str(den), ha='center', va='center',
            fontsize=28, fontweight='bold', color='#1a1a8c')
    return save_fig(fig, f'fraction_inline_{num}_{den}')

# ── AREA MODEL ───────────────────────────────────────────────────────────────

def fraction_aire(num, den):
    """Choose rectangle or circle based on denominator."""
    if den in (2, 4, 8):
        return _aire_cercle(num, den)
    else:
        return _aire_rectangle(num, den)

def _aire_rectangle(num, den):
    fig, ax = plt.subplots(figsize=(4, 2.5))
    ax.axis('off')
    ax.set_xlim(0, den)
    ax.set_ylim(0, 1)
    for i in range(den):
        color = '#4a90d9' if i < num else '#e8e8e8'
        rect = mpatches.Rectangle((i, 0), 1, 1,
                                   linewidth=2, edgecolor='#333333',
                                   facecolor=color)
        ax.add_patch(rect)
    ax.text(den/2, -0.25, f'{num}/{den}', ha='center', va='top',
            fontsize=16, fontweight='bold', color='#1a1a8c')
    ax.set_title('Modèle d\'aire', fontsize=12, pad=8, color='#333333')
    return save_fig(fig, f'fraction_aire_{num}_{den}')

def _aire_cercle(num, den):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_aspect('equal')
    ax.axis('off')
    theta = np.linspace(0, 2*np.pi, 300)
    ax.fill(np.cos(theta), np.sin(theta), color='#e8e8e8', zorder=1)
    ax.plot(np.cos(theta), np.sin(theta), color='#333333', linewidth=2, zorder=2)
    for i in range(num):
        start = np.pi/2 - i * 2*np.pi/den
        end   = np.pi/2 - (i+1) * 2*np.pi/den
        t = np.linspace(start, end, 100)
        wedge_x = [0] + list(np.cos(t)) + [0]
        wedge_y = [0] + list(np.sin(t)) + [0]
        ax.fill(wedge_x, wedge_y, color='#4a90d9', zorder=3)
    for i in range(den):
        angle = np.pi/2 - i * 2*np.pi/den
        ax.plot([0, np.cos(angle)], [0, np.sin(angle)],
                color='#333333', linewidth=2, zorder=4)
    ax.text(0, -1.3, f'{num}/{den}', ha='center', va='top',
            fontsize=16, fontweight='bold', color='#1a1a8c')
    ax.set_title('Modèle d\'aire', fontsize=12, pad=8, color='#333333')
    return save_fig(fig, f'fraction_aire_{num}_{den}')

# ── SET MODEL ────────────────────────────────────────────────────────────────

def fraction_ensemble(num, den, shape='cercles'):
    fig, ax = plt.subplots(figsize=(4, 2.5))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    cols = min(den, 5)
    rows = (den + cols - 1) // cols
    positions = []
    for r in range(rows):
        for c in range(cols):
            if len(positions) < den:
                x = 0.1 + c * (0.8 / cols) + (0.4 / cols)
                y = 0.75 - r * (0.55 / max(rows, 1))
                positions.append((x, y))

    for idx, (x, y) in enumerate(positions):
        color = '#4a90d9' if idx < num else '#cccccc'
        size = 0.06

        if shape == 'cercles':
            circle = plt.Circle((x, y), size, color=color,
                                 transform=ax.transAxes, zorder=3)
            ax.add_patch(circle)
            circle2 = plt.Circle((x, y), size, fill=False,
                                  edgecolor='#333333', linewidth=1.5,
                                  transform=ax.transAxes, zorder=4)
            ax.add_patch(circle2)

        elif shape == 'carres':
            rect = mpatches.FancyBboxPatch(
                (x - size, y - size), size*2, size*2,
                boxstyle='round,pad=0.005',
                facecolor=color, edgecolor='#333333', linewidth=1.5,
                transform=ax.transAxes, zorder=3)
            ax.add_patch(rect)

        elif shape == 'etoiles':
            star_x, star_y = _star_points(x, y, size*1.4, size*0.6)
            ax.fill(star_x, star_y, color=color,
                    transform=ax.transAxes, zorder=3)
            ax.plot(star_x, star_y, color='#333333', linewidth=1,
                    transform=ax.transAxes, zorder=4)

        elif shape == 'coeurs':
            hx, hy = _heart_points(x, y, size)
            ax.fill(hx, hy, color=color,
                    transform=ax.transAxes, zorder=3)
            ax.plot(hx, hy, color='#333333', linewidth=1,
                    transform=ax.transAxes, zorder=4)

    ax.text(0.5, 0.05, f'{num}/{den}', ha='center', va='bottom',
            fontsize=14, fontweight='bold', color='#1a1a8c',
            transform=ax.transAxes)
    ax.set_title('Modèle d\'ensemble', fontsize=12, pad=8, color='#333333')
    return save_fig(fig, f'fraction_ensemble_{shape}_{num}_{den}')

def _star_points(cx, cy, R, r, n=5):
    angles = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, 2*n + 1)
    radii  = [R if i % 2 == 0 else r for i in range(2*n + 1)]
    x = [cx + radii[i] * np.cos(angles[i]) for i in range(2*n + 1)]
    y = [cy + radii[i] * np.sin(angles[i]) for i in range(2*n + 1)]
    return x, y

def _heart_points(cx, cy, size):
    t = np.linspace(0, 2*np.pi, 100)
    x = cx + size * 0.75 * (16*np.sin(t)**3) / 16
    y = cy + size * 0.75 * (13*np.cos(t) - 5*np.cos(2*t) -
                             2*np.cos(3*t) - np.cos(4*t)) / 16
    return x, y

# ── NUMBER LINE ──────────────────────────────────────────────────────────────

def fraction_ligne(num, den, max_val=1):
    fig, ax = plt.subplots(figsize=(5, 1.8))
    ax.axis('off')
    ax.set_xlim(-0.1, max_val + 0.2)
    ax.set_ylim(-0.5, 1)

    ax.annotate('', xy=(max_val + 0.15, 0), xytext=(-0.05, 0),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2))

    total_parts = den * max_val
    for i in range(total_parts + 1):
        x = i / den
        is_whole = (i % den == 0)
        h = 0.25 if is_whole else 0.15
        ax.plot([x, x], [-h, h], color='#333333',
                linewidth=2 if is_whole else 1)
        if is_whole:
            ax.text(x, -0.35, str(i // den), ha='center',
                    va='top', fontsize=11, color='#333333')

    frac_val = num / den
    ax.plot(frac_val, 0, 'o', color='#e63946', markersize=12, zorder=5)
    ax.text(frac_val, 0.35, f'{num}/{den}', ha='center', va='bottom',
            fontsize=13, fontweight='bold', color='#e63946')

    ax.text(-0.05, -0.35, '0', ha='center', va='top',
            fontsize=11, color='#333333')
    ax.set_title('Droite numérique', fontsize=12, pad=4, color='#333333')
    return save_fig(fig, f'fraction_ligne_{num}_{den}_max{max_val}')

# ── THREE MODELS COMBINED ────────────────────────────────────────────────────

def fraction_trois_modeles(num, den, shape='cercles'):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3))
    fig.suptitle(f'Trois représentations de {num}/{den}',
                 fontsize=13, fontweight='bold', color='#1a1a8c', y=1.02)

    # 1. Area model
    ax = axes[0]
    ax.set_title('Modèle d\'aire', fontsize=11, color='#333333')
    if den in (2, 4, 8):
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        theta = np.linspace(0, 2*np.pi, 300)
        ax.fill(np.cos(theta), np.sin(theta), color='#e8e8e8')
        ax.plot(np.cos(theta), np.sin(theta), color='#333333', linewidth=2)
        for i in range(num):
            start = np.pi/2 - i * 2*np.pi/den
            end   = np.pi/2 - (i+1) * 2*np.pi/den
            t = np.linspace(start, end, 100)
            ax.fill([0]+list(np.cos(t))+[0],
                    [0]+list(np.sin(t))+[0], color='#4a90d9')
        for i in range(den):
            angle = np.pi/2 - i * 2*np.pi/den
            ax.plot([0, np.cos(angle)], [0, np.sin(angle)],
                    color='#333333', linewidth=2)
    else:
        ax.axis('off')
        ax.set_xlim(0, den)
        ax.set_ylim(-0.4, 1)
        for i in range(den):
            color = '#4a90d9' if i < num else '#e8e8e8'
            rect = mpatches.Rectangle((i, 0), 1, 1,
                                       linewidth=2, edgecolor='#333333',
                                       facecolor=color)
            ax.add_patch(rect)

    # 2. Set model
    ax = axes[1]
    ax.set_title('Modèle d\'ensemble', fontsize=11, color='#333333')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    cols = min(den, 5)
    rows = (den + cols - 1) // cols
    positions = []
    for r in range(rows):
        for c in range(cols):
            if len(positions) < den:
                x = 0.1 + c*(0.8/cols) + (0.4/cols)
                y = 0.75 - r*(0.55/max(rows, 1))
                positions.append((x, y))
    for idx, (x, y) in enumerate(positions):
        color = '#4a90d9' if idx < num else '#cccccc'
        circle = plt.Circle((x, y), 0.07, color=color,
                             transform=ax.transAxes, zorder=3)
        ax.add_patch(circle)
        circle2 = plt.Circle((x, y), 0.07, fill=False,
                              edgecolor='#333333', linewidth=1.5,
                              transform=ax.transAxes, zorder=4)
        ax.add_patch(circle2)

    # 3. Number line
    ax = axes[2]
    ax.set_title('Droite numérique', fontsize=11, color='#333333')
    ax.axis('off')
    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.5, 1)
    ax.annotate('', xy=(1.15, 0), xytext=(-0.05, 0),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2))
    for i in range(den + 1):
        x = i / den
        h = 0.2 if i in (0, den) else 0.12
        ax.plot([x, x], [-h, h], color='#333333',
                linewidth=2 if i in (0, den) else 1)
        if i in (0, den):
            ax.text(x, -0.32, str(i//den), ha='center',
                    va='top', fontsize=10, color='#333333')
    frac_val = num / den
    ax.plot(frac_val, 0, 'o', color='#e63946', markersize=10, zorder=5)
    ax.text(frac_val, 0.3, f'{num}/{den}', ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='#e63946')

    plt.tight_layout()
    return save_fig(fig, f'fraction_trois_modeles_{num}_{den}')

# ── EXISTING DIAGRAMS (keep all your current ones) ───────────────────────────

def droite_numerique(start=0, end=10):
    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.axis('off')
    ax.set_xlim(start - 0.5, end + 0.5)
    ax.set_ylim(-1, 1)
    ax.annotate('', xy=(end + 0.4, 0), xytext=(start - 0.4, 0),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2))
    for i in range(start, end + 1):
        ax.plot([i, i], [-0.2, 0.2], color='#333333', linewidth=2)
        ax.text(i, -0.4, str(i), ha='center', va='top',
                fontsize=11, color='#333333')
    return save_fig(fig, f'droite_numerique_{start}_{end}')

# ── GENERATE ALL ─────────────────────────────────────────────────────────────

def generate_all():
    """Generate only a basic set of diagrams - kept for compatibility."""
    paths = {}
    try:
        paths['droite_numerique'] = droite_numerique(0, 10)
    except Exception as e:
        print(f'Warning: could not generate droite_numerique: {e}')
    return paths

def generate_diagram(visuel_key):
    """Generate a single diagram by key. Called on demand."""
    try:
        # Parse fraction keys
        if visuel_key.startswith('fraction_affichage_'):
            parts = visuel_key.split('_')
            num, den = int(parts[2]), int(parts[3])
            return fraction_affichage(num, den)
        elif visuel_key.startswith('fraction_aire_'):
            parts = visuel_key.split('_')
            num, den = int(parts[2]), int(parts[3])
            return fraction_aire(num, den)
        elif visuel_key.startswith('fraction_ensemble_'):
            parts = visuel_key.split('_')
            shape = parts[2]
            num, den = int(parts[3]), int(parts[4])
            return fraction_ensemble(num, den, shape)
        elif visuel_key.startswith('fraction_ligne_'):
            parts = visuel_key.split('_')
            num, den = int(parts[2]), int(parts[3])
            max_val = int(parts[4].replace('max','')) if len(parts) > 4 else 1
            return fraction_ligne(num, den, max_val)
        elif visuel_key.startswith('fraction_trois_modeles_'):
            parts = visuel_key.split('_')
            num, den = int(parts[3]), int(parts[4])
            return fraction_trois_modeles(num, den)
        elif visuel_key == 'droite_numerique':
            return droite_numerique(0, 10)
        else:
            return None
    except Exception as e:
        print(f'Warning: could not generate diagram {visuel_key}: {e}')
        return None
