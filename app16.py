from tkinter import *
from tkinter import ttk, messagebox

# === Fonction pour trier les mots ===
def trier_mots():
    phrase = entree.get("1.0", END).strip()
    if not phrase:
        messagebox.showwarning("Attention", "Veuillez entrer une phrase.")
        return

    # Séparer les mots et les trier par longueur décroissante
    mots = phrase.split()
    mots_tries = sorted(mots, key=len, reverse=True)

    # Effacer les anciennes données
    for item in tableau.get_children():
        tableau.delete(item)

    # Afficher les mots triés avec leur longueur
    for mot in mots_tries:
        tableau.insert("", END, values=(mot, len(mot)))

    # Calcul des statistiques
    nb_mots = len(mots)
    nb_caracteres = sum(len(m) for m in mots)
    longueur_moyenne = nb_caracteres / nb_mots if nb_mots > 0 else 0

    stats.config(
        text=f"Nombre total de mots : {nb_mots}\n"
             f"Nombre total de caractères : {nb_caracteres}\n"
             f"Longueur moyenne : {longueur_moyenne:.2f} caractères"
    )

# === Fonction pour effacer ===
def effacer():
    entree.delete("1.0", END)
    for item in tableau.get_children():
        tableau.delete(item)
    stats.config(text="")

# === Exemple automatique ===
def exemple():
    entree.delete("1.0", END)
    entree.insert(END, "python is fun and powerful")
    trier_mots()

# === Fenêtre principale ===
fenetre = Tk()
fenetre.title("Tri des mots par longueur")
fenetre.geometry("500x500")
fenetre.configure(bg="#f2f2f2")

Label(fenetre, text="Saisissez une phrase :", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)

# Zone de texte pour saisir la phrase
entree = Text(fenetre, width=50, height=3, font=("Arial", 12))
entree.pack(pady=5)

# Boutons
frame_boutons = Frame(fenetre, bg="#f2f2f2")
frame_boutons.pack(pady=5)

Button(frame_boutons, text="Trier les mots", command=trier_mots).grid(row=0, column=0, padx=5)
Button(frame_boutons, text="Effacer", command=effacer).grid(row=0, column=1, padx=5)
Button(frame_boutons, text="Exemple", command=exemple).grid(row=0, column=2, padx=5)

# Statistiques
Label(fenetre, text="Statistiques :", bg="#f2f2f2", font=("Arial", 12, "bold")).pack(pady=5)
stats = Label(fenetre, text="", bg="#ffffff", width=60, height=3, anchor="w", justify=LEFT, relief="solid")
stats.pack(pady=5)

# Tableau des mots triés
Label(fenetre, text="Mots triés par longueur (décroissant)", bg="#f2f2f2", font=("Arial", 12, "bold")).pack(pady=5)

tableau = ttk.Treeview(fenetre, columns=("mot", "longueur"), show="headings", height=8)
tableau.heading("mot", text="Mot")
tableau.heading("longueur", text="Longueur")
tableau.column("mot", width=200)
tableau.column("longueur", width=100, anchor="center")
tableau.pack(pady=5)

fenetre.mainloop()
