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
# # Introduccion a brightway - pt. 3
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion: 
#
# https://docs.brightway.dev/en/latest/index.html

# %% [markdown]
# ## Explorando las matrices
# Ahora que sabemos como crear un actividad y metodos desde cero. Podemos concentrarnos en manipular las actividades que estan presentes en ecoinvent.
# Para esta parte usaremos un proyecto que hemos preparado para ustedes que contiene una biosfera y tecnosfera compatible con ecoinvent v3.9

# %%
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print


# %%
# Run this if you want a clean start
# if 'peru25-ei-3.9.1-cutoff' in bd.projects:
    # bd.projects.delete_project('peru25-ei-3.9.1-cutoff',delete_dir=True)

# %%
# bi.restore_project_directory('/media/ei391/brightway2-project-peru25-ei-3.9.1-cutoff-backup.tar.gz') # Este archivo contiene el proyecto
bd.projects.set_current('peru25-ei-3.9.1-cutoff')

# %%
# Tenemos dos bases de datos
bd.databases

# %%
# seleccionamos la base de datos ecoinvent y una actividad que tomaremos de ejemplo
ei = bd.Database("ecoinvent-3.9.1-cutoff")
harina = ei.search('fishmeal PE 65-67')
harina

# %%
print(harina[0].as_dict())

# %%
print(harina[1].as_dict())

# %%
# Elegimos un metodo que ya esta instalado y hace un LCA pero nos detenemos en la etapa de LCI
method=('IPCC 2021', 'climate change', 'global warming potential (GWP100)')
lca = bc.LCA({harina[0]:1},method=method) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida


# %%
# Recordemos que ecoinvent tiene 21238 actividades
# Entonces que dimensiones deberia tener la matriz de la tecnosfera?
lca.technosphere_matrix.toarray()

# %%
# Que dimensiones deberia tener el vector s?
lca.supply_array

# %%
# Si quisiera saber cuanto de 'anchoveta pescada en embarcaciones de madera' 
# se requiere en TOTAL para producir 1 kg de harina de pescado...
anchoveta = ei.search('anchovy PE wooden')[0]
anchoveta

# %%
# el lca.activity_dict me permite ubicar una actividad en la matriz.
lca.supply_array[
            lca.activity_dict[
                            anchoveta.id
                                ]
            ]

# %%
# Ahora continuamos con el LCIA
lca.lcia() # Calcula los impactos 
print("El impacto es: ", lca.score) 

# %% [markdown]
# ## Analisis de contribuciones
# Para entender las distintas contribuciones, tenemos que seguir utilizando el objeto LCA.
# Este objeto mantiene los resultados del ACV en memoria

# %% [markdown]
# ### Procesos mas importantes
# Para listar los procesos que generan mas impactos utilizaremos el paquete `bw2analyzer` y `pandas`.

# %%
import pandas as pd
import bw2analyzer as ba
ba.ContributionAnalysis().annotated_top_processes(lca=lca) # dificil de visulizar
# ba.ContributionAnalysis.annotated_top_processes

# %%
pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_processes(lca=lca)],
    columns=["score", "quantity", "name"]
)

# %% [markdown]
# ### Emisiones mas importantes
# De manera similar, podemos obtener el ranking de flujos ambiental que generan mayores impactos

# %%
import pandas as pd
import bw2analyzer as ba
pd.DataFrame(
    [(x, y, z["name"]) for x, y, z in ba.ContributionAnalysis().annotated_top_emissions(lca=lca)],
    columns=["score", "quantity", "name"]
)


# %% [markdown]
# La importancia de las emisiones en el impacto tiene que ver con la cantidad y con los factores de caracterizacion. 
# Podemos listar estos factores para revisarlos

# %%
for key, cf in bd.Method(method).load():
    # print(key, cf)
    print(bd.get_node(id=key), "CF: ",cf)
    

# %% [markdown]
# ## Analisis de incertidumbre
# Realizar simulaciones de Monte Carlo es tan facil que requiere modificar una sola linea de la clase LCA.

# %%
lca = bc.LCA(
    {harina[0]:1},
    method=method,
    use_distributions=True # Esto es nuevo
) # Instancia la clase

# El objeto LCA es ahora un 'generator'.
# Es decir que podemos iterarlo las veces que necesitemos



# %%
# Avanzamos un paso
next(lca)

results= []
# iteramos 50 veces, es decir muestreamos 100 veces.
for i in range(50):
    lca.lci()
    lca.lcia()
    results.append(lca.score)
    next(lca)

# %%
# Tenemos una lista de resultados 
# que, en promedio deberia aproximarse a 0.44
results

# %%
# Podemos utilizar el paquete `seaborn` para visualizar la dispersion de los impactos
import seaborn as sns
sns.histplot(results)

# %%
