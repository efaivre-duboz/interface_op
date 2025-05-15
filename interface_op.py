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
state_vars = [
    'stage',        # 0: login, 1: lieu, 2: scan, 3: production, 4: QA
    'user', 'location',
    'start_time', 'prod_end_time', 'qa_end_time',
    'pause_start', 'total_pause',
    'product', 'quantity'
]
for key in state_vars:
    if key not in st.session_state:
        st.session_state[key] = 0 if key == 'stage' else None

st.title("Production & Assurance Qualité")

# --- 1. Connexion ---
if st.session_state.stage == 0:
    st.subheader("Connexion opérateur")
    user = st.text_input("Nom d'utilisateur", key="login_user")
    pwd  = st.text_input("Mot de passe", type="password", key="login_pwd")
    if st.button("Se connecter"):
        if user == "OP1" and pwd == "123":
            st.session_state.user = user
            st.session_state.stage = 1
        else:
            st.error("Identifiants incorrects.")
    st.stop()

# --- 2. Sélection du lieu ---
if st.session_state.stage == 1:
    st.subheader("Sélection du lieu de production")
    lieu = st.selectbox("Lieu", ["Québec", "Saint-Marc"], key="select_location")
    if st.button("Valider lieu"):
        st.session_state.location = lieu
        st.session_state.stage = 2
        st.success(f"Lieu défini : {lieu}.")
    st.stop()

# Affichage informations globales
st.markdown(f"**Opérateur :** {st.session_state.user}")
st.markdown(f"**Lieu :** {st.session_state.location}")

# --- 3. Scan & début production ---
if st.session_state.stage == 2:
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("Déconnexion"):
            for k in state_vars:
                st.session_state[k] = 0 if k == 'stage' else None
            st.stop()
    with col1:
        st.subheader("Scan d'initialisation")
        scan = st.text_input("Produit, Quantité (ex: BLC-310 V2,10)", key="scan_input")
        if st.button("Valider scan"):
            parts = scan.split(",",1)
            if len(parts) != 2:
                st.error("Format invalide. Utilisez 'Produit,Quantité'.")
            else:
                prod, qty = parts[0].strip(), parts[1].strip()
                if prod not in recipes:
                    st.error(f"Produit '{prod}' non reconnu.")
                else:
                    try:
                        qty_f = float(qty)
                        st.session_state.product = prod
                        st.session_state.quantity = qty_f
                        st.session_state.start_time = datetime.now()
                        st.session_state.total_pause = timedelta()
                        st.session_state.stage = 3
                        st.success("Début production enregistré.")
                    except ValueError:
                        st.error("Quantité doit être un nombre.")
    st.stop()

# --- 4. Production & pause ---
if st.session_state.stage == 3:
    st.markdown(f"**Début prod :** {st.session_state.start_time:%Y-%m-%d %H:%M:%S}")
    qty = st.session_state.quantity
    rec = recipes[st.session_state.product]

    st.subheader("Recette calculée")
    df_req = pd.DataFrame([
        {'Ingrédient': i, 'Qté demandée': round(ratio*qty,3), 'Unité': unit}
        for i,(ratio,unit) in rec.items()
    ]).set_index('Ingrédient')
    st.table(df_req)

    st.subheader("Quantités réelles")
    for ingr,(ratio,unit) in rec.items():
        key = f"real_{ingr}"
        default = round(ratio*qty,3)
        st.number_input(
            label=f"{ingr} ({unit})", 
            value=st.session_state.get(key, default),
            step=0.001,
            key=key
        )

    # Pause / Reprendre
    if st.session_state.pause_start is None:
        if st.button("Pause"):
            st.session_state.pause_start = datetime.now()
            st.success("Production en pause.")
    else:
        st.markdown(f"**En pause depuis :** {st.session_state.pause_start:%H:%M:%S}")
        if st.button("Reprendre"):
            now = datetime.now()
            st.session_state.total_pause += now - st.session_state.pause_start
            st.session_state.pause_start = None
            st.success("Production reprise.")

    # Fin production
    if st.button("Fin production"):
        st.session_state.prod_end_time = datetime.now()
        st.session_state.stage = 4
        st.success("Fin production enregistrée.")
    st.stop()

# --- 5. Assurance Qualité & export ---
if st.session_state.stage == 4:
    st.markdown(f"**Fin prod / Début QA :** {st.session_state.prod_end_time:%Y-%m-%d %H:%M:%S}")
    tests = quality_tests.get(st.session_state.product, [])
    for t in tests:
        st.radio(label=t, options=["Conforme","Non conforme"], key=f"test_{t}")

    if st.button("Fin QA"):
        st.session_state.qa_end_time = datetime.now()
        # Calcul durée active hors pause
        active_dur = (st.session_state.qa_end_time - 
                      st.session_state.start_time - 
                      st.session_state.total_pause)
        # Construction de l'enregistrement
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
        # Ingrédients réels
        for ingr in recipes[st.session_state.product]:
            unit = recipes[st.session_state.product][ingr][1]
            record[f"{ingr} ({unit})"] = st.session_state.get(f"real_{ingr}")
        # Résultats QA
        for t in tests:
            record[f"Test {t}"] = st.session_state.get(f"test_{t}")

        df_new = pd.DataFrame([record])
        if os.path.exists(excel_path):
            try:
                df_old = pd.read_excel(excel_path)
                df_all = pd.concat([df_old, df_new], ignore_index=True)
            except:
                df_all = df_new
        else:
            df_all = df_new
        df_all.to_excel(excel_path, index=False)
        st.success("Données exportées. Retour au scan.")
        # Reset cycle (stage = 2 pour scan)
        for key in ['start_time','prod_end_time','qa_end_time','pause_start','total_pause','product','quantity']:
            st.session_state[key] = None
        st.session_state.stage = 2
        st.stop()
