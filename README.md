# Mi Proyecto

Este es un proyecto de FastAPI.

## Configuración del entorno

Primero, debes crear un entorno virtual para instalar las dependencias del proyecto. Puedes hacerlo con el siguiente comando:

```sh
python3 -m virtualenv venv
```

Luego activa el entorno virtual con:
En Windows:

```sh
venv\Scripts\activate
```

En Unix o MacOS:

```sh
source venv/bin/activate
```

Instalación de dependencias
Una vez que el entorno virtual esté activo, puedes instalar las dependencias con:

```sh
pip install -r requirements.txt
```

Configuración de variables de entorno

```sh
#.env
DB_URL_CONNECTION=postgresql://usuario:contraseña@host:5432/nombre_de_base_de_datos
FRONTEND_URL=http://localhost:8000
SECRET_KEY=tu_clave_secreta
ADMIN_USERNAME=nombre_de_usuario_admin
```

Ejecución del servidor
Para ejecutar el servidor, puedes usar el siguiente comando:

```sh
uvicorn main:app --host 0.0.0.0 --port 8080
```

Esto iniciará el servidor en el puerto 8080.

Uso
Una vez que el servidor esté en ejecución, puedes acceder a la documentación de la API en <http://localhost:8080/docs>.
