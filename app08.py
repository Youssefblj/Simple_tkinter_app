import tkinter as tk
from tkinter import ttk, messagebox

# Fonction pour calculer l'IMC
def calculer_imc():
    try:
        poids = float(entree_poids.get())
        taille = float(entree_taille.get())
        
        if taille <= 0 or poids <= 0:
            raise ValueError("Les valeurs doivent être positives.")
        
        imc = poids / (taille ** 2)
        imc_arrondi = round(imc, 1)
        
        # Déterminer la catégorie
        if imc < 18.5:
            categorie = "Insuffisance pondérale"
            couleur = "orange"
        elif 18.5 <= imc < 25:
            categorie = "Poids normal"
            couleur = "green"
        elif 25 <= imc < 30:
            categorie = "Surpoids"
            couleur = "blue"
        else:
            categorie = "Obésité"
            couleur = "red"
        
        # Affichage du résultat
        resultat_imc.config(text=f"Votre IMC : {imc_arrondi}", fg=couleur)
        resultat_categorie.config(text=f"Catégorie : {categorie}", fg=couleur)
    
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour le poids et la taille.")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Calculateur d'IMC")
fenetre.geometry("350x300")

# Titre
titre = tk.Label(fenetre, text="Calculateur d'IMC", font=("Arial", 16, "bold"))
titre.pack(pady=10)

# Poids
cadre_poids = tk.Frame(fenetre)
cadre_poids.pack(pady=5)
tk.Label(cadre_poids, text="Poids (kg) :").grid(row=0, column=0, padx=5)
entree_poids = ttk.Entry(cadre_poids, width=10)
entree_poids.grid(row=0, column=1)

# Taille
cadre_taille = tk.Frame(fenetre)
cadre_taille.pack(pady=5)
tk.Label(cadre_taille, text="Taille (m) :").grid(row=0, column=0, padx=5)
entree_taille = ttk.Entry(cadre_taille, width=10)
entree_taille.grid(row=0, column=1)

# Bouton de calcul
bouton_calcul = tk.Button(fenetre, text="Calculer l'IMC", command=calculer_imc, 
                          bg="green", fg="white", font=("Arial", 12, "bold"))
bouton_calcul.pack(pady=15)

# Résultats
resultat_imc = tk.Label(fenetre, text="", font=("Arial", 12, "bold"))
resultat_imc.pack(pady=5)

resultat_categorie = tk.Label(fenetre, text="", font=("Arial", 12, "bold"))
resultat_categorie.pack(pady=5)

# Boucle principale
fenetre.mainloop()
