from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# === Classe Compte Bancaire ===
class CompteBancaire:
    def __init__(self, nom, solde_initial=0.0):
        self.nom = nom
        self.solde = float(solde_initial)
        self.historique = []

    def deposer(self, montant):
        self.solde += montant
        self.historique.append(
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Dépôt", montant, self.solde)
        )

    def retirer(self, montant):
        if montant > self.solde:
            return False
        self.solde -= montant
        self.historique.append(
            (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Retrait", -montant, self.solde)
        )
        return True


# === Application Tkinter ===
class SystemeBancaire:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Système Bancaire")
        self.fenetre.geometry("650x600")
        self.fenetre.config(bg="#f7f7f7")

        self.comptes = {}
        self.compte_actif = None

        # === Création de Compte ===
        frame_creation = LabelFrame(fenetre, text="Création de Compte", bg="#f7f7f7")
        frame_creation.pack(padx=10, pady=10, fill="x")

        Label(frame_creation, text="Nom du titulaire :", bg="#f7f7f7").grid(row=0, column=0)
        self.nom_entry = Entry(frame_creation)
        self.nom_entry.grid(row=0, column=1, padx=5)

        Label(frame_creation, text="Solde initial ($) :", bg="#f7f7f7").grid(row=0, column=2)
        self.solde_init_entry = Entry(frame_creation)
        self.solde_init_entry.insert(0, "0")
        self.solde_init_entry.grid(row=0, column=3, padx=5)

        Button(frame_creation, text="Créer le Compte", command=self.creer_compte).grid(row=0, column=4, padx=5)

        # === Sélection du Compte ===
        frame_selection = LabelFrame(fenetre, text="Sélection du Compte", bg="#f7f7f7")
        frame_selection.pack(padx=10, pady=10, fill="x")

        Label(frame_selection, text="Compte sélectionné :", bg="#f7f7f7").grid(row=0, column=0)
        self.compte_box = ttk.Combobox(frame_selection, values=[])
        self.compte_box.grid(row=0, column=1, padx=5)

        Button(frame_selection, text="Actualiser", command=self.actualiser_comptes).grid(row=0, column=2, padx=5)
        Button(frame_selection, text="Sélectionner", command=self.selectionner_compte).grid(row=0, column=3, padx=5)

        self.label_solde = Label(frame_selection, text="Solde: $0.00", bg="#f7f7f7", fg="green", font=("Arial", 12, "bold"))
        self.label_solde.grid(row=1, column=0, columnspan=4, pady=5)

        # === Opérations Bancaires ===
        frame_ops = LabelFrame(fenetre, text="Opérations Bancaires", bg="#f7f7f7")
        frame_ops.pack(padx=10, pady=10, fill="x")

        Label(frame_ops, text="Montant à déposer ($):", bg="#f7f7f7").grid(row=0, column=0)
        self.montant_depot = Entry(frame_ops)
        self.montant_depot.grid(row=0, column=1, padx=5)
        Button(frame_ops, text="Déposer", command=self.deposer).grid(row=0, column=2, padx=5)

        Label(frame_ops, text="Montant à retirer ($):", bg="#f7f7f7").grid(row=1, column=0)
        self.montant_retrait = Entry(frame_ops)
        self.montant_retrait.grid(row=1, column=1, padx=5)
        Button(frame_ops, text="Retirer", command=self.retirer).grid(row=1, column=2, padx=5)

        # === Historique des Transactions ===
        frame_hist = LabelFrame(fenetre, text="Historique des Transactions", bg="#f7f7f7")
        frame_hist.pack(padx=10, pady=10, fill="both", expand=True)

        self.table = ttk.Treeview(frame_hist, columns=("Date", "Type", "Montant", "Solde"), show="headings")
        self.table.heading("Date", text="Date et Heure")
        self.table.heading("Type", text="Description")
        self.table.heading("Montant", text="Montant ($)")
        self.table.heading("Solde", text="Solde après ($)")
        self.table.pack(fill="both", expand=True)

    # === Fonctions ===
    def creer_compte(self):
        nom = self.nom_entry.get().strip()
        solde_init = self.solde_init_entry.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Veuillez entrer un nom.")
            return
        try:
            solde_init = float(solde_init)
        except ValueError:
            messagebox.showerror("Erreur", "Le solde initial doit être un nombre.")
            return

        if nom in self.comptes:
            messagebox.showwarning("Attention", "Ce compte existe déjà.")
            return

        self.comptes[nom] = CompteBancaire(nom, solde_init)
        messagebox.showinfo("Succès", f"Compte '{nom}' créé avec succès.")
        self.actualiser_comptes()

    def actualiser_comptes(self):
        self.compte_box["values"] = list(self.comptes.keys())

    def selectionner_compte(self):
        nom = self.compte_box.get()
        if nom not in self.comptes:
            messagebox.showwarning("Attention", "Veuillez choisir un compte valide.")
            return
        self.compte_actif = self.comptes[nom]
        self.mettre_a_jour_solde()
        self.mettre_a_jour_historique()

    def deposer(self):
        if not self.compte_actif:
            messagebox.showwarning("Aucun compte", "Sélectionnez un compte d'abord.")
            return
        try:
            montant = float(self.montant_depot.get())
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide.")
            return
        self.compte_actif.deposer(montant)
        self.mettre_a_jour_solde()
        self.mettre_a_jour_historique()

    def retirer(self):
        if not self.compte_actif:
            messagebox.showwarning("Aucun compte", "Sélectionnez un compte d'abord.")
            return
        try:
            montant = float(self.montant_retrait.get())
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide.")
            return
        if not self.compte_actif.retirer(montant):
            messagebox.showwarning("Fonds insuffisants", "Solde insuffisant.")
        self.mettre_a_jour_solde()
        self.mettre_a_jour_historique()

    def mettre_a_jour_solde(self):
        solde = self.compte_actif.solde
        self.label_solde.config(text=f"Solde: ${solde:.2f}")

    def mettre_a_jour_historique(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for date, type_op, montant, solde in self.compte_actif.historique:
            self.table.insert("", END, values=(date, type_op, montant, solde))


# === Lancer l'application ===
root = Tk()
app = SystemeBancaire(root)
root.mainloop()
