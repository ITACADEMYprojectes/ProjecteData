**Limpieza de datos**



***Faltan datos en alguna celda?***

* Todos los campos contienen 11162 valores, a excepción de los campos 'marital' -11157, 5 menos, ***imputar unknown***- y 'education' -11155, 7 menos, ***imputar unknown***-. 
* Supone un total de 12 registros a los que les falta algún valor -0.10% del total de registros-.
* ¿Los eliminamos? ***No, imputamos valores 'unknown***'





***Columnas que no aporten información para el análisis que estamos realizando?***

* Columnas que no contienen información relevante para nuestros análisis? En un principio, todas parecen aportar información susceptible de poder ser consultada y/o utilizada.
* Columnas con información redundante? No hay.
* Campos categóricos con un único nivel? No hay, en todos ellos mínimo hay 2 niveles -o valores- diferentes.
* Campos numéricos con un único valor? No hay. La desviación standard de cada una de las columnas es diferente de 0.





***Filas repetidas?***

* No hay ningún registros que tenga todos los campos idénticos.





***Valores numéricos atípicos (outliers)?***

* AGE: existen registros con el campo 'age'=null. ¿Le asignamos la media resultante del resto de valores del propio campo 'age'? -la media es de 41.24 años-.El resto de valores están comprendidos entre 18 y el máximo 95, parecen asumibles. ***Imputar la media***.
* BALANCE: existen valores negativos y positivos. Parecen correctos.
* DAY: valores comprendido entre 1 y 31, son correctos.
* DURATION: no hay valores negativos. ¿Añadimos una columna convirtiendo los segundos a minutos? Lo dejamos en segundos.
* CAMPAIGN: la media está en 2.5 veces y hay valores por encima de las 10,20 hasta 63 veces, ¿parecen demasiadas llamadas para una misma campaña?
* PDAYS: parecen datos correctos, el máximo está en 854 días (<944 días que comprende desde mayo de 2008 hasta noviembre de 2010.
* PREVIOUS: parecen datos correctos.





***Errores tipográficos en variables categóricas?***

* JOB: No se repite ningún valor. Tan solo 'admin.' es el único abreviado. ***Lo convierto a 'administrative'***.
* MARITAL: No se repite ningún valor.
* EDUCATION:  No se repite ningún valor. Tan solo coincide la categoría 'unknown' con las de la descripción del data set.
* DEFAULT:  No se repite ningún valor.
* HOUSING:  No se repite ningún valor.
* LOAN:  No se repite ningún valor.
* CONTACT: No se repite ningún valor. Hay un valore que no consta en la descripción del data set; 'unknown': mail, carta?
* MONTH:  No se repite ningún valor.
* POUTCOME:  No se repite ningún valor. Hay dos valores que no constan en la descripción del data set; 'unknown': se lo está pensando? y 'other': el cliente contrato otro tipo de producto?
* DEPOSIT:  No se repite ningún valor.
