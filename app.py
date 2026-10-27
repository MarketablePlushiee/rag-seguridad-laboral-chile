import os
import streamlit as st
from rag_engine import query_rag

# Configuración de la página
st.set_page_config(
    page_title="IntegraSST - Asistente Normativo de Seguridad Laboral",
    page_icon="🛡️",
    layout="wide"
)

# Título Principal y Encabezado
st.title("🛡️ IntegraSST: Asistente Normativo de Seguridad Laboral")
st.caption("Consulta inteligente basada en la legislación chilena vigente (Ley 16.744, DS 594, DS 44 y Código del Trabajo).")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configuración del Modelo")
    
    provider = st.selectbox(
        "Proveedor de LLM:",
        ["Google Gemini", "Groq"]
    )
    
    st.warning(
        "💡 **Recomendación:** Si no estás seguro de qué proveedor elegir, "
        "te sugerimos mantener la opción predeterminada, "
        "la cual está optimizada para la precisión de este asistente."
    )
    
    # Obtención segura de la API Key en segundo plano (sin mostrarla en la UI)
    system_gemini_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    system_groq_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
    
    default_key = system_gemini_key if provider == "Google Gemini" else system_groq_key
    
    # Campo opcional por si el usuario desea ingresar su propia clave privada
    with st.expander("🔑 Utilizar clave de API propia (Opcional)"):
        custom_key = st.text_input(
            f"Ingresa tu {provider} API Key:",
            type="password",
            help="Déjalo en blanco para utilizar la API Key del sistema."
        )
    
    api_key = custom_key.strip() if custom_key.strip() else default_key

    st.divider()

    # --- SECCIÓN DE SCOPE / BASE DE DATOS ---
    st.header("📚 Scope de Conocimiento")
    st.markdown(
        """
        Este asistente RAG responde **únicamente** con base en la siguiente normativa chilena cargada en el sistema:
        
        * 📜 **Ley N° 16.744:** Seguro Social sobre Accidentes del Trabajo y Enfermedades Profesionales.
        * 📜 **Decreto Supremo N° 594:** Condiciones Sanitarias y Ambientales Básicas en los Lugares de Trabajo.
        * 📜 **Decreto N° 44 (2024):** Gestión Preventiva de Riesgos Laborales.
        * 📜 **Código del Trabajo:** Artículos 184 y 184 bis (Protección y Riesgo Inminente).
        """
    )

    st.divider()

    # --- SECCIÓN DE DESCARGA DE DOCUMENTOS FUENTE ---
    st.header("📥 Descargar Fuentes Oficiales")
    st.caption("Comprueba la veracidad consultando los PDFs originales:")

    DATA_DIR = "./data"
    if os.path.exists(DATA_DIR):
        pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
        if pdf_files:
            for pdf in pdf_files:
                pdf_path = os.path.join(DATA_DIR, pdf)
                with open(pdf_path, "rb") as file_data:
                    st.download_button(
                        label=f"📄 {pdf}",
                        data=file_data.read(),
                        file_name=pdf,
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.info("No se encontraron archivos PDF en el directorio de datos.")
    else:
        st.warning("Carpeta de datos no encontrada.")

# --- HISTORIAL DE CHAT EN LA PÁGINA PRINCIPAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ENTRADA DE USUARIO Y PROCESAMIENTO ---
if prompt_input := st.chat_input("Ej: ¿Cuáles son las obligaciones del empleador ante un riesgo grave e inminente?"):
    if not api_key:
        st.error("⚠️ No se detectó una API Key válida. Por favor, configura la clave del sistema o ingresa una en el panel izquierdo.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Consultando base normativa y vectorizando datos..."):
            try:
                answer, retrieved_docs = query_rag(prompt_input, provider, api_key)
                st.markdown(answer)
                
                # Desplegable de evidencias recuperadas
                with st.expander("🔍 Ver artículos normativos consultados (Fuentes RAG)"):
                    for idx, doc in enumerate(retrieved_docs, 1):
                        src = doc.metadata.get("source", "Documento")
                        st.markdown(f"**Fuente {idx}:** `{src}`")
                        st.caption(doc.page_content[:400] + "...")
                        st.divider()
                        
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"❌ Error al procesar la consulta: {str(e)}")
