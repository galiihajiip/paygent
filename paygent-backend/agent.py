import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from tools.doku_tool import create_doku_payment_link

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
)

tools = [create_doku_payment_link]

PROMPT_TEMPLATE = """Kamu adalah PayGent, asisten keuangan AI yang proaktif dan profesional. Tugasmu adalah membantu user membuat tagihan dan payment link secara otomatis. Kamu berbicara dalam Bahasa Indonesia yang profesional namun ramah.

Kamu memiliki akses ke tools berikut:
{tools}

Gunakan format berikut untuk berpikir:
Question: pertanyaan atau permintaan dari user
Thought: pikirkan apa yang perlu kamu lakukan
Action: tool yang akan digunakan, harus salah satu dari [{tool_names}]
Action Input: input untuk tool tersebut dalam format JSON yang valid
Observation: hasil dari tool
... (ulangi Thought/Action/Action Input/Observation jika perlu)
Thought: Sekarang saya sudah punya jawaban finalnya
Final Answer: [Tulis respons profesional dalam Bahasa Indonesia. Jika berhasil mendapatkan payment link, format responsnya HARUS seperti ini: "Halo [Nama Klien]! 😊 Tagihan untuk [deskripsi item] sebesar Rp [nominal diformat dengan titik ribuan] telah berhasil dibuat. Silakan lakukan pembayaran melalui link berikut: [URL payment link]. Link ini berlaku selama 60 menit. Terima kasih! 🙏"]

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt_template = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template=PROMPT_TEMPLATE,
)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)


def run_paygent_agent(user_message: str) -> str:
    try:
        result = agent_executor.invoke({"input": user_message})
        return result["output"]
    except Exception as e:
        return f"Maaf, terjadi kesalahan internal pada agent. Detail: {str(e)}"
