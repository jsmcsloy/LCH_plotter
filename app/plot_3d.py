import numpy as np
import matplotlib.pyplot as plt

def lch_to_lab(L, C, H):
    H_rad = np.deg2rad(H)
    a = np.cos(H_rad) * C
    b = np.sin(H_rad) * C
    return np.array([L, a, b])

def lab_to_xyz(L, a, b):
    ref_X = 95.047
    ref_Y = 100.000
    ref_Z = 108.883

    Y = (L + 16) / 116
    X = a / 500 + Y
    Z = Y - b / 200

    X = ref_X * ((X ** 3) if (X ** 3 > 0.008856) else ((X - 16 / 116) / 7.787))
    Y = ref_Y * ((Y ** 3) if (Y ** 3 > 0.008856) else ((Y - 16 / 116) / 7.787))
    Z = ref_Z * ((Z ** 3) if (Z ** 3 > 0.008856) else ((Z - 16 / 116) / 7.787))

    return np.array([X, Y, Z])

def xyz_to_rgb(X, Y, Z):
    X /= 100
    Y /= 100
    Z /= 100

    R = X *  3.2406 + Y * -1.5372 + Z * -0.4986
    G = X * -0.9689 + Y *  1.8758 + Z *  0.0415
    B = X *  0.0557 + Y * -0.2040 + Z *  1.0570

    R = 1 if R > 1 else 0 if R < 0 else R
    G = 1 if G > 1 else 0 if G < 0 else G
    B = 1 if B > 1 else 0 if B < 0 else B

    return np.array([R, G, B])

def plot_lch_colors(L_values, C_values, H_values):
    points = []
    colors = []

    for L, C, H in zip(L_values, C_values, H_values):
        lab = lch_to_lab(L, C, H)
        xyz = lab_to_xyz(*lab)
        rgb = xyz_to_rgb(*xyz)

        points.append((L, C, H))
        colors.append(rgb)

    points = np.array(points)
    colors = np.array(colors)

    return (points, colors)


#    fig = plt.figure(figsize=(10, 10))
#    ax = fig.add_subplot(111, projection='3d')
#
#    ax.scatter(points[:, 1], points[:, 2], points[:, 0], c=colors, s=100)
#
#    ax.set_xlabel('Chroma (C)')
#    ax.set_ylabel('Hue (H)')
#    ax.set_zlabel('Lightness (L)')
#    ax.set_title('Combined LCH Chromacity Plot')

#    ax.set_xlim(0, 120)
#    ax.set_ylim(0, 360)
#    ax.set_zlim(0, 100)

#    plt.show()

if __name__ == "__main__":
    L_values = [80]
    C_values = [50]
    H_values = [220]

#    plot_lch_colors(L_values, C_values, H_values)
