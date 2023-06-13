# Bienvenidos a mi Projecto - una API y ML project de data sobre peliculas.

| Informacion  | 
| ------------- | 
| Esta es una API que proporciona una variedad de informacion sobre peliculas de un dataset. Desde, cantidad de peliculas por mes y por dia historicamente, la popularidad o cantidad de votos por pelicula y la cantidad de peliculas (entre otra info) sobre actores y directores. Luego se creo un sistema de recomendacion de peliculas usando ML.
 Toda la data fue proporcionada por IDMB. | 

#### Documentacion

https://movie-api-octacosta.onrender.com/docs

#### Como se usa?

## PROCESO
#### ETL

Comenzamos con dos datasets, "movies_datasets.csv" y "credits.csv". Los mismos estaban anidados con diccionarios o listas de diccionarios con la informacion.


[AÑADIR IMAGEN]

La columnas anidadas fueron desarmadas mediante funciones creadas utilizando la libreria AST para evaluar el verdadero tipo de dato de los valores de la columna.
Luego se continuo con los siguientes procesos:
* Luego evaluamnos los valores nulos de las columnas y los rellenamos o eliminamos segun sea necesario
* Se cambio el formato de la columna "release_year" para que sea el adecuado; AAAA-mm-dd. 
* Se creo una nueva columna para sacar el retorno dividiendo los valores de cada fila de las columnas "revenue" y "budget"
* Eliminar las columnas innecesarias

#### API

Para la creacion de la API se utilizo el framework FastAPI y para el deploy Render.

Luego de a limpieza de los datos se crearon 6 endpoints:

* /cantidad_filmaciones_mes/{mes}: Devuelve la cantidad de peliculas que se estrenaron en ese mes historicamente
* /cantidad_filmaciones_dia/{dia}: Devuelve la cantidad de peliculas que se estrenaron en ese dia historicamente
* /score_titulo/{pelicula}: Devuelve el año del estreno y de la popularidad de la pelicula ingresada
* /votos_titulo/{pelicula}: Devuelve la cantidad de votos y el promedio de votos de las peliculas ingresadas.
* /get_actor/{actor}: Devuelve la cantidad de pelicula, el retorno total y el promedio del actor.
* /get_director/{director}: Devuelve el retorno total, las peliculas, el año, el retorno por pelicula, presupuesto por pelicula, ganancia de la pelicula ingresada

#### MACHINE LEARNING  

Se genero un arcivo notebook en "EDA" en el que se analizo las distintas vaiables numeicas con respecto a 

