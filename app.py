import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Asistente Waldner - Botonera", layout="centered")

# --- SEGURIDAD ---
PASSWORD_GUEST = "Gu€st"

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("🔐 Acceso Restringido")
    pwd = st.text_input("Introduce la contraseña:", type="password")
    if st.button("Entrar"):
        if pwd == PASSWORD_GUEST:
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Streamlit leerá el Excel que subas al repositorio
    df = pd.read_excel("botonera.xlsx", sheet_name="ES", dtype=str)
    df.iloc[:, 0] = df.iloc[:, 0].str.replace(r'\.0$', '', regex=True).str.strip()
    return df

df = load_data()

st.title("🎹 Asistente de Botonera Waldner")
st.write("Identifica tu caso en el mosaico y selecciona el número correspondiente.")

# --- VISUALIZACIÓN ---
# Mostrar Mosaico
if os.path.exists("fotos_botonera/mosaico.jpg"):
    st.image("fotos_botonera/mosaico.jpg", use_column_width=True)

# Selector de caso
opciones = ["Selecciona un número..."] + sorted(df.iloc[:, 0].unique().tolist(), key=int)
seleccion = st.selectbox("Número de situación:", opciones)

if seleccion != "Selecciona un número...":
    fila = df[df.iloc[:, 0] == seleccion].iloc[0]
    
    st.divider()
    st.subheader(f"Caso {seleccion}: {fila.iloc[1]}")
    
    # Mostrar foto del caso
    foto_path = f"fotos_botonera/{seleccion}.jpg"
    if os.path.exists(foto_path):
        st.image(foto_path, caption=f"Situación {seleccion}")
    
    # Diagnóstico y Acción
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**📝 DIAGNÓSTICO:**\n\n{fila.iloc[2]}")
    with col2:
        st.success(f"**🛠 ACCIÓN:**\n\n{fila.iloc[3]}")

if st.button("Cerrar Sesión"):
    st.session_state["auth"] = False
    st.rerun()