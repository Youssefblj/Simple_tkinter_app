import tkinter as tk
from tkinter import ttk

# Fonction pour changer la couleur de fond
def changer_couleur(couleur):
    fenetre.configure(bg=couleur)
    etiquette.configure(text=f"Couleur actuelle : {couleur}", bg=couleur)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Changeur de Couleur")
fenetre.geometry("400x200")

# Couleur initiale
couleur_initiale = "orange"
fenetre.configure(bg=couleur_initiale)

# Étiquette affichant la couleur actuelle
etiquette = tk.Label(fenetre, text=f"Couleur actuelle : {couleur_initiale}", 
                     bg=couleur_initiale, font=("Arial", 12, "italic"))
etiquette.pack(pady=10)

# Cadre pour les boutons
cadre_boutons = tk.Frame(fenetre, bg=couleur_initiale)
cadre_boutons.pack(pady=10)

# Liste des couleurs disponibles
couleurs = {
    "Rouge": "red",
    "Vert": "green",
    "Bleu": "blue",
    "Jaune": "yellow",
    "Orange": "orange"
}

# Création des boutons
for nom, code_couleur in couleurs.items():
    bouton = ttk.Button(cadre_boutons, text=nom, command=lambda c=code_couleur: changer_couleur(c))
    bouton.pack(side=tk.LEFT, padx=5)

# Boucle principale
fenetre.mainloop()
