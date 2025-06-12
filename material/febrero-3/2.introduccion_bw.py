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
# # Introduccion a brightway - pt. 1
#
# En esta seccion hablaremos de los conceptos fundamentales de brigthway. Es importante aclarar que toda esta informacion esta disponible en linea en la pagina de documentacion:
#
# https://docs.brightway.dev/en/latest/index.html

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
print('bw2data version: ',bd.__version__)
print('bw2io version: ',bi.__version__)
print('bw2calc version: ',bc.__version__)


# %% [markdown]
# Este tutorial ha sido generado con las siguientes versiones:
# bw2data version:  (4, 4, 4)
# bw2io version:  0.9.9
# bw2calc version:  2.0.2
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

# %% [markdown]
# En caso desees realizar una copia del proyecto actual, puedes utilizar `bw2data.projects.copy_project`

# %%
bd.projects.copy_project(new_name="nuevo_proyecto_2")

# %%
# Verificamos
bd.projects

# %% [markdown]
# En caso desees eliminar un proyecto, puedes utilizar la funcion `bw2data.projects.delete_dir`

# %%
# El argumento `delete_dir` es booleano e indica
# si tambien se desea eliminar la carpeta que contiene los datos del proyecto.
bd.projects.delete_project(name='nuevo_proyecto', delete_dir=True)


# %% [markdown]
# 🚧 **Manos a la obra**:
# - Crea un nuevo proyecto llamado 'peru25'
# - Crea una copia de 'peru25' llamada 'peru25-prueba'
# - Activa el proyecto 'peru25'
#

# %%
# Inserta el codigo aqui

# %% [markdown]
# ## Creando una nueva biosfera
# Brightway esta fuertemente (pero no estrictamente) ligado a los modelos y esquemas utilizados por ecoinvent.
# Por esto, los metodos de impacto y flujos ambientales (biosfera) son aquellos proporcionados por ecoinvent a traves de su servicio ecoquery.
# Aunque los metodos son desarrollados por grupos de investigacion independientes, ecoinvent los centraliza y modifica a fin de que sean compatibles y listos para conectarse con su base de datos.

# %% [markdown]
# <div class="alert alert-block alert-danger">
# Versiones anteriores de este notebook sugerian el uso de bw2io.bw2setup().
# Este metodo ha sido eliminado (deprecated) y la manera standard de instalar una biosfera es la que se indica en las siguientes celdas.
# </div>

# %% [markdown]
# La forma mas actual de crear una biosfera es mediante el paquete bw2io.
# Para ello utilizaremos el modulo bw2io.remote:

# %%
bi.remote.get_projects() # Este metodo buscara distintas versiones de biosfera listas para ser utilizadas.

# %% [markdown]
# Elije la base de datos mas conveniente para tu proyecto. Recuerda que distintas versiones de ecoinvent son compatibles con version especificas de biosfera.
# Recuerda que `ecoinvent-3.8-biosphere` es compatible con versiones de ecoinvent menores a 3.8.
#
# En este ejemplo instalaremos la version 3.10 (que es compatible con versiones mayores a 3.10).
# Utilizaremos el metodo bw2io.remote.install_projects, que toma como argumentos el nombre de la version de biosfera desea, el nombre del proyecto, y el argumento `overwrite_existing=True`, que indica que bw2io puede sobre escribir en caso que el proyecto ya exista.
# %%
bi.remote.install_projects('ecoinvent-3.10-biosphere','nuevo_proyecto', overwrite_existing=True)
# %% [markdown]
# <div class="alert alert-block alert-info">
# Diferentes grupos de investigacion actualizan constanmente distintos metodos de impacto. Por ello, cada version de biosfera puede presentar nuevos metodos de impacto.
# </div>

# %% [markdown]
# La biosfera esta ahora almacenada en una base de datos. En la jerga de brightway, una base de datos no es mas que un objeto que permite acceder a los nodos contenidos en este. Podemos ver las bases de datos contenidas en este proyecto de la siguiente manera:

# %%
# La base de datos 'ecoinvent-3.10-biosphere' tiene ese nombre por defecto.
bd.databases

# %% [markdown]
# Podemos manipular la biosfera asignando la base de datos a una nueva variable `biosfera` de la siguiente forma:

# %%
biosfera = bd.Database('ecoinvent-3.10-biosphere')

# %% [markdown]
# Por ahora no exploraremos a detalle esta base de datos. Si embargo utilizaremos la funcion `random` que nos permite muestrear un nodo aleatorio para ver de que trata el contenido.

# %%
# Ejecuta esta celda multiples veces y veras que siempre tienes respuestas diferentes.
biosfera.random()


# %% [markdown]
# De manera similar, podemos explorar los diferentes metodos que fueron instalados previamente. En brightway, los metodos presentados como una combinacion de tres elementos:
# > (<'Nombre del metodo'>, <'Categoria de impacto'>, <'Indicador'>)

# %%
bd.methods
# Hay que 'convertir' bw2data.methods en una lista para poder ver todos los metodos disponibles
# list(bd.methods)

# %% [markdown]
# Buscar un metodo en una lista tan extensa puede ser muy problematico.
# Para facilitar la busqueda de una metodo en especifico, podemos utilizar el poder de python.

# %%
# bw2data.methods es un objeto sobre el que se puede iterar
# Por ejemplo, busquemos un metodo relacionado con el cambio climatico
for nombre, categoria, indicator in bd.methods:
    if categoria == 'climate change':
        print((nombre, categoria, indicator))

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Realiza un filtrado para saber que metodos cuentan con la categoria de impacto 'acidification' y con el indicador 'acidification potential (AP)'.
# > Ayuda: Puedes utilizar el operador logico `and` dentro de la condicion `if`.
#

# %%
# Inserta tu codigo aqui

# %% [markdown]
# ## Manipular bases de datos
# En la seccion anterior, dejamos que `bw2io.bw2setup` cree una base de datos nueva llamada 'ecoinvent-3.10-biosphere'. Una base de datos contiene nodos, ya sean de la biosfera o de la tecnosfera. En otros software, los nodos de la biosfera suelen ser llamados Elementary Flow y los de la tecnosfera, Activities. En brightway, se utiliza el concepto general de 'nodo' a cualquier elemento que este contenido en una base de datos. Este puede ser un flujo elemental o un actividad de la tecnosfera.
#
# En este sentido, una nueva base de datos puede ser creada de la siguiente manera:
#

# %%
# Primero, se asigna una instancia de base de datos a una variable
# Esta informacion esta en la memoria de la computadora pero no grabado en el disco
mi_db = bd.Database('mi_base_de_datos')

#Segundo, se registra la base de datos para que sea grabada en el disco
mi_db.register()

# %% [markdown]
# Podemos verificar que ahora existen 2 bases de datos, la biosfera creada por `bw2io` y `mi_base_de_datos`, creada por nosotros.

# %%
bd.databases

# %% [markdown]
# En muchas situaciones, puede que sea necesario realizar una copia de una base de datos. Esto puede realizarse de la siguiente forma:

# %%
new_database = bd.Database('ecoinvent-3.10-biosphere').copy('new_biosphere')

# %% [markdown]
# Para borrar una base de datos, solo hay que imaginar que `bd.databases` tiene las mismas propiedades que un diccionario de python y utilizar `del`
#

# %%
if 'new_biosphere' in bd.databases:
    del bd.databases['new_biosphere']

# %% [markdown]
# ## Manipular Actividades
# Una de las funcionalidades de brightway mas importantes es la creacion de actividades (o nodos, en general).
# Se puede crear una actividad utilizando la funcion `new_activity`, perteneciente a los objetos de base de datos. En este caso, se puede indicar cualquier cantidad de argumentos pero incluyendo SIEMPRE los argumentos `code`, `name`, `unit` y `location`. Estos cuatro argumentos son obligatorios porque es lo minimo requerido para tener actividades unicas.
#

# %%
bd.projects

# %%
if 'mi_base_de_datos' in bd.databases: # es una buena practica para siempre comenzar en un lienzo en blanco
    del bd.databases['mi_base_de_datos']



# %%
db = bd.Database('mi_base_de_datos')
db.register()
activity_ejemplo = db.new_activity(code='codigo-unico', name='nombre-no-unico', unit='unidad', location='PE')
activity_ejemplo.save() # Este paso es SIEMPRE necesario para grabar la informacion en el disco
print(list(db))

# %% [markdown]
# Esta actividad se encuentra ahora registrada en el disco y puede accederse utilizando su identificar `code` y la funcion `get`. Es importante aclarar que `code` es unico solo para la base de datos.

# %%
actividad = db.get('codigo-unico')
print(actividad)

# %% [markdown]
# Informacion mas detallada de esta actividad puede verse con la funcion `as_dict`, que devuelve un diccionary de python.

# %%
actividad.as_dict()

# %% [markdown]
# En caso deseado, la actividad puede borrarse utilizando la funcion `delete`.
#

# %%
actividad.delete()

# %% [markdown]
# Siguiendo el ejemplo de la bicicleta, podemos ta crear todos los nodos (tecnosfera y biosfera).

# %%
data = {
    'code': 'bici',
    'name': 'produccion bici',
    'location': 'PE',
    'unit': 'piece'
}

bike = db.new_activity(**data)
bike.save()

data = {
    'code': 'CF',
    'name': 'carbon fibre',
    'unit': 'kilogram',
    'location': 'CN'
}

cf = db.new_activity(**data)
cf.save()

ng = db.new_activity(
    name="Nat Gas",
    code='ng',
    location='NO',
    unit='MJ'
)

ng.save()

co2 = bd.Database('ecoinvent-3.10-biosphere').new_activity(
    name="Carbon Dioxide",
    code='co2',
    categories=('air',),
    type='emission',
)

co2.save()

print(list(db))


# %%
# n2o.delete()

# %%
# # En caso quiera borrar todos los nodos de `db`
# co2.delete()
# for i in db:
    # i.delete()

# %% [markdown]
# Ya contamos con todos los nodos, sin embargo estos estan desconectados.
# Sin una red conectada, no podemos hacer el computo del ACV. Para esto, tenemos que crear las 'conexiones/interacciones' entre todos los nodos. En brightway, estos se llaman 'exchanges', y pueden ser creados de la siguiente manera con la funcion `new_exchange`:
#

# %%

bike.new_exchange(
    amount=2.5,
    type='technosphere',
    input=cf
).save()

cf.new_exchange(
    amount=237.3,
    type='technosphere',
    input=ng,
).save()

ng.new_exchange(
    amount=26.6 / 237,
    type='biosphere',
    input=co2,
).save()

# %% [markdown]
# Podemos ahora crear un metodo nuevo que solo tenga un factor de caracterizacion:

# %%
ipcc = bd.Method(('IPCC',)) # Si no existe, lo crea
ipcc.write([
    (co2.key, {'amount': 1}),
])

# %% [markdown]
# El paquete `bw2calc` contiene las herramientas para realizar los calculos, como la clase LCA:

# %%
lca = bc.LCA({bike:1},method=('IPCC',)) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida
lca.lcia() # Calcula los impactos
print("El impacto es: ", lca.score)

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Se ha descubierto que la produccion de fibra de carbono emite 0.23 kg de monoxido dinitrogeno al aire $N_{2}O$ por cada kilogramo de fibra de carbono producido.
# - El factor de caracterizacion del $N_{2}O$ es 276.9
# - En cuanto ha aumentado el impacto ?


# %%
