# Agente GenAI iFood (POC RAG)

Este projeto é uma **Prova de Conceito (POC)** de um agente interno que utiliza **Retrieval-Augmented Generation (RAG)** para responder perguntas sobre **reembolsos e cancelamentos** com base em uma base de conhecimento em CSV.

A ideia não é construir um sistema completo, mas criar algo demonstrável para **portfólio, currículo ou entrevista técnica**.

---

## 🎯 Objetivo da POC

Criar um agente de IA capaz de:

1. Consultar informações oficiais (base de conhecimento)  
2. Responder perguntas operacionais de forma consistente  
3. Evitar respostas inventadas (*alucinações*)  
4. Sugerir fallback inteligente quando não há confiança  

---

## 📂 Estrutura esperada do CSV

O arquivo `base_conhecimento_ifood_genai.csv` deve conter as seguintes colunas:

| categoria   | pergunta                                | resposta                                                                 | fonte         |
|-------------|-----------------------------------------|--------------------------------------------------------------------------|---------------|
| reembolso   | Quando o cliente tem direito a reembolso total | Quando o restaurante cancela o pedido ou quando há erro comprovado na entrega. | Política 3.2 |
| reembolso   | Erro do restaurante garante reembolso   | Sim, cancelamentos por falha do restaurante geram reembolso total.       | Política 2.1 |

---

###  **Execução**

## ▶️ Como executar

No terminal:

```bash
python agente_ifood.py


---

###  **Exemplos de uso**

## 💬 Exemplos de uso
Você: Quando o cliente tem direito a reembolso total? Agente: Quando o restaurante cancela o pedido ou quando há erro comprovado na entrega. (Fonte: Política 3.2)
Você: Cliente foi cobrado após cancelamento Agente: Não encontrei resposta exata. Sugiro verificar o estorno no sistema financeiro.

---

## ⚠️ Fallback inteligente

Se a pergunta não estiver na base ou a confiança for baixa, o agente responde de forma contextual:

- **Reembolso** → "Sugiro validar manualmente com a política de reembolso."  
- **Cancelamento** → "Sugiro abrir um ticket interno para confirmar o procedimento."  
- **Cobrança** → "Sugiro verificar o estorno no sistema financeiro."  
- **Outros casos** → "Consulte a política oficial ou abra um ticket interno."

## 🚀 Ideias de evolução

- Logs de confiança da resposta  
- Interface web com Streamlit ou Gradio  
- Integração com APIs fictícias de pedidos/estorno  
- Classificação automática do tipo de caso

## 📜 Licença

Este projeto é apenas uma prova de conceito e pode ser adaptado conforme necessidade.
