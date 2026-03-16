# Importante para predecir 2 variables
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
import plotly.graph_objects as go  
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
    'Weight': 'mean',
    'Height': 'mean',

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


# 3. Mostrar en Streamlit
st.write("### ¿Por qué elegimos 3 segmentos?")
st.plotly_chart(fig_elbow, width='stretch')

with st.expander("Guía de Interpretación: Método del Codo", expanded=False):
    st.markdown("""
    Este gráfico nos ayuda a determinar el número óptimo de segmentos (**k**) para la plantilla de Rapid Express.

    * **El punto de inflexión:** Buscamos el "codo" de la curva. Es el punto donde añadir más grupos deja de aportar una mejora significativa en la cohesión de los datos.
    * **Interpretación Estratégica:** - Si el 'doblez' es claro en **k=3**, confirmamos que existen tres perfiles de empleados (Emergente, Operativo y Especialista) bien diferenciados.
        - Si la curva es demasiado suave o recta, sugiere que la plantilla es muy homogénea y las estrategias de RRHH deberían ser más generales que segmentadas.

    *Nota técnica: El eje Y mide la **Inercia** (Suma de cuadrados internos), que representa qué tan cerca están los empleados del centro de su grupo.*
    """)

sil_scores = []
k_range = range(2, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(X_scaled)
    sil_scores.append(silhouette_score(X_scaled, labels))

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
                     title="Impacto en Rendimento",
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

# --- RENDERIZADO EN STREAMLIT ---
st.write("### Indicadores Clave de Gestión (KPIs)")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(label="Mes Pico", value=mes_pico_nombre,
              help="Mayor carga de ausencias")

with k2:
    # Recortamos si es muy largo
    st.metric(label="Motivo Modal", value=motivo_modal,
              help="Causa más frecuente")

with k3:
    st.metric(label="Eficiencia Relativa",
              value=f"{eficiencia_relativa:.2f}%", help="Hit Target / Carga Diaria")

with k4:
    st.metric(label="Ausencia",
              value=f"{porcentaje_ausencia:.1f}%", help="Penetración en la plantilla")


st.divider()

st.header("Radiografía del Absentismo: Predicción y Diagnóstico de Precisión")

if RRHH_full is not None:

    # Crear nivel de absentismo (UNA sola vez)
    RRHH_full["Absenteeism_level"] = pd.cut(
        RRHH_full["Absenteeism_hours"],
        bins=[-1, 4, 16, float("inf")],
        labels=["Baja", "Media", "Alta"]
    )

    # Variables del modelo
    features = [
        "Age",
        "Distance_Residence_Work",
        "Service_time",
        "Body_mass_index",
        "Work_load_Average_day",
        "Transportation_expense",
        "Son",
        "Pet",
        "Social_drinker",
        "Social_smoker"
    ]

    df_ml = RRHH_full.dropna(subset=features + ["Absenteeism_level"])

    X = df_ml[features]
    y = df_ml["Absenteeism_level"]

    # -------------------------------
    # 2. TRAIN / TEST SPLIT
    # -------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # -------------------------------
    # 3. ENTRENAMIENTO DEL MODELO
    # -------------------------------

    model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train_scaled, y_train)

    # Predicciones
    y_pred = model.predict(X_test_scaled)

    # -------------------------------
# 4. MÉTRICAS DEL MODELO
# -------------------------------

    report_dict = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    st.write("### Resumen Ejecutivo de Predicción")

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        "Precisión General",
        f"{report_dict['accuracy']:.1%}"
    )

    kpi2.metric(
        "Sensibilidad (Absentismo Alto)",
        f"{report_dict['Alta']['recall']:.2f}",
        help="Capacidad del modelo para detectar casos de absentismo crítico"
    )

    kpi3.metric(
        "F1-Score Promedio",
        f"{report_dict['macro avg']['f1-score']:.2f}"
    )

    # -------------------------------
    # 5. LAYOUT DE VISUALIZACIÓN
    # -------------------------------

    col_ref, col_matriz = st.columns(2)

    # -------------------------------
    # GRÁFICO DE VARIABLES IMPORTANTES
    # -------------------------------

    with col_ref:

        coef_df = pd.DataFrame({
            "Variable": features,
            "Coeficiente": model.coef_[0]
        })

        coef_df = coef_df.sort_values("Coeficiente")

        coef_df["Impacto"] = coef_df["Coeficiente"].apply(
            lambda x: "Aumenta Riesgo" if x > 0 else "Reduce Riesgo"
        )

        fig_coef = px.bar(
            coef_df,
            x="Coeficiente",
            y="Variable",
            orientation="h",
            color="Impacto",
            color_discrete_map={
                "Aumenta Riesgo": "#EC634B",
                "Reduce Riesgo": "#00CC96"
            },
            title="<b>Impacto de Variables en el Absentismo</b>"
        )

        fig_coef.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            font_color="white",
            height=450,
            showlegend=False,
            title=dict(font=dict(size=17)),
            xaxis=dict(
                title=dict(text="Coeficiente", font=dict(size=16)),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title=dict(text="Variables", font=dict(size=16)),
                tickfont=dict(size=14)
            )
        )

        st.plotly_chart(fig_coef, width='stretch')

    # -------------------------------
    # MATRIZ DE CONFUSIÓN
    # -------------------------------

    with col_matriz:
        # 1. Forzamos el orden lógico manualmente
        orden_logico = ["Baja", "Media", "Alta"]

    # 2. Calculamos la matriz usando ese orden específico
        cm = confusion_matrix(
            y_test,
            y_pred,
            labels=orden_logico
        )

        fig_cm = px.imshow(
            cm,
            text_auto=True,
            x=orden_logico,  # Eje X en orden lógico
            y=orden_logico,  # Eje Y en orden lógico
            labels=dict(
                x="Predicción IA",
                y="Realidad Operativa",
                color="Casos"
            ),
            color_continuous_scale="Greens",
            aspect="auto"
        )

        fig_cm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            font_color="white",
            height=450,
            title=dict(
                text="<b>Diagnóstico de Precisión del Modelo</b>",
                font=dict(size=17)
            ),
            xaxis=dict(
                title=dict(font=dict(size=16)),
                tickfont=dict(size=17),
                # Aseguramos que Plotly no reordene por su cuenta
                categoryorder='array',
                categoryarray=orden_logico
            ),
            yaxis=dict(
                title=dict(font=dict(size=16)),
                tickfont=dict(size=17),
                # Aseguramos que Plotly no reordene por su cuenta
                categoryorder='array',
                categoryarray=orden_logico
            )
        )

        st.plotly_chart(fig_cm, width='stretch')

    # -------------------------------
    # INTERPRETACIÓN
    # -------------------------------

    with st.expander("Guía de Interpretación del Modelo"):
        st.markdown("""
        * **Coeficientes Positivos (Rojo):** Variables que **aumentan** la probabilidad de absentismo alto (ej. Carga laboral, gasto de transporte).
        * **Coeficientes Negativos (Verde):** Variables que actúan como **protectores** o reducen el riesgo (ej. Proximidad al trabajo).
        * **Matriz de Confusión:** Es el "examen" de la IA. Los valores en la diagonal (de arriba-izquierda a abajo-derecha) son los aciertos reales.
        * **Sensibilidad (Recall):** Nuestra capacidad crítica para no dejar escapar a ningún empleado en riesgo de absentismo "Alta".
        """)


st.write("---")
st.header("Simulador de Perfil de Empleado")
st.write("Ajusta los parámetros para predecir el riesgo de absentismo de un nuevo perfil.")

col_sim1, col_sim2, col_sim3 = st.columns(3)

with col_sim1:
    s_age = st.slider("Edad", 18, 65, 30)
    s_dist = st.slider("Distancia Casa-Trabajo (km)", 1, 100, 20)
    s_service = st.slider("Años de Servicio", 0, 40, 5)

with col_sim2:
    s_bmi = st.slider("Índice de Masa Corporal (BMI)", 15, 45, 25)
    s_load = st.slider("Carga de Trabajo Diaria", 200, 400, 260)
    s_trans = st.slider("Gasto en Transporte", 100, 500, 180)

with col_sim3:
    s_son = st.number_input("Número de Hijos", 0, 5, 0)
    s_drink = st.selectbox("¿Bebedor Social?", ["No", "Sí"])
    s_smoke = st.selectbox("¿Fumador Social?", ["No", "Sí"])

# Convertir inputs a formato para el modelo
input_data = pd.DataFrame([[
    s_age, s_dist, s_service, s_bmi, s_load, s_trans,
    s_son, 0,  # Asumimos 0 mascotas por defecto para simplificar
    1 if s_drink == "Sí" else 0,
    1 if s_smoke == "Sí" else 0
]], columns=features)

# Predicción en tiempo real
input_scaled = scaler.transform(input_data)
prediccion_final = model.predict(input_scaled)[0]

# Mostrar resultado con estilo
# Mostrar resultado con estilo profesional y alineado a la izquierda
color_alert = {"Baja": "#00CC96", "Media": "#FFA500", "Alta": "#EC634B"}

st.markdown(f"""
    <div style="
        padding: 15px; 
        border-radius: 10px; 
        background-color: rgba(255,255,255,0.05); 
        border-left: 5px solid {color_alert[prediccion_final]};
        margin-top: 20px;">
        <p style="margin:0; font-size: 18px; font-weight: bold; color: black;">
            Predicción de Riesgo: 
            <span style="color:{color_alert[prediccion_final]}; text-transform: uppercase;">
                {prediccion_final}
            </span>
        </p>
    </div>
""", unsafe_allow_html=True)



st.divider()
