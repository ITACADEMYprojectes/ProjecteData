# Justificación Técnica

# Técnica Elegida 
Analisis exploratória descriptiva

# **1) ¿Por qué elegiste esta técnica de análisis y no otra?**  

Elegimos un enfoque **exploratorio descriptivo** porque el objetivo de esta fase del proyecto era **comprender la estructura del dataset crudo**, identificar problemas de calidad y detectar patrones iniciales antes de aplicar cualquier modelo o técnica avanzada.

En el EDA utilizamos:

- **resúmenes estadísticos básicos** (`describe()`, medianas, rangos)  
- **visualizaciones exploratorias** (histogramas, boxplots, scatterplots)  
- **matriz de correlación de Pearson**  
- **detección visual de outliers**

Estas técnicas fueron elegidas porque:

- El dataset contiene **variables numéricas y categóricas sin limpiar**, por lo que métodos más complejos (regresiones, clustering, modelos predictivos) no serían válidos en esta etapa.  
- El objetivo era **diagnosticar el estado real de los datos**, no modelar.  
- Las técnicas descriptivas permiten detectar rápidamente:
  - sesgos en la distribución (como el right-skew del absentismo)  
  - valores atípicos extremos  
  - correlaciones operativas relevantes  
  - errores de tipado (como `Work_load_Average_day` en VARCHAR)  
- Son métodos robustos, transparentes y fáciles de interpretar para RRHH y Dirección.

En resumen: **estas técnicas eran las más adecuadas para un dataset crudo y para un objetivo exploratorio**, permitiendo fundamentar la necesidad del Data Cleaning posterior.

---

# **2) ¿Qué supuestos tiene la técnica que usaste y cómo verificaste que tus datos los cumplían?**  

Aunque el EDA es una técnica flexible, sí existen supuestos implícitos que verificamos:

### **a) Supuesto de integridad estructural**  
- Verificamos duplicados.  
- Revisamos tipos de datos (`info()`).  
- Confirmamos que no había valores nulos en el dataset crudo.  
- Detectamos columnas mal tipadas (Work_load_Average_day, Education, Son, etc.).

### **b) Supuesto de distribución adecuada para análisis descriptivo**  
- Usamos histogramas para verificar la forma de la distribución.  
- Identificamos sesgo positivo fuerte en Absentismo (right-skew).  
- Detectamos outliers visualmente mediante boxplots.

### **c) Supuesto de independencia entre observaciones**  
- Cada fila representa un empleado distinto → no hay dependencia temporal ni repetición sistemática.

### **d) Supuesto para correlación de Pearson**  
Pearson requiere:

- variables numéricas  
- relaciones lineales aproximadas  
- ausencia de codificación errónea  

Verificamos:

- `select_dtypes(include=[np.number])` para asegurar que solo entraran variables válidas  
- inspección visual de scatterplots (Age vs Hit_target)  
- detección de columnas excluidas automáticamente por estar en formato texto

### **e) Supuesto de tamaño de muestra suficiente**  
- 740 registros → más que suficiente para análisis descriptivo y correlacional.

---

# **3) ¿Qué limitaciones tiene esta técnica y cómo podrían afectar a tus conclusiones?**  

### **Limitaciones del EDA aplicado**

1. **No permite inferir causalidad**  
   Las correlaciones detectadas (por ejemplo, Age–Service_time) no implican causa-efecto.

2. **Variables clave quedaron fuera del análisis numérico**  
   Debido a errores de tipado en la base de datos (VARCHAR con comas), columnas como:
   - Work_load_Average_day  
   - Education  
   - Son  
   fueron excluidas automáticamente del heatmap.

   Esto limita la capacidad de analizar relaciones importantes.

3. **Presencia de outliers extremos**  
   Los valores de absentismo superiores a 100–120 horas distorsionan la media y pueden sesgar interpretaciones.

4. **Distribuciones no normales**  
   El absentismo está fuertemente sesgado → la media no es representativa.

5. **EDA no incluye segmentación avanzada**  
   No se aplicaron técnicas como clustering, PCA o modelos predictivos.

---

### **Cómo podrían afectar a las conclusiones**

- La media de absentismo puede estar inflada por pocos casos extremos.  
- La correlación entre variables puede estar incompleta por la ausencia de columnas mal tipadas.  
- No podemos afirmar causalidad, solo asociación.  
- Algunas conclusiones pueden cambiar después del Data Cleaning.

---

### **Cómo mejorar el análisis en el futuro**

- Repetir el EDA con variables corregidas.  
- Aplicar modelos estadísticos:
  - regresión lineal o logística  
  - árboles de decisión  
  - clustering de perfiles de absentismo  
- Analizar absentismo por segmentos (edad, servicio, cargas familiares).  
- Incorporar datos longitudinales si la empresa los tiene.

