import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import cv2

from odv.level import BackupedLevel

import os
os.chdir("../")

# map_size_x = []
# map_size_y = []
# minimap_size_x = []
# minimap_size_y = []
#
# for level_index in range(26):
#     print(f"\nLevel {level_index}")
#     level = BackupedLevel(level_index)
#     map_size_x.append(level.dvm.level_map.width)
#     map_size_y.append(level.dvm.level_map.height)
#     minimap_size_x.append(level.dvd.bgnd.minimap.width())
#     minimap_size_y.append(level.dvd.bgnd.minimap.height())

map_size_x =     [2560, 2112, 1600, 1920, 2560, 1280, 2368, 2112, 2240, 1600, 1600, 1280, 2240, 2368, 1600, 2240, 2240, 1600, 2560, 1280, 1280, 2560, 2432, 2432, 2944, 1024]
map_size_y =     [1600, 1088, 2368,  896, 1408,  768, 1920, 1088, 1600, 1472, 2240, 2368, 1728, 1728, 1408, 1600, 1600, 1024, 1728, 2240,  768, 1728, 1792, 1856, 1664,  960]
minimap_size_x = [ 300,  300,  207,  300,  300,  300,  300,  300,  300,  300,  218,  167,  300,  300,  300,  300,  300,  300,  300,  176,  300,  300,  300,  300,  300,  150]
minimap_size_y = [ 192,  159,  300,  145,  170,  184,  245,  159,  218,  278,  300,  300,  234,  223,  265,  217,  218,  197,  207,  300,  184,  207,  226,  231,  175,  142]


def print_reduction_factor():
    for i in range(25):
        factor = max(map_size_x[i], map_size_y[i])/290
        print(f"Level_{i:02}  f={round(factor,3)}")
        print(f"  x: {round(map_size_x[i]/factor) + 10} == {minimap_size_x[i]}")
        print(f"  y: {round(map_size_y[i]/factor) + 10} == {minimap_size_y[i]}")

    i = 25
    factor = max(map_size_x[i], map_size_y[i])/140
    print(f"Level_{i:02}  f={round(factor,3)}")
    print(f"  x: {round(map_size_x[i]/factor) + 10} == {minimap_size_x[i]}")
    print(f"  y: {round(map_size_y[i]/factor) + 10} == {minimap_size_y[i]}")




# Fonction pour charger les images
def load_images(_path, _indexes, _suffixe):
    filenames = [f"{_path}{i:02}{_suffixe}" for i in _indexes]
    images = [cv2.imread(file) for file in filenames]
    return images


# Fonction pour extraire les coefficients du filtre
def extract_filter_coefficients(original_images, filtered_images):
    # Assurez-vous que nous avons le même nombre d'images
    assert len(original_images) == len(filtered_images)

    # Dimensions des images (en supposant que toutes les images ont la même taille)
    height, width, _ = original_images[0].shape

    # Création des matrices pour les régressions
    A = []
    B = []

    # Pour chaque image
    for orig, filt in zip(original_images, filtered_images):
        # Redimensionner les images en vecteurs
        orig_vec = orig.reshape(-1, 3)  # Chaque pixel en un vecteur [R, G, B]
        filt_vec = filt.reshape(-1, 3)  # Idem pour l'image filtrée

        # Construire la matrice A et le vecteur B
        # Matrice A : [ori_r, ori_g, ori_b] pour chaque pixel
        A.extend(orig_vec)
        # Matrice B : [filt_r, filt_g, filt_b] pour chaque pixel
        B.extend(filt_vec)

    # Convertir en matrices NumPy
    A = np.array(A)
    B = np.array(B)

    # Trouver les coefficients en résolvant le système A @ coeffs = B
    coeffs, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

    # La matrice des coefficients
    coeffs = coeffs.T.reshape(3,3)
    return coeffs


def apply_filter(image_path, coeff_matrix):
    """
    Applique le filtre donné par coeff_matrix à une image.

    :param image: Image d'entrée (BGR)
    :param coeff_matrix: Matrice des coefficients de filtrage (3x3)
    :return: Image filtrée
    """
    image = cv2.imread(image_path)

    # Convertir l'image en espace de couleurs flottant (float32) pour éviter les problèmes de précision
    image_float = image.astype(np.float32) / 255.0  # Normalisation

    # Reshape l'image pour travailler avec les pixels individuellement
    height, width, _ = image_float.shape
    image_flat = image_float.reshape(-1, 3)  # Chaque pixel devient un vecteur [R, G, B]

    # Appliquer la transformation
    filtered_flat = np.dot(image_flat, coeff_matrix.T)  # Transpose de la matrice pour multiplication correcte

    # Reformatage de l'image filtrée
    filtered_flat = np.clip(filtered_flat, 0, 1)  # Clamp les valeurs entre 0 et 1
    filtered_image = (filtered_flat.reshape(height, width, 3) * 255).astype(np.uint8)  # Reformatage en uint8

    return filtered_image


# Charger les images
path = "extracted/map_to_minimap/"
indexes = [2,6,18]

original_images = load_images(path, indexes, "map.bmp")
filtered_images = load_images(path, indexes, "minimap.bmp")

# Extraire les coefficients du filtre
coefficients = extract_filter_coefficients(original_images, filtered_images)
print("Coefficients du filtre:")
print(f"{coefficients=}")

# coefficients=np.array([[ 0.06800281, -0.06996037,  0.38097899],
#                        [ 0.06879934, -0.11612666,  0.66285291],
#                        [ 0.01210211, -0.15162757,  0.9303298 ]])

#                    B     G     R
m=np.array([[  0,  -20,   0],      # blue
                  [  -5,  -20,   -5],      # green
                  [ -20,   5,  -20]],     # red
        dtype=np.float64)

t=np.array([[ 0, 1, 0],
            [ 0, 1, 0],
            [ 0, 1, 0]])

m/=100.

apply_id = 18

# filtered_image = apply_filter(f"{path}{apply_id:02}map.bmp", t)
filtered_image = apply_filter(f"{path}{apply_id:02}map.bmp", (coefficients *1.5 + m)*1.15)

# Sauvegarder ou afficher l'image filtrée
cv2.imwrite(f"{path}{apply_id:02}minimap_rebuilt.bmp", filtered_image)