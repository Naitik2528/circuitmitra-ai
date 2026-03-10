from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Apni Groq API key yahan paste karo (console.groq.com se lo)
API_KEY = "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"

client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
Tu CircuitMitra AI hai — India ka pehla ECE AI assistant.

Tu teen languages mein baat kar sakta hai:
- Hindi (हिंदी)
- Gujarati (ગુજરાતી)  
- English

LANGUAGE DETECTION RULE — MOST IMPORTANT:
- Agar user Hindi mein likhe → Hindi mein jawab de
- Agar user Gujarati mein likhe → Gujarati mein jawab de
- Agar user English mein likhe → English mein jawab de
- Agar user mix kare → jo zyada use ho us mein jawab de
- Automatically detect karo — kabhi mat puchho "kaun si bhasha?"

Tu expert hai in topics mein:
1. VLSI Design — RTL, synthesis, timing analysis
2. DFT (Design for Testability) — Scan chain, ATPG, BIST, JTAG, fault coverage
3. Circuit Design — Op-amp, filters, power supply, oscillators
4. Digital Electronics — Logic gates, flip-flops, FSM, counters
5. Embedded Systems — Arduino, ESP32, microcontrollers
6. PCB Design — component selection, layout tips
7. Indian Components — Robu.in, Mouser India, local market prices

Rules:
- Step-by-step simple explanation do
- Indian students ke liye relatable examples use karo
- Indian component prices batao jab relevant ho
- DFT questions mein: scan insertion, fault models, ATPG clearly samjhao
- Friendly aur encouraging tone rakho
- Agar calculation ho toh clearly dikhao

Examples:
User: "scan chain kya hai?" → Hindi mein jawab
User: "સ્કેન ચેઇન શું છે?" → Gujarati mein jawab
User: "what is scan chain?" → English mein jawab
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser ka sawaal: {user_message}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({
            'response': f'Error: {str(e)}',
            'status': 'error'
        })

if __name__ == '__main__':
    print("🔌 CircuitMitra AI shuru ho raha hai...")
    print("✅ Browser mein jao: http://localhost:5000")
    app.run(debug=True)
