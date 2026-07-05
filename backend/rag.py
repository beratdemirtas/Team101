import os
import logging
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAG_DATA_DIR = Path(__file__).resolve().parent / "rag_data"
CHROMA_PERSIST_DIR = Path(__file__).resolve().parent / "chroma_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
    "Sen genç yatırımcılar için Sokratik yöntemle eğitim veren, "
    "asla doğrudan 'al/sat' tavsiyesi vermeyen bir finansal mentorsun. "
    "Sadece sana verilen bağlamdaki verileri kullan."
)

_vector_store: Chroma = None
_llm: ChatGoogleGenerativeAI = None


def _load_and_split_pdfs() -> list:
    logger.info("PDF aranıyor: %s", RAG_DATA_DIR)

    if not RAG_DATA_DIR.exists():
        logger.error("Klasör bulunamadı: %s", RAG_DATA_DIR)
        return []

    pdf_files = list(RAG_DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        logger.error("Klasörde hiç .pdf dosyası yok: %s", RAG_DATA_DIR)
        return []

    documents = []
    for pdf_path in pdf_files:
        try:
            loader = PyMuPDFLoader(str(pdf_path))
            pages = loader.load()
            non_empty = [p for p in pages if p.page_content.strip()]
            if not non_empty:
                logger.warning("'%s' metin içermiyor (taranmış/resim bazlı olabilir).", pdf_path.name)
            else:
                logger.info("'%s' → %d sayfa yüklendi.", pdf_path.name, len(non_empty))
            documents.extend(non_empty)
        except Exception as e:
            logger.error("'%s' yüklenemedi: %s", pdf_path.name, e)

    if not documents:
        logger.error("Hiçbir PDF'den metin çıkarılamadı.")
        return []

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    logger.info("Toplam %d chunk oluşturuldu.", len(chunks))
    return chunks


def _get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if CHROMA_PERSIST_DIR.exists() and any(CHROMA_PERSIST_DIR.iterdir()):
        logger.info("Mevcut ChromaDB deposu yükleniyor.")
        _vector_store = Chroma(
            persist_directory=str(CHROMA_PERSIST_DIR),
            embedding_function=embeddings,
        )
    else:
        chunks = _load_and_split_pdfs()
        if not chunks:
            raise ValueError(
                f"Vektör deposu oluşturulamadı: '{RAG_DATA_DIR}' dizininde "
                "okunabilir metin içeren PDF bulunamadı."
            )
        logger.info("ChromaDB deposu ilk kez oluşturuluyor.")
        _vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(CHROMA_PERSIST_DIR),
        )

    return _vector_store


def _get_llm() -> ChatGoogleGenerativeAI:
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3,
        )
        logger.info("LLM nesnesi oluşturuldu ve önbelleğe alındı.")
    return _llm


async def ask_mentor(query: str) -> str:
    vector_store = _get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(query)

    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Bağlam:\n{context}\n\nSoru: {query}"),
    ]

    llm = _get_llm()
    response = await llm.ainvoke(messages)
    return response.content
