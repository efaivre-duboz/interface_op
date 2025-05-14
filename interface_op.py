import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Emplacement du fichier Excel sur OneDrive
excel_path = r"C:/Users/efaivre-duboz/OneDrive - SG Énergie/Production/historique_production.xlsx"

recipes = {
    "BLC-310 V2": {
        "Base organique pure": (0.98, "L"),
        "V584": (0.05, "kg"),
        "PD-585": (0.05, "kg"),
        "D&C Green 6": (0.00132, "kg")
    },
    # ... autres recettes ici ...
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
    df_real = pd.DataFrame(real_inputs)
    st.dataframe(df_real.set_index("Ingrédient"))

    st.subheader("Contrôle Qualité")
    test1 = st.radio("Test 1 :", ["Conforme", "Non conforme"], key="test1")
    test2 = st.radio("Test 2 :", ["Conforme", "Non conforme"], key="test2")
    test3 = st.radio("Test 3 :", ["Conforme", "Non conforme"], key="test3")

    assurance_qualite = "Revue nécessaire" if "Non conforme" in [test1, test2, test3] else "Aucune"

    if st.button("Exporter les données"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        export_data = {
            "Date et heure": timestamp,
            "Produit": product,
            "Quantité produite (L)": quantity,
            "Assurance qualité": assurance_qualite
        }

        for row in real_inputs:
            export_data[f"{row['Ingrédient']} ({row['Unité']})"] = row["Ajout réel"]

        df_export = pd.DataFrame([export_data])

        if os.path.exists(excel_path):
            try:
                existing_df = pd.read_excel(excel_path)
                df_combined = pd.concat([existing_df, df_export], ignore_index=True)
            except:
                df_combined = df_export
        else:
            df_combined = df_export

        df_combined.to_excel(excel_path, index=False)
        st.success("Les données ont été exportées dans l'historique de production.")

        if assurance_qualite == "Revue nécessaire":
            st.warning("Produit à auditer en raison d’un test non conforme.")
