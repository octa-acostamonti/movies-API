import pandas as pd
from fastapi import FastAPI
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
############################
# IMPORTAMOS LAS LIBRERIAS #
############################

app = FastAPI() # Instanciamos FastAPI en la variable app

#########################################################################
# IMPORTAMOS TODOS LOS DATASETS QUE UTILIZAREMOS EN LAS CALLS DE LA API #
#########################################################################


peliculas_mes = pd.read_csv("API/peliculas_mes.csv")

peliculas_dia = pd.read_csv("API/peliculas_dia.csv")

score_titulo = pd.read_csv("API/score_titulo.csv").drop(columns="Unnamed: 0")

votos_titulos = pd.read_csv("API/ votos_titulos.csv").drop(columns="Unnamed: 0")

nombre_actor = pd.read_csv("API/ nombre_actor.csv").drop(columns="Unnamed: 0")

nombre_director = pd.read_csv("API/ nombre_director.csv").drop(columns="Unnamed: 0")

df_ML = pd.read_csv("./Datasets/MachineLearning.csv")

@app.get("/")
def root():
    return "Hola Instructores de SoyHenry! Este es mi proyecto individual MLOps, espero que les guste"



@app.get("/cantidad_filmaciones_mes/{mes}")
def pelicula_mes(mes: str):
    try:
        mes = mes.capitalize() # Adecuamos el parametro de entrada al del dataset para no tener complicaciones
        cantidad = peliculas_mes.loc[peliculas_mes["mes"] == mes, "cantidad"].dropna().values # Buscamos y devolvemos la cantidad del mes que se indico en el parametro de entrada
        return {"mes": mes, "cantidad": int(cantidad[0])} # Devolvemos el mes ingresado con su respectiva cantidad
    
    except Exception as e:
        
        return "El mes ingresado no es valido"



@app.get("/cantidad_filmaciones_dia/{dia}")
def pelicula_dia(dia: str):
    try:
        dia = dia.capitalize() # Adecuamos el parametro de entrada al del dataset para no tener complicaciones
        cantidad = peliculas_dia.loc[peliculas_dia["dia"] == dia, "cantidad"].dropna().values # Buscamos y devolvemos la cantidad del dia que se indico en el parametro de entrada
        return {"dia": dia, "cantidad": int(cantidad[0]) }# Devolvemos el dia ingresado con su respectiva cantidad
    
    except Exception:
        
        return "El dia ingresado no es valido"
    


@app.get("/score_titulo/{pelicula}")
def titulo_score(pelicula:str):
    try:
        pelicula_info = score_titulo.loc[score_titulo["titulo"] == pelicula] # Filtramos el dataset para que nos muestre la data del titulo ingresado
        tit_score = pelicula_info.values[0] # Generamos otra variable en la que almacenamos los datos de la pelicula
        return {"titulo":pelicula, "anio":tit_score[1], "popularidad":tit_score[2]} # Devolvemos los valores requeridos
    
    except Exception: 
        return "El título ingresado no se encuentra"
    


@app.get("/votos_titulo/{pelicula}")
def titulo_votos(pelicula:str):
    try:
        peli_votos = votos_titulos.loc[votos_titulos["titulo"]==pelicula].values # Generamos una variable que contenga todos los datos requeridos para el return
        return {"titulo":pelicula, "anio":int(peli_votos[0][3]), "voto_total":int(peli_votos[0][1]), "voto_promedio":peli_votos[0][2]} # Retornamos los valores requeridos
    except Exception:
        return ("La pelicula no supera la cantidad ed 2000 votos")

############################################################################################################################################
# La funcion de actor es particular ya que en la columna de "actores" hay mas de un actor por fila. Entonces hay que revisar fila por fila # 
# para ver si el actor se encunetra en la columna. Esto claramente disminuye el rendimiento.                                                                                         #
############################################################################################################################################

@app.get("/get_actor/{actor}")
def actor_datos(actor:str):
    try:
        retorno_total = 0 # Inicializamos un conteo de retorno total
        cant_peliculas = 0 # Inicializamos un conteo de cantidad de peliculas
        for i, fila in nombre_actor.iterrows(): # Nos fijamos fila por fila
            if actor in fila["actores"]: # Generamos una condicion de que si el actor se encuentra en la columna "actores"
                retorno_total += fila["retorno"] # Sume a retorno total la columna retorno
                cant_peliculas += 1 # Y sume uno para la cantidad de peliculas
        retorno_promedio = retorno_total / cant_peliculas if cant_peliculas > 0 else 0 # Una vez terminado el bucle con el retorno total divido la cantidad del peliculas (si es mayor a 0) calculamos el retorno promedio
        return {"actor":actor, "cantidad_filmaciones":cant_peliculas, "retorno_total":retorno_total, "retorno_promedio":retorno_promedio} # Devolvemos los valores pertinentes
    except Exception:
        return "El actor ingresado no se encuentra"

@app.get("/get_director/{director}")
def director(director: str):
    try:
        dire = nombre_director.loc[nombre_director["director"] == director] # Filtramos las peliculas por las dirigidas por el director pedido
        dire["fecha_estreno"] = pd.to_datetime(dire["fecha_estreno"]) # Nos aseguramos que la columna fecha de estreno sea tipo "datetime"
        fecha_estreno = [date.strftime("%Y-%m-%d") for date in dire["fecha_estreno"]] # En esta variable almacenamos en una lista, en el formato requerido, las fechas de las peliculas del director
        return {"director":director,"retorno_total_director":dire["retorno"].sum(),"peliculas":list(dire["titulo"]),"año":fecha_estreno,
                "retorno_pelicula":list(dire["retorno"]),"budget_pelicula":list(dire["presupuesto"]),"revenue_pelicula":list(dire["recaudaccion"])} # Devolvemos los valores correspondientes

    except Exception as e:
        return f"Hubo un error:{e}"
    

"""
A PARTIR DE AQUI EMPIEZA LO RELACIONADO CON EL MODELO DE MACHINE LEARNING DE RECOMENDACION DE PELICULAS
"""

columnas_combinadas = df_ML["title"] + df_ML["generos"] + df_ML["actores"] + df_ML["overview"]
vec = TfidfVectorizer()
vector_columnas = vec.fit_transform(columnas_combinadas)
simil = cosine_similarity(vector_columnas)
todas_peliculas = df_ML["title"].tolist()

@app.get("/recomendacion/{pelicula}")
def recomendaciones(pelicula:str):
    try:
        encontrar_pelicula = difflib.get_close_matches(pelicula, todas_peliculas)
        if encontrar_pelicula:
            pelicula_encontrada = encontrar_pelicula[0]
            indice_pelicula = df_ML[df_ML.title == pelicula_encontrada].index.values[0]
            peliculas_similares = list(enumerate(simil[indice_pelicula]))
            ordenar_peliculas_similares = sorted(
                peliculas_similares, key=lambda x: x[1], reverse=True
            )
            i = 1
            recomendaciones = []
            for movie in ordenar_peliculas_similares[:6]:
                index = movie[0]
                pelicula_por_indice = df_ML[df_ML.index == index]["title"].values[0]
                if i < 7:
                    recomendaciones.append(pelicula_por_indice)
                    i += 1
            return {
                "lista_recomendada": recomendaciones}
        else:
            return "No se encontraron coincidencias cercanas para el título de la película proporcionado."
    except Exception as e:
        return f"Hubo un error: {e}"