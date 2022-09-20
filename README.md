# Simulador del modelo de Resiliencia

Implementación del modelo que hace parte de la herramienta de resiliencia.

## Prerrequisitos
- Python V 3.8
- Base de datos PostGIS (v 13) u Oracle express (v 21)

Para instalar las dependencias necesarias, ejecute:
 - pip install -r requirements.txt

Y si utiliza pip3, ejecute:

 - pip3 install -r requirements.txt

## Cómo ejecutar

Para facilitar la interacción con el programa le sugerimos usar el [servidor](https://github.com/PEM-Humboldt/herramienta-resiliencia-servidor) de la herramienta de resiliencia. Por medio del servidor, usted podrá cargar todos los insumos (capas y archivos de parámetros) y ejecutar la herramienta. También en las instricciones de ejecución del servidor podrá escoger qué base de datos usar, sin que sea necesaria una instalación manual.

### Preparación
Antes de poder ejecutar el programa usted debe cargar los insumos necesarios:

- A la base de datos debe cargar la información alfanumérica de coberturas y de habitat, estos deben quedar cargados en una tabla con nombre `<workspace>_coberturas` y `<workspace>_habitat`, reemplace `<workspace>` por el nombre del espacio de trabajo que va a usar al momento de ejecutar el programa.
- Debe copiar el archivo [parameters.xlsx](condiciones_iniciales/parameters.xlsx) y cambiarle el nombre a `<workspace>_parameters.xlsx`, reemplace `<workspace>` por el nombre del espacio de trabajo que va a usar al momento de ejecutar el programa.

El programa espera que las siguientes variables de ambiente estén configuradas para su correcta ejecución:

- DB_SYSTEM: sistema de base de datos que se va a usar, los posibles valores son 'postgres' u 'oracle'
- DB_ADDRESS: url o ip del host de la base de datos
- DB_PORT: puerto de la base de datos
- DB_USERNAME: nombre de usuario con el cual conectarse a la base de datos
- DB_PASSWORD: contraseña del usuario
- DB_NAME: nombre de la base de datos

### Ejecucuón

Ejecute el comando `python3 run_principal.py -o <nombre_archivo.csv> -w <nombre_workspace>`

El argumento `-o` corresponde al nombre que desea asignar al archivo de resultados de la simulación, tenga en cuenta que el nombre real será `<workspace>_<nombre_archivo.csv>`. El argumento `-w` corresponde al nombre del workspace en el que está trabajando, tenga en cuenta que este debe ser el mismo que se usó en las tablas de la base de datos.

## Autores
* **Jorge Amador** - [jaamadorm](https://github.com/jaamadorm)
* **Danny Ibarra Vega** - [dwibarrave](https://github.com/dwibarrave)
* **Manuel Galvez** - [ManuelStardust](https://github.com/ManuelStardust)
* **Erika Suarez Valencia** - [erikasv](https://github.com/erikasv)

## Licencia
Este proyecto está licenciado bajo la licencia [MIT](LICENSE)

## Reconocimientos

Esta simulador hace parte de la herramienta del componente 2 del convenio [FIBRAS](http://humboldt.org.co/fibras/componente2.html) entre el Instituto Humboldt y Ecopetrol
