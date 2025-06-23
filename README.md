# 🗂️ Sistema de Gestión de Tareas

Proyecto desarrollado en Python con Flask que permite registrar usuarios, autenticarse y gestionar tareas personales (crear, listar, actualizar y eliminar).

## 📁 Estructura del Proyecto

```
Sistema_de_Gestión_de_Tareas/
├── cliente.py
├── init_db.py
├── readme.md
├── requirements.txt
├── servidor.py
├── tareas.db
├── venv/ (entorno virtual)
```

## ⚙️ Tecnologías utilizadas

- Python 3.11+
- Flask
- Flask SQLAlchemy
- Werkzeug
- Requests

## 🧪 Instalación

1. Cloná el repositorio:

```bash
git clone https://github.com/Eli4118/PFO2.git
cd PFO2/Sistema_de_Gestión_de_Tareas
```

2. (Opcional pero recomendado) Crear entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate   # En Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Inicializar la base de datos:

```bash
python init_db.py
```

## 🚀 Cómo ejecutar

1. Iniciá el servidor Flask:

```bash
python servidor.py
```

2. En otra terminal, ejecutá el cliente:

```bash
python cliente.py
```

## 👤 Funcionalidades del cliente

- Registro de usuario
- Autenticación básica HTTP
- Crear nueva tarea
- Listar tareas existentes
- Editar descripción o marcar como completada
- Eliminar tareas

## 🔐 Seguridad

La autenticación se realiza mediante **Basic Auth** con hash de contraseña (SHA-256). No usar en producción sin HTTPS.

## 📝 Autor

Eliana Carmona  
Proyecto académico – PFO2 (Redes)