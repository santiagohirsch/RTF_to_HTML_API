# API de Conversión de RTF a HTML
Esta API permite convertir texto en formato RTF (Rich Text Format) a HTML. Cada línea del texto RTF se convierte en un párrafo `<p>` dentro de un contenedor `<div>`. La API está construida utilizando FastAPI y utiliza pypandoc para la conversión de RTF a texto plano.

## Descripción
- Endpoint: /convertir
- Método: POST
- Descripción: Convierte el texto en formato RTF proporcionado a HTML.

## Requisitos
- Python 3.7 o superior
- FastAPI
- Uvicorn
- pypandoc
- Pydantic

## Instalación
1. Clona este repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

2. Navega al directorio del proyecto:

```bash
cd <NOMBRE_DEL_DIRECTORIO>
```

3. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
```

4. Activa el entorno virtual:

- En Windows:

```bash
venv\Scripts\activate
```

- En macOS y Linux:

```bash
source venv/bin/activate
```

5. Instala las dependencias:

```bash
pip install fastapi uvicorn pypandoc pydantic
```

6. Instala pandoc si no está instalado. Puedes seguir las instrucciones aquí para tu sistema operativo.

- En Windows:
Seguir los pasos de instalación en la siguiente página web: https://pandoc.org/installing.html

- En macOS y Linux:

```bash
brew install pandoc
```

### Uso
Para ejecutar el servidor, usa el siguiente comando:

```bash
python app.py --host 127.0.0.1 --port 8080
```

Esto iniciará el servidor en http://127.0.0.1:8080.

Para más información sobre los argumentos, ejecutar el siguiente comando:

```bash
python app.py --help
```

### Cómo Usar la API
Envía una solicitud POST al endpoint /convertir con un cuerpo JSON utilizando la siguiente estructura:

```json
{
    "texto": "[texto RTF a convertir]"
}
```

**Ejemplo de Solicitud**

```json
{
  "texto": "{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}\\viewkind4\\uc1\\pard\\sb100\\sa100\\f0\\fs24 Esta es la primera línea.\\par Esta es la segunda línea, \\b negrita\\b0  texto.\\par Esta es la tercera línea, \\i cursiva\\i0  texto.\\par Esta es la cuarta línea, con una \\ul subrayado\\ul0 .\\par}"
}
```

**Respuesta Exitosa**
```json
{
  "respuesta": "<div><p>Esta es la primera línea.</p><p>Esta es la segunda línea, <b>negrita</b> texto.</p><p>Esta es la tercera línea, <i>cursiva</i> texto.</p><p>Esta es la cuarta línea, con una <u>subrayado</u>.</p></div>"
}
```

**Respuesta de Error**

- *400 Bad Request*: Si el cuerpo de la solicitud no contiene el campo `texto` o si el formato del JSON es incorrecto.

```json
{
  "detail": "Formato JSON inválido"
}
```

```json
{
  "detail": "Falta el texto RTF"
}
```

- *500 Internal Server Error*: Si ocurre un error al convertir el texto RTF a texto plano o al generar el HTML.

```json
{
  "detail": "Error al convertir RTF a texto plano: <detalles del error>"
}
```

```json
{
  "detail": "Error al generar el HTML: <detalles del error>"
}
```

### Configuración del Servidor
Puedes configurar la dirección IP y el puerto del servidor utilizando los parámetros `--host` y `--port` al ejecutar el script:

- `--host`: Dirección IP en la que el servidor escuchará. Por defecto es 127.0.0.1.
- `--port`: Puerto en el que el servidor escuchará. Por defecto es 8080.