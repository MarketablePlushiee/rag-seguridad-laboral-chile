# ⚖️ IntegraSST — Legal & OHS RAG Assistant

🌐 **Language / Idioma:** [English](#-english) | [Español](#-español)

---

## 🇬🇧 English

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-red?style=for-the-badge&logo=streamlit)](https://rag-seguridad-laboral-cl.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-purple?style=for-the-badge)](https://www.trychroma.com/)

Production-ready Retrieval-Augmented Generation (RAG) assistant designed to query Chilean Occupational Health and Safety (OHS / SST) legislation with zero hallucinations, verified grounding, and verbatim legal article citations.

---

### 📋 1. Knowledge Base & Scope

The system's vector database indexes the core Chilean labor safety legislative framework:

* **Ley 16.744:** Accidentes del Trabajo y Enfermedades Profesionales (Work Accidents & Occupational Diseases Act).
* **Decreto Supremo 594 (DS 594):** Condiciones Sanitarias y Ambientales Básicas en los Lugares de Trabajo (Basic Sanitary and Environmental Workplace Standards).
* **Decreto Supremo 44 (DS 44):** Reglamento sobre Gestión de Riesgos en el Trabajo (Workplace Risk Management Regulations).
* **Código del Trabajo (Título II):** De la Protección a los Trabajadores (Labor Code - Worker Protection Title).

---

### ⚙️ 2. RAG Architecture & Pipeline

```text
[PDF Documents] ➔ [RecursiveCharacterSplitter] ➔ [MiniLM Embeddings] ➔ [ChromaDB Vector Store]
                                                                                │
[User Query] ➔ [Similarity Search (Top K=6)] ➔ [Strict Grounded Prompt] ➔ [LLM Generator]
                                                                                │
                                                                       [Auditable Response]
```

1. **Document Ingestion & Chunking:** PDFs parsed into overlapping text chunks using `RecursiveCharacterTextSplitter` (`chunk_size=1000`, `chunk_overlap=200`).
2. **Dense Vector Embeddings:** Semantic indexing via `paraphrase-multilingual-MiniLM-L12-v2` dense vector embeddings inside ChromaDB.
3. **Retrieval Pipeline ($K=6$):** Top-6 relevant document chunks retrieved per query using cosine similarity.
4. **Anti-Hallucination System Prompting:** Strict system prompts forcing the LLM (Google Gemini / Groq) to rely exclusively on context chunks. If the retrieved chunks do not contain sufficient evidence, the model explicitly declines to answer.
5. **Traceability & Evidence Inspector:** Expansible UI drawer displaying exact source PDF names, article numbers, and similarity scores.

---

### 📊 3. System Capabilities & UI Previews

* **Verbatim Legal Citation:** Automatically extracts and links exact articles (e.g., *Ley 16.744 Art. 5°* for commuting accidents).
* **Out-of-Scope Protection:** Safely rejects queries outside OHS legislation (e.g., severance pay or contract termination terms).
* **Direct Document Download:** Download original official law PDFs directly from the sidebar.

![RAG Citation Accuracy](rag-preview-1.png)
*Figure 1: Exact legal article retrieval with chunk inspection drawer.*

![Scope Control](rag-preview-2.png)
*Figure 2: Out-of-scope query rejection preserving hallucination-proof grounding.*

---

### 📦 4. Local Installation & Setup

```bash
# 1. Clone repository
git clone [https://github.com/MarketablePlushiee/rag-seguridad-laboral-chile.git](https://github.com/MarketablePlushiee/rag-seguridad-laboral-chile.git)
cd rag-seguridad-laboral-chile

# 2. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment keys (.env or Streamlit secrets)
# GEMINI_API_KEY=your_gemini_api_key
# GROQ_API_KEY=your_groq_api_key

# 4. Run local Streamlit web application
streamlit run app.py
```

---

### 👨‍💻 Author & Contact

* **Ivan Latrille Brito** — [ivan.latrille1@gmail.com](mailto:ivan.latrille1@gmail.com)
* **Live Web App:** [Streamlit Cloud Demo](https://rag-seguridad-laboral-cl.streamlit.app/)
* **Portfolio:** [marketableplushiee.github.io/Portafolio](https://marketableplushiee.github.io/Portafolio/)

---
---

## 🇪🇸 Español

[![Streamlit App](https://img.shields.io/badge/Streamlit-Demo%20en%20Vivo-red?style=for-the-badge&logo=streamlit)](https://rag-seguridad-laboral-cl.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-purple?style=for-the-badge)](https://www.trychroma.com/)

Asistente RAG (Retrieval-Augmented Generation) listo para producción diseñado para consultar la legislación chilena de Seguridad y Salud en el Trabajo (SST) sin alucinaciones, con fidelidad comprobada y citas normativas explícitas.

---

### 📋 1. Base de Conocimiento y Alcance Normativo

La base de datos vectorial del sistema indexa el marco regulatorio fundamental de seguridad laboral en Chile:

* **Ley 16.744:** Seguro Social contra Riesgos de Accidentes del Trabajo y Enfermedades Profesionales.
* **Decreto Supremo 594 (DS 594):** Reglamento sobre Condiciones Sanitarias y Ambientales Básicas en los Lugares de Trabajo.
* **Decreto Supremo 44 (DS 44):** Reglamento sobre Gestión de Riesgos en el Trabajo.
* **Código del Trabajo (Título II):** De la Protección a los Trabajadores.

---

### ⚙️ 2. Arquitectura RAG y Pipeline

```text
[Documentos PDF] ➔ [RecursiveCharacterSplitter] ➔ [MiniLM Embeddings] ➔ [ChromaDB Vector Store]
                                                                                │
[Consulta Usuario] ➔ [Búsqueda Semántica (Top K=6)] ➔ [Prompt de Sistema] ➔ [Generador LLM]
                                                                                │
                                                                     [Respuesta Auditable]
```

1. **Ingesta y Segmentación:** Procesamiento de PDFs legales en bloques de texto mediante `RecursiveCharacterTextSplitter` (`chunk_size=1000`, `chunk_overlap=200`).
2. **Embeddings Vectoriales:** Indexación semántica utilizando embeddings `paraphrase-multilingual-MiniLM-L12-v2` almacenados en ChromaDB.
3. **Recuperación Semántica ($K=6$):** Extracción de los 6 fragmentos más relevantes por consulta usando similitud de coseno.
4. **Prompts Anti-Alucinación:** Reglas de sistema estrictas que obligan al LLM (Google Gemini / Groq) a responder basándose únicamente en el contexto recuperado. Si la información no está en la base de datos, el sistema declara explícitamente su ausencia.
5. **Inspección de Evidencias:** Desplegable interactivo en interfaz para auditar la fuente exacta, número de artículo y nivel de coincidencia.

---

### 📊 3. Capacidades del Sistema y Demostración

* **Citas Normativas Exactas:** Extracción directa de artículos (ej. *Ley 16.744 Art. 5°* para accidentes de trayecto).
* **Control de Alcance:** Rechazo seguro de consultas ajenas a la seguridad laboral (ej. indemnización por despido o finiquitos).
* **Descarga de Fuentes:** Descarga directa de los PDFs oficiales desde la barra lateral.

![Precisión de Citas RAG](rag-preview-1.png)
*Figura 1: Recuperación exacta de artículos legales con desplegable de inspección de evidencia.*

![Control de Alcance](rag-preview-2.png)
*Figura 2: Rechazo de preguntas fuera del alcance cargado para mitigar alucinaciones.*

---

### 📦 4. Instalación y Uso Local

```bash
# 1. Clonar el repositorio
git clone [https://github.com/MarketablePlushiee/rag-seguridad-laboral-chile.git](https://github.com/MarketablePlushiee/rag-seguridad-laboral-chile.git)
cd rag-seguridad-laboral-chile

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar llaves de entorno (.env o secretos de Streamlit)
# GEMINI_API_KEY=tu_api_key_de_gemini
# GROQ_API_KEY=tu_api_key_de_groq

# 4. Ejecutar la aplicación web local
streamlit run app.py
```

---

### 👨‍💻 Autor y Contacto

* **Ivan Latrille Brito** — [ivan.latrille1@gmail.com](mailto:ivan.latrille1@gmail.com)
* **Aplicación en Vivo:** [Streamlit Cloud Demo](https://rag-seguridad-laboral-cl.streamlit.app/)
* **Portafolio:** [marketableplushiee.github.io/Portafolio](https://marketableplushiee.github.io/Portafolio/)
