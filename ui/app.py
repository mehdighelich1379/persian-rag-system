import requests
import gradio as gr


# Backend API
API_URL = "http://127.0.0.1:8000/generate"

def ask_rag(question):
    if not question.strip():
        return "❗ لطفاً یک سؤال وارد کنید."

    try:
        payload = {"query": question}
        r = requests.post(API_URL, json=payload, timeout=60)
        r.raise_for_status()
        return r.json().get("answer", "⚠️ پاسخ نامعتبر از سرور دریافت شد.")
    except Exception as e:
        return f"❌ خطا در ارتباط با سرور:\n{e}"



# Custom CSS (Dark + Glass + RTL)
custom_css = """
body {
    background: radial-gradient(circle at top, #1f2937, #020617);
    color: #e5e7eb;
    font-family: Inter, sans-serif;
}

.gradio-container {
    background: transparent !important;
    direction: rtl;
    text-align: right;
}

.markdown {
    direction: rtl;
    text-align: right;
    line-height: 1.9;
    font-size: 15px;
}

textarea, input {
    direction: rtl;
    text-align: right;
    background: rgba(15, 23, 42, 0.8) !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

.glass {
    backdrop-filter: blur(14px);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 24px;
}

button {
    background: linear-gradient(135deg, #6366f1, #22d3ee) !important;
    color: #020617 !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
}

button:hover {
    transform: scale(1.02);
    transition: 0.2s ease;
}
"""


# UI
with gr.Blocks(css=custom_css, title="Persian RAG Resume Assistant") as demo:
    gr.Markdown(
        """
        <div class="glass" style="text-align:center">
            <h2 style="margin-bottom:8px">🤖 Persian RAG Resume Assistant</h2>
            <p style="opacity:0.75; font-size:14px">
                راهنمای هوشمند رزومه و استخدام (RAG فارسی)
            </p>
        </div>
        """
    )

    with gr.Column(elem_classes="glass"):
        inp = gr.Textbox(
            label="سؤال شما",
            placeholder="مثلاً: ریکروترها به چه رزومه‌هایی توجه می‌کنند؟",
            lines=3
        )

        out = gr.Markdown(label="پاسخ سیستم")

        btn = gr.Button("ارسال سؤال 🚀")

        btn.click(fn=ask_rag, inputs=inp, outputs=out)

demo.launch(
    server_name="127.0.0.1",
    server_port=7861,
    share=False,
    inbrowser=True
)
