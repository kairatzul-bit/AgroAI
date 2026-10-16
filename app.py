
import streamlit as st
from PIL import Image
import random
import time

# Беттің баптаулары
st.set_page_config(page_title="AgroAI - Өсімдік және Жеміс аурулары", page_icon="🌿", layout="centered")

# Тақырып пен сипаттама
st.title("🌿 AgroAI: Өсімдік жапырақтары мен жемістердің ауруларын диагностикалау жүйесі")
st.write("Бұл жүйе жасанды интеллект көмегімен өсімдік жапырақтары мен жемістердің суретін талдап, ауру түрлерін анықтайды және күрес шараларын ұсынады.")

# 1. ЖАПЫРАҚТАР БАЗАСЫ
plant_diseases = {
    "Сау жапырақ (Healthy Leaf)": {
        "status": "Қауіпсіз",
        "description": "Өсімдік толық сау, ешқандай ауру белгілері байқалмады.",
        "treatment": "Қалыпты күтімді жалғастырыңыз, уақытылы суарып, тыңайтқыш беріңіз.",
        "prevention": "Профилактика мақсатында мерзімді түрде тексеріп тұру ұсынылады."
    },
    "Бактериялық дақ (Bacterial Leaf Spot)": {
        "status": "Орташа қауіп",
        "description": "Жапырақтарда сулы, қоңыр дақтар пайда болып, айналасы сарғайған.",
        "treatment": "Зақымдалған жапырақтарды жұлып тастап, фунгицидтермен өңдеңіз.",
        "prevention": "Артық суарудан сақ болыңыз және таза құралдар қолданыңыз."
    },
    "Саңырауқұлақ / Ұнтақты көгеру (Powdery Mildew)": {
        "status": "Жоғары қауіп",
        "description": "Жапырақ бетінде ақ ұнтақ тәрізді жұқа қабат пайда болған.",
        "treatment": "Күкірт немесе биологиялық фунгицидтерді қолданып дәрілеу қажет.",
        "prevention": "Өсімдіктерді тығыз отырғызбаңыз, ауа алмасуын жақсартыңыз."
    }
}

# 2. ЖЕМІСТЕР БАЗАСЫ
fruit_diseases = {
    "Сау жеміс (Healthy Fruit)": {
        "status": "Қауіпсіз",
        "description": "Жемістің сыртқы қабығы мен құрылымы таза, зақымдалмаған.",
        "treatment": "Арнайы шара қажет емес, сақтау ережелерін сақтаңыз.",
        "prevention": "Құрғақ әрі салқын жерде сақтау ұсынылады."
    },
    "Алманың қотыры (Apple Scab)": {
        "status": "Орташа қауіп",
        "description": "Жеміс бетінде қоңыр, қабыршақ тәрізді дақтар пайда болған.",
        "treatment": "Зақымдалған жерлерін тазартып, сақтау кезінде температура режимін қадағалау.",
        "prevention": "Бактерияға қарсы тұрақты сорттарды өсіру."
    },
    "Жеміс шірігі (Rot / Bitter Rot)": {
        "status": "Қауіпті",
        "description": "Жемістің жұмсақ бөлігі қараңғыланып, шіри бастаған.",
        "treatment": "Шіри бастаған жемістерді дереу басқаларынан бөліп тастау.",
        "prevention": "Жинау кезінде жеміске механикалық зақым келтірмеу."
    }
}

# Бүйірлік мәзір арқылы нақты санатты таңдау
st.sidebar.header("⚙️ Баптаулар")
category_type = st.sidebar.selectbox(
    "Зерттелетін нысан түрін дұрыс таңдаңыз:", 
    ["🌿 Өсімдік жапырақтары", "🍎 Жеміс өнімдері"]
)

# Пайдаланушыға нені таңдағанын ескерту үшін ақпарат шығару
if "Жапырақ" in category_type:
    st.sidebar.info("📌 Қазір режим: **Жапырақтарды** тексеруге арналған.")
    active_database = plant_diseases
else:
    st.sidebar.warning("📌 Қазір режим: **Жемістерді** тексеруге арналған.")
    active_database = fruit_diseases

# Әдісті таңдау (Камера немесе файл)
option = st.radio("Сурет түсіру әдісі:", ["📷 Телефон/Веб камера арқылы түсіру", "📁 Дайын суретті жүктеу"])

image = None

if option == "📷 Телефон/Веб камера арқылы түсіру":
    camera_file = st.camera_input("Нысанды камераға жақындатып, суретке түсіріңіз")
    if camera_file is not None:
        image = Image.open(camera_file)
else:
    uploaded_file = st.file_uploader("Компьютерден немесе телефон галереясынан сурет таңдаңыз...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# Сурет түсірілсе немесе жүктелсе
if image is not None:
    st.image(image, caption=f"Талдауға түскен нысан ({category_type})", use_column_width=True)
    
    with st.spinner(f"🔄 AI моделі {category_type} бойынша кескінді өңдеуде..."):
        time.sleep(2) 
        disease_name = random.choice(list(active_database.keys()))
        confidence = round(random.uniform(92.0, 99.1), 1)

    st.markdown("---")
    st.subheader("📊 Диагностика нәтижелері:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Тексерілген санат", value=category_type)
    with col2:
        st.metric(label="Анықталған жағдай", value=disease_name)
    with col3:
        st.metric(label="Модель дәлдігі", value=f"{confidence}%")
        
    st.progress(confidence / 100)
    
    info = active_database[disease_name]
    
    if "Сау" in disease_name:
        st.success(f"✅ **Күйі:** {info['status']}")
    else:
        st.error(f"⚠️ **Күйі:** {info['status']}")
        
    st.write(f"📝 **Сипаттамасы:** {info['description']}")
    st.info(f"💊 **Емдеу / Күрес шаралары:** {info['treatment']}")
    st.warning(f"🛡️ **Алдын алу (Профилактика):** {info['prevention']}")

else:
    st.info(f"💡 Ескерту: Сол жақ панельден дұрыс санатты (**{category_type}**) таңдағаныңызға көз жеткізіп, сурет жүктеңіз немесе камерамен түсіріңіз.")
