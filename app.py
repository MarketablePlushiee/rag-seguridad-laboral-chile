import streamlit as st
from rag_engine import query_rag

st.set_page_config(
    page_title="Asistente RAG - Normativa de Seguridad Laboral Chile",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Asistente Jurídico RAG: Seguridad Laboral Chile")
st.caption("Consulta basada en Ley 16.744, DS 594, DS 44 y Código del Trabajo (Art. 184 / 184 bis)")

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configuración del Modelo")
    
    provider = st.selectbox(
        "Selecciona el proveedor de LLM:",
        ["Google Gemini", "Groq"]
    )
    
    DEFAULT_GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    DEFAULT_GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    
    if provider == "Google Gemini":
        api_key = st.text_input("Gemini API Key:", value=DEFAULT_GEMINI_KEY, type="password")
    else:
        api_key = st.text_input("Groq API Key:", value=DEFAULT_GROQ_KEY, type="password")
        
    st.info("💡 Este asistente consulta directamente el texto oficial de la legislación chilena.")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt_input := st.chat_input("Ej: ¿Cuáles son las obligaciones del empleador ante un riesgo grave e inminente?"):
    if not api_key:
        st.error("Por favor ingresa una API Key válida en el panel izquierdo para continuar.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Procesando consulta y vectorizando documentos si es la primera ejecución..."):
            try:
                answer, retrieved_docs = query_rag(prompt_input, provider, api_key)
                st.markdown(answer)
                
                with st.expander("📚 Ver artículos normativos consultados (Fuentes RAG)"):
                    for idx, doc in enumerate(retrieved_docs, 1):
                        src = doc.metadata.get("source", "Documento")
                        st.markdown(f"**Fuente {idx}:** `{src}`")
                        st.caption(doc.page_content[:400] + "...")
                        st.divider()
                        
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error al procesar la consulta: {str(e)}")
