import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ingest import build_vector_db, DB_DIR

SYSTEM_PROMPT = """Eres un experto Senior en Legislación Laboral y Prevención de Riesgos en Chile.
Responde a la consulta del usuario utilizando EXCLUSIVAMENTE el contexto normativo proporcionado a continuación.

Reglas estrictas:
1. Cita siempre el cuerpo legal exacto (ej. Ley 16.744, DS 594, DS 44 o Código del Trabajo) y el número de Artículo correspondiente.
2. Si la respuesta no se encuentra en el contexto, declara objetivamente que la información no está disponible en la base de datos cargada.
3. Mantén un tono técnico, formal y riguroso.

Contexto Normativo Recuperado:
{context}

Pregunta del usuario:
{question}
"""

def get_vector_store():
    # Si la base de datos no existe en la nube, se genera automáticamente
    if not os.path.exists(DB_DIR) or not os.listdir(DB_DIR):
        build_vector_db()

    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

def get_llm(provider: str, api_key: str):
    if provider == "Google Gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=api_key,
            temperature=0.1
        )
    elif provider == "Groq":
        return ChatGroq(
            model_name="openai/gpt-oss-120b",
            groq_api_key=api_key,
            temperature=0.1
        )
    else:
        raise ValueError("Proveedor no soportado.")

def format_docs(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "Desconocido")
        page = doc.metadata.get("page", None)
        page_str = f" (Pág. {page+1})" if page is not None else ""
        formatted.append(f"--- FUENTE: {source}{page_str} ---\n{doc.page_content}")
    return "\n\n".join(formatted)

def query_rag(question: str, provider: str, api_key: str):
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 6})
    
    docs = retriever.invoke(question)
    context_text = format_docs(docs)
    
    llm = get_llm(provider, api_key)
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "context": context_text,
        "question": question
    })
    
    return response, docs
