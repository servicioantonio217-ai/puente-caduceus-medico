from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Ocultamos tu llave por seguridad
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Usamos el modelo Flash, que es el más rápido para que no te haga esperar
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['POST', 'GET'])
def handle_request():
    # Si Vercel revisa que esté vivo
    if request.method == 'GET':
        return "El puente médico está activo y listo."
    
    # Recibimos el audio convertido a texto por tus gafas
    data = request.get_json(silent=True) or {}
    
    # Buscamos la pregunta en diferentes formatos comunes
    prompt = data.get('text', '') or data.get('query', '') or data.get('prompt', '') or str(data)
    
    if not prompt:
        return jsonify({"text": "No pude procesar la pregunta, intenta de nuevo."})

    try:
        # Instrucción interna de comportamiento clínico
        medical_prompt = f"Eres un asistente médico para un interno en rondas hospitalarias. Te van a hacer una consulta. Responde al grano, con datos precisos (dosis, diagnósticos, escalas) y sin saludos ni introducciones. Consulta: {prompt}"
        
        response = model.generate_content(medical_prompt)
        
        # Devolvemos la respuesta formateada a tus gafas
        return jsonify({"text": response.text})
    
    except Exception as e:
        return jsonify({"text": "Hubo un error de conexión."})
