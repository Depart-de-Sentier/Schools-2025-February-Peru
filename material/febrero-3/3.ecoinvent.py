# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Introduccion a brightway - pt. 2
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion: 
#
# https://docs.brightway.dev/en/latest/index.html

# %% [markdown]
# ## Exportar bases de datos y proyectos
# En la seccion anterior aprendimos a crear bases de datos de manera automatica ('biosphere3') y de manera manual ('mi_base_de_datos'). 
# En situaciones convencionales, es normal que necesitemos compartir nuestros modelos de inventario, ya sea durante el trabajo colaborativo o para reportar nuestro trabajo a revisores, colegas y cualquier por razones de transparencia.
# Para esto, bw2io ofrece una serie de herramientas que pueden usarse para exportar los modelos en diferentes formatos. 
# Por un tema de popularidad, en esta seccion nos enfocaremos en 3 herramientas:
# - Exportar una base de datos a excel
# - Exportar una base de datos a csv (dataframe)
# - Exportar un proyecto como archivo comprimido de respaldo.

# %% [markdown]
# ###  Exportar a excel
# Brightway utiliza un template para leer y exportar bases de datos en formato excel. Es conveniente para distribuir versiones finales del inventario. No es muy bueno almacenando informacion anidad. No permite 'trackear' los cambios debido a que *.xlsx no es un formato de texto.

# %%
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print
# Primero que nada, verifiquen que esten en el proyecto adecuado
bd.projects.current

# %%
# Si no es el proyecto adecuado, ya saben que hacer
bd.projects.set_current('nuevo_proyecto_2')

 # %%
 # bi.export.excel.write_lci_excel??

# %%
# dirpath es el argumento que controla en que ubicacion se exportara el archivo. 
# En sistemas operativos tipo UNIX (Linux, MacOS), '.' significa 'aqui'.
directorio = bi.export.excel.write_lci_excel(database_name='mi_base_de_datos',dirpath='.')

# %% [markdown]
# ###  Exportar a csv
# Brightway permite convertir los nodos (actividades) y aristas (exchanges) en DataFrames de [pandas](https://pandas.pydata.org/).
# Un DataFrame es un estructura de datos tabular que es muy usada en analisis y ciencia de datos, y puede ser exportada directamente como archivo CSV.
#

# %%
db.nodes_to_dataframe() # Solo los nodos

# %%
db.edges_to_dataframe() # Solo aristas

# %%
# La funcion `to_csv` es propia de pandas, no de brightway
db.nodes_to_dataframe().to_csv('mis-nodos.csv')
db.edges_to_dataframe().to_csv('mis-aristas.csv')

# %% [markdown]
# ###  Exportar proyecto completo como backup
# La ultima opcion mas comun es la de exportar el proyecto completo en forma de archivo comprimido. Esto suele hacer cuando se desea guardar copias de todas las bases de datos de un proyecto. La desventaja es que el archivo resultado puede ser pesado y no es adecuado si no se tienen los permisos para compartir bases de datos comerciales.

# %%
bi.backup_project_directory('nuevo_proyecto_2',dir_backup='.')

# %% [markdown]
# ## Importar bases de datos privadas
# Esta seccion es una continuacion natural de la anterior ya que simplemente aprenderemos a importar los archivos que fueron exportados previamente. Asumiremos, nuevamente, que excel, csv, y backup.tar.gz son los unicos formatos que nos interesan.
#
# ### Importar un archivo de excel

# %%
importador = bi.ExcelImporter('lci-mi_base_de_datos.xlsx')
importador.apply_strategies()
importador.match_database(fields=('name', 'code', 'unit', 'location'))  # Conecta nodos del archivo excel
importador.match_database('biosphere3', fields=('name','unit','categories')) # Conecta nodos con la base de datos biosphere3
importador.statistics()
importador.write_excel()

# %%
importador.match_database('biosphere3', fields=('name','unit','categories')) # Conecta nodos con la base de datos biosphere3
importador.statistics()

# %%
importador.write_database()
bd.databases # La base de datos se ha importado correctamente

# %%

# %% [markdown]
# ### Repliquemos los resultados
# Ahora podemos 'simular' un ejercicio de reproducibilidad, y realizar el calculo de los impactos una vez mas.

# %%
db = bd.Database('mi_base_de_datos')
bicicleta = db.get('bici') # seleccionamos la actividad que tiene codigo 'bici', la definimos en la seccion anterior

# %%
lca = bc.LCA({bicicleta:1},method=('IPCC',)) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida
lca.lcia() # Calcula los impactos 
print("El impacto es: ", lca.score) # Es el mismo 🎉

# %% [markdown]
# ### Importar el backup del proyecto
# Este modalidad no require mucha explicacion: El proyecto se carga nuevamente. 

# %%
bi.restore_project_directory(
    'brightway2-project-nuevo_proyecto_2-backup03-February-2025-10-47AM.tar.gz',  # nombre del archivo, creado celdas arriba
    project_name='nuevo_nuevo_proyecto_2', # Se puede elegir un nombre nuevo para el proyecto
    overwrite_existing = False
    )

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Un colega ha encontrado un error en tu modelo. La cantidad de Gas Natural consumida por la fibra de carbono no es 237.3, sino 23.73
# - Descarga el archivo de excel `lci-mi_base_de_datos.xlsx` a tu computadora personal y modifica el valor manualmente.
# - Importa el archivo excel modificado y vuelve a calcular el ACV. Cuanto ha cambiado el impacto final?

# %%
# Tu codigo aqui

# %% [markdown]
# ## Importar bases de datos comerciales
# Hemos aprendido a construir un modelo de ACV desde cero y de forma manual. Aunque esto resulta bastante util, en la realidad solemos combinar nuestros datos con aquellos provenientes de bases de datos comerciales. En esta seccion nos enfocaremos en la base de datos ecoinvent (v3.9), que es una de las mas utilizadas en el sector. 
#
# En la actualidad hay dos maneras de importar los datos de ecoinvent en nuestro proyecto:
# - Leyendo los archivos ecospold2 crudos directamente del disco y convirtiendolos en una base de datos de brigthway.
# - Utilizando la herramienta `import_ecoinvent_release` que descarga la base de datos desde un servidor remoto.
#   
# ### Importando ecoinvent (crudo) desde el disco
#
# Para este caso, es necesario haber descargado ecoinvent. Ecoinvent es distribuido en formato comprimido 7z, y contiene todas las actividades en formato ecospold2 (algo similar a XML). `bw2io` tiene funciones disenadas para interpretar la informacion, verificar que los `exchanges` sean correctos, y que los nodos de la biosfera existan en la base de datos 'biosphere3'.
#

# %%
# Los archivos ecospold2 se ven asi:
# !ls /media/ei391/datasets | head

# %%
# Para importar, hay que seguir los siguentes pasos:
# 1. Leer los archivos XML e dejar que brigthway los interprete.
db = bi.SingleOutputEcospold2Importer(dirpath='/media/ei391/datasets',db_name='ecoinvent39')

# %%
# 2. Aplicar una serie de estrategias para asegurarse que no existe informacion corrupta y que la importacion es posible
db.apply_strategies()

# %%
# 3. Ecoinvent esta listo en la memoria pero aun no ha sido grabado en el disco. 
# Hay que grabarlo en el disco.
db.write_database()

# %% [markdown]
# Para verificar que ha sido importado correctamente, podemos repetir el ejercicio realizado con la base de datos 'biosphere3' de la anterior seccion.bd.databases

# %%
bd.databases # Lista de las bases de datos

# %%
ei = bd.Database('ecoinvent39')
len(ei) # Muestra la cantidad de elementos

# %% [markdown]
# ### Importando ecoinvent desde un servidor remoto
# Para este caso utilizamos la funcion `bw2io.import_ecoinvent_release` que se encarga de 1) instalar una biosfera, 2) instalar los metodos de impacto mas actuales, y 3) instalar la base de datos ecoinvent. 
# Como podran imaginar, requiere la autenticacion del usuario que debe poseer un cuenta de acceso ecoinvent

# %%
# bw2io.import_ecoinvent_release(
#     version="3.9" 
#     system_model="cutoff", # Otras opciones son: "consequential", "apos" y "EN15804"
#     username="xxxx", # Tu usuario
#     password="xxxx", # Tu clave
#     biosphere_name="biosphere" # Optional, puedes guardar la base de datos de la biosfera con otro nombre.
# )


# %%
seleccionado = ei.random() # Explora las actividades
print(seleccionado.as_dict())

# %% [markdown]
# Como pueden notar, el contenido de la actividad ecoinvent es bastante rica. Existen campos fuera de `name`, `code`,`location` y `unit` que son nuevos para nosotros, lo que demuestra que brightway es lo suficientemente flexible al definir una actividad. 
#
# Lo que vimos en la celda anterior describe a una actividad, pero aun no describe sus conexiones (`exchanges`). Para acceder a ellas, hay que utilizar las funciones `exchanges`, `technosphere` o `biosphere`, segun lo que se desee observar.

# %%
# `exchanges` retorna un objeto the brightway que no es nativo de python
type(seleccionado.exchanges())

# %%
# Si deseamos leerlo al estilo de una lista, hay que convertirlo en una lista.
print(list(seleccionado.exchanges()))

# %%
# Si deseamos solo la tecnosfera, usamos la funcion correspondiente
print(list(seleccionado.technosphere()))

# %% [markdown]
# La impresion realizada en la celda de arriba nos muestra la informacion necesaria para poder construir las matrices. Sin embargo, brightway nos permite manipular el `exchange` y acceder a su metadata.

# %%
# Seleccionamos el segundo `exchange`de la lista
exchange = list(seleccionado.technosphere())[1]
print(exchange.as_dict())

# %% [markdown]
# ## Opciones de busqueda
# Como podran imaginar, manipular una base de datos con tantas actividades (~21k) es bastante complicado. Podemos utilizar funciones nativas de python (list comprehension) para realizar una busqueda.

# %%
truck = [x for x in ei if x['name'] == 'transport, freight, lorry >32 metric ton, EURO5'][0]
truck

# %% [markdown]
# Esta manera de buscar es mas 'pythonic'. Sin embargo, tambien puedes usar el buscador de brightway a traves de la funcion `search`.

# %%
ei.search('transport, freight RoW >32 EURO5')

# %%
ei.search?? # La funcion search prioriza algunos campos para hacer el filtro.
