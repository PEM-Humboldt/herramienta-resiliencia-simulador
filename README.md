# Simulador del modelo de resiliencia

Implementación del modelo que hace parte de la herramienta de resiliencia.

> # **Uso de este simulador**
>
> Se recomienda seguir las instrucciones del [servidor de la herramienta de resiliencia](https://github.com/PEM-Humboldt/herramienta-resiliencia-servidor) para poner en marcha todos los componentes que requiere el simulador para su correcto funcionamiento.
>
> Se desaconceja el uso del simulador sin el servidor, pues requiere de muchos ajustes manuales para cada ejecución.
>
> Las instrucciones de este repositorio están orientadas para las personas que deseen modificar el funcionamiento del simulador y no necesiten cambiar los insumos para sus pruebas.

# Tabla de contenido

1. [Prerrequisitos](#prerrequisitos)
1. [Instalación de dependencias](#instalación)
1. [Preparación](#preparación)
    1. [Base de datos](#cargar-información-a-la-base-de-datos)
    1. [Parámetros](#archivo-de-parámetros)
    1. [Variables de ambiente](#variables-de-ambiente)
1. [Ejecución](#ejecución)


# Prerrequisitos
- Python V 3.8
- Base de datos en PostGIS (v13) u Oracle express (v 21) o datos de conexión a una.

# Instalación
Para instalar las dependencias necesarias, ejecute:
 - pip install -r requirements.txt

Y si utiliza pip3, ejecute:

 - pip3 install -r requirements.txt

# Preparación
## Cargar información a la base de datos
A la base de datos se debe cargar la información alfanumérica de coberturas y de habitat, estos deben quedar cargados en una tabla con nombre `<workspace>_coberturas` y `<workspace>_habitat`, reemplace `<workspace>` por el nombre del espacio de trabajo que va a usar al momento de ejecutar el programa.

## Archivo de parámetros
Debe copiar el archivo [parameters.xlsx](condiciones_iniciales/parameters.xlsx) y cambiarle el nombre a `<workspace>_parameters.xlsx`, reemplace `<workspace>` por el nombre del espacio de trabajo que va a usar al momento de ejecutar el programa.

La descripción de las características de este archivo están en el manual de usuario.

## Variables de ambiente
Debe configurar las siguientes variables de ambiente:

- DB_SYSTEM: sistema de base de datos que se va a usar, los posibles valores son 'postgres' u 'oracle'
- DB_ADDRESS: url o ip del host de la base de datos
- DB_PORT: puerto de la base de datos
- DB_USERNAME: nombre de usuario con el cual conectarse a la base de datos
- DB_PASSWORD: contraseña del usuario
- DB_NAME: nombre de la base de datos

# Ejecución

Ejecute el comando siguiente comando para ejecutar el simulador:


`python3 run_principal.py -o <nombre_archivo.csv> -w <nombre_workspace>`

El argumento `-o` corresponde al nombre que desea asignar al archivo de resultados de la simulación, tenga en cuenta que el nombre real será `<workspace>_<nombre_archivo.csv>`. El argumento `-w` corresponde al nombre del workspace en el que está trabajando, tenga en cuenta que este debe ser el mismo que se usó en las tablas de la base de datos y el archivo de parámetros.

# Autores
* **Jorge Amador** - [jaamadorm](https://github.com/jaamadorm)
* **Danny Ibarra Vega** - [dwibarrave](https://github.com/dwibarrave)
* **Manuel Galvez** - [ManuelStardust](https://github.com/ManuelStardust)
* **Erika Suarez Valencia** - [erikasv](https://github.com/erikasv)

# Licencia
Este proyecto está licenciado bajo la licencia [MIT](LICENSE)

# Reconocimientos

Esta simulador hace parte de la herramienta del componente 2 del convenio [FIBRAS](http://humboldt.org.co/fibras/componente2.html) entre el Instituto Humboldt y Ecopetrol
