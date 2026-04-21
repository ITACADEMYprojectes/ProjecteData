# Results Carpeta para almacenar resultados y salidas del proyecto.

=====================================================
## Fede – Familiarización del Dataset

### Objetivo
Realizar una primera exploración del dataset para comprender su estructura, calidad de datos y variables clave, como base para el análisis de campañas de marketing bancario.

---

### Metodología
Se ha utilizado MySQL para llevar a cabo una exploración inicial del dataset mediante:

- Revisión de la estructura de la tabla  
- Análisis del volumen de datos  
- Identificación de la variable objetivo  
- Exploración de variables clave como el número de contactos (`campaign`)  
- Cálculo de la tasa de éxito en función del número de contactos  
- Revisión de valores nulos  
- Obtención de estadísticas básicas  

---

### Hallazgos Iniciales

- La variable objetivo identificada es `deposit`, que indica si el cliente acepta la campaña  
- La variable `campaign` representa el número de contactos realizados  
- Se observa que la tasa de éxito no sigue una relación lineal con el número de contactos  
- Los clientes con más intentos de contacto pueden presentar menor probabilidad de conversión  

---

### Evidencias

### Estructura de la tabla
![Estructura](familiarizacion_fede/estructura_tabla.png)

### Número total de registros
![Registros](familiarizacion_fede/registros_totales.png)

### Vista rápida de los datos
![Vista](familiarizacion_fede/vista_rapida_datos.png)

### Distribución de la variable objetivo
![Objetivo](familiarizacion_fede/distribucion_variable_objetivo.png)

### Distribución de contactos
![Contactos](familiarizacion_fede/distribucion_contactos.png)

### Relación contactos vs tasa de éxito
![Tasa](familiarizacion_fede/contactos_tasa_exito.png)

### Valores nulos
![Nulos](familiarizacion_fede/valores_nulos.png)

============================================================
