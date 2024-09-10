import argparse
from fastapi import FastAPI, HTTPException, Request, responses
from pydantic import BaseModel, ValidationError
import pypandoc
import re
import uvicorn

app = FastAPI()

class RTFRequest(BaseModel):
    texto: str

def extract_styles_and_lines(rtf_text: str):
    header_end_patterns = [r'\\viewkind', r'\\lang\d+', r'\\deff\d+', r'\\fonttbl', r'\\colortbl', r'\\pard', r'\\par']
    header_end_pos = len(rtf_text)

    for pattern in header_end_patterns:
        match = re.search(pattern, rtf_text)
        if match:
            header_end_pos = min(header_end_pos, match.start())

    rtf_text = rtf_text[header_end_pos:].lstrip()
    
    color_re = re.compile(r'\\cf(\d+)', re.DOTALL)
    font_size_re = re.compile(r'\\fs(\d+)', re.DOTALL)
    
    color_map = {
        '1': 'red',
        '2': 'green',
        '3': 'blue'
    }
    
    lines = []
    
    paragraphs = re.split(r'\\pard|\\par', rtf_text)
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        
        html_paragraph = pypandoc.convert_text(paragraph, 'html', format='rtf')
        
        cleaned_html_paragraph = re.sub(r'\s+', ' ', html_paragraph).strip()
        if not cleaned_html_paragraph:
            continue
        
        style_attributes = []

        color_match = color_re.search(paragraph)
        if color_match:
            color_code = color_match.group(1)
            color = color_map.get(color_code, 'black')  
            style_attributes.append(f'color: {color}')
            paragraph = paragraph.replace(f'\\cf{color_code}', '')

        font_size_match = font_size_re.search(paragraph)
        if font_size_match:
            size = int(font_size_match.group(1)) / 2  
            style_attributes.append(f'font-size: {size}px')
            paragraph = paragraph.replace(f'\\fs{font_size_match.group(1)}', '')

        if style_attributes:
            style_attribute_string = '; '.join(style_attributes)
            styled_html_paragraph = f'<span style="{style_attribute_string}">{cleaned_html_paragraph}</span>'
        else:
            styled_html_paragraph = cleaned_html_paragraph

        lines.append((cleaned_html_paragraph, styled_html_paragraph))

    return lines

def rtf_to_html_div(rtf_text: str) -> str:
    try:
        html_text = pypandoc.convert_text(rtf_text, 'html', format='rtf')
        
        styled_lines = extract_styles_and_lines(rtf_text)
        
        html_lines = html_text.split('\n')
        
        normalized_html_lines = [' '.join(line.split()) for line in html_lines]
        
        for original_line, styled_line in styled_lines:
            normalized_original_line = ' '.join(original_line.split())
            
            for i, line in enumerate(normalized_html_lines):
                if normalized_original_line in line:
                    normalized_html_lines[i] = line.replace(normalized_original_line, styled_line)
        
        final_html_text = '\n'.join(normalized_html_lines)
        
        html_div = f'<div>{final_html_text}</div>'
        
        return html_div
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir RTF a HTML: {str(e)}")


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
            return responses.HTMLResponse(content=html_div, media_type="text/html")
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
