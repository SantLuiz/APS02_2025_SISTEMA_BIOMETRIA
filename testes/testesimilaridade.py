import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu

def extract_minutiae(image_path):
    """Extrai minúcias de uma impressão digital."""
    # 1 - Carregar imagem em grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Não foi possível carregar a imagem: {image_path}")

    # 2 - Binarização
    blurred = cv2.GaussianBlur(img, (5,5), 0)
    thresh_val = threshold_otsu(blurred)
    binary = blurred > thresh_val

    # 3 - Skeletonização
    skeleton = skeletonize(binary)

    # 4 - Extrair minutiae (ridge endings e bifurcações)
    minutiae = []
    for y in range(1, skeleton.shape[0]-1):
        for x in range(1, skeleton.shape[1]-1):
            if skeleton[y, x]:
                neighborhood = skeleton[y-1:y+2, x-1:x+2]
                count = np.sum(neighborhood) - 1
                if count == 1 or count == 3:  # ridge ending ou bifurcação
                    minutiae.append((x, y, int(count)))
    return minutiae

def generate_template(minutiae_points):
    """
    Converte minúcias em um template estruturado.
    Para simplicidade, apenas normalizamos e retornamos como array numpy.
    """
    if not minutiae_points:
        return np.array([])
    template = np.array(minutiae_points, dtype=np.float32)
    # Opcional: normalizar posições
    template[:,0] /= template[:,0].max()
    template[:,1] /= template[:,1].max()
    return template

def compare_templates(template1, template2, tolerance=0.05):
    """
    Compara dois templates e retorna um score de similaridade (0 a 100).
    tolerance: distância máxima para considerar pontos como correspondentes
    """
    if template1.size == 0 or template2.size == 0:
        return 0.0

    matched = 0
    for x1, y1, type1 in template1:
        for x2, y2, type2 in template2:
            dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if type1 == type2 and dist <= tolerance:
                matched += 1
                break  # evita múltiplos matches para o mesmo ponto

    score = matched / max(len(template1), len(template2)) * 100
    return score

# ---------------------
# Exemplo de uso
# ---------------------

# Caminhos das imagens
imgCONTROLE = r"teste\user_1\1__M_Left_index_finger.BMP"
img1 = r"teste\user_1\1__M_Left_index_finger.BMP"
img2 = r"teste\user_1-EASY\1__M_Left_index_finger_CR.BMP"
img3 = r"teste\user_1-MEDIUM\1__M_Left_index_finger_CR.BMP"
img4 = r"teste\user_1-HARD\1__M_Left_index_finger_CR.BMP"


# Extrair minúcias e gerar templates
minutiae1 = extract_minutiae(img1)
minutiae2 = extract_minutiae(img2)
minutiae3 = extract_minutiae(img3)
minutiae4 = extract_minutiae(img4)
CONTROLE = extract_minutiae(imgCONTROLE)


template1 = generate_template(minutiae1)
template2 = generate_template(minutiae2)
template3 = generate_template(minutiae3)
template4 = generate_template(minutiae4)
templateCONTROLE = generate_template(CONTROLE)

# Comparar e gerar score
score = compare_templates(template1, template2)
print(f"Score de similaridade [EASY]: {score:.2f}%")

score = compare_templates(template1, template3)
print(f"Score de similaridade [MEDIUM]: {score:.2f}%")

score = compare_templates(template1, template4)
print(f"Score de similaridade [HARD]: {score:.2f}%")

score = compare_templates(template1, templateCONTROLE)
print(f"Score de similaridade [CONTROLE]: {score:.2f}%")

# Definir threshold para validar acesso
