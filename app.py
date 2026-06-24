import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Sistema Bancario Pro", layout="centered")

# Título
st.title("🏦 Sistema Bancario Pro")

# Menú lateral
menu = st.sidebar.selectbox("Menú", ["Inicio", "Captura", "Gráficas", "PDF"])

# ------------------ INICIO ------------------
if menu == "Inicio":
    st.subheader("Bienvenido")
    st.write("Sistema profesional de análisis financiero")

# ------------------ CAPTURA ------------------
elif menu == "Captura":
    st.subheader("Captura de datos")

    nombre = st.text_input("Nombre")
    ingreso = st.number_input("Ingreso", min_value=0)
    gastos = st.number_input("Gastos", min_value=0)

    if st.button("Crear reporte"):
        ahorro = ingreso - gastos

        df = pd.DataFrame({
            "Concepto": ["Ingreso", "Gastos", "Ahorro"],
            "Monto": [ingreso, gastos, ahorro]
        })

        df.to_csv("datos.csv", index=False)

        st.success(f"Ahorro calculado: {ahorro}")
        st.dataframe(df)

# ------------------ GRÁFICAS ------------------
elif menu == "Gráficas":
    st.subheader("Visualización")

    try:
        df = pd.read_csv("datos.csv")
        fig, ax = plt.subplots()
        ax.bar(df["Concepto"], df["Monto"])
        ax.set_title("Resumen financiero")
        st.pyplot(fig)
    except:
        st.warning("Primero captura datos")

# ------------------ PDF ------------------
elif menu == "PDF":
    st.subheader("Exportar PDF")

    if st.button("Generar PDF"):
        try:
            df = pd.read_csv("datos.csv")

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="REPORTE FINANCIERO", ln=True)

            for i in range(len(df)):
                pdf.cell(200, 10, txt=f"{df['Concepto'][i]}: {df['Monto'][i]}", ln=True)

            pdf.output("reporte.pdf")

            with open("reporte.pdf", "rb") as f:
                st.download_button("📥 Descargar PDF", f, file_name="reporte.pdf")

        except:
            st.warning("Primero captura datos")
