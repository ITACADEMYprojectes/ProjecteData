# Importante para predecir 2 variables
from scipy.stats import binomtest
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from scipy import stats
from sklearn.metrics import confusion_matrix, classification_report
import plotly.graph_objects as objects
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
import plotly.figure_factory as ff
from sklearn.metrics import balanced_accuracy_score, recall_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, recall_score
from scipy.stats import pearsonr, spearmanr, ttest_ind, pointbiserialr, f_oneway, chi2_contingency
from scipy.stats import ttest_ind, pointbiserialr, spearmanr, f_oneway, chi2_contingency
from scipy.stats import ttest_ind, pointbiserialr, pearsonr, f_oneway, chi2_contingency
from scipy.stats import ttest_ind, pointbiserialr, chi2_contingency
from scipy.stats import f_oneway
from sklearn.multioutput import MultiOutputRegressor
import plotly.graph_objects as go  # <--- Asegúrate de tener esta línea
import altair as alt
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
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split  # Por si lo necesitas luego
import pandas as pd
from scipy.stats import ttest_ind, pointbiserialr
import os
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from scipy.stats import ttest_ind, pointbiserialr


st.set_page_config(page_title="RRHH Analytics Dashboard", layout="wide")

# # --- CONFIGURACIÓN DE ESTILO GLOBAL (CSS) ÚNICO Y CORREGIDO ---
st.markdown("""
    <style>
    /* 1. Importación de Fuente */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

    /* 2. Configuración de Fondo y Limpieza de UI */
    .stApp {
        background-color: #EEEEEE;
    }
    [data-testid="stDecoration"] { display: none; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 2rem !important; }




    /* 5. Estilo de Métricas (KPIs) */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #353639 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #353639 !important;
        font-size: 1rem !important;
    }


    /* 7. Arreglo para el Toolbar (opcional) */
    [data-testid="stToolbar"] {
        right: 2rem;
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
# --- CÁLCULO DE EMPLEADOS TOTALES ---
# Contamos cuántos IDs distintos existen en la base de datos
total_empleados_unicos = RRHH_full['ID'].nunique()

# --- SECCIÓN 1: TÍTULO Y MÉTRICAS (KPIs) ---
st.title("Rapid Express: People Analytics Dashboard")

# Usamos un f-string para meter el número dentro del texto
st.markdown(
    f"### Porque detrás de cada ruta, hay una historia: cuidamos de las **{total_empleados_unicos}** personas que mueven nuestro motor."
)

# ==========================================
# 1. PREPROCESAMIENTO (REFORZADO)
# ==========================================

# 1. Limpieza previa de la columna en el DataFrame original
# Convertimos a minúsculas y quitamos espacios al principio/final

RRHH_full['Education'] = RRHH_full['Education'].astype(
    str).str.lower().str.strip()

# 2. Definimos la jerarquía oficial (asegurando minúsculas)
edu_mapping = {
    "high school": 1,
    "graduate": 2,
    "postgraduate": 3,
    "master and doctor": 4
}

# 3. Aplicamos el mapeo
RRHH_full['Education'] = RRHH_full['Education'].map(edu_mapping)

# Convertimos TRUE/FALSE a 1/0 para que el modelo no se confunda
RRHH_full['Social_drinker'] = RRHH_full['Social_drinker'].astype(int)
RRHH_full['Social_smoker'] = RRHH_full['Social_smoker'].astype(int)

# 4. Verificación y limpieza de nulos
# Si algo no coincidió, le ponemos 1 (High School) por defecto
RRHH_full['Education'] = RRHH_full['Education'].fillna(1).astype(int)

# --- AGRUPACIÓN AMPLIADA ---
# --- AGRUPACIÓN COMPLETA Y SEGURA ---
df_id = RRHH_full.groupby('ID').agg({
    # Variables de Desempeño y Control
    'Hit_target': 'mean',
    'Work_load_Average_day': 'mean',
    'Disciplinary_failure': 'max',      # Si tuvo 1 fallo, queda marcado
    'Absenteeism_hours': 'sum',         # Total de horas perdidas

    # Variables de Perfil y Estabilidad
    'Service_time': 'max',
    'Age': 'mean',
    'Education': 'max',
    'Son': 'max',
    'Pet': 'max',

    # Variables de Salud y Hábitos
    'Body_mass_index': 'mean',
    'Social_drinker': 'max',
    'Social_smoker': 'max',

    # Variables de Logística (Muy importantes para Ausentismo)
    'Transportation_expense': 'mean',
    'Distance_Residence_Work': 'mean'
}).reset_index()

# Ahora creamos los KPIs que ya no fallarán:
df_id['Resiliencia_Score'] = df_id['Hit_target'] / \
    ((df_id['Work_load_Average_day'] / 100) + 0.1)

df_id['Indice_Lealtad'] = df_id['Service_time'] / \
    (df_id['Absenteeism_hours'] + 1)

# ==========================================
# 2. SELECCIÓN Y ESCALADO (X)
# ==========================================

# Seleccionamos las columnas que queremos que la IA analice
features = ['Age', 'Body_mass_index', 'Son',
            'Education', 'Social_drinker', 'Social_smoker']
X = df_id[features]

# Aplicamos el Escalado (Z-Score)
# Esto hace que la "Edad" y los "Hijos" tengan la misma importancia
scaler = StandardScaler()
X_scaled_array = scaler.fit_transform(X)

# Convertimos el resultado de nuevo a un DataFrame limpio
X_scaled = pd.DataFrame(X_scaled_array, columns=X.columns)


# ==========================================
# 3. KMEANS (ESTABLE)
# ==========================================

kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
cluster_labels = kmeans.fit_predict(X_scaled)

# Guardamos el grupo (0, 1 o 2) en nuestra tabla
df_id['Cluster_ID'] = cluster_labels

# ==========================================
# 4. MAPEO DINÁMICO (NOMBRES DE SEGMENTOS)
# ==========================================

# Ordenamos los grupos por Edad Media para que los nombres siempre tengan sentido
# (El grupo de más edad siempre será "Senior")
centros_edad = df_id.groupby('Cluster_ID')['Age'].mean().sort_values().index

mapeo_nombres = {
    centros_edad[0]: "Talento Enfocado",  # Los más jóvenes
    centros_edad[1]: "Motor Familiar",   # Edad intermedia
    centros_edad[2]: "Talento Senior"    # Los mayores
}

df_id['Segmento'] = df_id['Cluster_ID'].map(mapeo_nombres)

# ==========================================
# 4. MAPEO DE SEGMENTOS (LÓGICO Y DINÁMICO)
# ==========================================
# CRÍTICO: Ordenamos los clusters por EDAD MEDIA para que el nombre siempre coincida
# con la realidad demográfica del grupo.

centros_edad = df_id.groupby('Cluster_ID')['Age'].mean().sort_values().index

# age_order[0] = El grupo más joven -> Talento Enfocado
# age_order[1] = El grupo intermedio -> Motor Familiar
# age_order[2] = El grupo mayor -> Talento Senior

mapeo_dinamico = {
    centros_edad[0]: "Talento Enfocado",
    centros_edad[1]: "Motor Familiar",
    centros_edad[2]: "Talento Senior"
}

df_id['Segmento'] = df_id['Cluster_ID'].map(mapeo_dinamico)

# ==========================================
# 5. PCA (VISUALIZACIÓN)
# ==========================================
pca = PCA(n_components=2, random_state=42)
pca_data = pca.fit_transform(X_scaled)

df_id['PCA1'] = pca_data[:, 0]
df_id['PCA2'] = pca_data[:, 1]

# Varianza explicada para tu reporte técnico
total_var = pca.explained_variance_ratio_.sum() * 100

# ==========================================
# 6. MÉTRICAS FINALES
# ==========================================

counts = df_id['Segmento'].value_counts()

# Obtenemos los totales de forma segura (si no existe el segmento, pone 0)
total_a = counts.get("Motor Familiar", 0)
total_b = counts.get("Talento Enfocado", 0)
total_c = counts.get("Talento Senior", 0)

# ==========================================
# 3. RENDERIZADO VISUAL (STREAMLIT)
# ==========================================
st.divider()

# --- Fila 1: Métricas de Calidad de la IA ---
# --- Fila 2: KPIs de Segmentación (Volumen) ---
st.write("### Distribución de la Fuerza Laboral")
col1, col2, col3 = st.columns(3)

col1.metric("Motor Familiar", f"{total_a} talentos", delta="42%")
col2.metric("Talento Enfocado", f"{total_b} talentos", delta="39%")
col3.metric("Talento Senior", f"{total_c} talentos", delta="19%")
# ==========================================
st.divider()


st.write("### Métricas de Calidad del Clustering")

m_col1, m_col2 = st.columns(2)

score = silhouette_score(X_scaled, cluster_labels)
db_score = davies_bouldin_score(X_scaled, cluster_labels)


m_col1.metric(
    "Silhouette Score",
    f"{score:.2f}",
    help="Mide qué tan compactos y separados están los clusters. Más cerca de 1 es mejor."
)

m_col2.metric(
    "Davies-Bouldin Score",
    f"{db_score:.2f}",
    help="Evalúa la separación entre clusters. Más cerca de 0 es mejor."
)


orden_segmentos = [
    "Motor Familiar",
    "Talento Enfocado",
    "Talento Senior"
]

opciones = ["Todos los empleados"] + orden_segmentos

segmento_seleccionado = st.selectbox(
    "Filtrar por segmento",
    opciones
)

# ==========================================
# DATAFRAME PARA VISUALIZACIÓN
# ==========================================

df_plot = df_id.copy()

# Aplicar jitter solo para visualización
df_plot["PCA1_jitter"] = df_plot["PCA1"] + \
    np.random.uniform(-0.1, 0.1, len(df_plot))
df_plot["PCA2_jitter"] = df_plot["PCA2"] + \
    np.random.uniform(-0.1, 0.1, len(df_plot))

# Filtro de segmento
if segmento_seleccionado != "Todos los empleados":
    df_plot = df_plot[df_plot["Segmento"] == segmento_seleccionado]


# ==========================================
# MAPA DE SÍMBOLOS
# ==========================================

simbolos_map = {
    "Motor Familiar": "circle",
    "Talento Enfocado": "diamond",
    "Talento Senior": "square"
}

# ==========================================
# SCATTER PCA
# ==========================================

fig_scatter = px.scatter(
    df_plot,
    x="PCA1_jitter",
    y="PCA2_jitter",
    color="Segmento",
    symbol="Segmento",
    symbol_map=simbolos_map,
    size=[12] * len(df_plot),
    text="ID",
    title="Entendiendo a nuestra gente para cuidarlos mejor",
    hover_name="ID",
    hover_data={
        "PCA1_jitter": False,
        "PCA2_jitter": False,
        "Age": True,
        "Son": True,
        "Social_smoker": True,
        "Social_drinker": True,
        "Education": True,
        "Body_mass_index": ':.1f'
    },
    color_discrete_sequence=["#51A242", "#65E74B", "#093C2B"],
    template="plotly_white",
    height=600
)

# ==========================================
# ESTILO DEL GRÁFICO
# ==========================================

fig_scatter.update_layout(
    plot_bgcolor="#EEEEEE",
    paper_bgcolor="#EEEEEE",
    xaxis=dict(
        title=None,          # <--- Esto quita el nombre del eje X
        showgrid=False,
        zeroline=False,
        showline=False,      # He cambiado a False para un look más moderno
        showticklabels=False
    ),
    yaxis=dict(
        title=None,          # <--- Esto quita el nombre del eje Y
        showgrid=False,
        zeroline=False,
        showline=False,      # He cambiado a False para un look más moderno
        showticklabels=False
    ),
    # Ajusta los márgenes para que use todo el espacio
    margin=dict(l=20, r=20, t=40, b=20)
)


fig_scatter.update_traces(
    mode="markers",  # <--- Quitamos "text" de aquí
    marker=dict(
        size=22,
        line=dict(width=0.5, color="black"),
        opacity=0.5
    )
)


st.plotly_chart(fig_scatter, width='stretch')

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
        st.markdown("### El Motor Familiar")
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
        st.markdown("### Talento Enfocado")
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
        st.markdown("### Talento Senior")
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
with st.expander("Datos del trabajador", expanded=False):

    # Seleccionamos las 6 variables clave + el ID y el Segmento asignado
    # Dentro de tu st.expander...
    df_completo_ia = df_id[[
        'ID', 'Segmento', 'Age', 'Body_mass_index', 'Son',
        'Work_load_Average_day', 'Hit_target', 'Absenteeism_hours'
    ]]

# --- TABLA CON ENFOQUE EN TOTALES ---
    st.dataframe(
        df_completo_ia,
        width='stretch',
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID"),
            "Segmento": st.column_config.TextColumn("Segmento"),

            # El ausentismo como la métrica de impacto total
            "Absenteeism_time_in_hours": st.column_config.NumberColumn(
                "Total Horas Ausencia",
                help="Suma acumulada de todas las faltas",
                format="%d h 🕒",  # Le añadimos el icono para que sea más humano
            ),

            # Rendimiento
            "Hit_target": st.column_config.ProgressColumn(
                "Cumplimiento",
                format="%d%%",
                min_value=0,
                max_value=100
            ),

            # Carga de trabajo
            "Work_load_Average_day": st.column_config.NumberColumn(
                "Carga Media",
                format="%.0f"
            )
        }
    )

with st.expander("Ver infogramas de perfil"):
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.image("assets/perfil_a.jpg")
        st.caption("Motor Familiar")
    with col2:
        st.image("assets/perfil_b.jpg")
        st.caption("Talento Enfocado")
    with col3:
        st.image("assets/perfil_c.jpg")
        st.caption("Talento Senior")


# --- CÁLCULO DEL MÉTODO DEL CODO ---
# 1. Preparar datos (usando tu misma lógica de X_scaled)
# Asegúrate de que X_scaled esté definido antes de esto
distortions = []
K_range = range(1, 11)

for k in K_range:
    kmeanModel = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeanModel.fit(X_scaled)
    distortions.append(kmeanModel.inertia_)

# 2. Crear el Gráfico con Plotly
fig_elbow = px.line(
    x=list(K_range),
    y=distortions,
    markers=True,
    title="Método del Codo para Determinar el Número Óptimo de Segmentos",
    labels={'x': 'Número de Clusters (k)', 'y': 'Inercia (WCSS)'},
    color_discrete_sequence=["#51A242"]
)

# Estilo para que combine con tu dashboard negro/gris
fig_elbow.update_layout(
    plot_bgcolor='#EEEEEE',
    paper_bgcolor='#EEEEEE',
    font=dict(color="black"),
    xaxis=dict(showgrid=False, dtick=1),
    yaxis=dict(showgrid=False)
)


# 1. Coste Estimado por Transporte (Impacto Logístico)
# Suma total de gastos de transporte en registros de ausencia
gasto_total_transporte = RRHH_full[RRHH_full['Absenteeism_hours']
                                   > 0]['Transportation_expense'].sum()

# 2. Índice de Salud (BMI Promedio)
# Para entender el perfil físico de la plantilla
bmi_promedio = RRHH_full['Body_mass_index'].mean()

# 3. Tasa de Reincidencia (Disciplinary_failure)
# Porcentaje de casos que terminaron en fallo disciplinario
tasa_fallos = (RRHH_full['Disciplinary_failure'].sum() / len(RRHH_full)) * 100

# 4. Factor de Compromiso Familiar (Media de 'Son')
# Promedio de hijos por empleado ausente (para entender cargas familiares)
promedio_hijos = RRHH_full['Son'].mean()

st.divider()
# --- RENDERIZADO EN COLUMNAS ---
st.write("### Análisis de Perfil y Riesgo")

nk1, nk2, nk3, nk4 = st.columns(4)

with nk1:
    st.metric(label="Gasto Transporte",
              value=f"R${gasto_total_transporte:,.0f}")
    st.caption("Asociado a días de ausencia")

with nk2:
    st.metric(label="IMC Promedio", value=f"{bmi_promedio:.1f}")
    # Color según rango de salud (opcional)
    status_bmi = "Sobrepeso" if bmi_promedio > 25 else "Normal"
    st.caption(f"Perfil: {status_bmi}")

with nk3:
    st.metric(label="Fallos Disc.",
              value=f"{tasa_fallos:.1f}%")
    st.caption("Impacto en disciplina")

with nk4:
    st.metric(label="Carga Familiar", value=f"{promedio_hijos:.1f}")
    st.caption("Promedio de hijos")

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

# 1. Unimos los datos
df_estacional = RRHH_full.merge(df_id[['ID', 'Segmento']], on='ID')

# 2. FILTRADO CRÍTICO: Quitamos el mes 0 antes de agrupar
df_estacional = df_estacional[df_estacional['Month_absence'] != 0]

# 3. Agrupamos (ahora solo habrá meses del 1 al 12)
df_mensual = df_estacional.groupby(['Month_absence', 'Segmento'])[
    'Absenteeism_hours'].sum().reset_index()

# 4. Creamos el gráfico
fig_estacional = px.line(
    df_mensual,
    x='Month_absence',
    y='Absenteeism_hours',
    color='Segmento',
    title="Patrón de Ausencias en un Ciclo Anual (Ene-Dic)",
    markers=True,
    labels={'Month_absence': 'Mes del Año',
            'Absenteeism_hours': 'Total Horas de Ausencia'},
    color_discrete_sequence=["#093C2B", '#65E74B', "#51A242"]
)

# --- AJUSTE EXTREMO PARA EL EJE X ---
fig_estacional.update_layout(
    plot_bgcolor='#EEEEEE',
    paper_bgcolor='#EEEEEE',
    font=dict(family="Inter", color="black"),
    xaxis=dict(
        showgrid=False,     # Quita líneas verticales
        showline=False,     # Quita la línea del eje X
        zeroline=False,     # Quita la línea del cero
        dtick=1,
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        showgrid=False,     # Quita líneas horizontales
        showline=False,     # Quita la línea del eje Y
        zeroline=False,     # Quita la línea del cero
        tickfont=dict(color='black')
    ),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)

fig_estacional.update_traces(
    line=dict(width=3),
    marker=dict(size=8, line=dict(width=0, color='white'))
)

st.plotly_chart(fig_estacional, width='stretch')


st.divider()

st.header("Lógica & Exito: ¿Qué impulsa el rendimiento y la buena conducta?")


# Limpieza de nombres de columnas
RRHH_full.columns = RRHH_full.columns.str.strip()

# Selección de variables global
features_pred = [
    'Distance_Residence_Work', 'Service_time',
    'Age', 'Son', 'Pet', 'Body_mass_index',
    'Social_drinker', 'Social_smoker', 'Education'
]


# --- Preparación ---
df_id['Good_Conduct'] = 1 - df_id['Disciplinary_failure']

# --- Clasificación de variables con test explícito ---
continuous_vars = {
    'Distance_Residence_Work': 'pearson',
    'Service_time': 'pearson',
    'Age': 'pearson',
    'Body_mass_index': 'pearson',
    'Son': 'pearson',
    'Pet': 'pearson'
}

binary_vars = {
    'Social_drinker': 'ttest',
    'Social_smoker': 'ttest'
}

categorical_vars = {
    'Education': 'anova_spearman'
}

results_table = []

# --- 1. Impacto vs Hit_target ---
impact_hit = []

# Continuous vars vs Hit_target (Pearson)
for var, test in continuous_vars.items():
    r, p_val = pearsonr(df_id[var], df_id['Hit_target'])
    impact_hit.append({'Variable': var, 'Impacto': r})
    results_table.append({
        'Variable': var,
        'Tipo': 'Numérica',
        'Test': 'Pearson',
        'p-value': round(p_val, 4),
        'Impacto': round(r, 4),
        'Target': 'Hit_target',
        'Conclusión': 'Significativa' if p_val < 0.05 else 'No significativa'
    })

# Binary vars vs Hit_target (ANOVA / diferencia media)
for var, test in binary_vars.items():
    grupos = [df_id[df_id[var] == c]['Hit_target']
              for c in df_id[var].unique()]
    if len(grupos) > 1:
        f_stat, p_val = f_oneway(*grupos)
        impact = max([g.mean() for g in grupos]) - \
            min([g.mean() for g in grupos])
    else:
        f_stat, p_val = np.nan, np.nan
        impact = 0
    impact_hit.append({'Variable': var, 'Impacto': impact})
    results_table.append({
        'Variable': var,
        'Tipo': 'Boolean',
        'Test': 'ANOVA / Diferencia media',
        'p-value': round(p_val, 4) if not np.isnan(p_val) else np.nan,
        'Impacto': round(impact, 4),
        'Target': 'Hit_target',
        'Conclusión': 'Significativa' if (not np.isnan(p_val) and p_val < 0.05) else 'No significativa'
    })

# Education vs Hit_target (agrupando por empleado)
if 'Education' in df_id.columns and 'ID' in df_id.columns:
    df_edu = df_id.groupby('ID').agg({
        'Education': 'max',  # o el valor representativo
        'Hit_target': 'mean'
    }).reset_index()

    # ANOVA
    categorias = df_edu['Education'].unique()
    datos_por_grupo = [df_edu[df_edu['Education'] == c]
                       ['Hit_target'] for c in categorias]
    if len(datos_por_grupo) > 1:
        f_stat, p_val = f_oneway(*datos_por_grupo)
        impact = max([g.mean() for g in datos_por_grupo]) - \
            min([g.mean() for g in datos_por_grupo])
    else:
        f_stat, p_val, impact = np.nan, np.nan, 0

    # Spearman
    r_s, p_s = spearmanr(df_edu['Education'],
                         df_edu['Hit_target'], nan_policy='omit')
    impact_hit.append({'Variable': 'Education', 'Impacto': r_s})
    results_table.append({
        'Variable': 'Education',
        'Tipo': 'Ordinal',
        'Test': 'ANOVA + Spearman',
        'p-value': round(p_s, 4),
        'Impacto': round(r_s, 4),
        'Target': 'Hit_target',
        'Conclusión': 'Significativa' if p_s < 0.05 else 'No significativa'
    })

# --- 2. Impacto vs Disciplinary_failure ---
impact_disc = []

# Continuous vars vs Disciplinary_failure (T-test / Point-biserial)
for var, test in continuous_vars.items():
    grupo_falta = df_id[df_id['Disciplinary_failure'] == 1][var]
    grupo_no_falta = df_id[df_id['Disciplinary_failure'] == 0][var]
    t_stat, p_val = ttest_ind(grupo_falta, grupo_no_falta, nan_policy='omit')
    df_temp = df_id[[var, 'Disciplinary_failure']].dropna()
    corr_biserial, _ = pointbiserialr(
        df_temp['Disciplinary_failure'], df_temp[var])
    impact_disc.append({'Variable': var, 'Impacto': corr_biserial})
    results_table.append({
        'Variable': var,
        'Tipo': 'Numérica',
        'Test': 'T-test / Point-biserial',
        'p-value': round(p_val, 4),
        'Impacto': round(corr_biserial, 4),
        'Target': 'Disciplinary_failure',
        'Conclusión': 'Significativa' if p_val < 0.05 else 'No significativa'
    })

# Binary vars vs Disciplinary_failure (Chi² / V de Cramer)
for var, test in binary_vars.items():
    tabla = pd.crosstab(df_id[var], df_id['Disciplinary_failure'])
    chi2, p_val, dof, expected = chi2_contingency(tabla)
    n = tabla.sum().sum()
    min_dim = min(tabla.shape)-1
    v_cramer = np.sqrt(chi2/(n*min_dim)) if min_dim > 0 else np.nan
    impact_disc.append({'Variable': var, 'Impacto': v_cramer})
    results_table.append({
        'Variable': var,
        'Tipo': 'Boolean',
        'Test': 'Chi² / V de Cramer',
        'p-value': round(p_val, 4),
        'Impacto': round(v_cramer, 4),
        'Target': 'Disciplinary_failure',
        'Conclusión': 'Significativa' if p_val < 0.05 else 'No significativa'
    })

# Education vs Disciplinary_failure (Chi² / V de Cramer)
tabla = pd.crosstab(df_edu['Education'], df_id.groupby('ID')[
                    'Disciplinary_failure'].max())
chi2, p_val, dof, expected = chi2_contingency(tabla)
n = tabla.sum().sum()
min_dim = min(tabla.shape)-1
v_cramer = np.sqrt(chi2/(n*min_dim)) if min_dim > 0 else np.nan
impact_disc.append({'Variable': 'Education', 'Impacto': v_cramer})
results_table.append({
    'Variable': 'Education',
    'Tipo': 'Ordinal',
    'Test': 'Chi² / V de Cramer',
    'p-value': round(p_val, 4),
    'Impacto': round(v_cramer, 4),
    'Target': 'Disciplinary_failure',
    'Conclusión': 'Significativa' if p_val < 0.05 else 'No significativa'
})

# --- 3. Gráficos lado a lado ---
st.write("### Impacto de Variables: Disciplinary vs Hit_target")
col1, col2 = st.columns(2)

with col1:
    df_disc = pd.DataFrame(impact_disc).sort_values('Impacto', ascending=True)
    fig_disc = px.bar(df_disc, x='Impacto', y='Variable', orientation='h',
                      title="Impacto en Disciplina",
                      color='Impacto', color_continuous_scale='RdYlGn',
                      template='plotly_white')
    fig_disc.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20),
                           coloraxis_showscale=False,
                           yaxis=dict(tickfont=dict(size=17)),
                           plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE')
    st.plotly_chart(fig_disc, width='stretch')

with col2:
    df_hit = pd.DataFrame(impact_hit).sort_values('Impacto', ascending=True)
    fig_hit = px.bar(df_hit, x='Impacto', y='Variable', orientation='h',
                     title="Impacto en Rendimiento",
                     color='Impacto', color_continuous_scale='RdYlGn',
                     template='plotly_white')
    fig_hit.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20),
                          coloraxis_showscale=False,
                          yaxis=dict(tickfont=dict(size=17)),
                          plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE')
    st.plotly_chart(fig_hit, width='stretch')

# --- 4. Tabla de resultados ---
with st.expander("Tabla de Tests y Resultados", expanded=False):
    df_results = pd.DataFrame(results_table)
    st.dataframe(df_results, width='stretch')

st.divider()
# --- 2. MACHINE LEARNING (EL PESO DE LAS VARIABLES) ---
st.header("Work vs. Life")

# Preparación de datos y entrenamiento (Igual que antes)
X_data = RRHH_full[features_pred].dropna()
y_p = RRHH_full.loc[X_data.index, ['Disciplinary_failure', 'Hit_target']]
X_p = pd.get_dummies(X_data, columns=[
                     'Education'], drop_first=True) if 'Education' in X_data.columns else pd.get_dummies(X_data, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X_p, y_p, test_size=0.2, random_state=42)

rf_model = MultiOutputRegressor(
    RandomForestRegressor(n_estimators=200, random_state=42))
rf_model.fit(X_train, y_train)


# --- 1. MODELO DE DISCIPLINA (Clasificación) ---
# Usamos class_weight='balanced' para compensar que hay pocos fallos
model_disc = RandomForestClassifier(
    n_estimators=200, class_weight='balanced', random_state=42)
model_disc.fit(X_train, y_train.iloc[:, 0])
y_pred_disc = model_disc.predict(X_test)

# --- 2. MODELO DE RENDIMIENTO (Regresión) ---
model_hit = RandomForestRegressor(n_estimators=200, random_state=42)
model_hit.fit(X_train, y_train.iloc[:, 1])
y_pred_hit = model_hit.predict(X_test)

# --- 3. MÉTRICAS REALISTAS ---
acc_bal = balanced_accuracy_score(
    y_test.iloc[:, 0], y_pred_disc)  # Ajusta por desequilibrio
# ¿Detectamos a los que fallan?
rec_risk = recall_score(y_test.iloc[:, 0], y_pred_disc)

c1, c3 = st.columns(2)

with c1:
    st.metric(
        label="Poder Predictivo (Conducta)",
        value="Moderado (54.9%)",
        delta="Estadísticamente válido",
        help="Capacidad del modelo para diferenciar perfiles positivos de riesgos."
    )

with c3:
    st.metric(
        label="Predictor de Rendimiento",
        value="No lineal",
        delta="-0.06 R²",
        delta_color="off",
        help="El rendimiento depende de factores externos no registrados en este estudio."
    )

st.write("")  # Espaciador
# --- (Aquí sigue tu código de importancias y el gráfico fig_rf) ---

# Preparación de datos
X_data = RRHH_full[features_pred].dropna()
y_p = RRHH_full.loc[X_data.index, ['Disciplinary_failure', 'Hit_target']]
X_p = pd.get_dummies(X_data, columns=[
                     'Education'], drop_first=True) if 'Education' in X_data.columns else pd.get_dummies(X_data, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X_p, y_p, test_size=0.2, random_state=42)

# Modelo Multi-Output
rf_model = MultiOutputRegressor(
    RandomForestRegressor(n_estimators=200, random_state=42))
rf_model.fit(X_train, y_train)

# Importancias
imp_disc = rf_model.estimators_[0].feature_importances_
imp_hit = rf_model.estimators_[1].feature_importances_

df_imp_dual = pd.DataFrame({
    'Variable': X_p.columns,
    'Impacto Disciplina': imp_disc,
    'Impacto Rendimiento': imp_hit
}).melt(id_vars='Variable', var_name='Tipo de Impacto', value_name='Importancia')

# Crear un diccionario de mapping para los dummies de Education
education_map = {
    'Education_1': "High School",
    'Education_2': "Graduate",
    'Education_3': "Postgraduate",
    'Education_4': "Master & Doctor"
}

# Copiamos df_imp_dual para visualización
df_vis = df_imp_dual.copy()

# Reemplazamos solo las columnas de Education
df_vis['Variable'] = df_vis['Variable'].replace(education_map)

# Ahora usar df_vis en los gráficos
col_left, col_right = st.columns(2)

with col_left:
    df_disc_plot = df_vis[df_vis['Tipo de Impacto'] == 'Impacto Disciplina'].sort_values(
        'Importancia', ascending=True
    )
    fig_disc = px.bar(
        df_disc_plot,
        x='Importancia', y='Variable', orientation='h',
        title='Impacto en Disciplina', template='plotly_white',
        color='Importancia', color_continuous_scale='Greens'
    )
    fig_disc.update_layout(
        plot_bgcolor="#EEEEEE",
        paper_bgcolor="#EEEEEE",
        xaxis=dict(tickfont=dict(size=17)),
        yaxis=dict(tickfont=dict(size=17))
    )
    st.plotly_chart(fig_disc, width='stretch')

with col_right:
    df_hit_plot = df_vis[df_vis['Tipo de Impacto'] == 'Impacto Rendimiento'].sort_values(
        'Importancia', ascending=True
    )
    fig_hit = px.bar(
        df_hit_plot,
        x='Importancia', y='Variable', orientation='h',
        title='Impacto en Rendimiento', template='plotly_white',
        color='Importancia', color_continuous_scale='Greens'
    )
    fig_hit.update_layout(
        plot_bgcolor="#EEEEEE",
        paper_bgcolor="#EEEEEE",
        xaxis=dict(tickfont=dict(size=16)),
        yaxis=dict(tickfont=dict(size=16))
    )
    st.plotly_chart(fig_hit, width='stretch')

# --- EXTRACCIÓN AUTOMÁTICA DE INSIGHTS ---
# Obtenemos las 3 variables más importantes para cada objetivo
top_3_disc = df_imp_dual[df_imp_dual['Tipo de Impacto']
                         == 'Impacto Disciplina'].nlargest(3, 'Importancia')
top_3_hit = df_imp_dual[df_imp_dual['Tipo de Impacto']
                        == 'Impacto Rendimiento'].nlargest(3, 'Importancia')


with st.expander("Interpretación Estratégica de la IA", expanded=False):

    def format_var(name):
        return name.replace('_', ' ').title()

    col_ins_1, col_ins_2 = st.columns(2)

    with col_ins_1:
        st.subheader("Foco: Disciplina")
        st.write("Variables con mayor peso en la estabilidad conductual:")
        for i, (idx, row) in enumerate(top_3_disc.iterrows()):
            st.success(f"**{i+1}. {format_var(row['Variable'])}**")
        st.caption(
            "Estas variables son las que mejor separan a un perfil cumplidor de uno con riesgo disciplinario.")

    with col_ins_2:
        st.subheader("Foco: Rendimiento")
        st.write("Variables clave para alcanzar los objetivos (Hit Target):")
        for i, (idx, row) in enumerate(top_3_hit.iterrows()):
            st.success(f"**{i+1}. {format_var(row['Variable'])}**")
        st.caption(
            "Optimizar o filtrar por estos factores maximiza la probabilidad de éxito operativo.")


# ==========================================
# IDENTIFICACIÓN DEL TALENTO IDEAL (PERFIL TOP)
# ==========================================

# Filtramos: Sin fallos, Rendimiento >= 95% Y Cero Absentismo
df_talento_ideal = RRHH_full[
    (RRHH_full['Disciplinary_failure'] == 0) &
    (RRHH_full['Hit_target'] >= 95) &
    (RRHH_full['Absenteeism_hours'] == 0)
]

total_ideales = len(df_talento_ideal)
# --- SECCIÓN: EL TALENTO IDEAL EN EXPANDER ---
with st.expander("Ver Cuadro de Honor", expanded=False):
    # Filtramos: Sin fallos, Rendimiento >= 95% Y Cero Absentismo
    df_talento_ideal = RRHH_full[
        (RRHH_full['Disciplinary_failure'] == 0) &
        (RRHH_full['Hit_target'] >= 95) &
        (RRHH_full['Absenteeism_hours'] == 0)
    ]

    total_ideales = len(df_talento_ideal)

    st.write(f"### El Talento Ideal ({total_ideales} empleados)")

    if total_ideales > 0:
        st.info(
            f"Hemos identificado a {total_ideales} profesionales con conducta impecable, "
            f"rendimiento superior al 95% y 0 ausencias."
        )

        st.dataframe(
            df_talento_ideal[['ID', 'Education',
                              'Hit_target', 'Service_time', 'Age']],
            width='stretch',
            hide_index=True,
            column_config={
                "Hit_target": st.column_config.ProgressColumn("Rendimiento", format="%d%%", min_value=0, max_value=100),
                "Service_time": "Antigüedad",
                "Age": "Edad"
            }
        )
    else:
        st.warning(
            "No hay empleados que cumplan los tres criterios simultáneamente (Disciplina + Rendimiento + Presencia)."
        )

# --- 3. EXPLORADOR DE DATOS (EL DETALLE) ---
with st.expander("Explorar Dataset Completo (RRHH_full)"):
    st.write("Auditoría de datos originales.")
    search_id = st.text_input("🔍 Buscar por ID de empleado:", "")
    df_display = RRHH_full[RRHH_full['ID'].astype(
        str).str.contains(search_id)] if search_id else RRHH_full

    st.dataframe(
        df_display, width='stretch',
        column_config={
            "Hit_target": st.column_config.ProgressColumn("Rendimiento (%)", format="%f", min_value=0, max_value=100),
            "Disciplinary_failure": st.column_config.CheckboxColumn("Fallo Disciplinario")
        }
    )

    csv = RRHH_full.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", data=csv,
                       file_name='RRHH_full.csv', mime='text/csv')

st.divider()

# --- CÁLCULO DE LOS 4 KPIs CON TUS COLUMNAS ---

# 1. Mes pico de carga (Basado en 'Month_absence' y 'Absenteeism_hours')
mes_pico_idx = RRHH_full.groupby('Month_absence')[
    'Absenteeism_hours'].sum().idxmax()
meses_map = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
             7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
mes_pico_nombre = meses_map.get(mes_pico_idx, f"Mes {mes_pico_idx}")

# 2. Motivo modal (Basado en 'Reason_Description' para que Verônica lo entienda mejor)
# Si prefieres el número, cambia a 'Reason_absence'
motivo_modal = RRHH_full['Reason_Description'].mode()[0]

# 3. Índice de eficiencia relativa (Basado en 'Hit_target' y 'Work_load_Average_day')
eficiencia_relativa = (RRHH_full['Hit_target'].mean(
) / RRHH_full['Work_load_Average_day'].mean()) * 100

# 4. Porcentaje de empleados ausentes (Basado en 'ID' y 'Absenteeism_hours')
total_empleados = RRHH_full['ID'].nunique()
empleados_ausentes = RRHH_full[RRHH_full['Absenteeism_hours'] > 0]['ID'].nunique(
)
porcentaje_ausencia = (empleados_ausentes / total_empleados) * 100
st.divider()


def clasificar_perfil_id(row):

    if row['Disciplinary_failure'] == 1 and row['Riesgo_Carga'] == 'Saturación':
        return 'Perfil de Inestabilidad'

    if row['Riesgo_Carga'] == 'Saturación' and row['Riesgo_Distancia'] != 'Local':
        return 'Saturado Logístico'

    if row['Service_time'] < 5 and row['Riesgo_Carga'] in ['Óptima', 'Saturación']:
        return 'En desarrollo operativo'

    return 'Perfil Estable'


@st.cache_data
def procesar_datos():
    # Cargar datos
    RRHH = pd.read_csv("full_RRHH.csv")
    df_analisis = RRHH.copy()

    # --- 1. CREACIÓN DE BINS (BASE DEL SISTEMA) ---
    df_analisis['Riesgo_Distancia'] = pd.cut(
        df_analisis['Distance_Residence_Work'],
        bins=[0, 16, 49, 53],
        labels=['Local', 'Media', 'Crítica']
    )

    df_analisis['Riesgo_Carga'] = pd.cut(
        df_analisis['Work_load_Average_day'],
        bins=[0, 244, 284, 400],
        labels=['Ligera', 'Óptima', 'Saturación']
    )

    # --- 2. AGRUPACIÓN POR EMPLEADO ---
    df_empleados = df_analisis.groupby('ID').agg({
        'Service_time': 'max',
        'Distance_Residence_Work': 'mean',
        'Work_load_Average_day': 'mean',
        'Hit_target': 'mean',
        'Disciplinary_failure': 'max',
    }).reset_index()

    # 🔥 IMPORTANTE: recalcular bins a nivel empleado (CONSISTENCIA)
    df_empleados['Riesgo_Distancia'] = pd.cut(
        df_empleados['Distance_Residence_Work'],
        bins=[0, 16, 49, 53],
        labels=['Local', 'Media', 'Crítica']
    )

    df_empleados['Riesgo_Carga'] = pd.cut(
        df_empleados['Work_load_Average_day'],
        bins=[0, 244, 284, 400],
        labels=['Ligera', 'Óptima', 'Saturación']
    )

    df_empleados['Perfil_Riesgo'] = df_empleados.apply(
        clasificar_perfil_id, axis=1
    )

    return df_analisis, df_empleados


# Ejecutar proceso
try:
    df_analisis, df_empleados = procesar_datos()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'full_RRHH.csv'. Por favor, cárgalo en la carpeta del proyecto.")
    st.stop()


# Datos consolidados de tus 3 semanas
data = {
    'Semana': ['Semana 1', 'Semana 2', 'Semana 3'],
    'Ausencia (%)': [91.67, 96.30, 95.07],
    'Eficiencia (%)': [35.44, 34.8, 34.85],
    'Mes Pico': ['March', 'July', 'July'],
    'Motivo': ['Medical consultation', 'Medical consultation', 'Medical consultation']
}

df_evolucion = pd.DataFrame(data)

# --- CÁLCULOS PARA LOS NUEVOS KPIs ---

# 1. Impacto de Cargas Familiares (Hijos)
# Comparamos el promedio de horas de ausencia de quienes tienen hijos vs los que no
promedio_hijos = RRHH_full[RRHH_full['Son'] > 0]['Absenteeism_hours'].mean()
promedio_sin_hijos = RRHH_full[RRHH_full['Son']
                               == 0]['Absenteeism_hours'].mean()
diff_familiar = promedio_hijos - promedio_sin_hijos

# 2. Eficiencia de Desplazamiento (Costo por KM)
# ¿Cuánto nos cuesta en transporte cada KM que recorre el empleado?
costo_km_promedio = (RRHH_full['Transportation_expense'] /
                     RRHH_full['Distance_Residence_Work']).mean()

# 3. Ratio de Hábitos Sociales (Social Drinkers)
# ¿Qué porcentaje de las horas totales de ausencia vienen de "Social Drinkers"?
horas_bebedores = RRHH_full[RRHH_full['Social_drinker']
                            == 1]['Absenteeism_hours'].sum()
total_horas_abs = RRHH_full['Absenteeism_hours'].sum()
pct_horas_social = (horas_bebedores / total_horas_abs) * 100

# --- VISUALIZACIÓN EN STREAMLIT ---


st.header("Evolución de Gestión de Absentismo")

# Columnas para los KPIs actuales (Semana 3)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    # Comparamos 95.08 vs 95.10 (Semana 2)
    st.metric("Ausencia Actual", "95.07%")

with kpi2:
    st.metric("Eficiencia Relativa", "34.85%",
              delta="Sin cambios", delta_color="off")

with kpi3:
    st.metric("Motivo Principal", "Medical Consultation",
              help="Medical consultation es el motivo recurrente")

with kpi4:
    st.metric(
        label="Factor Familiar",
        value=f"+{diff_familiar:.1f} horas",
        delta="Exceso de ausencia (Padres)",
        delta_color="inverse",
        help="Diferencia de horas de ausencia promedio entre empleados con hijos vs. sin hijos."
    )

with kpi5:
    st.metric(
        label="Impacto Hábitos Sociales",
        value=f"{pct_horas_social:.1f}%",
        delta="Social Drinkers",
        delta_color="normal",
        help="Porcentaje del total de horas de ausencia que corresponden a bebedores sociales."
    )
# --- GRÁFICO DE TENDENCIA ACTUALIZADO ---
fig_evolucion = px.line(
    df_evolucion,
    x='Semana',
    y=['Ausencia (%)', 'Eficiencia (%)'],
    markers=True,
    title="<b>Tendencia: Ausencia vs Eficiencia</b>",
    labels={"value": "Porcentaje (%)", "variable": "Indicador"},
    color_discrete_map={
        "Ausencia (%)": "#E74C3C",
        "Eficiencia (%)": "#3498DB"
    }
)

# --- ACTIVAR Y FORMATEAR LAS ETIQUETAS ---
fig_evolucion.update_traces(
    textposition="top center",  # Pone el número arriba del punto
    texttemplate='%{y:.2f}%',   # Formato con 2 decimales y el símbolo %
    mode="lines+markers+text"   # Asegura que se vean las 3 cosas
)

# --- AJUSTE DE FONDO Y TAMAÑO DE EJES ---
fig_evolucion.update_layout(
    # Fondo transparente para integrarse a tu app
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="grey",  # Color de fuente para los textos

    # Título
    title=dict(
        font=dict(size=17),
        x=0,
        xanchor='left'
    ),

    # Leyenda arriba
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="right",
        x=1,
        title_text="",
        font=dict(size=14)
    ),

    hovermode="x unified",
    margin=dict(t=100, b=50)
)

# --- AUMENTAR TAMAÑO DE EJES X e Y ---
fig_evolucion.update_xaxes(
    title_font=dict(size=20, color="grey"),  # Título del eje X
    tickfont=dict(size=16, color="grey"),  # Números/Semana del eje X
    gridcolor="rgba(200, 200, 200, 0.1)"    # Cuadrícula muy sutil
)

fig_evolucion.update_yaxes(
    title_font=dict(size=20, color="grey"),  # Título del eje Y
    tickfont=dict(size=16, color="grey"),  # Números del eje Y
    gridcolor="rgba(200, 200, 200, 0.1)",
    range=[0, 105]  # Mantiene la perspectiva real de los datos
)

# Renderizar
st.plotly_chart(fig_evolucion, width='stretch',
                key="linea_evolucion_final")

st.divider()

st.header("Distribución de Rendimiento por Perfil (Clasificación Manual)")

# 1. Aseguramos la limpieza de nombres
df_empleados['Perfil_Riesgo'] = df_empleados['Perfil_Riesgo'].replace({
    'Junior Vulnerable': 'En desarrollo operativo'
})

# 2. Calculamos totales y frecuencias
total_n = len(df_empleados)
conteo = df_empleados['Perfil_Riesgo'].value_counts()

# 3. Función auxiliar para el formato "Cantidad (Porcentaje%)"


def fmt_manual(perfil):
    n = conteo.get(perfil, 0)
    pct = (n / total_n) * 100 if total_n > 0 else 0
    return f"{n} ({pct:.1f}%)"


# 4. Renderizado de Columnas
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Perfil Estable",
    fmt_manual("Perfil Estable")
)

col2.metric(
    "Saturados Logísticos",
    fmt_manual("Saturado Logístico")
)

col3.metric(
    "En desarrollo operativo",
    fmt_manual("En desarrollo operativo")
)

col4.metric(
    "Perfil de Inestabilidad",
    fmt_manual("Perfil de Inestabilidad")
)

df_empleados['Perfil_Riesgo'] = df_empleados['Perfil_Riesgo'].replace({
    'Junior Vulnerable': 'En desarrollo operativo'
})

# 2. ACTUALIZACIÓN DE LA LISTA DE ORDEN (Muy importante)
orden_perfiles = [
    'Perfil Estable',
    'En desarrollo operativo',
    'Saturado Logístico',
    'Perfil de Inestabilidad'
]

# 3. CREACIÓN DEL BOXPLOT
fig_dispersion = px.box(
    df_empleados,
    x='Perfil_Riesgo',
    y='Hit_target',
    color='Perfil_Riesgo',
    points="all",
    category_orders={"Perfil_Riesgo": orden_perfiles},
    labels={
        "Perfil_Riesgo": "Perfil Detectado",
        "Hit_target": "Rendimiento (%)"
    },
    color_discrete_map={
        'Perfil Estable': "#3A93D4",
        'Saturado Logístico': '#F1C40F',
        'En desarrollo operativo': "#DB3434",
        'Perfil de Inestabilidad': "#17A11E"
    },
    title="<b>Validación Visual: Distribución de Rendimiento por Perfil</b>"
)

fig_dispersion.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    template="plotly_dark",
    font_color="black",
    height=500,
    showlegend=False,
    title=dict(font=dict(size=18)),
    xaxis=dict(
        title=dict(font=dict(size=18)),
        tickfont=dict(size=16),
        categoryorder='array',
        categoryarray=orden_perfiles  # Esto elimina huecos vacíos
    ),
    yaxis=dict(
        title=dict(font=dict(size=18)),
        tickfont=dict(size=18),
        gridcolor="rgba(0,0,0,0.1)"
    )

)

fig_dispersion.update_traces(marker=dict(line=dict(width=0)))


st.plotly_chart(fig_dispersion, width='stretch', key="box_final_ok")

# --- NOTA TÉCNICA AL PIE (CAPTION) ---
st.markdown(f"""

        <p style="font-size: 13px; color: grey; line-height: 1.4;">
            Este análisis cruza las variables de <b>Antigüedad</b> (Service_time), <b>Logística</b> (Distance_Residence_Work), <b>Carga Laboral (Work_Load_Average) y  <b>Targes (Hit_Target).</b>
            <br>
        </p>

    """, unsafe_allow_html=True)

# ==========================================================
# 🔍 DETALLE ESTADÍSTICO: CLASIFICACIÓN MANUAL
# ==========================================================
with st.expander("Ver Caracterización de Perfiles Manuales (Reglas de Negocio)"):
    st.write("Resumen de métricas basado en la lógica de clasificación original:")

    # 1. Calculamos las medias sobre el dataframe ANTES de que la IA lo sobrescriba
    # Nota: Asegúrate de que 'Perfil_Riesgo' en este punto del código aún tenga tus etiquetas manuales
    df_detalle_manual = df_empleados.groupby('Perfil_Riesgo').agg({
        'ID': 'count',
        'Work_load_Average_day': 'mean',
        'Distance_Residence_Work': 'mean',
        'Service_time': 'mean',
        'Hit_target': 'mean'
    }).rename(columns={'ID': 'Nº Empleados'})

    # 2. Aplicar formato y estilo
    df_manual_fmt = df_detalle_manual.style.format({
        'Work_load_Average_day': '{:.1f} unidades',
        'Distance_Residence_Work': '{:.1f} km',
        'Service_time': '{:.1f} años',
        'Hit_target': '{:.1f}%'
        # Azul para diferenciar de la IA
    }).background_gradient(cmap='Blues', subset=['Hit_target'])

    st.dataframe(df_manual_fmt, width='stretch')

    st.caption(
        "Nota: Estos valores reflejan la situación actual bajo tus criterios de segmentación manual.")


with st.expander("Ver Validación Estadística (ANOVA)"):

    grupo_ligera = df_analisis[df_analisis['Riesgo_Carga']
                               == 'Ligera']['Hit_target']
    grupo_optima = df_analisis[df_analisis['Riesgo_Carga']
                               == 'Óptima']['Hit_target']
    grupo_saturacion = df_analisis[df_analisis['Riesgo_Carga']
                                   == 'Saturación']['Hit_target']

    f_stat, p_val = stats.f_oneway(
        grupo_ligera, grupo_optima, grupo_saturacion)

    st.write(f"**Análisis de Varianza (Carga Laboral):**")
    st.write(f"- F-Statistic: `{f_stat:.4f}`")
    st.write(f"- P-Valor: `{p_val:.4f}`")

    if p_val < 0.05:
        st.success(
            "✅ Diferencias significativas confirmadas: La carga afecta el rendimiento.")
    else:
        st.warning("⚠️ No se detectaron diferencias significativas.")

# --- Debajo de st.plotly_chart(fig_dispersion, ...) ---

st.info("""
**Lógica de Clasificación de Perfiles**

* **Perfil Estable:** Colaboradores que mantienen un equilibrio entre carga, distancia y experiencia.
* **En desarrollo operativo:** Empleados con menos de 5 años de antigüedad enfrentando cargas de trabajo superiores a la media.
* **Saturado Logístico:** Colaboradores con alta carga laboral (> 284 unidades) y que viven a más de 16km de la sede.
* **Perfil de Inestabilidad:** Empleados con fallos disciplinarios y carga de trabajo crítica (> 284 unidades).

*Nota: Los datos representan promedios agrupados por ID de empleado para capturar tendencias de largo plazo.*
""")

st.divider()

# X debe contener las columnas que usaste para entrenar
X = df_empleados[['Service_time',
                  'Distance_Residence_Work', 'Work_load_Average_day']]
y = df_empleados['Perfil_Riesgo']

# --- 2. ENTRENAMIENTO DEL MODELO (Define 'clf' globalmente aquí) ---
# Lo limitamos a profundidad 3 para que sea consistente con tu análisis
clf = DecisionTreeClassifier(
    max_depth=3, class_weight='balanced', random_state=42)
clf.fit(X, y)

# --- 1. CÁLCULO DE MÉTRICAS POR SEGMENTO ---
# Agrupamos por Perfil para obtener las medias
df_resumen = df_empleados.groupby('Perfil_Riesgo').agg({
    'ID': 'count',
    'Work_load_Average_day': 'mean',
    'Distance_Residence_Work': 'mean',
    'Hit_target': 'mean',
    'Service_time': 'mean'
}).rename(columns={'ID': 'Cantidad'}).reset_index()


# ==========================================================
# 🤖 BLOQUE DE INTELIGENCIA ARTIFICIAL (CLUSTERING)
# ==========================================================

# 1. Preparación de datos: Seleccionamos las variables de influencia
columnas_ia = ['Service_time',
               'Distance_Residence_Work', 'Work_load_Average_day']
X_ia = df_empleados[columnas_ia]

# 2. Normalización: Escalamos los datos para que sean comparables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_ia)

# 3. Ejecución del Modelo: La IA busca 4 grupos automáticamente
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_empleados['Cluster_Num'] = kmeans.fit_predict(X_scaled)

# ==========================================================
# 🧠 MAPEADOR CORREGIDO (Basado en datos reales de Imagen 3)
# ==========================================================
# 1. Obtenemos las medias de cada cluster numérico
resumen_ia = df_empleados.groupby('Cluster_Num').agg({
    'Service_time': 'mean',
    'Distance_Residence_Work': 'mean',
    'Work_load_Average_day': 'mean'
})

# 2. Lógica Automática de Identificación
# El que tiene menos antigüedad es el Junior (En desarrollo)
id_junior = resumen_ia['Service_time'].idxmin()

# El que tiene más distancia es el Saturado Logístico
id_logistico = resumen_ia['Distance_Residence_Work'].idxmax()

# El que tiene más carga laboral es el de Inestabilidad
# (Excluimos al logístico si coincide para no repetir)
id_inestable = resumen_ia['Work_load_Average_day'].idxmax()

# El que sobra es el Estable
todos = set(resumen_ia.index)
usados = {id_junior, id_logistico, id_inestable}
id_estable = list(todos - usados)[0] if len(todos - usados) > 0 else None

# 3. Creamos el mapeador dinámico
mapeo_dinamico = {
    str(id_junior): "En desarrollo operativo",
    str(id_logistico): "Saturado Logístico",
    str(id_inestable): "Perfil de Inestabilidad",
    str(id_estable): "Perfil Estable"
}

# 4. Aplicamos al DataFrame
df_empleados['Perfil_Riesgo'] = df_empleados['Cluster_Num'].astype(
    str).map(mapeo_dinamico)

# 6. RECALCULAR RESUMEN: Para que tus tablas y métricas m1, m2... se actualicen
df_resumen = df_empleados.groupby('Perfil_Riesgo').agg({
    'ID': 'count',
    'Work_load_Average_day': 'mean',
    'Distance_Residence_Work': 'mean',
    'Hit_target': 'mean',
    'Service_time': 'mean'
}).rename(columns={'ID': 'Cantidad'}).reset_index()

# ==========================================================
# 📊 A PARTIR DE AQUÍ COMIENZA TU INFORME (YA ACTUALIZADO)
# ==========================================================

st.subheader("Resumen Operativo por Segmento (Validado por IA)")

# 1. Calculamos el total y las frecuencias
total_empleados = len(df_empleados)
counts = df_empleados['Perfil_Riesgo'].value_counts()

# 2. Creamos las columnas
m1, m2, m3, m4 = st.columns(4)

# Función auxiliar para formatear: "Cantidad (Porcentaje%)"


def fmt_metric(label):
    count = counts.get(label, 0)
    pct = (count / total_empleados) * 100
    return f"{count} ({pct:.1f}%)"


# 3. Renderizado de métricas
m1.metric(
    "Perfil Estable",
    fmt_metric("Perfil Estable"),
    "Grupo Base"
)

m2.metric(
    "Saturado Logístico",
    fmt_metric("Saturado Logístico"),
    "Riesgo Carga",
    delta_color="inverse"
)

m3.metric(
    "En desarrollo operativo",
    fmt_metric("En desarrollo operativo"),
    "En Formación"
)

m4.metric(
    "Perfil de Inestabilidad",
    fmt_metric("Perfil de Inestabilidad"),
    "Críticos",
    delta_color="inverse"
)

# --- 1. APLICAR JITTER ---
df_jitter = df_empleados.copy()
df_jitter['Distancia en Km'] = df_jitter['Distance_Residence_Work'] + \
    np.random.uniform(-0.3, 0.3, len(df_jitter))
df_jitter['Antigüedad'] = df_jitter['Service_time'] + \
    np.random.uniform(-0.3, 0.3, len(df_jitter))
# --- CONFIGURACIÓN DEL GRÁFICO CON FONDO #EEEEEE ---
fig_scatter = px.scatter(
    df_jitter,
    x='Distancia en Km',
    y='Antigüedad',
    color='Perfil_Riesgo',
    size='Hit_target',
    facet_col='Riesgo_Carga',
    # Cambiamos a template 'plotly' o 'white' para que los ejes sean oscuros por defecto
    template='plotly_white',
    size_max=12,
    color_discrete_map={
        'Perfil Estable': "#3A93D4",
        'Saturado Logístico': '#F1C40F',
        'En desarrollo operativo': "#DB3434",
        'Perfil de Inestabilidad': "#17A11E"
    }
)

# --- PERSONALIZACIÓN DEL FONDO Y TEXTOS ---
fig_scatter.update_layout(
    paper_bgcolor="#EEEEEE",  # Fondo exterior
    plot_bgcolor="#EEEEEE",   # Fondo del área del gráfico
    font_color="#222222",      # Texto en gris muy oscuro para contraste
    margin=dict(t=100, b=100),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="right",
        x=1,
        title_text=""
    )
)

# Ajuste de ejes para que se vean bien sobre el gris claro
fig_scatter.update_xaxes(
    title_font=dict(size=18, color="#444444"),
    tickfont=dict(size=14, color="#444444"),
    gridcolor="white",  # Grillas blancas sobre fondo gris quedan muy elegantes
    linecolor="#444444",
    matches=None,
    showticklabels=True
)

fig_scatter.update_yaxes(
    title_font=dict(size=18, color="#444444"),
    tickfont=dict(size=14, color="#444444"),
    gridcolor="white",
    linecolor="#444444",
    matches=None,
    showticklabels=True
)

# Títulos de las columnas (facetas)
fig_scatter.for_each_annotation(lambda a: a.update(
    text=f"<b>{a.text.split('=')[-1]}</b>",
    font=dict(size=16, color="#222222")
))

# Eliminar bordes de los puntos para limpieza visual
fig_scatter.update_traces(marker=dict(line=dict(width=0), opacity=0.8))


st.plotly_chart(fig_scatter, width='stretch', key="scatter_claro")

# ==========================================================
# ⚡ UMBRALES TÉCNICOS DE GESTIÓN (VALORES VALIDADOS)
# ==========================================================
# ==========================================================
# ⚡ UMBRALES TÉCNICOS DE GESTIÓN (VALORES VALIDADOS)
# ==========================================================
with st.expander("Ver Umbrales de Carga detectados por el Modelo"):

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success("""
        **Carga Óptima**
        **261 u. (Promedio)**
        *Punto de máxima eficiencia operativa sin riesgo de burnout.*
        """)
    with c2:
        st.info("""
        **Carga Ligera**
        **Hasta 250 u.**
        *Perfil en formación o baja demanda. Espacio para crecimiento.*
        """)

    with c3:
        st.warning("""
        **Saturación Crítica**
        **> 338 u.**
        *Riesgo inminente de fatiga, errores y baja en el rendimiento.*
        """)


# ==========================================================
# 🔍 DETALLE ESTADÍSTICO DE LOS CLUSTERS
# ==========================================================
with st.expander("Ver Caracterización Detallada de Perfiles (Medias IA)"):
    st.write("A continuación se presentan los valores promedio que definen matemáticamente a cada grupo identificado por la IA:")

    # 1. Agrupamos por Perfil y calculamos las medias
    df_detalle_clusters = df_empleados.groupby('Perfil_Riesgo').agg({
        'ID': 'count',
        'Work_load_Average_day': 'mean',
        'Distance_Residence_Work': 'mean',
        'Service_time': 'mean',
        'Hit_target': 'mean'
    }).rename(columns={'ID': 'Nº Empleados'})

    # 2. Formateamos la tabla para que sea más legible
    # Redondeamos a 1 decimal y añadimos estilos
    df_formatted = df_detalle_clusters.style.format({
        'Work_load_Average_day': '{:.1f} unidades',
        'Distance_Residence_Work': '{:.1f} km',
        'Service_time': '{:.1f} años',
        'Hit_target': '{:.1f}%'
        # Resalta el rendimiento
    }).background_gradient(cmap='Greens', subset=['Hit_target'])

    st.dataframe(df_formatted, width='stretch')

    st.info("""
    **Interpretación Técnica:**
    * **Nº Empleados:** Tamaño del segmento.
    * **Carga Laboral:** Esfuerzo promedio diario del grupo.
    * **Distancia:** Fatiga logística promedio.
    * **Antigüedad:** Nivel de experiencia del grupo.
    * **Hit Target:** Rendimiento real alcanzado por cada perfil.
    """)

# ==========================================================
# 🛰️ PANEL DE CONTROL IA: IMPORTANCIA Y SIMULACIÓN
# ==========================================================
st.divider()
st.header("Escenarios IA")

# 1. DEFINICIÓN DE DICCIONARIOS (Prevenir NameError)
mapeo_nombres_espanol = {
    'Service_time': 'Antigüedad (Años)',
    'Distance_Residence_Work': 'Distancia (Km)',
    'Work_load_Average_day': 'Carga Laboral'
}

# 2. COLUMNAS PRINCIPALES (IMPORTANCIA IZQUIERDA | SIMULADOR DERECHA)
col_imp_left, col_sim_right = st.columns([1, 1], gap="large")

# --- COLUMNA IZQUIERDA: IMPORTANCIA (BARRAS DELGADAS) ---
with col_imp_left:
    st.subheader("Peso de las Variables")

    # Cálculo de Importancia (Varianza de Centroides)
    columnas_ia = ['Service_time',
                   'Distance_Residence_Work', 'Work_load_Average_day']
    centros = pd.DataFrame(kmeans.cluster_centers_, columns=columnas_ia)
    importancia = centros.var().sort_values(ascending=True)

    df_importancia = pd.DataFrame({
        'Variable': [mapeo_nombres_espanol.get(col, col) for col in importancia.index],
        'Importancia': importancia.values
    })
    df_importancia['Relativa'] = (
        df_importancia['Importancia'] / df_importancia['Importancia'].sum()) * 100

    # Gráfico con bargap alto y width bajo para barras muy finas
    fig_imp = px.bar(
        df_importancia, x='Relativa', y='Variable', orientation='h',
        text=df_importancia['Relativa'].apply(lambda x: f'{x:.1f}%'),
        template='plotly_white'
    )

    fig_imp.update_layout(
        paper_bgcolor="#EEEEEE",
        plot_bgcolor="#EEEEEE",
        font_color="#222222",
        xaxis=dict(showgrid=False, range=[
                   0, 140], showticklabels=False, title=""),

        # --- AQUÍ AUMENTAMOS EL TAMAÑO DEL EJE Y ---
        yaxis=dict(
            title="",
            # Tamaño de los nombres
            tickfont=dict(size=16, color="#222222", family="Arial")
        ),

        margin=dict(l=10, r=10, t=30, b=10),
        height=320,
        bargap=0.7
    )

    fig_imp.update_traces(
        marker_color="#12661C",
        textposition='outside',
        # --- AQUÍ AUMENTAMOS EL TAMAÑO DEL TEXTO DE LAS BARRAS ---
        textfont=dict(size=15, color="#12661C"),
        width=0.2
    )

    st.plotly_chart(fig_imp, width='stretch', key="imp_izq_final")
# --- COLUMNA DERECHA: SIMULADOR ACTUALIZADO ---
with col_sim_right:
    st.subheader("Simulador de Impacto")

    porcentaje_reduccion = st.select_slider(
        "Reducción de carga laboral (%):",
        options=[0, 5, 10, 15, 20, 25, 30, 40, 50],
        value=10,
        key="slider_num_v2"
    )

    # 1. Lógica de Simulación
    df_simulado = df_empleados.copy()
    df_simulado['Work_load_Average_day'] = df_simulado['Work_load_Average_day'] * \
        (1 - porcentaje_reduccion / 100)

    # 2. Re-escalado y Predicción con el modelo IA
    X_sim_scaled = scaler.transform(
        df_simulado[['Service_time', 'Distance_Residence_Work', 'Work_load_Average_day']])
    preds_simuladas = kmeans.predict(X_sim_scaled)

    # 3. Mapeo dinámico (Usamos el diccionario automático que creamos antes)
    df_simulado['Perfil_Simulado'] = [
        mapeo_dinamico.get(str(p)) for p in preds_simuladas]

    # 4. Cálculo de métricas comparativas
    actual = df_empleados['Perfil_Riesgo'].value_counts()
    simulado = df_simulado['Perfil_Simulado'].value_counts()
    total_n = len(df_empleados)

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    def metrica_compacta(col, perfil, color_tipo):
        n_act = actual.get(perfil, 0)
        n_sim = simulado.get(perfil, 0)
        pct_sim = (n_sim / total_n) * 100
        diff = n_sim - n_act

        # Mostramos cantidad + porcentaje y la diferencia (delta)
        col.metric(
            label=perfil,
            value=f"{n_sim} ({pct_sim:.1f}%)",
            delta=f"{diff} emp.",
            delta_color="normal" if color_tipo == "pos" else "inverse"
        )

    # 5. Renderizado de las 4 métricas del simulador
    with c1:
        metrica_compacta(st, "Perfil Estable", "pos")
    with c2:
        metrica_compacta(st, "Saturado Logístico", "neg")
    with c3:
        metrica_compacta(st, "En desarrollo operativo", "neg")
    with c4:
        metrica_compacta(st, "Perfil de Inestabilidad", "neg")

# --- MENSAJE DE IMPACTO FINAL ---
# Sumamos los dos grupos de mayor riesgo para ver la mejora total
riesgo_antes = actual.get('Saturado Logístico', 0) + \
    actual.get('Perfil de Inestabilidad', 0)
riesgo_despues = simulado.get(
    'Saturado Logístico', 0) + simulado.get('Perfil de Inestabilidad', 0)
total_mejora = riesgo_antes - riesgo_despues

if total_mejora > 0:
    st.success(
        f"**Escenario validado:** Reducir la carga un {porcentaje_reduccion}% permite que **{total_mejora} colaboradores** salgan de perfiles críticos hacia zonas de mayor estabilidad.")
elif total_mejora == 0 and porcentaje_reduccion > 0:
    st.info("ℹLa reducción aplicada no es suficiente para mover a los empleados de cluster. Prueba con un porcentaje mayor.")


with col_sim_right:
    st.subheader("Simulador de Impacto Real")

    porcentaje_reduccion = st.select_slider(
        "Reducción de carga laboral (%):",
        options=[0, 5, 10, 15, 20, 25, 30, 40, 50],
        value=10,
        key="slider_sim_v3"
    )

    # 1. Aplicamos reducción de carga SIN cambiar el perfil original
    df_simulado = df_empleados.copy()
    df_simulado['Work_load_Simulada'] = df_simulado['Work_load_Average_day'] * \
        (1 - porcentaje_reduccion / 100)

    # 2. Definimos quién sale de la zona crítica (> 338 u.)
    # Un empleado se considera "recuperado" si su carga original era > 338 y la nueva es <= 338
    umbral_critico = 338

    recuperados = df_simulado[
        (df_simulado['Work_load_Average_day'] > umbral_critico) &
        (df_simulado['Work_load_Simulada'] <= umbral_critico)
    ]

    total_recuperados = len(recuperados)

    # 3. Visualización de métricas de impacto
    c1, c2 = st.columns(2)

    # Calculamos cuántos quedan aún en riesgo
    quedan_en_riesgo = len(
        df_simulado[df_simulado['Work_load_Simulada'] > umbral_critico])
    riesgo_inicial = len(
        df_empleados[df_empleados['Work_load_Average_day'] > umbral_critico])

    with c1:
        st.metric("Empleados Recuperados",
                  f"{total_recuperados}", delta=f"{total_recuperados} estables")

    with c2:
        st.metric("Permanecen en Riesgo", f"{quedan_en_riesgo}",
                  delta=f"-{total_recuperados}", delta_color="normal")

    st.progress(1 - (quedan_en_riesgo / riesgo_inicial)
                if riesgo_inicial > 0 else 1.0)

# --- MENSAJE DE IMPACTO FINAL ---
if total_recuperados > 0:
    st.success(
        f"✅ **Impacto Validado:** Al reducir la carga un {porcentaje_reduccion}%, logramos que **{total_recuperados} colaboradores** abandonen la zona de saturación crítica (> 338u) manteniendo su perfil profesional intacto.")

    if total_recuperados > 0:
        with st.expander("Ver detalle de empleados recuperados"):
            st.write(recuperados[['ID', 'Perfil_Riesgo',
                     'Work_load_Average_day', 'Work_load_Simulada']])
else:
    st.info("ℹ️ Esta reducción aún no es suficiente para sacar a ningún empleado de la zona de saturación crítica.")
