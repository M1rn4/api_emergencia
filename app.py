from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

@app.route("/detectar_emergencia", methods=["POST"])
def detectar_emergencia():
    try:
        data = request.get_json()
        hr = data.get("hr")          # frecuencia cardíaca promedio
        spo2 = data.get("spo2")      # saturación de oxígeno promedio
        temp = data.get("temp")      # temperatura promedio
        actividad = data.get("actividad")  # run, sit o walk

        # Reglas simples adaptadas al contexto de la actividad
        if spo2 < 90 and hr > 170 and temp > 38:
            riesgo = "multi-riesgo"
        elif spo2 < 90:
            riesgo = "hipoxia"
        elif hr > 170:
            riesgo = "taquicardia"
        elif temp > 38:
            riesgo = "hipertermia"
        else:
            riesgo = "normal"

        return jsonify({
            "riesgo": riesgo,
            "actividad": actividad,
            "recomendacion": generar_recomendacion(riesgo, actividad)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generar_recomendacion(riesgo, actividad):
    if riesgo == "multi-riesgo":
        return "🚨 Suspender actividad inmediatamente y buscar asistencia médica."
    elif riesgo == "hipoxia":
        return "⚠️ Verificar el sensor y oxigenación. Reducir la actividad física."
    elif riesgo == "taquicardia":
        return "💓 Descansar. Si persiste, buscar evaluación médica."
    elif riesgo == "hipertermia":
        return "🌡 Hidratarse y buscar un lugar fresco. Monitorear temperatura."
    else:
        return "✅ Sin riesgos detectados."

# 🔧 Adaptado para Render (no usar solo debug en local)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
