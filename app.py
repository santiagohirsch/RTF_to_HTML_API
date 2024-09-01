import argparse
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError
from pypandoc import convert_text
import uvicorn

app = FastAPI()

class RTFRequest(BaseModel):
    texto: str

def rtf_to_html_div(rtf_text: str) -> str:
    try:
        plain_text = convert_text(rtf_text, 'plain', format='rtf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir RTF a texto plano: {str(e)}")
    
    lines = plain_text.splitlines()
    html_div = '<div>'
    for line in lines:
        if line.strip(): 
            html_div += f'<p>{line}</p>'
    html_div += '</div>'
    return html_div

@app.post('/convertir')
async def convert_rtf_to_html(request: Request):
    try:
        body = await request.json()
        rtf_request = RTFRequest(**body)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Estructura JSON inválida: {e.errors()}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato JSON inválido")

    text = rtf_request.texto
    if text:
        try:
            html_div = rtf_to_html_div(text)
            return {'respuesta': html_div}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el HTML: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail='Falta el texto RTF')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convertir texto RTF a HTML')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Dirección IP para ejecutar el servidor')
    parser.add_argument('--port', type=int, default=8080, help='Puerto para ejecutar el servidor')
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
