
import tkinter as tk
from tkinter import messagebox
from palabras import tematicas
from logica import elegir_palabra, comparar, cargar_datos, guardar_datos

#configuracion
filas = 6
columnas = 5
tamano_celda = 60



#variables globales
datos = cargar_datos()
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
    global intento_actual, letra_actual, secreta, mensaje_label, racha_label, datos

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
        respuesta = messagebox.askyesno( "¡Ganaste 🎊!" , f"ganaste en el intento {intento_actual +1}!\nRacha: {datos["racha"]}\n\nJugar de nuevo?" )
        if respuesta:
          ventana.destroy()
        else: 
          ventana.destroy()
        return
    
    intento_actual += 1
    letra_actual = 0
    


    if intento_actual >= filas: 
        datos["racha"] = 0
        datos["jugadas"].append(secreta)
        guardar_datos(datos)
        respuesta = messagebox.askyesno("Perdiste" , f"💀 la palabra era {secreta.upper()}, jugar de nuevo?")
    if respuesta : 
        ventana.destroy()
        return  
    
    else: 
        ventana.destroy()
    return


    
def abrir_juego(nombre_tematica):
    global ventana, celdas, letras, intento_actual, letra_actual
    global racha_label, mensaje_label, secreta, marco

    intento_actual = 0
    letra_actual = 0
    celdas = []
    letras = []
    secreta = elegir_palabra(datos["jugadas"], tematicas[nombre_tematica])
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

    ventana.bind("<Key>", presionar_tecla)
    ventana.focus_force()
    ventana.mainloop()


def iniciar_tematica(nombre, seleccion):
    global secreta
    secreta = elegir_palabra(datos["jugadas"], tematicas[nombre])
    seleccion.destroy()
    abrir_juego(nombre)


def mostrar_seleccion(): 
    seleccion = tk.Tk()
    seleccion.title("WORDLE")
    seleccion.geometry("400x500")
    seleccion.configure(bg=color_fondo)

    tk.Label(seleccion, text="WORDLE", font=("Arial", 48, "bold"), bg=color_fondo, fg=color_texto).pack(pady=30)

    tk.Label(seleccion, text="Elegi una tematica: ", font=("Arial", 16), bg=color_fondo, fg=color_texto).pack(pady=10)

    for nombre in tematicas:
        tk.Button(seleccion, text=nombre, font=("Arial", 14, "bold"), bg=color_verde, fg="white", width=20, pady=8, command=lambda n=nombre: iniciar_tematica(n, seleccion)).pack(pady=6)


    seleccion.mainloop()

mostrar_seleccion()
