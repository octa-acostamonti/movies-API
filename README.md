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

Al disponer de la memoria gratuita que ofrece Render, se decidio achicar el dataset tomando en consideracion solo las peliculas mas relevantes. Para eso se decanto con la columna de popularidad para conseguir las peliculas mas "recomendadas" por el publico en general. 

Se genero un archivo notebook denominado "EDA" en el que se analizo las distintas variables numericas con respecto a la popularidad. Esto se hizo con el objetivo de reducir el tamaño del dataset a las peliculas mas relevantes para poder hacer un sistema efectivo de recomendacion

Primero se comparo la popularidad con el presupuesto:
* La hipotesis era que cuanto mas presupuesto una pelicula tenia, mas atraccion generaria y, por tanto, mas popularidad.

[INSERTAR IMAGEN]

* Como vemos, luego de plotear nos damos cuenta que la hipotesis no era cierta. Hay peliculas de menos presupuesto que son mas populares, mientras que hay algunas que tienen mucho presupuesto y son menos populares que las de menor presupuesto. Hipotesis descartada.

Luego se ploteo la popularidad segun el año:
* La hipotesis era que cuanto mas nueva la pelicula, mas relevancia tenia y, por tanto, mayor popularidad.

[INSERTAR IMAGEN]

* Como se logra apreciar, desde 1980 en adelante, la popularidad de las peliculas aumento drasticamente, con picos historicos rompuiendose año tras año. Hipotesis adoptada. Se reducira el dataset a peliculas luego de 1980

* Por ultimo, se tomo en consideracion la columna "runtime" que expresa la duracion de peliculas por minuto. La hipotesis era que las duraciones mas similes a las de una pelicula (≈90 minutos) eran las que mas popularidad tenian.

[INSERTAR IMAGEN]

* Como se puede notar, las pelicualas entre 30 y 350 minutos som las mas populares. Hipotesis comprobada. Vamos a achicar los datos a los ubicados entre 30 y 350.


Luego de todo este analisis nos quedan aproximadamente 33300 peliculas. Como se planteo en el principio, Render solo permite 512 mb, por lo que esa cantidad de peliculas no podra ser utilizado ya que analizar la similiritud del coseno (un proceso matematica para conseguir la distancia de similitud en una matriz) cuesta muchos recursos. Luego de mucha experimentacion, el punto optimo fue hacer un dataset de 4000 peliculas.

#### ESPERO QUE LES GUSTE

