from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

#Carregar a base de conhecimento
loader = CSVLoader(file_path="base_conhecimento_ifood_genai.csv")
docs = loader.load()

#Criar embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

#Configurar o modelo de linguagem local
pipe = pipeline("text2text-generation", model="google/flan-t5-small")
llm = HuggingFacePipeline(pipeline=pipe)

#Criar o agente RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=False
)

#Função com fallback funcional
CONFIDENCE_THRESHOLD = 0.6  #limiar ajustado para não descartar respostas corretas

def safe_answer(question: str) -> str:
    #Busca com score
    results = db.similarity_search_with_score(question, k=3)

    if not results:
        return "Não encontrei informações suficientes na base. Sugiro abrir um ticket interno ou consultar a política oficial."

    doc_top, score_top = results[0]

    #Se a confiança for baixa (score alto), usa fallback
    if score_top is None or score_top > CONFIDENCE_THRESHOLD:
        q_lower = question.lower()
        if "reembolso" in q_lower:
            return "Não encontrei resposta exata. Sugiro validar manualmente com a política de reembolso."
        elif "cancelamento" in q_lower:
            return "Não encontrei resposta exata. Sugiro abrir um ticket interno para confirmar o procedimento."
        elif "cobrança" in q_lower or "cobrado" in q_lower:
            return "Não encontrei resposta exata. Sugiro verificar o estorno no sistema financeiro."
        else:
            return "Não encontrei informações suficientes na base. Consulte a política oficial ou abra um ticket interno."

    #Se passou no limiar, retorna a resposta da base
    resposta = doc_top.page_content
    fonte = doc_top.metadata.get("fonte", "")
    saida = resposta
    if fonte:
        saida += f" (Fonte: {fonte})"
    return saida

#Loop interativo
def main():
    banner = r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║                  >>>  Agente GenAI iFood  <<<                    ║
    ║              Sistema de Respostas com RAG (POC)                  ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:
        question = input("Você: ")
        if question.lower() in ["sair", "exit", "quit"]:
            print("Agente: Até logo!")
            break
        response = safe_answer(question)
        print("Agente:\n", response, "\n")

if __name__ == "__main__":
    main()