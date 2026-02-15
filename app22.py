import tkinter as tk
from tkinter import ttk, messagebox

# ===============================
# Gestion des notes - Version finale avec sélection module
# ===============================

students = []
selected_student = None

# ---------- UTILITAIRES ----------
def find_student_by_id(sid):
    for s in students:
        if s["id"] == sid:
            return s
    return None

# ---------- ÉTUDIANTS ----------
def add_student():
    nom = entry_nom.get().strip()
    prenom = entry_prenom.get().strip()
    age_txt = entry_age.get().strip()

    if not nom or not prenom or not age_txt:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
        return

    try:
        age = int(age_txt)
    except ValueError:
        messagebox.showerror("Erreur", "L'âge doit être un nombre entier.")
        return

    students.append({
        "id": len(students) + 1,
        "nom": nom,
        "prenom": prenom,
        "age": age,
        "modules": {},
        "average": None
    })

    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    update_student_list()

def update_student_list():
    for i, s in enumerate(students, start=1):
        s["id"] = i
    for r in tree_students.get_children():
        tree_students.delete(r)
    for s in students:
        avg = f"{s['average']:.2f}" if s["average"] is not None else "--"
        tree_students.insert("", tk.END, iid=str(s["id"]), values=(s["id"], s["nom"], s["prenom"], s["age"], avg))

def on_student_select(event):
    global selected_student
    sel = tree_students.selection()
    if not sel:
        selected_student = None
    else:
        sid = int(sel[0])
        selected_student = find_student_by_id(sid)
    update_module_table()
    calculer_moyenne_generale()
    update_selected_label()

def delete_student():
    sel = tree_students.selection()
    if not sel:
        messagebox.showwarning("Attention", "Sélectionnez un étudiant à supprimer.")
        return
    sid = int(sel[0])
    if not messagebox.askyesno("Confirmation", "Supprimer cet étudiant ?"):
        return
    global selected_student
    students[:] = [s for s in students if s["id"] != sid]
    selected_student = None
    update_student_list()
    update_module_table()
    calculer_moyenne_generale()
    update_selected_label()

def clear_all():
    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment tout supprimer ?"):
        return
    global students, selected_student
    students = []
    selected_student = None
    update_student_list()
    update_module_table()
    calculer_moyenne_generale()
    update_selected_label()

# ---------- MODULES / NOTES ----------
def update_controls_fields(*args):
    """Met à jour les champs de contrôle selon le nombre choisi"""
    for widget in frame_controles.winfo_children():
        widget.destroy()

    try:
        n = int(spin_controls.get())
    except Exception:
        n = 2

    global entries_controles
    entries_controles = []
    for i in range(n):
        tk.Label(frame_controles, text=f"Contrôle {i+1} :").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        e = tk.Entry(frame_controles, width=6)
        e.grid(row=i, column=1, sticky="w", padx=5, pady=2)
        entries_controles.append(e)

def save_module():
    if not selected_student:
        messagebox.showwarning("Attention", "Sélectionnez un étudiant d'abord.")
        return

    module_name = combo_module.get().strip()
    if not module_name:
        messagebox.showwarning("Attention", "Choisissez un module.")
        return

    try:
        controles = [float(e.get()) for e in entries_controles if e.get().strip() != ""]
        exam = float(entry_exam.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des notes valides (0-20).")
        return

    if not controles:
        messagebox.showwarning("Attention", "Entrez au moins une note de contrôle.")
        return

    # Calcul: contrôles moyenne 40%, examen 60% (ajustable)
    moyenne_controles = sum(controles) / len(controles)
    moyenne = round(moyenne_controles * 0.4 + exam * 0.6, 2)
    label_note_module.config(text=f"Note du module : {moyenne:.2f} / 20")

    selected_student["modules"][module_name] = {
        "controles": controles,
        "exam": exam,
        "moyenne": moyenne
    }

    update_module_table()
    calculer_moyenne_generale()
    update_student_list()

def update_module_table():
    for r in tree_modules.get_children():
        tree_modules.delete(r)
    if not selected_student:
        return
    for m, d in selected_student["modules"].items():
        controles = ", ".join(f"{c:.2f}" for c in d["controles"])
        tree_modules.insert("", tk.END, values=(m, controles, f"{d['exam']:.2f}", f"{d['moyenne']:.2f}"))

def on_module_select(event):
    """Lorsque l'utilisateur sélectionne une ligne dans la table modules,
       on charge les valeurs dans les champs pour édition/consultation."""
    sel = tree_modules.selection()
    if not sel or not selected_student:
        return
    item = sel[0]
    vals = tree_modules.item(item, "values")
    if not vals:
        return
    module_name = vals[0]
    # sécuriser l'accès
    data = selected_student["modules"].get(module_name)
    if not data:
        return

    # définir module dans le combobox
    combo_module.set(module_name)

    # ajuster spinbox au nombre de contrôles et recréer entrées
    n = len(data["controles"])
    spin_controls.delete(0, tk.END)
    spin_controls.insert(0, str(n))
    update_controls_fields()

    # remplir contrôles
    for i, val in enumerate(data["controles"]):
        if i < len(entries_controles):
            entries_controles[i].delete(0, tk.END)
            entries_controles[i].insert(0, f"{val:.2f}")

    # remplir examen
    entry_exam.delete(0, tk.END)
    entry_exam.insert(0, f"{data['exam']:.2f}")

    # afficher note du module
    label_note_module.config(text=f"Note du module : {data['moyenne']:.2f} / 20")

def calculer_moyenne_generale():
    if not selected_student:
        return
    modules = selected_student["modules"]
    if not modules:
        selected_student["average"] = None
    else:
        selected_student["average"] = round(sum(d["moyenne"] for d in modules.values()) / len(modules), 2)
    update_overall_label()
    update_student_list()

def update_overall_label():
    if not selected_student or selected_student["average"] is None:
        label_moyenne_gen.config(text="Moyenne générale : -- / 20")
    else:
        label_moyenne_gen.config(text=f"Moyenne générale : {selected_student['average']:.2f} / 20")

def update_selected_label():
    if not selected_student:
        label_selected.config(text="Étudiant sélectionné : Aucun")
    else:
        label_selected.config(
            text=f"Étudiant sélectionné : {selected_student['nom']} {selected_student['prenom']} (Âge {selected_student['age']})"
        )

# ========================= INTERFACE =========================
root = tk.Tk()
root.title("Gestion des notes - Tkinter")
root.geometry("1250x720")

main = tk.Frame(root)
main.pack(fill=tk.BOTH, expand=True)

main.grid_columnconfigure(0, weight=3)
main.grid_columnconfigure(1, weight=2)
main.grid_rowconfigure(0, weight=1)

# ---------- PARTIE GAUCHE ----------
left = tk.Frame(main, relief=tk.GROOVE, bd=2)
left.grid(row=0, column=0, sticky="nsew", padx=(0,5), pady=4)

tk.Label(left, text="Ajouter un étudiant (max 20)", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10,6))
tk.Label(left, text="Nom").grid(row=1, column=0, sticky="w", padx=10)
entry_nom = tk.Entry(left)
entry_nom.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=2)

tk.Label(left, text="Prénom").grid(row=2, column=0, sticky="w", padx=10)
entry_prenom = tk.Entry(left)
entry_prenom.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=2)

tk.Label(left, text="Âge").grid(row=3, column=0, sticky="w", padx=10)
entry_age = tk.Entry(left, width=5)
entry_age.grid(row=3, column=1, sticky="w", padx=10)

tk.Button(left, text="Ajouter l'étudiant", bg="#4CAF50", fg="white", command=add_student).grid(row=3, column=2, sticky="e", padx=10)

cols = ("ID", "Nom", "Prénom", "Âge", "Moyenne")
tree_students = ttk.Treeview(left, columns=cols, show="headings", selectmode="browse")
for c in cols:
    tree_students.heading(c, text=c)
    if c == "ID":
        tree_students.column(c, width=40, anchor="center")
    elif c == "Moyenne":
        tree_students.column(c, width=100, anchor="center")
    else:
        tree_students.column(c, width=150)

tree_students.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=(8,6))
scroll = ttk.Scrollbar(left, orient=tk.VERTICAL, command=tree_students.yview)
tree_students.configure(yscroll=scroll.set)
scroll.grid(row=4, column=3, sticky="ns", pady=(8,6))
tree_students.bind("<<TreeviewSelect>>", on_student_select)

btn_frame_left = tk.Frame(left)
btn_frame_left.grid(row=5, column=0, columnspan=4, sticky="ew", padx=10, pady=6)
btn_frame_left.grid_columnconfigure((0,1,2), weight=1)
tk.Button(btn_frame_left, text="Supprimer", bg="#f44336", fg="white", command=delete_student).grid(row=0, column=0, sticky="ew", padx=3)
tk.Button(btn_frame_left, text="Vider tout", bg="#9E9E9E", fg="white", command=clear_all).grid(row=0, column=1, sticky="ew", padx=3)

# ---------- PARTIE DROITE ----------
right = tk.Frame(main, relief=tk.GROOVE, bd=2)
right.grid(row=0, column=1, sticky="nsew", padx=(5,0), pady=4)

tk.Label(right, text="Saisie des notes", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=6)
label_selected = tk.Label(right, text="Étudiant sélectionné : Aucun")
label_selected.grid(row=1, column=0, columnspan=4, sticky="w", padx=10)

tk.Label(right, text="Module (1–8):").grid(row=2, column=0, sticky="w", padx=10)
combo_module = ttk.Combobox(right, values=[f"Module {i}" for i in range(1,9)], state="readonly")
combo_module.grid(row=2, column=1, sticky="w", padx=10)
combo_module.set("Module 1")

tk.Label(right, text="Nombre de contrôles (1–3):").grid(row=2, column=2, sticky="e")
spin_controls = tk.Spinbox(right, from_=1, to=3, width=5, command=update_controls_fields)
spin_controls.grid(row=2, column=3, sticky="w", padx=5)
spin_controls.delete(0, tk.END)
spin_controls.insert(0, "2")

# Cadre dynamique des contrôles
frame_controles = tk.Frame(right)
frame_controles.grid(row=3, column=0, columnspan=4, sticky="w")
entries_controles = []
update_controls_fields()

tk.Label(right, text="Examen final :").grid(row=4, column=0, sticky="w", padx=10, pady=(4,2))
entry_exam = tk.Entry(right, width=6)
entry_exam.grid(row=4, column=1, sticky="w", padx=10, pady=(4,2))

label_note_module = tk.Label(right, text="Note du module : -- / 20", font=("Segoe UI", 9))
label_note_module.grid(row=5, column=0, columnspan=4, sticky="w", padx=10, pady=4)
tk.Label(right, text="Modules de l'étudiant", font=("Segoe UI", 10, "bold")).grid(row=5, column=0, columnspan=4, sticky="w", padx=10, pady=(10,4))

cols2 = ("Module", "Contrôles", "Examen", "Note")
tree_modules = ttk.Treeview(right, columns=cols2, show="headings", selectmode="browse", height=10)
for c in cols2:
    tree_modules.heading(c, text=c)
    if c == "Module":
        tree_modules.column(c, width=140, anchor="w")
    else:
        tree_modules.column(c, width=120, anchor="center")

tree_modules.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=10, pady=(8,6))
tree_modules.bind("<<TreeviewSelect>>", on_module_select)

label_moyenne_gen = tk.Label(right, text="Moyenne générale : -- / 20", font=("Segoe UI", 10, "bold"))
label_moyenne_gen.grid(row=7, column=0, columnspan=3, sticky="e", padx=10, pady=(6,10))

btn_frame_right = tk.Frame(right)
btn_frame_right.grid(row=8, column=0, columnspan=4, sticky="ew", padx=10, pady=(6,10))
btn_frame_right.grid_columnconfigure((0,1,2), weight=1)
tk.Button(btn_frame_right, text="Enregistrer module", bg="#4CAF50", fg="white", command=save_module).grid(row=0, column=0, sticky="ew", padx=4)
tk.Button(btn_frame_right, text="Recalculer moyenne", bg="#2196F3", fg="white", command=calculer_moyenne_generale).grid(row=0, column=1, sticky="ew", padx=4)
tk.Button(btn_frame_right, text="Calculer", bg="#FF9800", fg="white", command=calculer_moyenne_generale).grid(row=0, column=2, sticky="ew", padx=4)

root.mainloop()
