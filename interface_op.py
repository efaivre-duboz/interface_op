import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

   #Emplacement du fichier Excel sur OneDrive#
excel_path = r"C:/Users/efaivre-duboz/OneDrive - SG Énergie/Production/historique_production.xlsx"
os.makedirs(os.path.dirname(excel_path), exist_ok=True)
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
for key in [
    'logged_in', 'user', 'location',
    'start_time', 'prod_end_time', 'qa_end_time',
    'pause_start', 'total_pause', 'product', 'quantity'
]:
    if key not in st.session_state:
        st.session_state[key] = None

st.title("Production & Assurance Qualité")

# --- 0. Connexion (page unique avec Logout) ---
if not st.session_state.logged_in:
    st.subheader("Connexion opérateur")
    u = st.text_input("Nom d'utilisateur")
    p = st.text_input("Mot de passe", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Se connecter"):
            if u == "OP1" and p == "123":
                st.session_state.logged_in = True
                st.session_state.user = u
                st.success("Connecté en tant que OP1.")
            else:
                st.error("Identifiants incorrects.")
    with c2:
        if st.button("Logout"):
            for k in list(st.session_state.keys()):
                st.session_state[k] = None
            st.success("Déconnecté.")
    st.stop()

# --- 1. Sélection du lieu ---
if st.session_state.location is None:
    st.subheader("Sélection du lieu de production")
    lieu = st.selectbox("Lieu", ["Québec", "Saint-Marc"])
    if st.button("Valider lieu"):
        st.session_state.location = lieu
        st.success(f"Lieu : {lieu}")
    st.stop()

# Affichage informations globales
st.markdown(f"**Opérateur :** {st.session_state.user}")
st.markdown(f"**Lieu :** {st.session_state.location}")

# --- 2. Scan & début production ---
if st.session_state.start_time is None:
    st.subheader("Scan d'initialisation")
    scan = st.text_input("Produit,Quantité (ex: BLC-310 V2,10)", key="scan_input")
    if st.button("Valider scan"):
        try:
            prod, qty = [x.strip() for x in scan.split(",",1)]
            assert prod in recipes
            st.session_state.product = prod
            st.session_state.quantity = float(qty)
            st.session_state.start_time = datetime.now()
            st.session_state.total_pause = timedelta()
            st.success("Début production capturé.")
        except AssertionError:
            st.error("Produit non reconnu.")
        except:
            st.error("Format invalide.")
    st.stop()

# Affichage début production
st.markdown(f"**Début prod :** {st.session_state.start_time:%Y-%m-%d %H:%M:%S}")

# --- 3. Production & pause ---
qty = st.session_state.quantity
rec = recipes[st.session_state.product]
st.subheader("Recette calculée")
df = pd.DataFrame([{'Ingrédient':i,'Qté':round(r*qty,3),'Unité':u} for i,(r,u) in rec.items()]).set_index('Ingrédient')
st.table(df)

st.subheader("Quantités réelles")
for ingr in rec:
    key = f"real_{ingr}"
    default = round(rec[ingr][0]*qty,3)
    st.number_input(ingr, value=st.session_state.get(key,default), step=0.001, key=key)

if st.session_state.pause_start is None:
    if st.button("Pause" ):
        st.session_state.pause_start = datetime.now()
        st.success("Production en pause.")
        st.stop()
else:
    st.markdown(f"**En pause depuis :** {st.session_state.pause_start:%H:%M:%S}")
    if st.button("Reprendre"):
        now = datetime.now()
        st.session_state.total_pause += now - st.session_state.pause_start
        st.session_state.pause_start = None
        st.success("Production reprise.")
        st.stop()

if st.session_state.prod_end_time is None:
    if st.button("Fin production"):
        st.session_state.prod_end_time = datetime.now()
        st.success("Fin production capturée.")
    st.stop()

# --- 4. Assurance Qualité & export ---
st.markdown(f"**Fin prod / Début QA :** {st.session_state.prod_end_time:%Y-%m-%d %H:%M:%S}")
tests = quality_tests.get(st.session_state.product,[])
for t in tests:
    st.radio(t, ["Conforme","Non conforme"], key=f"test_{t}")

if st.button("Fin QA"):
    st.session_state.qa_end_time = datetime.now()
    active = st.session_state.qa_end_time - st.session_state.start_time - st.session_state.total_pause
    rec_record = {**{
        'Opérateur':st.session_state.user,
        'Lieu':st.session_state.location,
        'Produit':st.session_state.product,
        'Quantité':st.session_state.quantity,
        'Début prod':st.session_state.start_time,
        'Fin prod':st.session_state.prod_end_time,
        'Pause':st.session_state.total_pause,
        'Fin QA':st.session_state.qa_end_time,
        'Durée active':active
    }}
    rec_record.update({ingr:st.session_state[f"real_{ingr}"] for ingr in rec})
    rec_record.update({f"Test {t}":st.session_state[f"test_{t}"] for t in tests})
    dfnew = pd.DataFrame([rec_record])
    old = pd.read_excel(excel_path) if os.path.exists(excel_path) else pd.DataFrame()
    pd.concat([old,dfnew],ignore_index=True).to_excel(excel_path,index=False)
    st.success("Données exportées. Nouveau cycle.")
    # Reset cycle
    for k in ['start_time','prod_end_time','qa_end_time','product','quantity','pause_start','total_pause']:
        st.session_state[k]=None
    st.stop()


