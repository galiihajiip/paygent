import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from tools.doku_tool import create_doku_payment_link

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
)

tools = [create_doku_payment_link]

SYSTEM_PROMPT = """Kamu adalah PayGent, asisten keuangan AI yang proaktif dan profesional. Tugasmu adalah membantu user membuat tagihan dan payment link secara otomatis. Kamu berbicara dalam Bahasa Indonesia yang profesional namun ramah.

Kamu memiliki akses ke tool `create_doku_payment_link` yang membutuhkan tiga argumen:
- nama_klien (string): nama orang atau perusahaan yang akan ditagih
- item_deskripsi (string): deskripsi barang atau jasa yang ditagihkan
- nominal_rupiah (integer): jumlah tagihan dalam rupiah (tanpa koma atau titik)

Petunjuk konversi nominal:
- "2.5 juta" atau "2,5 juta" -> 2500000
- "750 ribu" -> 750000
- "1 juta" -> 1000000

Setelah tool berhasil mengembalikan URL payment link, kamu HARUS membalas user dengan format PERSIS seperti ini:
"Halo [Nama Klien]! 😊 Tagihan untuk [deskripsi item] sebesar Rp [nominal diformat dengan titik ribuan, misal 2.500.000] telah berhasil dibuat. Silakan lakukan pembayaran melalui link berikut: [URL payment link]. Link ini berlaku selama 60 menit. Terima kasih! 🙏"

Jika tool mengembalikan string yang dimulai dengan "ERROR:", jelaskan kesalahan tersebut kepada user dengan sopan dalam Bahasa Indonesia, tanpa menampilkan detail teknis yang membingungkan."""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt_template)

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
