import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu
import hashlib

def extract_minutiae(image_path):
    # Step 1 - Read and convert to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Step 2 - Apply Gaussian blur and binarization
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    thresh_val = threshold_otsu(blurred)
    binary = blurred > thresh_val

    # Step 3 - Skeletonization (reduces ridges to 1-pixel width)
    skeleton = skeletonize(binary)

    # Step 4 - Find minutiae points (ridge endings & bifurcations)
    minutiae = []
    for y in range(1, skeleton.shape[0] - 1):
        for x in range(1, skeleton.shape[1] - 1):
            if skeleton[y, x]:
                neighborhood = skeleton[y-1:y+2, x-1:x+2]
                count = np.sum(neighborhood) - 1  # exclude center pixel
                if count == 1 or count == 3:  # ridge ending or bifurcation
                    minutiae.append((x, y, count))

    return minutiae

def generate_template(minutiae_points):
    """
    Convert minutiae list into a compact, hashed template.
    In real systems, this would be a binary vector or proprietary format.
    """
    arr = np.array(minutiae_points).flatten()
    string_repr = ",".join(map(str, arr))
    return hashlib.sha256(string_repr.encode()).hexdigest()

# Example usage
import os
#path = r"teste\user_1\1__M_Left_index_finger.BMP"

#print( os.listdir(os.getcwd()))

#if not os.path.exists(path):
    #print("Arquivo não encontrado:", path)

for i in os.listdir(r"teste\user_1"):
    path = os.path.join(r"teste\user_1",i)

    minutiae = extract_minutiae(path)
    template = generate_template(minutiae)

    #print(f"Extracted {len(minutiae)} minutiae points.")
    print(f"Template (SHA-256): {template}")
