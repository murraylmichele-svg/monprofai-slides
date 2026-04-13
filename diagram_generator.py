import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

DIAGRAMS_FOLDER = r'C:\Users\murra\OneDrive\Desktop\MonProf-Slides\diagrams'

def ensure_folder():
    os.makedirs(DIAGRAMS_FOLDER, exist_ok=True)

def get_path(filename):
    ensure_folder()
    return os.path.join(DIAGRAMS_FOLDER, filename)

def generate_types_angles():
    fig, axes = plt.subplots(1, 4, figsize=(10, 3))
    configs = [
        (30,  'Aigu\n< 90°',  '#2196F3'),
        (90,  'Droit\n= 90°', '#4CAF50'),
        (120, 'Obtus\n> 90°', '#FF9800'),
        (180, 'Plat\n= 180°', '#9C27B0'),
    ]
    for ax, (deg, label, color) in zip(axes, configs):
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        rad = np.radians(deg)
        x2 = np.cos(rad)
        y2 = np.sin(rad)

        # Base arm always horizontal right
        ax.annotate('', xy=(1.2, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))

        # Second arm
        if deg < 180:
            ax.annotate('', xy=(x2 * 1.2, y2 * 1.2), xytext=(0, 0),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))
        else:
            ax.annotate('', xy=(-1.2, 0), xytext=(0, 0),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))

        # Vertex dot
        ax.plot(0, 0, 'o', color=color, markersize=6)

        # Arc
        if 0 < deg < 180:
            arc = mpatches.Arc((0, 0), 0.4, 0.4, angle=0,
                               theta1=0, theta2=deg, color=color, lw=1.5)
            ax.add_patch(arc)

        # Label
        ax.text(0, -0.35, label, ha='center', va='top',
                fontsize=11, color=color, fontweight='bold')

    plt.tight_layout()
    path = get_path('types_angles.png')
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', transparent=False)
    plt.close()
    return path

def generate_single_angle(deg, label, filename):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_aspect('equal')
    ax.axis('off')
    color = '#1565C0'
    rad = np.radians(deg)
    x2 = np.cos(rad)
    y2 = np.sin(rad)

    # Always draw base arm (horizontal right)
    ax.annotate('', xy=(1.2, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

    # Draw second arm
    if deg < 180:
        ax.annotate('', xy=(x2 * 1.2, y2 * 1.2), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2.5))
    else:
        ax.annotate('', xy=(-1.2, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

    # Vertex dot
    ax.plot(0, 0, 'o', color=color, markersize=8)

    # Arc and degree label
    if 0 < deg < 180:
        arc = mpatches.Arc((0, 0), 0.5, 0.5, angle=0,
                           theta1=0, theta2=deg, color='#E53935', lw=2)
        ax.add_patch(arc)
        mid_rad = np.radians(deg / 2)
        ax.text(0.38 * np.cos(mid_rad), 0.38 * np.sin(mid_rad),
                f'{deg}°', fontsize=12, color='#E53935', fontweight='bold')

    # Name label
    ax.text(0, -0.3, label, ha='center', fontsize=13,
            color=color, fontweight='bold')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    plt.tight_layout()
    path = get_path(filename)
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', transparent=False)
    plt.close()
    return path

def generate_rapporteur():
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')

    # Semicircle
    theta = np.linspace(0, np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), 'b-', lw=3)
    ax.plot([-1, 1], [0, 0], 'b-', lw=3)

    # Center point
    ax.plot(0, 0, 'bo', markersize=6)

    # Tick marks and labels
    for angle in range(0, 181, 10):
        rad = np.radians(angle)
        inner = 0.85 if angle % 30 == 0 else 0.90
        ax.plot([inner * np.cos(rad), np.cos(rad)],
                [inner * np.sin(rad), np.sin(rad)], 'b-', lw=1.5)
        if angle % 30 == 0:
            lx = 0.72 * np.cos(rad)
            ly = 0.72 * np.sin(rad)
            ax.text(lx, ly, str(angle), ha='center', va='center',
                    fontsize=8, color='#1565C0', fontweight='bold')

    # Base line label
    ax.text(-1.15, -0.12, '180°', fontsize=9, color='#1565C0')
    ax.text(1.05, -0.12, '0°', fontsize=9, color='#1565C0')
    ax.text(0, -0.2, 'Centre', fontsize=9, color='#1565C0', ha='center')
    ax.text(0, 1.15, 'Rapporteur', fontsize=12,
            color='#1565C0', ha='center', fontweight='bold')

    plt.tight_layout()
    path = get_path('rapporteur.png')
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', transparent=False)
    plt.close()
    return path

def generate_all():
    paths = {}
    paths['types_angles'] = generate_types_angles()
    paths['angle_aigu']   = generate_single_angle(45,  'Angle aigu',  'angle_aigu.png')
    paths['angle_droit']  = generate_single_angle(90,  'Angle droit', 'angle_droit.png')
    paths['angle_obtus']  = generate_single_angle(120, 'Angle obtus', 'angle_obtus.png')
    paths['angle_plat']   = generate_single_angle(180, 'Angle plat',  'angle_plat.png')
    paths['rapporteur']   = generate_rapporteur()
    print('Diagrams generated:')
    for k, v in paths.items():
        print(f'  {k}: {v}')
    return paths

if __name__ == '__main__':
    generate_all()