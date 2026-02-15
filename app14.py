from tkinter import *

# === Fonction pour générer la table de multiplication ===
def generer_table():
    try:
        nombre = int(entree.get())
        zone_texte.delete(1.0, END)  # Effacer l'ancien contenu
        for i in range(1, 13):
            resultat = nombre * i
            zone_texte.insert(END, f"{nombre} x {i} = {resultat}\n")
    except ValueError:
        zone_texte.delete(1.0, END)
        zone_texte.insert(END, "Veuillez entrer un nombre valide !")

# === Création de la fenêtre principale ===
fenetre = Tk()
fenetre.title("Table de Multiplication")
fenetre.geometry("300x400")
fenetre.configure(bg="#f7f0dc")

# === Label et champ de saisie ===
label = Label(fenetre, text="Entrez un nombre :", bg="#f7f0dc", font=("Arial", 12))
label.pack(pady=10)

entree = Entry(fenetre, font=("Arial", 12), justify="center")
entree.pack(pady=5)

# === Bouton pour générer la table ===
bouton = Button(fenetre, text="Afficher la table", command=generer_table, font=("Arial", 11))
bouton.pack(pady=10)

# === Zone d'affichage du résultat ===
zone_texte = Text(fenetre, width=25, height=12, font=("Consolas", 12))
zone_texte.pack(pady=10)

# === Lancer l'application ===
fenetre.mainloop()
