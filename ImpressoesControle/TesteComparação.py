import os
import cv2
import numpy as np
import sqlite3
from tkinter import Tk, filedialog
from skimage.morphology import skeletonize
from skimage.filters import threshold_otsu

# Import functions from verifica.py (import absoluto do root do projeto)
# Substitua 'extract_minutiae', 'generate_template', 'compare_templates' pelos nomes reais
from verifica import extract_minutiae, generate_template, compare_templates

# =====================
# Database Connection
# =====================

DB_PATH = r"C:\Users\LuizS\Desktop\APS02_2025_SISTEMA_BIOMETRIA\biometria.db"

# =====================
# File Selection
# =====================
Tk().withdraw()  # Hide main Tk window
image_path = filedialog.askopenfilename(
    title="Select fingerprint (.bmp)",
    filetypes=[("BMP images", "*.bmp")]
)

if not image_path:
    print("❌ No image selected.")
    exit()

# =====================
# Get user input
# =====================
user_name = input("Enter the username to compare fingerprints: ").strip()

# =====================
# Extract minutiae and template from the chosen image
# =====================
print(f"\nProcessing fingerprint image: {image_path}")
minutiae = extract_minutiae(image_path)
template_input = generate_template(minutiae)

if template_input.size == 0:
    print("⚠️ No minutiae detected in the selected fingerprint.")
    exit()

# =====================
# Load stored templates for the given user
# =====================
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get user ID from username
cur.execute("SELECT ID FROM USUARIOS WHERE NOME = ?", (user_name,))
user = cur.fetchone()
if not user:
    print(f"❌ User '{user_name}' not found in database.")
    conn.close()
    exit()

user_id = user[0]

# Retrieve all fingerprint templates for this user
cur.execute("SELECT ID, DESCRICAO_DEDO, TEMPLATE FROM DIGITAIS WHERE ID_USUARIO = ?", (user_id,))
fingerprints = cur.fetchall()
conn.close()

if not fingerprints:
    print(f"⚠️ No fingerprints registered for user '{user_name}'.")
    exit()

# =====================
# Compare with each stored fingerprint
# =====================
print(f"\nComparing with {len(fingerprints)} registered fingerprints for user '{user_name}'...\n")

best_score = 0.0
best_finger = None

for fid, desc, template_blob in fingerprints:
    stored_template = np.frombuffer(template_blob, dtype=np.float32)
    stored_template = stored_template.reshape(-1, 3)

    score = compare_templates(template_input, stored_template)
    print(f"🖐️ {desc}: {score:.2f}% similarity")

    if score > best_score:
        best_score = score
        best_finger = desc

print("\n===============================")
print(f"✅ Best match: {best_finger} ({best_score:.2f}% similarity)")
print("===============================")
