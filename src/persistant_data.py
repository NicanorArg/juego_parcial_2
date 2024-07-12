import json
import os

def get_path_actual(filename:str) -> str:
    """concatena el nombre de un archivo con la ruta del directorio actual

    Args:
        filename (str): nombre del archivo

    Returns:
        str: ruta del directorio concatenada con el nombre del archivo
    """
    ruta = os.path.dirname(__file__)
    return os.path.join(ruta, filename)

def convert_csv_a_lista(csv_file:str) -> list[dict]:
    """usa el contenido de un archivo csv proporcionado como parametro para crear una lista de diccionarios

    Args:
        csv_file (str): nombre del archivo csv, sin ruta especificada; el archivo csv y el archivo que lo lee deben encontrarse en el mismo directorio

    Returns:
        list: lista de diccionarios 
    """
    with open(get_path_actual(csv_file), "r", encoding="utf-8") as archivo_csv:
        keys = archivo_csv.readline().strip("\n").split(",")

        lista_final = []
        for linea in archivo_csv.readlines():
            datos = linea.strip("\n").split(",")
            diccionario = {}
            for i in range(len(keys)):
                key = keys[i]
                dato = datos[i]
                if dato.isdigit():
                    dato = int(dato)
                diccionario[key] = dato
            lista_final.append(diccionario)
    return lista_final

def overwrite_scoreboard(scores: list[dict]) -> None:
    """escribe/sobreescribe los datos del scoreboard con los puntajes actualmente guardados en memoria

    Args:
        scores (list[dict]): lista de diccionarios
    """
    with open(get_path_actual("scoreboard.csv"), "w", encoding="utf-8") as scoreboard:
        encabezado = ",".join(scores[0].keys()) + "\n"
        scoreboard.write(encabezado)
        for score in scores:
            line = ""
            for value in score.values():
                line += f"{value},"
            line += "\n"
            scoreboard.write(line)

def read_difficulty_settings() -> dict:
    """carga los elementos dentro del archivo difficulty_settings.json

    Returns:
        dict: diccionario con los modificadores de dificultad
    """
    with open(get_path_actual("difficulty_settings.json"), "r", encoding="utf-8") as json_file:
        difficulty_settings = json.load(json_file)

    return difficulty_settings

def overwrite_difficulty_settings(difficulty_settings: list[dict]) -> None:
    """escribe o sobreescribe el archivo difficulty_settings.json con los modificadores de dificultad actualmente guardados

    Args:
        difficulty_settings (list[dict]): diccionario con las variables de dificultad
    """
    with open(get_path_actual("difficulty_settings.json"), "w", encoding="utf-8") as json_file:
        json.dump(difficulty_settings, json_file, indent=4)

try:
    scores = convert_csv_a_lista("scoreboard.csv")
except FileNotFoundError:
    scores = [{"type": "hi-score", "score": 0}, {"type": "last score", "score": 0}]

try:
    difficulty_settings = read_difficulty_settings()
except FileNotFoundError:
    difficulty_settings = {"enemy_difficulty": 2, "starting_lives": 3}
