Proyecto 1 - Programación 4
Consulta de propiedades edáficas de suelos en Colombia

Descripción:
Aplicación de consola en Python dividida en módulos (api, ui y main) que lee la base de datos de suelos desde Excel, filtra por departamento, municipio, cultivo y cantidad de registros, y muestra en tablas tanto las filas consultadas como la mediana de pH, Fósforo (P) y Potasio (K).

Mejora en el filtrado (búsqueda sin tildes):
En el archivo Excel varios municipios y cultivos están guardados con tildes (por ejemplo: Plátano, Medellín, Cúcuta o Café). Para evitar que el usuario tenga que escribir las tildes exactas al buscar, en el módulo api/consultas.py se implementó una función con la librería nativa "unicodedata" que normaliza el texto y elimina los acentos tanto en la entrada del usuario como en las columnas del DataFrame, pasando todo a mayúsculas antes de comparar.

Cómo ejecutar el proyecto:
1. Instalar las librerías necesarias:
   pip install -r requerimientos.txt

2. Ejecutar el archivo principal:
   python main.py