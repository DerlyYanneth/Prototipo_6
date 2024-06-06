import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# Montar el directorio estático
app.mount("/static", StaticFiles(directory="static"), name="static")

class Question(BaseModel):
    question: str

@app.post("/chat")
async def chat(question: Question):
    try:
        # Prompt modificado para incluir la restricción de responder solo preguntas médicas en español
        modified_prompt = f"Por favor, responde solo preguntas relacionadas con medicina en español. Pregunta: {question.question}"

        # Realiza una solicitud a la API de Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"prompt": modified_prompt, "model": "llama2", "stream": True}
        )
        response.raise_for_status()
        data = response.json()

        # Obtiene la respuesta de la API de Ollama
        answer = data.get("response")
        if not answer:
            raise HTTPException(status_code=500, detail="No se pudo obtener una respuesta")

        return {"response": answer}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/http_chat")
async def http_chat(question: Question):
    response = obtener_respuesta(question.question)
    return {"response": response}

@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())

def obtener_respuesta(pregunta):
    url = 'http://localhost:11434/api/generate'  # URL de la API de Ollama, asumiendo que tiene un endpoint similar
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'prompt': pregunta,
        'max_tokens': 150,
        'temperature': 0.7
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        respuesta = response.json()
        return respuesta['choices'][0]['text'].strip()
    except requests.exceptions.RequestException as e:
        return f"Ocurrió un error: {str(e)}"
        
if __name__ == "_main_":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")