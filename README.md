# <center>Clasificación automática de sonidos utilizando aprendizaje máquina</center>

## Index

- [Descripcion](#descripcion)
- [Pre-Requisitos](#pre-requisitos-📋)
- [Instalacion](#instalacion-🔧)
- [Autores](#autores-✒️)

## Descripcion

Proyecto para la materia de Base de Datos 2 que consiste en crear un modelo de aprendizaje maquina capaz de clasificar de manera automatizada los sonidos

## Pre-Requisitos 📋

```
Python >= 3.6
```

## Instalacion 🔧

_Para utilizar el proyecto primero debes instalar un entorno virtual en la ubicacion de la carpeta donde haya sido clonado el repo_

```
python -m venv venv
```

_Una vez hecho esto debemos activar el entorno virtual_

```
venv\Scripts\activate
```

_Ahora que tenemos nuestro entorno virtual solo nos queda instalar las dependencias del proyecto_

```
pip install -r requirements.txt
```

_Luego ejecutar el siguiente comando en consola para ejecutar el proyecto_

```
py model.py
```

> [!NOTE]  
> Si eres un desarrollador y quieres aportar al proyecto recuerde que debe cambiar el interpete de python al del entorno virtual Ctrl + Shift + Python Seleccionar Interprete y escoges el del entorno virtual Venv

> [!NOTE]
> En caso de no tener previamente un dataseet hecho para entrenar al modelo te recomiendo usar cortador.py y createCsv.py para picar los audios en 30 segundos, guardarlos en una carpeta que sera la encargada de clasificarlo con la ayuda del cortador.py y el createCsv.py solo se encargara de leer la carpeta Sound y create el csv de tu dataseet para entrenar el modelo

## Autores ✒️

- **Emmanuel Salcedo** - _Developer_
- [HopeAero](https://github.com/HopeAero)
- **Luis Vásquez** - _Developer_
- [luizzzito](https://github.com/luizzzito)
- **Luis Hernandez (Greenie Warren)** - _Developer_
- [GreenieWarren](https://github.com/GreenieWarren)
