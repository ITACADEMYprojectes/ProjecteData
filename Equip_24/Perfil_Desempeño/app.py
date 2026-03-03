import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# 1. Configuración de la página
st.set_page_config(page_title="RRHH Analytics Dashboard", layout="wide")

# 2. Carga de datos
base_path = os.path.dirname(os.path.abspath(__file__))
file_name = 'full_RRHH.csv'
csv_path = os.path.join(base_path, file_name)


@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


RRHH_full = load_data(csv_path)

# Verificación de carga
if RRHH_full is None:
    st.error(f"❌ No se encontró el archivo '{file_name}'")
    st.stop()  # Detiene la ejecución si no hay datos

# --- SECCIÓN 1: TÍTULO Y MÉTRICAS (KPIs) ---
st.title("Diagnóstico Sociodemográfico y Plan de Fidelización")

# ==========================================
# 1. LÓGICA DE PROCESAMIENTO (DATAFRAMES E IA)
# ==========================================

# Agrupación inicial
df_id = RRHH_full.groupby('ID').agg({
    'Age': 'mean',
    'Body_mass_index': 'mean',
    'Son': 'mean',
    'Education': 'first',
    'Social_drinker': 'max',
    'Social_smoker': 'max'
}).reset_index()

# Pre-procesamiento y Clustering
df_numeric = pd.get_dummies(
    df_id, columns=['Education', 'Social_drinker', 'Social_smoker'])
X = df_numeric.drop(columns=['ID'])
X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

# Mapeo de nombres y creación de la columna 'Segmento'
mapeo_nombres = {
    "0": "Segmento A: Motor Familiar",
    "1": "Segmento B: Talento Enfocado",
    "2": "Segmento C: Talento Senior"
}
df_id['Cluster_ID'] = cluster_labels.astype(str)
df_id['Segmento'] = df_id['Cluster_ID'].map(mapeo_nombres)

# PCA para las coordenadas del gráfico
pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)
df_id['PCA1'] = pca_data[:, 0]
df_id['PCA2'] = pca_data[:, 1]

# ==========================================
# 2. CÁLCULO DE MÉTRICAS (Basado en los DFs ya listos)
# ==========================================
total_a = len(df_id[df_id['Cluster_ID'] == "0"])
total_b = len(df_id[df_id['Cluster_ID'] == "1"])
total_c = len(df_id[df_id['Cluster_ID'] == "2"])
promedio_hijos = df_id['Son'].mean()

# ==========================================
# 3. RENDERIZADO VISUAL (STREAMLIT)
# ==========================================

st.subheader("Visualización de Segmentos (PCA) y Plan de Acción")

# KPIs de Segmentación
col1, col2, col3 = st.columns(3)
col1.metric("Motor Familiar (A)", f"{total_a} personas", delta="42%")
col2.metric("Talento Enfocado (B)", f"{total_b} personas", delta="39%")
col3.metric("Talento Senior (C)", f"{total_c} personas", delta="19%")


# Frase dinámica y Selector de Color
orden_segmentos = [
    "Segmento A: Motor Familiar",
    "Segmento B: Talento Enfocado",
    "Segmento C: Talento Senior"
]
opciones = ["Todos los empleados"] + orden_segmentos

# El gráfico (usando el DataFrame ya procesado arriba)

# 1. Usamos Jitter para separar a los "gemelos" (IDs con mismos datos)
# Esto crea la columna jitter si no la tenías
df_id['PCA1_jitter'] = df_id['PCA1'] + np.random.uniform(-0.1, 0.1, len(df_id))
df_id['PCA2_jitter'] = df_id['PCA2'] + np.random.uniform(-0.1, 0.1, len(df_id))
fig_scatter = px.scatter(
    df_id,
    x='PCA1_jitter',
    y='PCA2_jitter',
    color='Segmento',
    size=[10] * len(df_id),
    hover_name='ID',
    hover_data={
        'PCA1_jitter': False,
        'PCA2_jitter': False,
        'PCA1': False,
        'PCA2': False,
        'Age': True,
        'Son': True
    },
    color_discrete_sequence=["#FF5AE1", '#00D1C1', "#2B8ACF"],
    template='plotly_white',
    height=600
)

fig_scatter.update_traces(
    marker=dict(
        line=dict(width=0)  # Elimina el borde
    )
)

# --- AQUÍ AUMENTAMOS EL TAMAÑO DE LA LETRA ---
fig_scatter.update_layout(
    xaxis=dict(
        title=dict(text='PCA 1 (Variación Principal)',
                   font=dict(size=20)),  # Título del eje X
        tickfont=dict(size=14)  # Números del eje X
    ),
    yaxis=dict(
        title=dict(text='PCA 2 (Variación Secundaria)',
                   font=dict(size=20)),  # Título del eje Y
        tickfont=dict(size=14)  # Números del eje Y
    ),
    legend=dict(
        font=dict(size=16),  # Tamaño de letra de la leyenda
        title=dict(font=dict(size=18))  # Título de la leyenda
    )
)


st.plotly_chart(fig_scatter, width="stretch")
st.markdown("""
<p style='font-style: italic; color: #808495; font-size: 1.1em;'>
Cada punto representa a un empleado en nuestro universo organizacional, agrupado por patrones que nos ayudan a cuidar mejor de nuestro talento.
</p>
""", unsafe_allow_html=True)
# --- GUÍA DE LECTURA DEL MAPA ---
with st.expander("¿Cómo leer este mapa de segmentación?", expanded=False):
    st.markdown("""
    Este gráfico utiliza **Inteligencia Artificial (K-Means + PCA)** para agrupar a los empleados según sus perfiles sociodemográficos únicos.

    ###  Variables analizadas:
    Para crear estos grupos, el modelo ha procesado 6 dimensiones clave de cada empleado:
    1. **Edad** (`Age`): Media de edad del trabajador.
    2. **Carga Familiar** (`Son`): Número de hijos.
    3. **Salud Física** (`Body_mass_index`): Índice de masa corporal promedio.
    4. **Educación** (`Education`): Nivel de estudios alcanzado.
    5. **Hábitos Sociales** (`Social_drinker` y `Social_smoker`): Si el empleado fuma o consume alcohol habitualmente.

    ###  Guía de interpretación:
    * **Ejes (PCA1 y PCA2):** Son "super-variables" que combinan las 6 anteriores. Si dos puntos están **cerca**, significa que esos empleados tienen vidas y hábitos muy parecidos.
    * **Colores (Segmentos):** Representan los 3 perfiles estratégicos identificados (Motor Familiar, Talento Enfocado y Senior).
    * **Interactividad:** Puedes hacer zoom, aislar segmentos haciendo clic en la leyenda o pasar el ratón para ver el **ID del empleado**.
    """)


with st.expander("Ver detalle de decisiones estratégicas por Segmento"):
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("### Segmento A: El Motor Familiar")
        st.info("**42% de la Plantilla**")
        st.write("""
        * **Perfil:** Media de 37 años, alta carga familiar (1.4 hijos) y estilo de vida sedentario por falta de tiempo.
        * **Riesgos:** Burnout por fricción vida-trabajo, estrés logístico y fatiga física acumulada.
        * **Palanca:** Conciliación Efectiva.
        * **Acciones:** Smart Working y flexibilidad horaria escolar.
            * Beneficios como cheques guardería.
            * Rutas recurrentes (menor carga cognitiva) y formación en ergonomía.
        """)

    with col_b:
        st.markdown("### Segmento B: Talento Enfocado")
        st.info("**39% de la Plantilla**")
        st.write("""
        * **Perfil:** Saludable (bajo IMC), sin cargas familiares, alta energía y disponibilidad.
        * **Riesgos:** Fuga de talento por falta de retos y estancamiento en tareas repetitivas.
        * **Palanca:** Desarrollo y Upskilling.
        * **Acciones:** Planes de carrera vertical/horizontal y certificación "Senior".
            * Ranking mensual de eficiencia con incentivos por volumen.
            * Promoción a coordinadores de zona o proyectos piloto.
        """)

    with col_c:
        st.markdown("### Segmento C: Talento Senior")
        st.info("**19% de la Plantilla**")
        st.write("""
        * **Perfil:** Mayor edad, fumadores (gestión de estrés de riesgo) y amplia experiencia.
        * **Riesgos:** Fatiga física, lesiones y accidentes por desgaste acumulado.
        * **Palanca:** Bienestar Integral y Reconocimiento.
        * **Acciones:** * Programa de fisioterapia preventiva y deshabituación tabáquica.
            * Transición a roles de **Mentoring**.
            * Adaptación de rutas (menos entregas) y vehículos automáticos.
        """)
# Cálculos de métricas

# --- SECCIÓN 3: PLAN DE ACCIÓN ESTRATÉGICO Y LISTADO ---


# Creamos un único expander que contenga tanto la estrategia como los datos

    # 1. Columnas de Estrategia


with st.expander("Utiliza esta tabla para buscar IDs específicos y su asignación de segmento."):

    df_tabla = df_id[['ID', 'Segmento', 'Age', 'Son', 'Body_mass_index']]
    st.dataframe(df_tabla, width="stretch", hide_index=True)

st.divider()
st.header("Análisis de Indicadores de Absentismo y Eficiencia")
# Diccionario para convertir números en nombres de meses
meses_map = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
total_empleados = RRHH_full['ID'].nunique()
ausentes = RRHH_full[RRHH_full['Absenteeism_hours'] > 0]['ID'].nunique()
pct_ausentes = (ausentes / total_empleados) * 100
mes_pico_num = RRHH_full.groupby('Month_absence')[
    'Absenteeism_hours'].sum().idxmax()
motivo_modal_id = RRHH_full['Reason_Description'].mode()[0]
eficiencia_relativa = RRHH_full['Hit_target'].mean(
) / RRHH_full['Work_load_Average_day'].mean()

# --- CÁLCULOS ACTUALIZADOS ---

# 1. Obtienes el número (ej: 3)
mes_pico_id = RRHH_full.groupby('Month_absence')[
    'Absenteeism_hours'].sum().idxmax()

# 2. Lo traduces usando el diccionario (ej: "Marzo")
mes_pico_nombre = meses_map.get(mes_pico_id, "Desconocido")
# --- TÍTULO DE LA SECCIÓN DE MÉTRICAS ---


# Render de métricas con los nombres exactos de tus fórmulas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Porcentaje de empleados ausentes",
        value=f"{pct_ausentes:.1f}%",
        help="Cálculo: (Nº empleados con ausencia / Total empleados) x 100"
    )

with col2:
    st.metric(
        label="Mes pico de carga por ausencias",
        value=mes_pico_nombre,
        help="Mes con la mayor suma de horas de absentismo"
    )

with col3:
    st.metric(
        label="Motivo modal de absentismo laboral",
        value=str(motivo_modal_id)[:15],
        help=f"Motivo más frecuente: {motivo_modal_id}"
    )

with col4:
    st.metric(
        label="Índice de eficiencia relativa por carga laboral",
        value=f"{eficiencia_relativa:.2f}",
        help="Cálculo: Σ(Hit target) / Σ(Work load Average/day)"
    )

st.divider()


st.write(
    f"Cantidad de ausencias registradas (filas totales): {len(RRHH_full)}")
st.write(f"Cantidad de empleados únicos (bolitas en el gráfico): {len(df_id)}")


# Verificación de datos antes de la IA
st.write(f"Empleados únicos detectados: {df_id['ID'].nunique()}")
st.write(f"¿Hay valores vacíos?: {df_id.isnull().sum().sum()} datos faltantes")

# Esto te dirá cuántos empleados sobreviven al procesamiento
X_check = pd.get_dummies(
    df_id, columns=['Education', 'Social_drinker', 'Social_smoker'])
st.write(f"Empleados que entrarían al gráfico: {len(X_check.dropna())}")


st.divider()
