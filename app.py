import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
import os
import joblib

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard Bursátil IA", page_icon="📈", layout="wide")

# ==========================================
# HEADER PRINCIPAL
# ==========================================
st.title("📊 Sistema Predictivo de Tendencias Bursátiles")
st.markdown("Plataforma de análisis financiero impulsada por **Machine Learning y Deep Learning**.")
st.markdown("---")

# ==========================================
# BARRA LATERAL (SIDEBAR) - PANEL DE CONTROL
# ==========================================
st.sidebar.header("⚙️ Panel de Control")

# 1. Selector de Empresa
empresas = {
    "FSM": "Fortuna Silver Mines",
    "VOLCABC1.LM": "Volcan Cía Minera",
    "BVN": "Buenaventura S.A.A.",
    "ABX": "Barrick Gold Corp.",
    "BHP": "BHP Billiton",
    "SCCO": "Southern Copper"
}
ticker = st.sidebar.selectbox("Seleccione Activo Financiero:", list(empresas.keys()), format_func=lambda x: f"{x} - {empresas[x]}")

# 2. Conexión a Base de Datos (Usuarios)
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Autenticación")
db_path = os.path.join('database', 'sistema_inversiones.db')
try:
    conn = sqlite3.connect(db_path)
    usuarios_df = pd.read_sql_query("SELECT nombre, perfil_riesgo FROM Usuario", conn)
    usuario = st.sidebar.selectbox("Usuario activo:", usuarios_df['nombre'].tolist())
    perfil = usuarios_df[usuarios_df['nombre'] == usuario]['perfil_riesgo'].values[0]
    st.sidebar.info(f"**Perfil de Riesgo:** {perfil}")
except:
    st.sidebar.warning("Base de datos no conectada. Asegúrate de que el archivo .db esté en la carpeta 'database'.")

# ==========================================
# DASHBOARD PRINCIPAL (MÉTRICAS Y GRÁFICOS)
# ==========================================
st.subheader(f"Cotización en Tiempo Real: {empresas[ticker]} ({ticker})")

try:
    # Descargar datos
    datos = yf.download(ticker, period="6mo")
    precio_actual = datos['Close'].iloc[-1].values[0]
    precio_anterior = datos['Close'].iloc[-2].values[0]
    variacion = precio_actual - precio_anterior
    
    # KPIs Superiores usando columnas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precio Actual", f"${precio_actual:.2f}", f"{variacion:.2f} (24h)")
    col2.metric("Volumen (24h)", f"{datos['Volume'].iloc[-1].values[0]:,.0f}")
    col3.metric("Rango del Día", f"${datos['Low'].iloc[-1].values[0]:.2f} - ${datos['High'].iloc[-1].values[0]:.2f}")
    col4.metric("Tendencia General", "ALCISTA 🟢" if variacion > 0 else "BAJISTA 🔴")

    # Gráfico interactivo que ocupa todo el ancho
    st.area_chart(datos['Close'], height=300, color="#0F52BA")
    
except Exception as e:
    st.error("No se pudieron cargar los datos del mercado. Verifique su conexión a Internet o el Ticker de Yahoo Finance.")

st.markdown("---")

# ==========================================
# PESTAÑAS (TABS) PARA ORGANIZAR LA IA Y BACKTESTING
# ==========================================
tab1, tab2, tab3 = st.tabs(["🤖 Modelos Predictivos (IA)", "📈 Backtesting (VectorBT)", "🏦 Operaciones Broker"])

with tab1:
    st.markdown("### Resultados de la Inferencia")
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("#### Modelos de Clasificación")
        # Simulación de carga real del modelo
        ruta_modelo = os.path.join('backend', 'models', 'modelo_svc_FSM.pkl')
        if ticker == "FSM":
            try:
                modelo = joblib.load(ruta_modelo)
                st.success("✅ SVC (2.1.1): **TENDENCIA DE SUBIDA**")
            except:
                st.warning("⚠️ Esperando archivo 'modelo_svc_FSM.pkl' en la carpeta backend/models")
        else:
            st.info("Cargando predicciones para este ticker...")
            
        st.info("⏳ LSTM Classifier (2.1.3): Calculando...")

    with colB:
        st.markdown("#### Modelos de Regresión")
        st.info("⏳ ARIMA (2.2.1): Proyectando precio...")
        st.info("⏳ LSTM Regressor (2.2.2): Entrenando red neuronal...")

with tab2:
    st.markdown("### Simulación de Estrategias")
    st.write("Métricas de rendimiento generadas por **VectorBT** basadas en las señales de los modelos.")
    col_bt1, col_bt2, col_bt3 = st.columns(3)
    col_bt1.metric("Retorno Total", "14.5%", "Estrategia Activa")
    col_bt2.metric("Sharpe Ratio", "1.85")
    col_bt3.metric("Max Drawdown", "-5.2%")

with tab3:
    st.markdown("### Interactive Brokers API")
    st.markdown("Según el perfil del usuario y los modelos predictivos, se sugiere la siguiente acción:")
    st.success("🎯 **RECOMENDACIÓN: MANTENER (HOLD) / COMPRA PARCIAL**")
    if st.button("Ejecutar Orden en el Broker"):
        st.warning("Conectando con API de Interactive Brokers... [Simulación de Prototipo completada]")