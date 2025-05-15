import streamlit as st
import pandas as pd
from datetime import datetime
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

for var in [
    'start_time', 'prod_end_time', 'qa_end_time',
    'product', 'quantity',
    'logged_in', 'user', 'location'
]:
    if var not in st.session_state:
        st.session_state[var] = None
       
st.title("Production & Assurance Qualité")

# 0. Connexion opérateur
if not st.session_state.logged_in:
    st.subheader("Connexion opérateur")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "OP1" and password == "123":
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Connecté en tant que OP1")
            st.stop()
        else:
            st.error("Identifiants incorrects.")
    st.stop()

# 1. Sélection du lieu de production
if not st.session_state.location:
    st.subheader("Sélection du lieu de production")
    lieu = st.selectbox("Lieu", ["Québec", "Saint-Marc"])
    if st.button("Valider le lieu"):
        st.session_state.location = lieu
        st.success(f"Lieu défini: {lieu}")
        st.stop()
    st.stop()

# Affichage des informations utilisateur et lieu
st.markdown(f"**Opérateur :** {st.session_state.user}")
st.markdown(f"**Lieu de production :** {st.session_state.location}")

# 2. Scan code-barres -> début production
if st.session_state.start_time is None:
    st.subheader("Scan d'initialisation")
    scan = st.text_input("Produit, Quantité (ex: BLC-310 V2, 10)", key="scan_input")
    if scan and st.button("Valider scan"):
        try:
            prod, qty = [s.strip() for s in scan.split(",",1)]
            if prod not in recipes:
                st.error(f"Produit '{prod}' non reconnu.")
            else:
                st.session_state.product = prod
                st.session_state.quantity = float(qty)
                st.session_state.start_time = datetime.now()
                st.success("Début de production enregistré.")
                st.stop()
        except:
            st.error("Format invalide. Utilisez 'Produit, Quantité'.")
    st.stop()

# 3. Saisie production -> fin production
st.markdown(f"**Début production :** {st.session_state.start_time:%Y-%m-%d %H:%M:%S}")
qty = st.session_state.quantity
recipe = recipes[st.session_state.product]
st.subheader("Quantités calculées")
data = []
for ingr, (ratio, unit) in recipe.items():
    needed = ratio * qty
    data.append({"ingr":ingr, "needed":round(needed,3), "unit":unit})
st.table(pd.DataFrame(data).rename(columns={"ingr":"Ingrédient","needed":"Qté demandée","unit":"Unité"}).set_index("Ingrédient"))

st.subheader("Quantités réelles")
for row in data:
    key = f"real_{row['ingr']}"
    if key not in st.session_state:
        st.session_state[key] = row['needed']
    st.session_state[key] = st.number_input(f"{row['ingr']} ({row['unit']})", value=st.session_state[key], step=0.001, key=key)

if st.session_state.prod_end_time is None:
    if st.button("Fin production"):
        st.session_state.prod_end_time = datetime.now()
        st.success("Fin de production enregistrée.")
        st.stop()
    st.stop()

# 4. QA -> fin QA
st.markdown(f"**Fin production / Début QA :** {st.session_state.prod_end_time:%Y-%m-%d %H:%M:%S}")
tests = quality_tests.get(st.session_state.product, [])
for test in tests:
    key = f"test_{test}"
    if key not in st.session_state:
        st.session_state[key] = "Conforme"
    st.session_state[key] = st.radio(f"{test}", ["Conforme","Non conforme"], key=key)

if st.session_state.qa_end_time is None:
    if st.button("Fin QA"):
        st.session_state.qa_end_time = datetime.now()
        st.success("Fin QA enregistrée.")
        st.stop()
    st.stop()

# 5. Export des données
st.markdown(f"**Fin QA :** {st.session_state.qa_end_time:%Y-%m-%d %H:%M:%S}")
if st.button("Exporter données"):
    duration = st.session_state.qa_end_time - st.session_state.start_time
    export = {
        "Opérateur": st.session_state.user,
        "Lieu": st.session_state.location,
        "Produit": st.session_state.product,
        "Quantité (L)": st.session_state.quantity,
        "Début production": st.session_state.start_time,
        "Fin production": st.session_state.prod_end_time,
        "Fin QA": st.session_state.qa_end_time,
        "Durée totale": duration
    }
    for ingr in recipes[st.session_state.product]:
        key = f"real_{ingr}"
        export[f"{ingr} ({recipes[st.session_state.product][ingr][1]})"] = st.session_state[key]
    for test in tests:
        export[f"Test {test}"] = st.session_state[f"test_{test}"]
    df_new = pd.DataFrame([export])
    if os.path.exists(excel_path):
        try:
            df_old = pd.read_excel(excel_path)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        except:
            df_all = df_new
    else:
        df_all = df_new
    df_all.to_excel(excel_path, index=False)
    st.success("Données exportées vers Excel.")
