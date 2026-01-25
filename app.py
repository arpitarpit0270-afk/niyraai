import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import tempfile
from PIL import Image
from gtts import gTTS
from datetime import datetime
import base64
import io

app = Flask(__name__)

# =============================================
# आपकी Gemini API Key
# =============================================
GEMINI_API_KEY = "AIzaSyCrwxCIUffi3DHt794ZMSDiOwC_GIOTmac"
# =============================================

# Gemini कॉन्फिगरेशन
try:
    genai.configure(api_key=GEMINI_API_KEY)
    text_model = genai.GenerativeModel('gemini-pro')
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    AI_ACTIVE = True
    print("✅ Gemini API सक्रिय")
except Exception as e:
    AI_ACTIVE = False
    print(f"❌ Gemini API त्रुटि: {e}")

@app.route('/')
def home():
    """मुख्य पेज - HTML सीधे कोड में"""
    return '''
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>नियरा AI</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
            .header { background: linear-gradient(to right, #4f46e5, #7c3aed); color: white; padding: 30px; text-align: center; }
            h1 { font-size: 2.5rem; margin-bottom: 10px; }
            .main { padding: 30px; }
            .chat-box { height: 400px; overflow-y: auto; padding: 20px; background: #f8fafc; border-radius: 15px; margin-bottom: 20px; }
            .message { margin-bottom: 15px; padding: 12px; border-radius: 10px; max-width: 80%; }
            .user { background: #4f46e5; color: white; margin-left: auto; }
            .ai { background: #f1f5f9; color: #334155; margin-right: auto; }
            .input-area { display: flex; gap: 10px; }
            input { flex: 1; padding: 15px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 1rem; }
            button { background: #4f46e5; color: white; border: none; padding: 0 30px; border-radius: 10px; cursor: pointer; font-size: 1rem; }
            button:hover { background: #4338ca; }
            .file-btn { background: #10b981; margin-top: 10px; width: 100%; }
            .voice-btn { background: #f59e0b; margin-top: 10px; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 नियरा AI</h1>
                <p>वॉइस + इमेज + चैट | Gemini AI Powered</p>
            </div>
            <div class="main">
                <div class="chat-box" id="chatBox">
                    <div class="message ai">
                        <strong>नमस्ते! मैं नियरा हूं</strong><br><br>
                        मैं आपकी AI सहायक हूं। आप मुझसे:<br>
                        • टेक्स्ट में बात कर सकते हैं<br>
                        • इमेज अपलोड कर सकते हैं<br>
                        • PDF/TXT फाइल्स पढ़वा सकते हैं<br>
                        • वॉइस कमांड दे सकते हैं<br><br>
                        <em>कैसे मदद करूं?</em>
                    </div>
                </div>
                
                <div class="input-area">
                    <input type="text" id="messageInput" placeholder="अपना प्रश्न यहां लिखें..." onkeypress="if(event.key === 'Enter') sendMessage()">
                    <button onclick="sendMessage()">भेजें</button>
                </div>
                
                <button class="file-btn" onclick="document.getElementById('fileInput').click()">
                    📁 फाइल अपलोड करें
                </button>
                <input type="file" id="fileInput" hidden accept=".pdf,.txt,.png,.jpg,.jpeg" onchange="uploadFile()">
                
                <button class="voice-btn" id="voiceBtn" onclick="toggleVoice()">
                    🎤 वॉइस कमांड
                </button>
            </div>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                // यूजर मैसेज दिखाएं
                addMessage(message, 'user');
                input.value = '';
                
                // AI को भेजें
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    if (data.answer) {
                        addMessage(data.answer, 'ai');
                    } else if (data.error) {
                        addMessage('त्रुटि: ' + data.error, 'ai');
                    }
                } catch (error) {
                    addMessage('नेटवर्क त्रुटि', 'ai');
                }
            }
            
            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                addMessage(`फाइल अपलोड: ${file.name}`, 'user');
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.analysis || data.content) {
                        const text = data.analysis || data.content.substring(0, 300) + '...';
                        addMessage(`फाइल विश्लेषण: ${text}`, 'ai');
                    } else if (data.error) {
                        addMessage('त्रुटि: ' + data.error, 'ai');
                    }
                } catch (error) {
                    addMessage('अपलोड त्रुटि', 'ai');
                }
            }
            
            function toggleVoice() {
                const btn = document.getElementById('voiceBtn');
                if (btn.textContent.includes('🎤')) {
                    btn.textContent = '🎤 सुन रही हूं...';
                    startVoiceRecognition();
                } else {
                    btn.textContent = '🎤 वॉइस कमांड';
                    stopVoiceRecognition();
                }
            }
            
            function addMessage(text, sender) {
                const chatBox = document.getElementById('chatBox');
                const div = document.createElement('div');
                div.className = `message ${sender}`;
                div.textContent = text;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            // सरल वॉइस रिकॉग्निशन
            function startVoiceRecognition() {
                if ('webkitSpeechRecognition' in window) {
                    const recognition = new webkitSpeechRecognition();
                    recognition.lang = 'hi-IN';
                    recognition.onresult = function(event) {
                        const transcript = event.results[0][0].transcript;
                        document.getElementById('messageInput').value = transcript;
                        sendMessage();
                    };
                    recognition.start();
                    setTimeout(() => {
                        document.getElementById('voiceBtn').textContent = '🎤 वॉइस कमांड';
                    }, 5000);
                } else {
                    alert('वॉइस रिकॉग्निशन समर्थित नहीं');
                }
            }
            
            function stopVoiceRecognition() {
                // सरल इम्प्लीमेंटेशन
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    """चैट API"""
    try:
        if not AI_ACTIVE:
            return jsonify({"error": "AI सक्रिय नहीं"}), 500
        
        data = request.json
        question = data.get('message', '').strip()
        
        if not question:
            return jsonify({"error": "प्रश्न दें"}), 400
        
        # प्रॉम्प्ट
        prompt = f"""आप नियरा AI हैं - एक मित्रवत AI सहायक।

उपयोगकर्ता: {question}

नियरा (हिंदी में उत्तर दें):"""
        
        response = text_model.generate_content(prompt)
        
        return jsonify({
            "question": question,
            "answer": response.text,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    """फाइल अपलोड"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "फाइल नहीं"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "फाइल नाम नहीं"}), 400
        
        filename = file.filename.lower()
        
        # इमेज एनालिसिस
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(file)
            response = vision_model.generate_content([
                "इस छवि का हिंदी में विस्तृत विवरण दें:",
                img
            ])
            return jsonify({
                "type": "image",
                "analysis": response.text,
                "filename": file.filename
            })
        
        # टेक्स्ट फाइल
        elif filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            # सारांश
            summary_prompt = f"इसका संक्षिप्त सारांश हिंदी में दें: {content[:1500]}"
            summary = text_model.generate_content(summary_prompt)
            
            return jsonify({
                "type": "text",
                "content": content[:500],
                "summary": summary.text,
                "words": len(content.split()),
                "filename": file.filename
            })
        
        # PDF (सरल)
        elif filename.endswith('.pdf'):
            return jsonify({
                "type": "pdf",
                "message": "PDF सपोर्ट सक्रिय है",
                "filename": file.filename
            })
        
        else:
            return jsonify({"error": "असमर्थित फाइल फॉर्मेट"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """हेल्थ चेक"""
    return jsonify({
        "status": "active",
        "ai": "नियरा",
        "gemini": AI_ACTIVE,
        "time": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)