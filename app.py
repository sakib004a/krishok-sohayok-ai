import os
import gradio as gr
from PIL import Image
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY Environment Variable পাওয়া যায়নি!")

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_plant_health(image):
    if image is None:
        return "⚠️ অনুগ্রহ করে একটি ছবি আপলোড করুন অথবা ক্যামেরা দিয়ে ছবি তুলুন।"
    try:
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        image = image.convert("RGB")
        image.thumbnail((800, 800))

        prompt = """
তুমি একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ এবং Plant Disease Detection AI।
ছবিটি বিশ্লেষণ করে সহজ ও পরিষ্কার বাংলায় উত্তর দাও।

১. 🌱 ফসল/গাছের অবস্থা: গাছটি সুস্থ নাকি অসুস্থ?
২. 🦠 সম্ভাব্য রোগ বা সমস্যা: রোগ, পোকা, ছত্রাক, ভাইরাস, ব্যাকটেরিয়া বা পুষ্টির ঘাটতি। সম্ভব হলে বাংলা ও ইংরেজি নাম দাও। নিশ্চিত না হলে অনুমানকে নিশ্চিত রোগ বলবে না।
৩. 🔍 দৃশ্যমান লক্ষণ: ছবিতে কী কী লক্ষণ দেখা যাচ্ছে?
৪. 💊 সমাধান: প্রাকৃতিক/ঘরোয়া, জৈব এবং প্রয়োজন হলে রাসায়নিক ব্যবস্থা ও নিরাপদ প্রয়োগের পরামর্শ দাও। রাসায়নিক ব্যবহারে পণ্যের লেবেল এবং স্থানীয় কৃষি কর্মকর্তার নির্দেশনা মানতে বলো।
৫. 🛡️ প্রতিরোধ: পানি, সার ও পরিচর্যার পরামর্শ দাও।
৬. 📊 নিশ্চিত হওয়ার মাত্রা: আনুমানিক confidence দাও। ছবি অস্পষ্ট হলে তা জানিয়ে পরিষ্কার ছবি চাইবে।
গাছ সুস্থ হলে সেটি জানিয়ে সাধারণ পরিচর্যার পরামর্শ দাও। গাছ শনাক্ত করা না গেলে রোগ নির্ণয় করবে না।
"""
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[image, prompt]
        )
        return response.text or "⚠️ Gemini কোনো উত্তর দেয়নি। আবার চেষ্টা করুন।"
    except Exception as e:
        return f"""## ❌ বিশ্লেষণ করা যায়নি

সম্ভাব্য কারণ: API Key, Gemini model availability, quota/rate limit,
ইন্টারনেট সংযোগ অথবা API permission সমস্যা।

**সার্ভারের বার্তা:**
`{str(e)}`

কিছুক্ষণ পর আবার চেষ্টা করুন। API quota শেষ হলে quota reset বা উপযুক্ত limit প্রয়োজন হতে পারে।
"""


CSS = r"""
.gradio-container {
  max-width: 1120px !important; margin: 0 auto !important;
  background: #f5f7ef !important;
  font-family: 'Noto Sans Bengali','Hind Siliguri',sans-serif !important;
}
footer {display:none !important}
#hero {
  background:linear-gradient(120deg,#103b2b,#1d6846 68%,#2d8054);
  color:white;border-radius:26px;padding:30px 34px;margin:8px 0 20px;
  box-shadow:0 14px 35px rgba(18,60,45,.16);
}
#hero .eyebrow {color:#d7f2a0;font-size:13px;font-weight:800;letter-spacing:1.5px}
#hero h1 {color:white;font-size:clamp(28px,4vw,42px);margin:8px 0}
#hero p {color:#e6f2e9;font-size:16px;max-width:700px;line-height:1.8}
#hero .pill {display:inline-block;padding:7px 13px;border-radius:30px;background:#ffffff20;color:#f2ffd7;font-size:12px}
.panel {background:white;border:1px solid #e4eadf;border-radius:20px;padding:18px;box-shadow:0 8px 24px #143c280b}
.section-title {color:#153e2e;font-weight:800;font-size:20px;margin:4px 0}
.section-sub {color:#64756b;font-size:13px;margin-bottom:10px}
#scan-btn {background:linear-gradient(100deg,#1b6847,#2b8a58)!important;border:0!important;color:white!important;font-weight:800!important;border-radius:14px!important;min-height:52px}
#clear-btn {border-radius:14px!important;min-height:48px}
#result {background:white;border:1px solid #e4eadf;border-radius:20px;padding:20px;min-height:300px;color:#24382d}
#tips {background:#edf5df;border:1px solid #dce9c8;border-radius:18px;padding:15px 18px;color:#294a35;line-height:1.8}
#footer-note{text-align:center;color:#758278;font-size:12px;padding:18px 0 6px}
"""

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="green", secondary_hue="lime", neutral_hue="slate"),
    css=CSS,
    title="কৃষক সহায়ক | AI Plant Doctor"
) as demo:
    gr.HTML("""
    <div id="hero">
      <div class="eyebrow">SMART FARMING • AI POWERED</div>
      <h1>🌾 কৃষক সহায়ক</h1>
      <p>আপনার গাছের স্বাস্থ্য জানুন সহজেই। ছবি আপলোড করুন অথবা ক্যামেরা দিয়ে ছবি তুলুন—
      AI আপনাকে সম্ভাব্য সমস্যা ও করণীয় বুঝতে সাহায্য করবে।</p>
      <span class="pill">🌱 আপনার ফসল, আমাদের যত্ন</span>
    </div>
    """)
    with gr.Row():
        with gr.Column(scale=5, elem_classes=["panel"]):
            gr.HTML('<div class="section-title">📸 গাছের ছবি দিন</div><div class="section-sub">পাতা, ফল, ফুল বা পুরো গাছের পরিষ্কার ছবি ব্যবহার করুন।</div>')
            plant_image = gr.Image(
                sources=["upload", "webcam"], type="pil",
                label="ছবি আপলোড / ক্যামেরা", height=330
            )
            with gr.Row():
                scan_btn = gr.Button("🔍 গাছের স্বাস্থ্য পরীক্ষা করুন", variant="primary", elem_id="scan-btn")
                clear_btn = gr.ClearButton([plant_image], value="↻ মুছে ফেলুন", elem_id="clear-btn")
            gr.HTML("""
            <div id="tips"><b>📌 ভালো ফলাফলের জন্য</b><br>
            • পর্যাপ্ত আলোতে ছবি তুলুন<br>• আক্রান্ত পাতার কাছ থেকে পরিষ্কার ছবি দিন<br>
            • একবারে একটি গাছ বা একটি সমস্যার ছবি দিন</div>
            """)
        with gr.Column(scale=6):
            gr.HTML('<div class="section-title">🩺 AI কৃষি ডাক্তারের রিপোর্ট</div><div class="section-sub">ছবি বিশ্লেষণের পর ফলাফল এখানে দেখা যাবে।</div>')
            result = gr.Markdown(
                "### 🌿 আপনার গাছের রিপোর্ট এখানে দেখা যাবে\n\nবাম পাশ থেকে ছবি দিন, তারপর **গাছের স্বাস্থ্য পরীক্ষা করুন** বাটনে চাপ দিন।",
                elem_id="result"
            )
    gr.HTML('<div id="footer-note">কৃষক সহায়ক • AI-ভিত্তিক প্রাথমিক পরামর্শ • চূড়ান্ত রোগ নির্ণয় ও কীটনাশক ব্যবহারে স্থানীয় কৃষি বিশেষজ্ঞের পরামর্শ নিন।</div>')
    scan_btn.click(analyze_plant_health, inputs=plant_image, outputs=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.queue().launch(server_name="0.0.0.0", server_port=port)
