import tkinter as tk
from tkinter import ttk, messagebox

# === Fonctions ===
def ajouter_element():
    element = entree.get().strip()
    if element:
        liste_gauche.insert(tk.END, element)
        entree.delete(0, tk.END)
    else:
        messagebox.showwarning("Attention", "Veuillez entrer un élément à ajouter.")

def deplacer_selection_gauche_droite():
    selection = liste_gauche.curselection()
    if selection:
        for i in selection:
            element = liste_gauche.get(i)
            liste_droite.insert(tk.END, element)
        for i in reversed(selection):
            liste_gauche.delete(i)
    else:
        messagebox.showinfo("Info", "Sélectionnez un élément à déplacer.")

def deplacer_selection_droite_gauche():
    selection = liste_droite.curselection()
    if selection:
        for i in selection:
            element = liste_droite.get(i)
            liste_gauche.insert(tk.END, element)
        for i in reversed(selection):
            liste_droite.delete(i)
    else:
        messagebox.showinfo("Info", "Sélectionnez un élément à déplacer.")

def deplacer_tout_gauche_droite():
    elements = liste_gauche.get(0, tk.END)
    for element in elements:
        liste_droite.insert(tk.END, element)
    liste_gauche.delete(0, tk.END)

def deplacer_tout_droite_gauche():
    elements = liste_droite.get(0, tk.END)
    for element in elements:
        liste_gauche.insert(tk.END, element)
    liste_droite.delete(0, tk.END)


# === Fenêtre principale ===
fenetre = tk.Tk()
fenetre.title("Exemple de Déplacement ListBox")
fenetre.geometry("600x300")

# === Champ d’entrée et bouton d’ajout ===
cadre_ajout = tk.Frame(fenetre)
cadre_ajout.pack(pady=10)

tk.Label(cadre_ajout, text="Entrez un élément :").pack(side=tk.LEFT)
entree = ttk.Entry(cadre_ajout, width=25)
entree.pack(side=tk.LEFT, padx=5)
ttk.Button(cadre_ajout, text="Ajouter à la liste", command=ajouter_element).pack(side=tk.LEFT)

# === Cadre principal avec les ListBox ===
cadre_listes = tk.Frame(fenetre)
cadre_listes.pack(pady=10)

# ListBox gauche
liste_gauche = tk.Listbox(cadre_listes, selectmode=tk.MULTIPLE, width=20, height=10)
liste_gauche.grid(row=0, column=0, padx=10)
for item in ["Tomates", "Mangues", "Cerises", "Ananas"]:
    liste_gauche.insert(tk.END, item)

# Cadre pour les boutons de déplacement
cadre_boutons = tk.Frame(cadre_listes)
cadre_boutons.grid(row=0, column=1, padx=10)

tk.Button(cadre_boutons, text=">", width=5, command=deplacer_selection_gauche_droite).pack(pady=2)
tk.Button(cadre_boutons, text="<", width=5, command=deplacer_selection_droite_gauche).pack(pady=2)
tk.Button(cadre_boutons, text=">>", width=5, command=deplacer_tout_gauche_droite).pack(pady=2)
tk.Button(cadre_boutons, text="<<", width=5, command=deplacer_tout_droite_gauche).pack(pady=2)

# ListBox droite
liste_droite = tk.Listbox(cadre_listes, selectmode=tk.MULTIPLE, width=20, height=10)
liste_droite.grid(row=0, column=2, padx=10)
liste_droite.insert(tk.END, "Pomme")

# === Boucle principale ===
fenetre.mainloop()
