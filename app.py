import os
from datetime import datetime

import google.generativeai as genai
from flask import Flask, jsonify, request
from PIL import Image
from PyPDF2 import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_MB", "8")) * 1024 * 1024

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
TEXT_MODEL_NAME = os.environ.get("GEMINI_TEXT_MODEL", "gemini-1.5-flash")
VISION_MODEL_NAME = os.environ.get("GEMINI_VISION_MODEL", TEXT_MODEL_NAME)

AI_ACTIVE = False
text_model = None
vision_model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        text_model = genai.GenerativeModel(TEXT_MODEL_NAME)
        vision_model = genai.GenerativeModel(VISION_MODEL_NAME)
        AI_ACTIVE = True
        print("✅ Gemini API सक्रिय")
    except Exception as exc:
        print(f"❌ Gemini API त्रुटि: {exc}")
else:
    print("⚠️ GEMINI_API_KEY सेट नहीं है; ऐप demo mode में चलेगा")


def ai_reply(prompt):
    """Return a Gemini response, or a helpful demo-mode message."""
    if not AI_ACTIVE or text_model is None:
        return (
            "Demo mode: AI चलाने के लिए deployment settings में GEMINI_API_KEY add करें. "
            "आपका message app तक सही पहुंच रहा है."
        )
    response = text_model.generate_content(prompt)
    return getattr(response, "text", "").strip() or "माफ़ कीजिए, अभी उत्तर नहीं मिला।"


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>नियरा AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: Inter, Arial, sans-serif; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
            .container { max-width: 860px; margin: 0 auto; background: white; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
            .header { background: linear-gradient(to right, #4f46e5, #7c3aed); color: white; padding: 32px; text-align: center; }
            h1 { font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 10px; }
            .main { padding: 28px; }
            .chat-box { height: 430px; overflow-y: auto; padding: 20px; background: #f8fafc; border-radius: 18px; margin-bottom: 18px; border: 1px solid #e2e8f0; }
            .message { margin-bottom: 14px; padding: 13px 15px; border-radius: 14px; max-width: 82%; line-height: 1.45; white-space: pre-wrap; }
            .user { background: #4f46e5; color: white; margin-left: auto; }
            .ai { background: #eef2ff; color: #26314d; margin-right: auto; }
            .input-area { display: flex; gap: 10px; }
            input { flex: 1; padding: 15px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; }
            button { background: #4f46e5; color: white; border: none; padding: 0 24px; border-radius: 12px; cursor: pointer; font-size: 1rem; font-weight: 700; min-height: 50px; }
            button:hover { filter: brightness(0.95); }
            button:disabled { opacity: 0.65; cursor: not-allowed; }
            .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
            .file-btn { background: #10b981; width: 100%; }
            .voice-btn { background: #f59e0b; width: 100%; }
            .status { color: #64748b; font-size: 0.9rem; margin-top: 12px; text-align: center; }
            @media (max-width: 640px) { .input-area, .actions { grid-template-columns: 1fr; display: grid; } .message { max-width: 96%; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 नियरा AI</h1>
                <p>Hindi chat, image analysis, PDF/TXT reader और voice input</p>
            </div>
            <div class="main">
                <div class="chat-box" id="chatBox">
                    <div class="message ai"><strong>नमस्ते! मैं नियरा हूं।</strong><br><br>आप chat कर सकते हैं, image/PDF/TXT upload कर सकते हैं, या voice command दे सकते हैं।</div>
                </div>
                <div class="input-area">
                    <input type="text" id="messageInput" placeholder="अपना प्रश्न यहां लिखें..." onkeypress="if(event.key === 'Enter') sendMessage()">
                    <button id="sendBtn" onclick="sendMessage()">भेजें</button>
                </div>
                <div class="actions">
                    <button class="file-btn" onclick="document.getElementById('fileInput').click()">📁 फाइल अपलोड करें</button>
                    <button class="voice-btn" id="voiceBtn" onclick="startVoiceRecognition()">🎤 वॉइस कमांड</button>
                </div>
                <input type="file" id="fileInput" hidden accept=".pdf,.txt,.png,.jpg,.jpeg" onchange="uploadFile()">
                <p class="status" id="status">Ready</p>
            </div>
        </div>
        <script>
            const chatBox = document.getElementById('chatBox');
            const statusEl = document.getElementById('status');
            function setLoading(isLoading, text = 'Ready') {
                document.getElementById('sendBtn').disabled = isLoading;
                statusEl.textContent = text;
            }
            function addMessage(text, sender) {
                const div = document.createElement('div');
                div.className = `message ${sender}`;
                div.textContent = text;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                addMessage(message, 'user');
                input.value = '';
                setLoading(true, 'AI सोच रही है...');
                try {
                    const response = await fetch('/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
                    const data = await response.json();
                    addMessage(data.answer || `त्रुटि: ${data.error || 'Unknown error'}`, 'ai');
                } catch (error) {
                    addMessage('नेटवर्क त्रुटि. कृपया फिर कोशिश करें.', 'ai');
                } finally {
                    setLoading(false);
                }
            }
            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                if (!file) return;
                const formData = new FormData();
                formData.append('file', file);
                addMessage(`फाइल अपलोड: ${file.name}`, 'user');
                setLoading(true, 'फाइल पढ़ी जा रही है...');
                try {
                    const response = await fetch('/upload', { method: 'POST', body: formData });
                    const data = await response.json();
                    addMessage(data.analysis || data.summary || data.content || `त्रुटि: ${data.error || 'Unknown error'}`, 'ai');
                } catch (error) {
                    addMessage('अपलोड त्रुटि. कृपया फिर कोशिश करें.', 'ai');
                } finally {
                    fileInput.value = '';
                    setLoading(false);
                }
            }
            function startVoiceRecognition() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    addMessage('इस browser में voice recognition supported नहीं है.', 'ai');
                    return;
                }
                const recognition = new SpeechRecognition();
                recognition.lang = 'hi-IN';
                recognition.onstart = () => statusEl.textContent = 'सुन रही हूं...';
                recognition.onresult = (event) => {
                    document.getElementById('messageInput').value = event.results[0][0].transcript;
                    sendMessage();
                };
                recognition.onend = () => statusEl.textContent = 'Ready';
                recognition.start();
            }
        </script>
    </body>
    </html>
    """


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("message", "").strip()
    if not question:
        return jsonify({"error": "प्रश्न दें"}), 400
    prompt = f"""आप नियरा AI हैं - एक मित्रवत हिंदी AI सहायक।

उपयोगकर्ता: {question}

नियरा:"""
    return jsonify({"question": question, "answer": ai_reply(prompt), "timestamp": datetime.now().strftime("%H:%M:%S")})


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "फाइल नहीं"}), 400
    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "फाइल नाम नहीं"}), 400

    filename = uploaded_file.filename.lower()
    try:
        if filename.endswith((".png", ".jpg", ".jpeg")):
            if not AI_ACTIVE or vision_model is None:
                return jsonify({"type": "image", "analysis": "Image upload ठीक है. Image AI analysis के लिए GEMINI_API_KEY set करें.", "filename": uploaded_file.filename})
            image = Image.open(uploaded_file.stream)
            response = vision_model.generate_content(["इस छवि का हिंदी में विस्तृत विवरण दें:", image])
            return jsonify({"type": "image", "analysis": response.text, "filename": uploaded_file.filename})

        if filename.endswith(".txt"):
            content = uploaded_file.read().decode("utf-8", errors="replace")
            summary = ai_reply(f"इस text का संक्षिप्त सारांश हिंदी में दें:\n\n{content[:4000]}")
            return jsonify({"type": "text", "content": content[:800], "summary": summary, "words": len(content.split()), "filename": uploaded_file.filename})

        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file.stream)
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:5]).strip()
            if not text:
                return jsonify({"error": "PDF से text नहीं पढ़ पाया"}), 400
            summary = ai_reply(f"इस PDF text का संक्षिप्त सारांश हिंदी में दें:\n\n{text[:4000]}")
            return jsonify({"type": "pdf", "content": text[:1000], "summary": summary, "pages_read": min(len(reader.pages), 5), "filename": uploaded_file.filename})

        return jsonify({"error": "असमर्थित फाइल फॉर्मेट"}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "active", "ai": "नियरा", "gemini": AI_ACTIVE, "model": TEXT_MODEL_NAME if AI_ACTIVE else "demo", "time": datetime.now().isoformat()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
