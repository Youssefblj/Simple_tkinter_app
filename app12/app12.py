from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import os

# === Fonction pour échanger les images ===
base_path = os.path.dirname(__file__)

def echanger_images():
    global img1_tk, img2_tk
    img1_tk, img2_tk = img2_tk, img1_tk
    label_gauche.config(image=img1_tk)
    label_droite.config(image=img2_tk)

# === Création de la fenêtre principale ===
fenetre = Tk()
fenetre.title("Échangeur d'Images")

# === Chargement des images (à modifier selon vos fichiers) ===
# Assurez-vous d’avoir deux fichiers image (ex: image1.jpg et image2.jpg)
img1 = Image.open(os.path.join(base_path, "image1.jpg")).resize((250, 250))
img2 = Image.open(os.path.join(base_path, "image2.png")).resize((250, 250))

# Conversion en format compatible Tkinter
img1_tk = ImageTk.PhotoImage(img1)
img2_tk = ImageTk.PhotoImage(img2)

# === Création des labels pour afficher les images ===
label_gauche = Label(fenetre, image=img1_tk)
label_gauche.grid(row=0, column=0, padx=10, pady=10)

label_droite = Label(fenetre, image=img2_tk)
label_droite.grid(row=0, column=1, padx=10, pady=10)

# === Bouton pour échanger les images ===
btn_swap = Button(fenetre, text="Échanger les Images", command=echanger_images)
btn_swap.grid(row=1, column=0, columnspan=2, pady=10)

# === Boucle principale ===
fenetre.mainloop()
