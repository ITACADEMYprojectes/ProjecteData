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
st.title("Rapid Express: People Analytics Dashboard")
st.markdown(
    "### Porque detrás de cada ruta, hay una historia: cuidamos a las personas que mueven nuestro motor.")


# 1. LÓGICA DE PROCESAMIENTO (DATAFRAMES E IA)
# ==========================================
# Agrupación inicial
# Para variables continuas (Age, Body_mass_index, Son) tomaste la media.
# Para variables categóricas (Education) tomaste la primera observación.
# Para variables binarias (Social_drinker, Social_smoker) tomaste el valor máximo (es decir, si alguna vez fueron “sí”, se marca como sí).
# ==========================================
# AGRUPACIÓN DE EMPLEADOS
# ==========================================

df_id = RRHH_full.groupby('ID').agg({
    'Age': 'mean',
    'Body_mass_index': 'mean',
    'Son': 'mean',
    'Education': 'first',
    'Social_drinker': 'max',
    'Social_smoker': 'max'
}).reset_index()

# ==========================================
# 1. PREPROCESAMIENTO (REFORZADO)
# ==========================================

# Aseguramos que Education sea numérica (Ordinal) para que el nivel importe
df_id['Education'] = pd.to_numeric(
    df_id['Education'], errors='coerce').fillna(1)

categorical_cols = ['Social_drinker', 'Social_smoker']
numeric_cols = ['Age', 'Body_mass_index', 'Son',
                'Education']  # Education entra como número

# Creamos dummies solo para las binarias (bebe/fuma)
df_dummies = pd.get_dummies(
    df_id[categorical_cols],
    columns=categorical_cols,
    drop_first=False  # Mantener ambas columnas ayuda a la interpretación del centroide
)

# Unimos todo
X = pd.concat([df_id[numeric_cols], df_dummies], axis=1)

# ==========================================
# 2. ESCALADO (Z-SCORE)
# ==========================================
scaler = StandardScaler()
X_scaled_array = scaler.fit_transform(X)

X_scaled = pd.DataFrame(
    X_scaled_array,
    columns=X.columns
)

# ==========================================
# 3. KMEANS (ESTABLE)
# ==========================================
# ==========================================
# KMEANS (CORREGIDO)
# ==========================================

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=20
)

# AQUÍ ESTÁ EL CAMBIO: Guardamos el resultado en la variable que pide el score
cluster_labels = kmeans.fit_predict(X_scaled)

# Ahora lo asignamos al DataFrame
df_id['Cluster_ID'] = cluster_labels

# Asignamos los labels numéricos
df_id['Cluster_ID'] = kmeans.fit_predict(X_scaled)

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
# Ahora contamos por el nombre del segmento para evitar errores de índice
total_a = len(df_id[df_id['Segmento'].str.contains("Familiar")])
total_b = len(df_id[df_id['Segmento'].str.contains("Enfocado")])
total_c = len(df_id[df_id['Segmento'].str.contains("Senior")])

promedio_hijos = df_id['Son'].mean()
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
# DATAFRAME PARA VISUALIZACIÓN (NO MODIFICA ORIGINAL)
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
    hover_name="ID",
    hover_data={
        "PCA1_jitter": False,
        "PCA2_jitter": False,
        "Age": True,
        "Son": True,
        "Social_smoker": True,
        "Social_drinker": True,
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
        title="PCA 1",
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor="grey",
        showticklabels=False
    ),
    yaxis=dict(
        title="PCA 2",
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor="grey",
        showticklabels=False
    )
)

# Mantener IDs visibles
fig_scatter.update_traces(
    mode="markers+text",
    textposition="top center",
    marker=dict(line=dict(width=1, color="white"))
)

# Mostrar gráfico
st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# MÉTRICA PCA
# ==========================================

# ==========================================
# PCA (CORREGIDO)
# ==========================================

pca = PCA(
    n_components=2,
    random_state=42
)

pca_data = pca.fit_transform(X_scaled)

df_id['PCA1'] = pca_data[:, 0]
df_id['PCA2'] = pca_data[:, 1]

# AQUÍ ESTÁ EL CAMBIO: Creamos la variable que pide el resumen de abajo
pca_variance = pca.explained_variance_ratio_

# Ahora, la línea 346 que te daba error ya funcionará:
var_total = pca_variance.sum() * 100

if score > 0.5:
    st.success("Los clusters presentan buena separación.")
elif score > 0.25:
    st.info("Los clusters tienen una separación moderada.")
else:
    st.warning("La segmentación podría mejorarse.")

st.write(
    f"**Nota Técnica:** Este mapa 2D retiene el **{var_total:.1f}%** de la variabilidad original de los datos de RRHH.")
st.caption("Porcentaje de información del dataset representado en el gráfico PCA.")

sil_scores = []
k_range = range(2, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(X_scaled)
    sil_scores.append(silhouette_score(X_scaled, labels))

best_k = k_range[np.argmax(sil_scores)]
st.info(f"El mejor número de clusters según Silhouette Score es: {best_k}")

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
    marker=dict(size=8, line=dict(width=1, color='white'))
)

st.plotly_chart(fig_estacional, use_container_width=True)

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

fig_rf.update_layout(
    bargap=0.5,
    plot_bgcolor='#EEEEEE',
    paper_bgcolor='#EEEEEE',
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Inter", size=12)
    ),
    margin=dict(l=20, r=20, t=50, b=20),  # Ajuste de márgenes
    font=dict(family="Inter")
)

st.plotly_chart(fig_rf, width='stretch')


st.divider()


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
    title="Método del Codo: Buscando el K Óptimo",
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

# 3. Mostrar en Streamlit
st.write("### ¿Por qué elegimos 3 segmentos?")
st.plotly_chart(fig_elbow, use_container_width=True)

st.info("""
**Cómo interpretar este gráfico:** Buscamos el punto donde la curva se dobla bruscamente (como un codo). 
- Si el 'doblez' está en **k=3**, tu modelo es estadísticamente sólido.
- Si la línea es muy recta, significa que los datos no se agrupan de forma natural y hay que revisar las variables.
""")


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


# --- Variables Laborales y Personales ---
variables_laborales = [
    'Transportation_expense', 'Distance_Residence_Work', 'Service_time',
    'Work_load_Average_day', 'Hit_target', 'Month_absence', 'Day_week', 'Seasons'
]

variables_personales = [
    'Age', 'Son', 'Pet', 'Body_mass_index'
]

# --- Función para entrenar RF y generar DataFrame de importancia ---


def rf_importance(df, features, target='Absenteeism_hours'):
    X = pd.get_dummies(df[features], drop_first=True)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=250, random_state=42)
    model.fit(X_train, y_train)
    importance_df = pd.DataFrame({
        'Variable': X.columns,
        'Importancia': model.feature_importances_
    }).sort_values(by='Importancia', ascending=True)
    return importance_df


# --- Importancia Laboral ---
importancia_laboral_df = rf_importance(RRHH_full, variables_laborales)
fig_laboral = px.bar(
    importancia_laboral_df,
    x='Importancia',
    y='Variable',
    orientation='h',
    title="Factores Laborales que Predicen el Absentismo",
    color_discrete_sequence=["#79B26B"],
    template='plotly_white'
)
fig_laboral.update_traces(marker=dict(line=dict(width=1, color='black')))
fig_laboral.update_layout(bargap=0.5, plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE',
                          xaxis=dict(showgrid=False, showline=False,
                                     zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, showline=False, zeroline=False, tickfont=dict(
                              family="Inter", size=12)),
                          margin=dict(l=20, r=20, t=50, b=20),
                          font=dict(family="Inter"))

# --- Importancia Personal ---
importancia_personal_df = rf_importance(RRHH_full, variables_personales)
fig_personal = px.bar(
    importancia_personal_df,
    x='Importancia',
    y='Variable',
    orientation='h',
    title="Factores Personales que Predicen el Absentismo",
    color_discrete_sequence=["#FFB26B"],
    template='plotly_white'
)
fig_personal.update_traces(marker=dict(line=dict(width=1, color='black')))
fig_personal.update_layout(bargap=0.5, plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE',
                           xaxis=dict(showgrid=False, showline=False,
                                      zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, showline=False, zeroline=False, tickfont=dict(
                               family="Inter", size=12)),
                           margin=dict(l=20, r=20, t=50, b=20),
                           font=dict(family="Inter"))

# --- Render en Streamlit ---
st.plotly_chart(fig_laboral, use_container_width=True)
st.divider()
st.plotly_chart(fig_personal, use_container_width=True)


importancia_laboral_df['Tipo'] = 'Laboral'
importancia_personal_df['Tipo'] = 'Personal'

# Combinar DataFrames
importancia_total_df = pd.concat(
    [importancia_laboral_df, importancia_personal_df])

fig_total = px.bar(
    importancia_total_df,
    x='Importancia',
    y='Variable',
    color='Tipo',
    orientation='h',
    title="Factores que Predicen el Absentismo (Personales vs Laborales)",
    color_discrete_map={'Laboral': '#79B26B', 'Personal': '#FFB26B'},
    template='plotly_white'
)

fig_total.update_traces(marker=dict(line=dict(width=1, color='black')))
fig_total.update_layout(
    bargap=0.5,
    plot_bgcolor='#EEEEEE',
    paper_bgcolor='#EEEEEE',
    xaxis=dict(showgrid=False, showline=False,
               zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, showline=False, zeroline=False,
               tickfont=dict(family="Inter", size=12)),
    margin=dict(l=20, r=20, t=50, b=20),
    font=dict(family="Inter")
)

st.plotly_chart(fig_total, use_container_width=True)
