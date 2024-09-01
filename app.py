import argparse
from fastapi import FastAPI, Query, HTTPException
from pypandoc import convert_text
import uvicorn

app = FastAPI()

def rtf_to_html_div(rtf_text):
    plain_text = convert_text(rtf_text, 'plain', format='rtf')
    lines = plain_text.splitlines()
    html_div = '<div>'
    for line in lines:
        if line: 
            html_div += f'<p>{line}</p>'
    html_div += '</div>'
    return html_div

@app.get('/convert')
async def convert_rtf_to_html(text: str = Query(..., description="El texto RTF a convertir a HTML")):
    if text:
        html_div = rtf_to_html_div(text)
        return {'respuesta': html_div}
    else:
        raise HTTPException(status_code=400, detail="No se ha proporcionado texto RTF")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convertir texto RTF a HTML')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Dirección IP para ejecutar el servidor')
    parser.add_argument('--port', type=int, default=8080, help='Puerto para ejecutar el servidor')
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)