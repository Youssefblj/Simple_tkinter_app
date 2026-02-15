import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import qrcode

# === Fonction pour générer le QR Code ===
def generer_qr():
    titre = entry_titre.get()
    auteur = entry_auteur.get()
    isbn = entry_isbn.get()

    if not titre or not auteur or not isbn:
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")
        return

    data = f"Titre: {titre}\nAuteur: {auteur}\nISBN: {isbn}"
    qr = qrcode.make(data)
    qr.save("qrcode_temp.png")

    img = Image.open("qrcode_temp.png").resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)
    label_qr.config(image=img_tk)
    label_qr.image = img_tk

# === Fonction pour sauvegarder le QR Code ===
def sauvegarder_qr():
    fichier = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image PNG", "*.png")])
    if fichier:
        data = f"Titre: {entry_titre.get()}\nAuteur: {entry_auteur.get()}\nISBN: {entry_isbn.get()}"
        qr = qrcode.make(data)
        qr.save(fichier)
        messagebox.showinfo("Sauvegarde réussie", f"QR Code sauvegardé sous : {fichier}")

# === Interface Tkinter ===
fenetre = tk.Tk()
fenetre.title("Générateur de QR Code pour Livres")
fenetre.geometry("400x500")
fenetre.configure(bg="#f4f4f4")

# Champs de saisie
tk.Label(fenetre, text="Titre du livre:").pack(pady=5)
entry_titre = tk.Entry(fenetre, width=40)
entry_titre.pack()

tk.Label(fenetre, text="Auteur:").pack(pady=5)
entry_auteur = tk.Entry(fenetre, width=40)
entry_auteur.pack()

tk.Label(fenetre, text="ISBN:").pack(pady=5)
entry_isbn = tk.Entry(fenetre, width=40)
entry_isbn.pack()

# Boutons
tk.Button(fenetre, text="Générer le QR Code", command=generer_qr, bg="#4CAF50", fg="white").pack(pady=15)

label_qr = tk.Label(fenetre, text="Le QR Code apparaîtra ici", bg="#f4f4f4")
label_qr.pack(pady=20)

tk.Button(fenetre, text="Sauvegarder le QR Code", command=sauvegarder_qr, bg="#2196F3", fg="white").pack(pady=10)

fenetre.mainloop()
