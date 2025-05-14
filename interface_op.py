
import streamlit as st
import pandas as pd
from datetime import datetime

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

st.title("Livre de recette")

product = st.selectbox("Choisir un produit à produire :", list(recipes.keys()))
quantity = st.number_input("Quantité à produire (Litre de produit fini) :", min_value=1.0, step=1.0)

data_export = []

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if product and quantity:
    st.subheader("Ingrédients calculés :")
    recipe = recipes[product]
    data = []

    for ingredient, (ratio, unit) in recipe.items():
        qty = ratio * quantity
        data.append({
            "Ingrédient": ingredient,
            "Ratio": ratio,
            "Quantité demandée": round(qty, 3),
            "Unité": unit
        })

    df = pd.DataFrame(data)
    st.dataframe(df[["Ingrédient", "Ratio", "Quantité demandée", "Unité"]].set_index("Ingrédient"))

    st.subheader("Quantités réellement ajoutées :")
    real_inputs = []
    for row in data:
        ingredient = row["Ingrédient"]
        unit = row["Unité"]
        default_qty = row["Quantité demandée"]
        real = st.number_input(
            f"{ingredient} ajouté ({unit})",
            value=default_qty,
            key=f"real_{ingredient}"
        )
        real_inputs.append({
            "Ingrédient": ingredient,
            "Quantité demandée": default_qty,
            "Ajout réel": round(real, 3),
            "Écart": round(real - default_qty, 3),
            "Unité": unit
        })

    st.subheader("Récapitulatif des ajouts :")
    df_real = pd.DataFrame(real_inputs).set_index("Ingrédient")
    st.dataframe(df_real[["Quantité demandée", "Ajout réel", "Écart", "Unité"]])

    st.subheader("Contrôle qualité :")
    test_results = {}
    for i in range(1, 4):
        test_results[f"Test {i}"] = st.radio(
            f"Test {i}",
            ["Conforme", "Non conforme"],
            key=f"test_{i}"
        )

    assurance_qualite = "Nécessaire" if "Non conforme" in test_results.values() else "Non nécessaire"

    if "Non conforme" in test_results.values():
        st.warning("⚠️ Résultat non conforme détecté. Mettre le produit en audit pour vérification qualité.")

    if st.button("Exporter les données"):
        df_real.to_csv("ajustements_production.csv")
        pd.DataFrame.from_dict(test_results, orient='index', columns=["Résultat"]).to_csv("controle_qualite.csv")

        historique = {
            "Date et heure": timestamp,
            "Produit": product,
            "Ingrédients": ", ".join(df["Ingrédient"]),
            "Assurance qualité": assurance_qualite
        }
        pd.DataFrame([historique]).to_csv("historique_production.csv", mode='a', index=False, header=False)

        st.success("Fichiers exportés : ajustements_production.csv, controle_qualite.csv et historique_production.csv")
