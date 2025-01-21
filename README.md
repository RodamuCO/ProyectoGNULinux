# ProyectoGNULinux

## Descripción 
La siguiente aplicación es una herramienta enfocada a la gestión de tareas del usuario

## Características 
- **Agregación y eliminación de tareas**: El programa permite al usuario agregar tareas y descripciones a las mismas para que el usuario tenga mayor facilidad para recordar lo que debe realizar y a la hora en la que debe.
- **Interfaz simple**: El programa dispone de una interfaz intuitiva para facilitar su uso
- **Actualización a tiempo real**: El programa se actualiza en tiempo real para verificar el tiempo restante de la tarea que el usuario debe reallizar

- ## Requisitos del sistema
- **Sistema operativo**: Linux
- **Python**: Versión 3.6 o superior
  
- **Importante**: Utilizar python 3 e instalar las dependencias que necesita el programa

## Instalación
1. Clonar este repositorio
```
   git clone https://github.com/RodamuCO/ProyectoGNULinux
   cd ProyectoGNULinux
```
2. Instalar las dependencias de python en caso de no tenerlas instaladas
```
  pip install tk 
  pip install tkcalendar
  pip install json
  pip install pandas
```
3. Ejecuta el programa
```
  python3 GestorTareas.py
```

## Usar el programa

1. Agregar tareas

-Escribe un título y una descripción.
-Usa el calendario para seleccionar la fecha límite.
-Selecciona la hora y los minutos del plazo.
-Haz clic en "Agregar tarea".

---

2. Eliminar tareas

-Escribe el título exacto de la tarea en el campo de título.
-Haz clic en "Eliminar tarea".

---
3.Visualización de tareas

-Todas las tareas aparecerán en una tabla con su título, descripción y fecha límite.
-Los colores indican el estado de cada tarea (verde, amarillo o rojo).
*Verde: Más de 30 minutos restantes.
*Amarillo: 30 minutos o menos para el vencimiento.
*Rojo: La fecha límite ya pasó.

