import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import data_manager as dm

# Configuración de Gemini (asegúrate de tener tu .env)
load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("API Key de Gemini no configurada. Crea un archivo .env.")

st.title("🤖 Asistente de Marketing con IA")
st.markdown("Genera comunicaciones personalizadas para los clientes de Kingdom Barber.")

df_clientes, _, _, _ = dm.cargar_datos()

# Selector de cliente
cliente_nombre = st.selectbox("Selecciona un cliente:", options=df_clientes['Nombre'])

# Información del cliente seleccionado
cliente_info = df_clientes[df_clientes['Nombre'] == cliente_nombre].iloc[0]

opcion = st.radio(
    "¿Qué tipo de mensaje quieres generar?",
    ('Recordatorio de Cita', 'Promoción de Cumpleaños', 'Sugerencia de Nuevo Servicio')
)

if st.button(f"Generar Mensaje: {opcion}"):
    prompt = ""
    if opcion == 'Recordatorio de Cita':
        prompt = f"Eres el asistente de Kingdom Barber. Escribe un mensaje de WhatsApp corto y amigable para {cliente_info['Nombre']} recordándole su próxima cita. Invítalo a llegar 5 minutos antes para disfrutar de un café. El tono debe ser moderno y exclusivo."
    elif opcion == 'Promoción de Cumpleaños':
        prompt = f"Eres el asistente de Kingdom Barber. Crea un mensaje de WhatsApp para {cliente_info['Nombre']} felicitándolo por su cumpleaños y ofreciéndole un 20% de descuento en su próximo 'Ritual Completo' como regalo."
    elif opcion == 'Sugerencia de Nuevo Servicio':
        prompt = f"Eres el asistente de Kingdom Barber. Redacta un mensaje para {cliente_info['Nombre']} presentándole un nuevo servicio llamado 'Tratamiento de Keratina para Barba'. Describe brevemente sus beneficios (suavidad y brillo) e invítalo a probarlo en su próxima visita."

    with st.spinner("La IA está creando el mensaje perfecto..."):
        response = model.generate_content(prompt)
        st.subheader("Mensaje Sugerido:")
        st.text_area("Puedes copiar este texto:", response.text, height=200)