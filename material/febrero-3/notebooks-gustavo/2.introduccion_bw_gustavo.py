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
bd.projects.set_current('peru25')

# %%
bd.projects.copy_project(new_name='peru25-prueba')

# %%
bd.projects.set_current('peru25')

# %% [markdown]
# ## Creando una nueva biosfera
# Brightway esta fuertemente (pero no estrictamente) ligado a los modelos y esquemas utilizados por ecoinvent.
# Por esto, los metodos de impacto y flujos ambientales (biosfera) son aquellos proporcionados por ecoinvent a traves de su servicio ecoquery. 
# Aunque los metodos son desarrollados por grupos de investigacion independientes, ecoinvent los centraliza y modifica a fin de que sean compatibles y listos para conectarse con su base de datos.

# %% [markdown]
# Lo primero que haremos sera crear una biosfera (a la ecoinvent) y los multiples metodos de impacto disponibles por defecto.
# Para esto, el paquete `bw2io` cuenta con una funcion llama `bw2setup`, asi:

# %%
bi.bw2setup()

# %% [markdown]
# El mensaje de la celda de arriba nos dice que `bw2io` ha creado una base de datos llamada 'biosphere3' que contiene 4709 nodos (flujos ambientales).
# Adicionalmente, 762 metodos de impacto nuevos han sido creados.
#

# %% [markdown]
# <div class="alert alert-block alert-info">
# Diferentes grupos de investigacion actualizan constanmente distintos metodos de impacto. Por ello, cada version de `bw2io` puede presentar nuevos metodos de impacto. Puedes ver la version de bw2io asi: `bw2io.__version__`
# </div>

# %% [markdown]
# La biosfera esta ahora almacenada en una base de datos. En la jerga de brightway, una base de datos no es mas que un objeto que permite acceder a los nodos contenidos en este. Podemos ver las bases de datos contenidas en este proyecto de la siguiente manera:

# %%
# La base de datos 'biosphere3' tiene ese nombre por defecto. 
bd.databases

# %% [markdown]
# Podemos manipular la biosfera asignando la base de datos a una nueva variable `biosfera` de la siguiente forma:

# %%
biosfera = bd.Database('biosphere3')

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
list(bd.methods) 

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
# bw2data.methods es un objeto sobre el que se puede iterar
# Por ejemplo, busquemos un metodo relacionado con el cambio climatico
for nombre, categoria, indicator in bd.methods:
    if categoria == 'acidification' and indicator=='acidification potential (AP)':
        print((nombre, categoria, indicator))

# %%
# Inserta tu codigo aqui
# bw2data.methods es un objeto sobre el que se puede iterar
# Por ejemplo, busquemos un metodo relacionado con el cambio climatico
for nombre, categoria, indicator in bd.methods:
    if 'IPCC' in nombre:
        print((nombre, categoria, indicator))

# %% [markdown]
# ## Manipular bases de datos
# En la seccion anterior, dejamos que `bw2io.bw2setup` cree una base de datos nueva llamada 'biosphere3'. Una base de datos contiene nodos, ya sean de la biosfera o de la tecnosfera. En otros software, los nodos de la biosfera suelen ser llamados Elementary Flow y los de la tecnosfera, Activities. En brightway, se utiliza el concepto general de 'nodo' a cualquier elemento que este contenido en una base de datos. Este puede ser un flujo elemental o un actividad de la tecnosfera.
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
new_database = bd.Database('biosphere3').copy('new_biosphere')

# %%
bd.databases

# %% [markdown]
# Para borrar una base de datos, solo hay que imaginar que `bd.databases` tiene las mismas propiedades que un diccionario de python y utilizar `del`
#

# %%
if 'new_biosphere' in bd.databases:
    del bd.databases['new_biosphere']

# %%
bd.databases

# %% [markdown]
# ## Manipular Actividades
# Una de las funcionalidades de brightway mas importantes es la creacion de actividades (o nodos, en general).
# Se puede crear una actividad utilizando la funcion `new_activity`, perteneciente a los objetos de base de datos. En este caso, se puede indicar cualquier cantidad de argumentos pero incluyendo SIEMPRE los argumentos `code`, `name`, `unit` y `location`. Estos cuatro argumentos son obligatorios porque es lo minimo requerido para tener actividades unicas. 
#

# %%
bd.projects.current

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

co2 = bd.Database('biosphere3').new_activity(
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
co2.delete()
for i in db:
    i.delete()

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

cf.new_exchange(
    amount=26.6 / 237, 
    type='biosphere',
    input=co2,
).save()

# %% [markdown]
# Podemos ahora crear un metodo nuevo que solo tenga un factor de caracterizacion:

# %%
# for i in db:
#     print(i.as_dict())

# %%
mi_metodo = bd.Method(('dummy',)) # Si no existe, lo crea
mi_metodo.write([
    (co2.key, {'amount': 1}),
])

# %% [markdown]
# El paquete `bw2calc` contiene las herramientas para realizar los calculos, como la clase LCA:

# %%
lca = bc.LCA({bike:1},method=('dummy',)) # Instancia la clase
lca.lci() # calcula el inventario de ciclo de vida
lca.lcia() # Calcula los impactos 
print("El impacto es: ", lca.score)

# %% [markdown]
# 🚧 **Manos a la obra**:
# - Se ha descubierto que la produccion de fibra de carbono emite 0.23 kg de monoxido dinitrogeno al aire $N_{2}O$ por cada kilogramo de fibra de carbono producido.
# - El factor de caracterizacion del $N_{2}O$ es 276.9
# - En cuanto ha aumentado el impacto ?  


# %%
# 1 Crear nodo de biosfera n2o
n2o = bd.Database('biosphere3').new_activity(
    name="monoxido dinitrogeno", 
    code='n2o', 
    categories=('air',),
    type='emission',
).save()

# %%
n2o = bd.Database('biosphere3').get('n2o')
n2o

# %%
# 2 Crear factor de caracterizacion de n2o
mi_metodo = bd.Method(('dummy',)) # Si no existe, lo crea
mi_metodo.write([
    (n2o.key, {'amount': 276.9}),
])

# %%
# 3 Conectar cf con n2o
cf.new_exchange(
    amount=0.23,
    type='biosphere',
    input=n2o
).save()

# %%
lca_2 = bc.LCA({bike:1},method=('dummy',)) # Instancia la clase
lca_2.lci() # calcula el inventario de ciclo de vida
lca_2.lcia() # Calcula los impactos 
print("El impacto de lca es: ", lca.score)
print("El impacto de lca_2 es: ", lca_2.score)

# %%
