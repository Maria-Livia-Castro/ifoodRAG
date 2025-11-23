from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

#Carregar a base de conhecimento
loader = CSVLoader(file_path="base_conhecimento_ifood_genai.csv")
docs = loader.load()

#Criar embeddings (rodam localmente, sem token)
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

#Função com fallback
def safe_answer(question: str) -> str:
    docs = db.as_retriever().get_relevant_documents(question)

    if not docs:
        return "Não encontrei informações suficientes na base. Sugiro abrir um ticket interno ou consultar a política oficial."

    resposta = docs[0].page_content
    fonte = docs[0].metadata.get("fonte", "")

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