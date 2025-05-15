import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import warnings

# Configuration du fichier Excel
# Chemin OneDrive local
onedrive_folder = r"C:/Users/efaivre-duboz/OneDrive - SG Énergie/Production"
# Si ce dossier existe localement, on y enregistre; sinon, on utilise le répertoire courant
if os.path.isdir(onedrive_folder):
    excel_dir = onedrive_folder
else:
    excel_dir = os.getcwd()
os.makedirs(excel_dir, exist_ok=True)
excel_path = os.path.join(excel_dir, "historique_production.xlsx")

# Utilisateurs
# Dictionnaire username: password
users = {
    "OP1": "123",
    # Ajouter d'autres utilisateurs ici
    "ADMIN": "PASS",
    # Ajouter d'autres utilisateurs ici
}


recipes = {
    "BLC-310 V2": {
        "Base organique pure": (0.98, "L"),
        "V584": (0.05, "kg"),
        "PD-585": (0.05, "kg"),
        "D&C Green 6": (0.00132, "kg")
    },
    "BLC-402": {
        "Base Ester bio": (1.00, "L")
    },
    "BLC-406": {
        "Base Ester bio": (0.943, "L"),
        "ETHAL LA-4": (0.066, "L")
    },
    "BLC-475": {
        "Base Ester bio": (0.40, "L"),
        "FlorasolV LX300": (0.55, "L"),
        "NINOL 11-CM": (0.05, "L")
    },
    "BLC-489": {
        "Base organique pure": (0.656, "L"),
        "Base Ester bio": (0.40, "L")
    },
    "BLC-505": {
        "Eau": (0.498, "L"),
        "Glycérine 95%": (0.320, "L"),
        "Méthanol": (0.08, "L"),
        "Estisurf 970": (0.025, "L"),
        "Cycloteric CAB": (0.076, "L")
    },
    "BLC-530": {
        "Base organique pure": (0.9, "L"),
        "Base Ester bio": (0.1, "L")
    },
    "BLC-530JLE": {
        "Base organique pure": (0.800, "L"),
        "Base Ester bio": (0.200, "L")
    },
    "BLC-540": {
        "Base organique pure": (0.864, "L"),
        "Base Ester bio": (0.2, "L"),
        "PD-555": (0.01, "L")
    },
    "LGD-600": {
        "Méthanol": (0.15, "L"),
        "Heptane": (0.65, "L"),
        "Isopropyle alcool": (0.21, "L")
    },
    "Base Ester bio": {
        "Base organique pure": (1.00, "L"),
        "Méthanol": (0.267, "L"),
        "Méthanolate de sodium": (0.0145, "kg"),
        "Acide citrique": (0.0107, "kg"),
        "Eau chaude": (0.5625, "L")
    },
    "BLC-100": {
        "Base Ester Bio": (0.97, "L"),
        "NALUBE BL-1208": (0.023, "L"),
        "PD-585": (0.009, "L")
    },
    "BLC-1405": {
        "Eau": (0.750, "L"),
        "CITRI-MET": (0.108, "kg"),
        "Florasolv LX300": (0.058, "L"),
        "Base Ester bio": (0.037, "L"),
        "NINOL 11-CM": (0.085, "L")
    },
    "BLC-1500": {
        "Eau": (0.600, "L"),
        "Bio-Terge PAS-8S": (0.001, "L"),
        "Méthanol": (0.400, "L"),
        "Keyacid Blue FG Liquid": (0.0275, "L"),
        "Keyacid Tartrazine Supra Liquid": (0.015, "L")
    },
    "BLC-1520": {
        "Eau": (0.800, "L"),
        "Méthanol": (0.200, "L"),
        "Keyacid Tartrazine Supra Liquid": (0.015, "L")
    },
    "BLC-1650": {
        "Eau": (0.875, "L"),
        "Glycol ether EB": (0.083, "L"),
        "Bio-Soft GSB-9": (0.05, "L"),
        "Carbonate de sodium": (0.035, "kg")
    },
    "BIOPAV 20S": {
        "Eau": (0.470, "L"),
        "Glycérine 80-85%": (0.400, "L"),
        "Méthanol": (0.100, "L"),
        "Cycloteric CAPB": (0.0318, "kg")
    },
    "BIOPAV Huile démoulage Ecoform": {
        "Base organique brute": (1.000, "L"),
        "Parfum": (0.0003, "L")
    },
    "BIOPAV Huile démoulage structurale": {
        "Base organique brute": (0.700, "L"),
        "Base Ester bio": (0.300, "L"),
        "Parfum": (0.0003, "L")
    },
    "BIOPAV Huile démoulage hydroform": {
        "Base aqueuse brute": (0.500, "L"),
        "Eau": (0.500, "L"),
        "Parfum": (0.0003, "L")
    },
    "BIOPAV 100": {
        "Base Ester bio": (0.850, "L"),
        "Base organique brute": (0.150, "L"),
        "Parfum": (0.0003, "L")
    },
    "BIOPAV 1000": {
        "Estisol 190": (0.6665, "L"),
        "Base Ester bio": (0.3335, "L")
    },
    "BIOPAV 20S Ontario": {
        "Base aqueuse brute": (0.450, "L"),
        "Eau": (0.550, "L"),
        "Pigment bleu": (0.00001375, "L"),
        "Parfum": (0.0003, "L")
    },
    "BIOPAV 20S Québec": {
        "Base aqueuse pure": (0.300, "L"),
        "Base aqueuse brute": (0.120, "L"),
        "Eau": (0.580, "L"),
        "Pigment bleu": (0.00001375, "L"),
        "Parfum": (0.0003, "L"),
        "Sucre": (0.010, "kg")
    }
}

quality_tests = {key: ["Couleur", "Odeur", "pH", "Densité"] for key in recipes.keys()}

# --- Initialisation du session_state ---
state_vars = [
    'stage',  # 0=login,1=lieu,2=scan,3=prod,4=QA
    'login_error','scan_error',
    'user','location','product','quantity',
    'start_time','prod_end_time','qa_end_time','pause_start','total_pause'
]
for var in state_vars:
    if var not in st.session_state:
        st.session_state[var] = (0 if var == 'stage' else None)

st.title("Production & Assurance Qualité")

# Supprimer FutureWarning concat
warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Callbacks ---
def login():
    username = st.session_state.login_user.strip()
    pwd = st.session_state.login_pwd.strip()
    if username in users and users[username] == pwd:
        st.session_state.user = username
        st.session_state.stage = 1
        st.session_state.login_error = None
    else:
        st.session_state.login_error = "Nom d'utilisateur ou mot de passe incorrect."

def set_location():
    st.session_state.location = st.session_state.select_location
    st.session_state.stage = 2

def logout():
    for v in state_vars:
        st.session_state[v] = (0 if v == 'stage' else None)

def handle_scan():
    value = st.session_state.scan_input
    parts = value.split(',', 1)
    if len(parts) != 2:
        st.session_state.scan_error = "Format invalide. Utilisez 'Produit,Quantité'."
        return
    prod, qty = parts[0].strip(), parts[1].strip()
    if prod not in recipes:
        st.session_state.scan_error = f"Produit '{prod}' non reconnu."
        return
    try:
        qty_f = float(qty)
    except ValueError:
        st.session_state.scan_error = "Quantité doit être un nombre."
        return
    # success
    st.session_state.product = prod
    st.session_state.quantity = qty_f
    st.session_state.start_time = datetime.now()
    st.session_state.total_pause = timedelta()
    st.session_state.stage = 3
    st.session_state.scan_error = None

def start_pause():
    st.session_state.pause_start = datetime.now()

def resume_prod():
    now = datetime.now()
    st.session_state.total_pause += now - st.session_state.pause_start
    st.session_state.pause_start = None

def end_production():
    st.session_state.prod_end_time = datetime.now()
    st.session_state.stage = 4

def finalize():
    st.session_state.qa_end_time = datetime.now()
    active_dur = st.session_state.qa_end_time - st.session_state.start_time - st.session_state.total_pause
    record = {
        'Opérateur': st.session_state.user,
        'Lieu': st.session_state.location,
        'Produit': st.session_state.product,
        'Quantité (L)': st.session_state.quantity,
        'Début prod': st.session_state.start_time,
        'Fin prod': st.session_state.prod_end_time,
        'Pause totale': st.session_state.total_pause,
        'Fin QA': st.session_state.qa_end_time,
        'Durée active': active_dur
    }
    # Ingrédients
    for ingr,(r,u) in recipes[st.session_state.product].items():
        record[f"{ingr} ({u})"] = st.session_state.get(f"real_{ingr}")
    # Tests QA
    for t in quality_tests.get(st.session_state.product, []):
        record[f"Test {t}"] = st.session_state.get(f"test_{t}")
    df_new = pd.DataFrame([record])
    # concat si existant
    if os.path.exists(excel_path) and os.path.getsize(excel_path) > 0:
        try:
            df_old = pd.read_excel(excel_path)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        except:
            df_all = df_new
    else:
        df_all = df_new
    df_all.to_excel(excel_path, index=False)
    st.success(f"Données enregistrées dans : {excel_path}")
    # reset cycle
    for v in ['product','quantity','start_time','prod_end_time','qa_end_time','pause_start','total_pause','scan_error']:
        st.session_state[v] = None
    st.session_state.stage = 2

# --- UI selon l'étape ---
if st.session_state.stage == 0:
    st.subheader("Connexion opérateur")
    st.text_input("Nom d'utilisateur", key="login_user")
    st.text_input("Mot de passe", type="password", key="login_pwd")
    st.button("Se connecter", on_click=login)
    if st.session_state.login_error:
        st.error(st.session_state.login_error)

elif st.session_state.stage == 1:
    st.subheader("Sélection du lieu de production")
    st.selectbox("Lieu", ["Québec","Saint-Marc"], key="select_location")
    st.button("Valider lieu", on_click=set_location)

elif st.session_state.stage == 2:
    col1, col2 = st.columns([3,1])
    with col2:
        st.button("Déconnexion", on_click=logout)
    with col1:
        st.subheader("Scan d'initialisation")
        st.text_input("Produit,Quantité (ex: BLC-310 V2,10)", key="scan_input")
        st.button("Valider scan", on_click=handle_scan)
        if st.session_state.scan_error:
            st.error(st.session_state.scan_error)

elif st.session_state.stage == 3:
    st.markdown(f"**Début production :** {st.session_state.start_time:%Y-%m-%d %H:%M:%S}")
    rec = recipes[st.session_state.product]
    st.subheader("Recette calculée")
    df_req = pd.DataFrame([
        {'Ingrédient': i, 'Qté demandée': round(r*st.session_state.quantity,3), 'Unité': u}
        for i,(r,u) in rec.items()
    ]).set_index('Ingrédient')
    st.table(df_req)
    st.subheader("Quantités réelles")
    for ingr,(r,u) in rec.items():
        st.number_input(f"{ingr} ({u})",
                         value=st.session_state.get(f"real_{ingr}", round(r*st.session_state.quantity,3)),
                         key=f"real_{ingr}")
    st.button("Pause", on_click=start_pause)
    if st.session_state.pause_start:
        st.markdown(f"**En pause depuis :** {st.session_state.pause_start:%H:%M:%S}")
        st.button("Reprendre", on_click=resume_prod)
    st.button("Fin production", on_click=end_production)

elif st.session_state.stage == 4:
    st.markdown(f"**Fin prod / Début QA :** {st.session_state.prod_end_time:%Y-%m-%d %H:%M:%S}")
    for t in quality_tests.get(st.session_state.product, []):
        st.radio(t, ["Conforme","Non conforme"], key=f"test_{t}")
    st.button("Fin QA", on_click=finalize)
