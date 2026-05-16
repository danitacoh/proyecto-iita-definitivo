import random
import json
import os

def elegir_palabra(jugadas, lista):
    disponibles= [p for p in lista if p not in jugadas]
    if not disponibles: 
        disponibles = lista
    return random.choice(disponibles)

def comparar(secreta, intento):
    resultado = []
    secreta_lista = list(secreta) #copia para evitar letras

    #primera pasada
    for i in range(5): 
        if intento[i] == secreta[i]:
            resultado.append("verde")
            secreta_lista[i] = None 
        else: 
            resultado.append(None)

    #segunda pasada

    for i in range(5):
        if resultado[i] is not None:
            continue
        if intento[i] in secreta_lista:
            resultado[i] = "amarillo"
            secreta_lista[secreta_lista.index(intento[i])] = None
        else: 
            resultado[i] = "gris"

    return resultado

def cargar_datos():
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            return json.load(f)
    return {"racha": 0, "jugadas": []}


def guardar_datos(datos): 
    with open ("datos.json", "w") as f: 
        json.dump( datos, f)
