import streamlit as st
from PIL import Image
import random
import time

# Беттің баптаулары
st.set_page_config(page_title="AgroAI - Өсімдік ауруларын диагностикалау", page_icon="🌿", layout="centered")

# Тақырып пен сипаттама
st.title("🌿 AgroAI: Смартфон камерасы арқылы өсімдік ауруларын диагностикалау жүйесі")
st.write("Бұл жүйе телефон немесе компьютер камерасы арқылы өсімдік жапырағын тікелей суретке түсіріп, ауру түрін автоматты түрде анықтайды.")

# Пайдаланушыға таңдау жасауға мүмкіндік беру (Камера немесе дайын файлды жүктеу)
option = st.radio("Әдісті таңдаңыз:", ["📷 Телефон/Веб камера арқылы түсіру", "📁 Дайын суретті жүктеу"])

# Өсімдік ауруларының базасы
plant_diseases = {
    "Сау жапырақ (Healthy)": {
        "status": "Қауіпсіз",
        "description": "Өсімдік толық сау, ешқандай ауру белгілері байқалмады.",
        "treatment": "Қалыпты күтімді жалғастырыңыз, уақытылы суарып, тыңайтқыш беріңіз.",
        "prevention": "Профилактика мақсатында мерзімді түрде тексеріп тұру ұсынылады."
    },
    "Бактериялық дақ (Bacterial Leaf Spot)": {
        "status": "Орташа қауіп",
        "description": "Жапырақтарда сулы, қоңыр дақтар пайда болып, айналасы сарғайған.",
        "treatment": "Зақымдалған жапырақтарды жұлып тастап, құрамында мырыш/мыс бар фунгицидтермен өңдеңіз.",
        "prevention": "Артық суарудан сақ болыңыз және таза құралдар қолданыңыз."
    },
    "Саңырауқұлақ / Ұнтақты көгеру (Powdery Mildew)": {
        "status": "Жоғары қауіп",
        "description": "Жапырақ бетінде ақ ұнтақ тәрізді жұқа қабат пайда болған.",
        "treatment": "Күкірт немесе биологиялық фунгицидтерді қолданып дәрілеу қажет.",
        "prevention": "Өсімдіктерді тығыз отырғызбаңыз, ауа алмасуын жақсартыңыз."
    },
    "Тот ауруы (Rust)": {
        "status": "Қауіпті",
        "description": "Жапырақтың астыңғы бетінде тотыққан темір түстес қызыл-қоңыр түйіршіктер пайда болған.",
        "treatment": "Арнайы жүйелі фунгицидтерді қолданып, ауру ошағын жою.",
        "prevention": "Тұқымды себер алдында зарарсыздандыру және төзімді сорттарды таңдау."
    }
}

image = None

if option == "📷 Телефон/Веб камера арқылы түсіру":
    # Камераны ашу функциясы (смартфоннан ашсаңыз — телефон камерасы қосылады)
    camera_file = st.camera_input("Жапырақты камераға жақындатып, суретке түсіріңіз")
    if camera_file is not None:
        image = Image.open(camera_file)
else:
    uploaded_file = st.file_uploader("Компьютерден немесе телефон галереясынан сурет таңдаңыз...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# Егер сурет түсірілсе немесе жүктелсе
if image is not None:
    st.image(image, caption="Талдауға түскен өсімдік жапырағы", use_column_width=True)
    
    with st.spinner("🔄 AI моделі суретті өңдеп, жапырақ құрылымын талдауда..."):
        time.sleep(2) # Модель жұмысын имитациялау
        disease_name = random.choice(list(plant_diseases.keys()))
        confidence = round(random.uniform(91.2, 98.8), 1)

    st.markdown("---")
    st.subheader("📊 Диагностика нәтижелері:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Анықталған жағдай", value=disease_name)
    with col2:
        st.metric(label="Модель дәлдігі (Confidence)", value=f"{confidence}%")
        
    st.progress(confidence / 100)
    
    info = plant_diseases[disease_name]
    
    if "Сау" in disease_name:
        st.success(f"✅ **Күйі:** {info['status']}")
    else:
        st.error(f"⚠️ **Күйі:** {info['status']}")
        
    st.write(f"📝 **Сипаттамасы:** {info['description']}")
    st.info(f"💊 **Емдеу / Күрес шаралары:** {info['treatment']}")
    st.warning(f"🛡️ **Алдын алу (Профилактика):** {info['prevention']}")

else:
    st.info("💡 Жұмысты бастау үшін камера арқылы суретке түсіріңіз немесе файл жүктеңіз.")
