# CONSIDERACIONES PARA ANTES DEL CURSO

Por favor revisa las siguientes consideraciones antes de tu llegada al curso. 
Si encuentras algún problema, no dudes en contactarnos que nosotros intentaremos 
resolverlo para que todo esté listo en tu computadora.

## TRABAJO EN SERVIDORES REMOTOS + COMPUTADORAS PERSONALES

En la primera etapa del curso utilizaremos servidores remotos para ejecutar los 
ejercicios.
Esto nos permitirá que todos utilicemos el mismo entorno de computación bajo el 
control completo de los instructores.
Esto ayudará a que solo nos concentremos en aprender los conceptos básicos sin 
preocuparnos en las configuraciones y particularidades de cada computadora.

Una vez interiorizados los conceptos fundamentales, la segunda parte del curso se 
realizará en las computadoras personales de cada alumno.
Esto permitirá que cada uno utilice su propia computadora y se familiarice con la 
manera de utilizar brightway dentro y fuera de las aulas.

> **_NOTA:_** Recomendamos contar con al menos 8 GB de RAM en la computadora personal. \
> Algunos calculos pueden ser muy intensivos en cuestión de uso de memoria. 

## TECNOLOGÍAS FUNDAMENTALES: ANACONDA y GIT

Los participantes deberán descargar e instalar una distribución de anaconda para 
gestionar los entornos de python. 
De igual forma, cada computadora debe tener GIT instalado, que será el Sistema de 
Control de Versiones (VCS en inglés) que utilizaremos.


1. Instalar GIT
- Descargar el instalador de GIT adecuado para tu sistema operativo  (https://git-scm.com/downloads)
Instalar GIT
- Clonar el repositorio del curso ejecutando este código en un terminal (en Windows puedes abrir Git BASH):

    ```bash
    git clone https://github.com/Depart-de-Sentier/Schools-2025-February-Peru
    cd Schools-2025-February-Peru
    ```
- ¡Ya tienes GIT listo en tu computadora y todos los documentos requeridos para el curso!
- Puedes encontrar más información respecto a GIT aquí: https://www.freecodecamp.org/espanol/news/aprende-los-conceptos-basicos-de-git-en-menos-de-10-minutos/

1. Instalar anaconda
- Descarga el instalador adecuado para tu Sistema Operativo (https://www.anaconda.com/download/success)
- Instala anaconda
- Imaginemos que deseamos crear un entorno de python nuevo llamado `mi-entorno`. Este se puede crear ejecutando los siguientes comandos en una terminal (e.g., utiliza `Anaconda prompt` en windows):

    ```console
    conda create -n mi-entorno python==3.10
    conda activate mi-entorno 
    ```
- Ya tienes un entorno de python EXCLUSIVO y AISLADO que ejecutara python en version 3.10.
- Si deseas aprender mas o por que esto es importante, consulta aquí: https://www.toolify.ai/es/ai-news-es/gua-para-principiantes-de-anaconda-en-linux-y-windows-tutorial-de-entornos-de-trabajo-en-python-977984

## ACERCA DE ACTIVITY-BROWSER Y BRIGHTWAY

- Para crear un entorno dedicado exclusivamente a activity-browser en el contexto de este curso puedes utilizar el archivo `environment_ab.yaml` que se encuentra en la carpeta `material/environments/`.
- Este puede crearse ejecutando el siguiente código en una terminal (e.g., utiliza `Anaconda prompt` en windows).
    
    ```console
    conda env create -f materials/environments/environment_ab.yaml
    conda activate activity-browser 
    ```
- Activity-browser puede ejecutarse abriendo una terminal y ejecutando este código:
    
    ```console
    conda activate activity-browser 
    activity-browser
    ```
- Para instalar un entorno dedicado exclusivamente a brightway, hay seguir las mismas instrucciones cambiando el archivo `environment_ab.yaml` por `environment_bw.yaml`, asi:

    ```console
    conda env create -f environment_bw.yaml
    conda activate bw25 
    ```

## ACERCA DE ECOINVENT

En el curso utilizaremos la base de datos de ecoinvent 3.10. 
Esta base de datos es comercial asi que no puede ser compartida en este repositorio.
Al inicio del curso explicaremos como será la manera de manejar estos datos.

## ACERCA DE LOS EDITORES DE TEXTO

A excepción de las sesiones con activity-browser, la mayor parte del curso requerirá que los alumnos programen código.
En este sentido, en teoría, solo necesitamos un editor de texto para modificar los archivos que contienen el código, y un terminal para ejecutarlos.
En la práctica, esto puede ser un poco intimidante para aquellos que comienzan en el mundo de la programación o de brigthway.
Por esta razón, el curso utilizará *jupyter notebook* como tecnología fundamental para escribir el código y ejecutarlo al mismo tiempo. 

No debes preocuparte por instalar esta tecnología, ya que la instalación de anaconda ya la incluye.
Si deseas saber más acerca de jupyter notebook, consulta aquí: https://ebac.mx/blog/jupyter-notebook 


