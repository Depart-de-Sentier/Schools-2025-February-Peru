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
# # Introduccion
#
# <div class="alert alert-block alert-warning">
# ⚠️ Este curso no pretende ser intensivo ni rigurozo en lo que refiere al ACV como metodologia y se parte del supuesto que los conceptos son conocidos por los estudiantes. Por esta razon, es posible que algunas definiciones sean genericas ya que solo se utilizan para dar contexto a las explicaciones. 
# </div>
#
#
#

# %% [markdown]
# En el ACV, buscamos entender los impactos ambientales en todo el ciclo de vida de un producto o servicio. Sin embargo, para poder estimar este impacto, es importante primero entender como es el sistema en el producto o servicio opera. Dicho sistema se representa con un modelo de cadena de suministro que contiene las multiples etapas del ciclo de vida del producto. Imaginemos que deseamos calcular el impacto de ciclo de vida de la produccion de una bicicleta en un sistema extremadamente reducido. En este caso, podemos interpretar el grafo (coleccion de nodos y aristas) como: 
# > *Para producir 1 bicicleta, se necesita 2.5kg de fibra de carbono, y a su vez, para producir 1 kg de fibra de carbono se requiere 237 MJ de gas natural y se emitiran 26.6kg de CO2 en el proceso.*
#
# ![image info](./pictures/simple-graph.png)
#
# En la figura, los nodos circulares representan actividades que ocurren en la tecnosfera, mientras que los nodos rectangulares representan elementos de la biosfera. Como mencionamos anteriormente, el primer paso es saber cuantas unidades de cada producto de la tecnosfera se produciran a causa de la demanda de bicicletas, y, en consecuencia, cuantas emisiones se genraron en el proceso. Esta informacion da paso a finalmente estimar los impactos totales en todo el ciclo de vida. 
#
# La manera mas comun para afrontar este problema de forma matematica es mediante un problema de algebra lineal, y esto esta claramente presentado y discutido en [este libro](https://link.springer.com/book/10.1007/978-94-015-9900-9). En este enfoque, la tecnosfera se representa como una matriz en la que cada columna contiene la 'receta' para producir una unidad de una determinado producto (matriz $A_{productos \times actividades}$). La biosfera se presenta como otra matriz de dimensiones $B_{flujos \times actividades}$, y la demanda (unidad funcional) se presenta como un vector $f_{productos}$. Adicional a esto, una matriz $Q_{impactos \times flujos}$ se introduce para convertir los flujos en impactos a traves de factores de caracterizacion.
# En esta representacion, los valores positivos indican 'salida', mientras que los valores negativos indican 'consumo'.
#
# $$ A = \begin{bmatrix} 1 & 0 & 0  \\\ -237 & 1 & 0 \\\ 0 & -2.5 & 1  \end{bmatrix}$$
#
# $$ B = \begin{bmatrix} 1 & 26.6 & 0  \end{bmatrix}$$
#
# $$ y = \begin{bmatrix} 0 \\\ 1 \\\ 0 \end{bmatrix}$$ 
#
# $$ Q = \begin{bmatrix} 1 \end{bmatrix}$$
#
# El problema ahora es obtener un vector de abastecimiento $s_{productos}$, que representa los flujos en toda la tecnosfera a causa de la demanda de $f$. Por suerte este problema fue resuelto en el campo del Input-Output hace muchos anos y solo hace falta resolver la siguiente ecuacion:
#
# $$ s = A^{-1}f $$
#
# Un vez obtenido $s$, podremos saber todos los flujos ambientales obteniendo $ g = Bs $ y todos los impactos resolviendo $h =Qg$
#
# Este sistema de ecuaciones puede resolverse fácilmente utilizando cualquier paquete o
# libreria que permita invertir la matriz $A$.
# Para demostrar este ejemplo, utilizaremos el paquete [numpy](https://numpy.org/), que 
# permite manipular arreglos multidimensionales de manera rapida y eficiente.
# Como podran ver mas adelante, brightway ha sido construido utilizando numpy como motor
# de calculo.
#
# %%
# Importamos las librerias numpy and scipy. 
# OJO: Aun no utilizamos brightway, este es tan solo un ejemplo.
from rich import print # Solo para mejorar la grafica de las impresiones
import numpy as np
import scipy as sp

A = np.array([ [1, 0,0 ], [-237,1,0] , [0,-2.5,1]])
B = np.array([[0,26.6,0]])
f = np.array([0,1,0])
Q = np.array([1])

# Verificamos
print(f"Las dimensiones de A son: {A.shape}")
print("A: \n", A)
# %%
__global___

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
