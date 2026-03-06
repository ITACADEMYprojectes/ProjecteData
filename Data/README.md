## Data Understanding

El conjunto de datos analizado corresponde a registros de ausentismo laboral.  
Cada fila representa una instancia de ausencia registrada para un empleado, y las columnas recogen tanto variables demográficas y de salud como información relacionada con el contexto laboral y personal del trabajador.

En cuanto a la estructura del dataset, se identifican variables de distinta naturaleza. Por un lado, variables de identificación y contexto temporal, como el ID del empleado, el mes y el día de la semana en que se produjo la ausencia, y la estación del año. Por otro lado, se incluyen variables relacionadas con el entorno laboral, como la razón de la ausencia, el tiempo de servicio, la carga de trabajo promedio diaria y si el empleado alcanzó o no el objetivo fijado.

El dataset también recoge información sobre el perfil personal y de salud del empleado: la edad, el peso, la altura y el índice de masa corporal, así como variables sobre hábitos y estilo de vida como el consumo de alcohol, el tabaquismo y la tenencia de mascotas. Adicionalmente, se incluye el nivel educativo y el número de hijos, junto con la distancia desde el domicilio al lugar de trabajo y el gasto en transporte.

La variable objetivo del análisis es el tiempo de ausentismo en horas, que cuantifica el número de horas de ausencia registradas en cada incidencia. Los valores de esta variable presentan una distribución variada, con registros que van desde 0 horas hasta casos excepcionales que alcanzan las 40 horas, lo que sugiere la presencia de valores atípicos que deberán ser considerados en fases posteriores del análisis.

Tras una inspección inicial del dataset, se confirmó que el conjunto de datos cuenta con 740 registros y 21 variables, sin valores ausentes en ninguna de ellas, lo cual representa una ventaja importante de cara al procesamiento posterior. No obstante, se detectaron algunas inconsistencias en el formato de ciertas variables que requirieron correcciones para garantizar una interpretación correcta de los datos. Asimismo, algunas variables que estaban codificadas como números representan en realidad categorías sin orden jerárquico, por lo que fueron tratadas como tal. Estas correcciones se aplicaron como paso previo al análisis, con el objetivo de asegurar la calidad y fiabilidad de los resultados obtenidos.
