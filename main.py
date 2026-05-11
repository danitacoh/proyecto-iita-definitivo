import random
import json
import os
import tkinter as tk

palabras_animales = [
    "gatos", "perro", "tigre", "koala", "panda",
    "cisne", "buhos", "ranas", "cebra", "pulpo",
    "toros", "lobos", "llama", "tapir", "alces",
    "dingo", "bicho", "nutri", "garza", "liebre"
]

palabras_ciudades = [
    "paris", "tokio", "cairo", "miami", "dubai",
    "delhi", "lagos", "oslo", "berna", "quito",
    "accra", "dakar", "hanoi", "minsk", "sofia",
    "rabat", "brest", "tours", "lieja", "nicer"
]

palabras_comida = [
    "pizza", "pasta", "torta", "queso", "limon",
    "mango", "melon", "sopas", "leche", "cacao",
    "tacos", "crepe", "sushi", "fideo", "asado",
    "jugos", "vinos", "plato", "wafer", "dulce"
]

palabras_argentina = [
    "asado", "joda", "posta", "fiaca", "salta",
    "jujuy", "lujan", "tigre", "bicho", "pibe",
    "guiso", "yerba", "bombo", "tango", "cumbi",
    "chori", "mate", "trucho", "villa", "bardo"
]
#palabras para intentar


tematicas = {
    "🐾 Animales": palabras_animales,
    "🏙️ Ciudades": palabras_ciudades,
    "🍕 Comida": palabras_comida,
    "🇦🇷 Modo Argentino": palabras_argentina
}

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



#configuracion
filas = 6
columnas = 5
tamano_celda = 60

#variables globales
datos = cargar_datos()
secreta = elegir_palabra(datos["jugadas"], palabras_animales)
intento_actual = 0
letra_actual = 0
celdas = []
letras = []

#colores
color_fondo = "#ffe4f0"
color_celda = "#ffffff"
color_verde = "#f06292"
color_amarillo = "#f8bbd0"
color_gris = "#e0e0e0"
color_texto = "#880e4f"

#ventana
ventana = tk.Tk()
ventana.title("Wordle")
ventana.configure(bg=color_fondo)
ventana.geometry("1000x1000")

#titulo 
titulo = tk.Label(ventana, text="WORDLE", font=("Arial",48, "bold"), bg=color_fondo, fg=color_texto)
titulo.pack(pady=10)

#grilla
marco = tk.Frame(ventana, bg=color_fondo)
marco.pack(pady=10)

for fila in range(filas):
    fila_celdas = []
    fila_letras = []
    for col in range(columnas):
        celda = tk.Label(marco, text="", width=4, height=2, font=("Arial", 24, "bold"), bg=color_celda, fg=color_texto, relief="solid", borderwidth=2)
        celda.grid(row=fila, column=col, padx=4, pady=4)
        fila_celdas.append(celda)
        fila_letras.append("")
    celdas.append(fila_celdas)
    letras.append(fila_letras)

#racha
racha_label = tk.Label(ventana, text=f"🔥 Racha: {datos["racha"]}", font=("Arial, 14"), bg=color_fondo, fg=color_texto)
racha_label.pack(pady=5)

#mensaje
mensaje_label = tk.Label(ventana, text="", font=("Arial", 14), bg=color_fondo, fg=color_texto)
mensaje_label.pack(pady=5)

#logica del teclado
def presionar_tecla(evento):
    global intento_actual, letra_actual

    tecla = evento.keysym

    if tecla == "Return":
        enviar_intento()
    elif tecla == "BackSpace":
        if letra_actual > 0:
            letra_actual -=1
            letras[intento_actual][letra_actual] = ""
            celdas[intento_actual][letra_actual].config(text="")
    elif len(tecla) == 1 and tecla.isalpha():
        if letra_actual < columnas:
            letras[intento_actual][letra_actual] = tecla.lower()
            celdas[intento_actual][letra_actual].config(text=tecla.upper())
            letra_actual +=1

def enviar_intento():
    global intento_actual, letra_actual

    if letra_actual < columnas:
        mensaje_label.config(text="escribi 5 letras primero")
        return 
    
    intento = "".join(letras[intento_actual])
    resultado = comparar(secreta,intento)

    colores = {"verde": color_verde, "amarillo": color_amarillo, "gris": color_gris}
    for i in range (columnas):
        celdas[intento_actual][i].config(bg=colores[resultado[i]])
    
    if intento == secreta:
        datos ["racha"] += 1
        datos["jugadas"].append(secreta)
        guardar_datos(datos)
        racha_label.config(text = f"🔥Racha: {datos["racha"]}")
        mensaje_label.config(text = "¡Ganaste 🎊!")
        return
    
    intento_actual += 1
    letra_actual = 0


    if intento_actual >= filas: 
        datos["racha"] = 0
        datos["jugadas"].append(secreta)
        guardar_datos(datos)
        mensaje_label.config(text = f"💀 Perdiste, la palabra era {secreta.upper()}")
        return


ventana.bind("<Key>", presionar_tecla)
ventana.focus_force()


ventana.mainloop()

