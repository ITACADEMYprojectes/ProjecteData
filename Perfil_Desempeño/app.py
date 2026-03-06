from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import scipy.stats as stats
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import silhouette_score
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


st.set_page_config(page_title="RRHH Analytics Dashboard", layout="wide")

# --- CONFIGURACIÓN DE ESTILO GLOBAL (CSS) ---
st.markdown("""
    <style>
    /* 1. Elimina la barra de decoración de colores arriba del todo */
    [data-testid="stDecoration"] {
        display: none;
    }

    /* 2. Hace el Header totalmente transparente */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        background: transparent !important;
    }

    /* 3. Asegura que el contenedor de la página no tenga padding superior extra */
    .block-container {
        padding-top: 2rem !important; /* Puedes bajar este número a 1rem si quieres menos espacio */
    }

    /* 4. Por si la barra blanca es el Toolbar de Streamlit */
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Importamos una fuente moderna de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    /* Aplicamos la fuente a toda la app */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Inter', sans-serif !important;
    }

    /* Opcional: Ajustar el tamaño de los títulos para que se vean más "Tech" */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -1px;
    }
    
    /* Estilo para las métricas (KPIs) */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 1. Importar Fuente */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    /* 2. Color de fondo para toda la App (#eeeeeeff) */
    .stApp {
        background-color: #EEEEEE; /* El 'ff' final es opacidad al 100% */
    }

    /* 3. Aplicar Fuente Global */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Inter', sans-serif !important;
        color: #31333F; /* Un gris oscuro para que resalte sobre el fondo claro */
    }

    /* 4. Opcional: Hacer que las tarjetas (expander) sean blancas puras 
       para que resalten sobre el fondo gris claro */
    .streamlit-expanderHeader {
        background-color: white !important;
        border-radius: 5px;
    }
    
    [data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

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
# El logo ocupa 1 parte y el título 4
st.title("Rapid Express: People Analytics Dashboard")
st.markdown(
    "### Porque detrás de cada ruta, hay una historia: cuidamos a las personas que mueven nuestro motor.")


# 1. LÓGICA DE PROCESAMIENTO (DATAFRAMES E IA)
# ==========================================
# Agrupación inicial
# Para variables continuas (Age, Body_mass_index, Son) tomaste la media.
# Para variables categóricas (Education) tomaste la primera observación.
# Para variables binarias (Social_drinker, Social_smoker) tomaste el valor máximo (es decir, si alguna vez fueron “sí”, se marca como sí).

df_id = RRHH_full.groupby('ID').agg({
    'Age': 'mean',
    'Body_mass_index': 'mean',
    'Son': 'mean',
    'Education': 'first',
    'Social_drinker': 'max',
    'Social_smoker': 'max'
}).reset_index()

# Pre-procesamiento y Clustering # variables numéricas + dummies para categóricas
# Aplicaste KMeans con 3 clusters, generando un label para cada empleado.
# Transformaste variables categóricas en dummies (0/1) para que KMeans pueda procesarlas.

df_numeric = pd.get_dummies(
    df_id, columns=['Education', 'Social_drinker', 'Social_smoker'])
X = df_numeric.drop(columns=['ID'])

# Variables numéricas con StandardScaler para que todas tengan la misma importancia.
X_scaled = StandardScaler().fit_transform(X)

# Aplicaste KMeans con 3 clusters, generando un label para cada empleado.
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
# Redujiste la dimensión de los datos a 2 componentes principales para poder graficarlos.
# Esto es útil para mostrar un scatter plot de los clusters y ver cómo se separan visualmente.
pca = PCA(n_components=2)
pca_data = pca.fit_transform(X_scaled)
df_id['PCA1'] = pca_data[:, 0]
df_id['PCA2'] = pca_data[:, 1]


# ==========================================
# 2. CÁLCULO DE MÉTRICAS (Basado en los DFs ya listos)
# ==========================================
# Calculaste tamaño de cada cluster (cuántos empleados tiene cada segmento).
# Calculaste promedio de hijos para ver características demográficas generales.

total_a = len(df_id[df_id['Cluster_ID'] == "0"])
total_b = len(df_id[df_id['Cluster_ID'] == "1"])
total_c = len(df_id[df_id['Cluster_ID'] == "2"])
promedio_hijos = df_id['Son'].mean()


#### CLUSTERS TESTS ####
# ==========================================
# 3. RENDERIZADO VISUAL (STREAMLIT)
# ==========================================
st.divider()

# --- Fila 1: Métricas de Calidad de la IA ---
# --- Fila 2: KPIs de Segmentación (Volumen) ---
st.write("### Distribución de la Fuerza Laboral")
col1, col2, col3 = st.columns(3)

col1.metric("Motor Familiar (A)", f"{total_a} personas", delta="42%")
col2.metric("Talento Enfocado (B)", f"{total_b} personas", delta="39%")
col3.metric("Talento Senior (C)", f"{total_c} personas", delta="19%")
# ==========================================

st.write("### Métricas de Rendimiento del Modelo")
m_col1, m_col2, m_col3 = st.columns(3)

# Calculamos los scores (asegúrate de que estas variables estén definidas arriba)
score = silhouette_score(X_scaled, cluster_labels)
db_score = davies_bouldin_score(X_scaled, cluster_labels)

m_col1.metric("Silhouette Score", f"{score:.2f}",
              help="Cercano a 1 es ideal. Mide qué tan bien separados están los grupos.")
m_col2.metric("Inertia (WCSS)", f"{kmeans.inertia_:.1f}",
              help="Mide la cohesión interna de los clusters. Menor es más compacto.")
m_col3.metric("Davies-Bouldin Score", f"{db_score:.2f}",
              help="Cercano a 0 es ideal. Mide la separación entre clusters.")


st.subheader("Visualización de Segmentos (PCA) y Plan de Acción")


# Frase dinámica y Selector de Color
orden_segmentos = [
    "Segmento A: Motor Familiar",
    "Segmento B: Talento Enfocado",
    "Segmento C: Talento Senior"
]
opciones = ["Todos los empleados"] + orden_segmentos

# El gráfico (usando el DataFrame ya procesado arriba)
# 1. Usamos Jitter para separar a los "gemelos"
df_id['PCA1'] = df_id['PCA1'] + np.random.uniform(-0.1, 0.1, len(df_id))
df_id['PCA2'] = df_id['PCA2'] + np.random.uniform(-0.1, 0.1, len(df_id))

# 1. Definimos los símbolos que queremos para cada segmento
# 1. Mapa de símbolos
simbolos_map = {
    "Segmento A: Motor Familiar": "circle",
    "Segmento B: Talento Enfocado": "diamond",
    "Segmento C: Talento Senior": "square"
}
fig_scatter = px.scatter(
    df_id,
    x='PCA1',
    y='PCA2',
    color='Segmento',
    symbol='Segmento',
    symbol_map=simbolos_map,
    size=[12] * len(df_id),
    text='ID',
    hover_name='ID',
    hover_data={
        'PCA1': False,
        'PCA2': False,
        'Age': True,
        'Son': True,
        'Social_smoker': True,
        'Social_drinker': True,
        'Body_mass_index': ':.1f'
    },
    color_discrete_sequence=["#51A242", "#65E74B", "#093C2B"],
    template='plotly_white',
    height=600
)

# --- EL TRUCO PARA EL FONDO INVISIBLE (#EEEEEE) ---
fig_scatter.update_layout(
    plot_bgcolor='#EEEEEE',  # Color del área donde están los puntos
    paper_bgcolor='#EEEEEE',  # Color del área exterior (bordes/leyenda)
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='grey',
        showticklabels=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='grey',
        showticklabels=False
    )
)

# Mantener los IDs visibles sobre el color gris
fig_scatter.update_traces(
    mode='markers+text',
    textposition='top center',
    marker=dict(line=dict(width=1, color='white'))
)

st.plotly_chart(fig_scatter, use_container_width=True)

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
        st.info("**42%**")
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
        st.info("**39%**")
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
        st.info("**19%**")
        st.write("""
        * **Perfil:** Mayor edad, fumadores (gestión de estrés de riesgo) y amplia experiencia.
        * **Riesgos:** Fatiga física, lesiones y accidentes por desgaste acumulado.
        * **Palanca:** Bienestar Integral y Reconocimiento.
        * **Acciones:** * Programa de fisioterapia preventiva y deshabituación tabáquica.
            * Transición a roles de **Mentoring**.
            * Adaptación de rutas (menos entregas) y vehículos automáticos.
        """)

# --- EXPANDER DE DATOS Y MÉTRICAS TÉCNICAS ---
with st.expander("Ver datos del trabajador", expanded=False):

    # PARTE 2: La Tabla Completa
    st.write("### Nuestros talentos")
    st.write(
        "Esta tabla muestra la información exacta que procesó el algoritmo para cada talento:")

    # Seleccionamos las 6 variables clave + el ID y el Segmento asignado
    df_completo_ia = df_id[[
        'ID', 'Segmento', 'Age', 'Body_mass_index', 'Son',
        'Education', 'Social_drinker', 'Social_smoker'
    ]]

    # Mostramos la tabla interactiva
    st.dataframe(
        df_completo_ia,
        width='stretch',
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID Empleado", format="%d"),
            "Social_drinker": st.column_config.CheckboxColumn("Bebedor Social"),
            "Social_smoker": st.column_config.CheckboxColumn("Fumador Social"),
            "Body_mass_index": st.column_config.NumberColumn("IMC", format="%.1f")
        }
    )
    # Opción de descarga para el usuario
    csv = df_completo_ia.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar tabla completa de segmentación (CSV)",
        data=csv,
        file_name='segmentacion_empleados_rapidexpress.csv',
        mime='text/csv',
    )

# --- SECCIÓN 3: PLAN DE ACCIÓN ESTRATÉGICO Y LISTADO ---


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
col1, col2, col3, col4, col5 = st.columns(5)

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
    # Definimos el umbral de alerta
    umbral_alerta = 0.50
    delta_eficiencia = eficiencia_relativa - umbral_alerta

    st.metric(
        label="Eficiencia en Días de Incidencias",
        value=f"{eficiencia_relativa:.2f}",
        delta=f"{delta_eficiencia:.2f} (Bajo el objetivo)",
        delta_color="inverse",  # Esto hará que si es negativo salga en rojo
        help="Cálculo: Σ(Hit target) / Σ(Work load). Un valor ideal debería estar por encima de 0.50."
    )

# En lugar de sumar todo, saca el promedio por registro
eficiencia_promedio_por_caso = RRHH_full['Hit_target'].mean() / 100

# O mejor aún, compáralo contra el 100% que sería el objetivo ideal
with col5:
    st.metric(
        label="Nivel de Cumplimiento en Días Críticos",
        value=f"{RRHH_full['Hit_target'].mean():.1f}%",
        delta=f"{RRHH_full['Hit_target'].mean() - 100:.1f}% vs Ideal",
        help="Promedio de cumplimiento de objetivos durante los días que se registraron ausencias."
    )

st.divider()

st.header("Ciclo Estacional de Absentismo")

st.write("### Impacto en la Operación Global")

# Cálculos basados en tus datos
total_horas_absentismo = RRHH_full['Absenteeism_hours'].sum()
# Asumiendo 75168 como constante de capacidad total o calculada
total_horas_laborables = 75168
tasa_ausentismo = (total_horas_absentismo / total_horas_laborables) * 100

col_inv1, col_inv2, col_inv3 = st.columns(3)

with col_inv1:
    st.metric(
        label="Total Horas de Absentismo",
        value=f"{total_horas_absentismo:,}".replace(",", "."),
        help="Suma total de horas no trabajadas registradas en el periodo de 3 años."
    )

with col_inv2:
    st.metric(
        label="Capacidad Laboral Total",
        value=f"{total_horas_laborables:,}".replace(",", "."),
        help="Total de horas disponibles contratadas por la organización."
    )

with col_inv3:
    # Usamos un color de delta inverso (rojo si sube) para la tasa de ausencia
    st.metric(
        label="Tasa de Ausentismo Global",
        value=f"{tasa_ausentismo:.2f} %",  # Ejemplo de comparativa
        help="Porcentaje de tiempo perdido sobre el total de la capacidad instalada."
    )


# Unimos los datos para tener el nombre del segmento en cada fila de ausencia
df_estacional = RRHH_full.merge(df_id[['ID', 'Segmento']], on='ID')

# Agrupamos por mes para aplanar los años en un solo ciclo de 12 meses
df_mensual = df_estacional.groupby(['Month_absence', 'Segmento'])[
    'Absenteeism_hours'].sum().reset_index()
fig_estacional = px.line(
    df_mensual,
    x='Month_absence',
    y='Absenteeism_hours',
    color='Segmento',
    title="Patrón de Ausencias en un Ciclo Anual",
    markers=True,
    labels={'Month_absence': 'Mes',
            'Absenteeism_hours': 'Total Horas de Ausencia'},
    color_discrete_sequence=["#093C2B", '#65E74B', "#51A242"]
)

# --- ESTILO SMART FLOW v6.0.4 ---
fig_estacional.update_layout(
    plot_bgcolor='#EEEEEE',  # Fondo del área de trazado
    paper_bgcolor='#EEEEEE',  # Fondo exterior del gráfico
    xaxis=dict(
        dtick=1,             # Fuerza a mostrar todos los meses (1 al 12)
        showgrid=False,      # Quita líneas verticales
        showline=True,       # Deja solo la línea base
        linecolor='grey'
    ),
    yaxis=dict(
        showgrid=False,      # Quita líneas horizontales
        showline=True,       # Deja solo la línea base
        linecolor='grey'
    ),
    font=dict(family="Inter"),  # Mantiene la coherencia tipográfica
    legend=dict(
        bgcolor='rgba(0,0,0,0)'  # Leyenda con fondo transparente
    )
)

# Hacer las líneas un poco más gruesas y los puntos más definidos
fig_estacional.update_traces(
    line=dict(width=3),
    marker=dict(size=8, line=dict(width=1, color='white'))
)

st.plotly_chart(fig_estacional, use_container_width=True)
# ==========================================
# 4. KPIs DE IMPACTO OPERATIVO
# ==========================================


# 1. Preparación de datos para predicción
# Usamos variables que influyen en el tiempo de ausencia
features_pred = [
    'Transportation_expense', 'Distance_Residence_Work', 'Service_time',
    'Age', 'Work_load_Average_day', 'Hit_target', 'Son', 'Pet', 'Body_mass_index',
    'Month_absence', 'Day_week', 'Seasons'
]

# Convertimos categóricas (Day_week, Seasons) si no son numéricas
X_p = pd.get_dummies(RRHH_full[features_pred], drop_first=True)
y_p = RRHH_full['Absenteeism_hours']

# 2. Entrenamiento
X_train, X_test, y_train, y_test = train_test_split(
    X_p, y_p, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=250, random_state=42)
rf_model.fit(X_train, y_train)


# Extraer importancia de las variables
importances = rf_model.feature_importances_
feature_names = X_p.columns
feature_importance_df = pd.DataFrame(
    {'Variable': feature_names, 'Importancia': importances}).sort_values(by='Importancia', ascending=True)

fig_rf = px.bar(
    feature_importance_df,
    x='Importancia',
    y='Variable',
    orientation='h',
    title="¿Qué factores predicen el absentismo? (Random Forest Importance)",
    color_discrete_sequence=["#A0F08B"]
)

# --- AÑADIR BORDE A LAS BARRAS ---
fig_rf.update_traces(
    marker=dict(
        line=dict(
            # Grosor del borde (puedes subirlo a 1.5 o 2 si quieres que se note más)
            width=0,
            color="#1E6C09"     # Color del borde
        )
    )
)
# ---------------------------------

st.divider()

# Footer estilo Software Developer


st.write("###  Factores Clave del Absentismo (IA)")

# 1. Aseguramos que los nombres de las columnas estén limpios
RRHH_full.columns = RRHH_full.columns.str.strip()

# 2. Selección de variables para el modelo
features_pred = [
    'Transportation_expense', 'Distance_Residence_Work', 'Service_time',
    'Age', 'Work_load_Average_day', 'Hit_target', 'Son', 'Pet', 'Body_mass_index',
    'Month_absence', 'Day_week', 'Seasons'
]

# 3. Preparación y entrenamiento rápido
X_p = pd.get_dummies(RRHH_full[features_pred], drop_first=True)
y_p = RRHH_full['Absenteeism_hours']

X_train, X_test, y_train, y_test = train_test_split(
    X_p, y_p, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=250, random_state=42)
rf_model.fit(X_train, y_train)

# 4. Crear DataFrame de importancia
importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Variable': X_p.columns,
    'Importancia': importances
}).sort_values(by='Importancia', ascending=True)


# 5. RENDERIZADO DEL GRÁFICO
fig_rf = px.bar(
    feature_importance_df,
    x='Importancia',
    y='Variable',
    orientation='h',
    title="¿Qué factores predicen el absentismo?",
    color_discrete_sequence=["#79B26B"],  # Tu color verde
    template='plotly_white'
)

# Añadir bordes a las barras (como ya tenías)
fig_rf.update_traces(
    marker=dict(line=dict(width=1, color='black'))
)

# --- NUEVO: DISMINUIR GROSOR DE LAS BARRAS ---
fig_rf.update_layout(
    bargap=0.5,  # <--- AJUSTA ESTE VALOR (entre 0 y 1).
    # 0.5 significa que el espacio entre barras es el 50% de la barra.
                 # Prueba con 0.6 o 0.7 si las quieres aún más finas.

    # Mantenemos tu estilo limpio sin grids
    xaxis=dict(showgrid=False, showline=False, zeroline=False),
    yaxis=dict(showgrid=False, showline=False, zeroline=False),
    plot_bgcolor='white'
)


# Estilo ultra limpio: Sin grids y SIN líneas de ejes
# 5. RENDERIZADO DEL GRÁFICO (Feature Importance)
fig_rf = px.bar(
    feature_importance_df,
    x='Importancia',
    y='Variable',
    orientation='h',
    title="¿Qué factores predicen el absentismo?",
    color_discrete_sequence=["#79B26B"],
    template='plotly_white'
)

# Añadir bordes a las barras y ajustar grosor (bargap)
fig_rf.update_traces(
    marker=dict(line=dict(width=1, color='black'))
)

# --- ESTILO SMART FLOW v6.0.4 (FONDO GRIS #EEEEEE) ---
fig_rf.update_layout(
    bargap=0.5,              # Barras más finas y elegantes
    plot_bgcolor='#EEEEEE',  # Fondo del área de las barras
    paper_bgcolor='#EEEEEE',  # Fondo del contenedor exterior
    xaxis=dict(
        showgrid=False,
        showline=False,      # Sin línea de eje X
        zeroline=False,
        showticklabels=False  # Quitamos los números de abajo para máxima limpieza
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,      # Sin línea de eje Y
        zeroline=False,
        # Dejamos las etiquetas de las variables (Age, Son, etc.)
        tickfont=dict(family="Inter", size=12)
    ),
    margin=dict(l=20, r=20, t=50, b=20),  # Ajuste de márgenes
    font=dict(family="Inter")
)

st.plotly_chart(fig_rf, width='stretch')
st.divider()

st.markdown(
    """
    <div style="text-align: right; color: #808080; font-size: 12px; font-family: 'Courier New', monospace;">
        <strong>SYSTEM STATUS:</strong> Operational<br>
        <strong>MODULE:</strong> People Analytics Core<br>
        <strong>VERSION:</strong> 6.0.4<br>
        <strong>BUILD:</strong> 2026_MAR_05<br>
        <span style="color: #A1EF8B;">●</span> Connected to RapidExpress_DB
    </div>
    """,
    unsafe_allow_html=True
)
