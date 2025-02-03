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
# # COMENCEMOS!
# Si ejecutas este notebook utilizando los servidores de DDS, no olvides configurar el entorno
# y selecciona el siguiente: 
#
# Hacer click en Python 3 [conda env ...]
# ![image info](./pictures/acceso1.png)
#
# Seleccionar el entorno: summerschoolperu
# ![image info](./pictures/acceso2.png)

# %% [markdown]
# # Estructura computacional del ACV
#
#
#
# Este sistema de ecuaciones puede resolverse fácilmente utilizando cualquier paquete o
# libreria que permita invertir la matriz $A$.
# Para demostrar este ejemplo, utilizaremos el paquete [numpy](https://numpy.org/), que 
# permite manipular arreglos multidimensionales de manera rapida y eficiente.
# Como podran ver mas adelante, brightway ha sido construido utilizando numpy como motor
# de calculo.
#
# Recordemos que necesitamos construir las siguientes matrices: 
# $$ A = \begin{bmatrix} -2 & 100  \\\ 10 & 0  \end{bmatrix}$$
#
# $$ B = \begin{bmatrix} 1 & 10  \\\ 0.1 & 2 \\\ 0 & -50   \end{bmatrix}$$
#
# $$ y = \begin{bmatrix} 0 \\\ 1 \end{bmatrix}$$ 
#
# $$ Q = \begin{bmatrix} 0 & 1 & 0  \\\ 1 & 0.1 & 0 \\\ 0 & 0 & -15 \end{bmatrix}$$
#
# ... y tambien necesitamos obtener $s$, $h$ y $g$ utilizando estas ecuaciones:
# $$ s = A^{-1}f $$
#
# $$ g = Bs $$
#
# $$ h = Qg $$
# %%
# Importamos las librerias numpy and scipy. 
# OJO: Aun no utilizamos brightway, este es tan solo un ejemplo.
from rich import print # Solo para mejorar la grafica de las impresiones
import numpy as np
import scipy as sp

A = np.array([ [-2, 100 ], [ 10,0] ])
B = np.array([[1,10],[0.1,2],[0,-50]])
f = np.array([0,1])
Q = np.array([[0,1,0], [1,0.1,0],[0,0,-15]])

# Verificamos
print(f"Las dimensiones de A son: {A.shape}")
print("A: ", A)
# %%

A_inv = np.linalg.inv(A) # np.lingalg.inv permite invertir matrices 
s = A_inv.dot(f) 
g = B.dot(s)

print("s: ", s)
print("g: ", g)
# %% [markdown]
# Con los vectores $s$, y $g$ calculados, es posible obtener el vector $h$ que representa el vector de impactos ambientales.
# Podriamos decir que este es el `final` del flujo metodologico en el analisis de ciclo de vida.
# %%

h = Q.dot(g) 
print("h: ", h)

# %%
# Celda comentada para que el resto ejecute.

# %% [markdown]
# # Introduccion a Brightway
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion: 
#
# https://docs.brightway.dev/en/latest/index.html

# %% [markdown]
# ## Modulos

# %%

# %% [markdown]
# ## Configura tu proyecto brightway
# Debido al gran tamano de las bases de datos utilizadas en ACV, brightway require grabar cierta informacion en disco. 
# Por esta razon, cada vez que se crea un proyecto nuevo es necesario configurarlo.
#
# El primer paso consiste en importar las dependencias necesarias:
# %%
import bw2data as bd
import bw2io as bi
import bw2calc as bc
from rich import print

# %% [markdown]
# Podemos ver la lista de proyectos existentes utilizando el modulo `bw2data`:

# %%
bd.projects

# %% [markdown]
# Cualquier entorno de ejecucion de python que importe al paquete `bw2data` estara configurado con el proyecto ``default`` por defecto.
#

# %%
bd.projects.current

# %% [markdown]
# En caso que desee cambiar de proyecto, la funcion `bw2data.set_current(<el-nombre-de-tu-proyecto>)` permite elegir un proyecto existente. En el caso que el proyecto no exista, esta funcion creara un proyecto nuevo.

# %%
bd.projects.set_current('nuevo_proyecto')

# %%
# Puede ver que 'nuevo_proyecto' aparece ahora en la lista de proyectos.
bd.projects

# %% [markdown]
# <div class="alert alert-block alert-warning">
# ⚠️ Todas las modificaciones realizadas por los distintos modulos de brightway se realizan EXCLUSIVAMENTE en el contexto del proyecto. Por ello es importante verificar que trabaja con el proyecto correcto.
# </div>
#

# %% [markdown]
# Para guardar registro de los proyectos y distinta informacion necesaria, `bw2data` grabara algunos archivos en el disco. Pueden existir casos (muy excepcionales) en los que necesites acceder a estos archivos de manera directa. Para ello puedes localizarlos utilizando la funcion `bw2data.projects.dir`

# %%
bd.projects.dir

# %% [markdown]
# ## Manipular Actividades

# %%

# %% [markdown]
# ## Configurando tu proyecto brigthway
#
#
#
# ## Exportar bases de datos y proyectos
# ## Importar bases de datos comerciales
# ## Importar bases de datos privadas
# ## Calcular un ACV
#
#
#
#
#
#
#
#

