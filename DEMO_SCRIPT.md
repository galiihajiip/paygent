# PayGent Demo Script – Agenthon

> **Kategori:** Best Payment Use Case
> **Tagline:** Asisten penagihan AI yang mengubah kalimat bahasa Indonesia menjadi payment link Doku dalam hitungan detik.

---

## Pre-Demo Checklist

- [ ] Backend berjalan: `uvicorn main:app --reload --port 8000`
- [ ] Frontend berjalan: `npm run dev` di port 3000
- [ ] `.env` backend sudah berisi `GROQ_API_KEY` dan kredensial Doku Sandbox yang valid
- [ ] Browser terbuka di `http://localhost:3000`
- [ ] Tab DevTools Network siap untuk menunjukkan real API call (opsional)

---

## Skenario Demo 1 – Tagihan Freelance

**Konteks naratif:**
"Bayangkan Anda seorang freelancer designer yang baru saja menyelesaikan project landing page untuk klien. Biasanya, Anda perlu login ke dashboard payment gateway, isi form, lalu copy-paste link. Dengan PayGent, cukup ketik satu kalimat."

**Input demonstrator (ketik di chat):**

```
Tolong tagihkan PT Kreasi Digital 2.500.000 rupiah untuk jasa pembuatan landing page.
```

**Expected output:**
Agent akan menampilkan pesan profesional berisi payment link Doku yang bisa diklik. Format respons mengikuti template:

> Halo PT Kreasi Digital! 😊 Tagihan untuk jasa pembuatan landing page sebesar Rp 2.500.000 telah berhasil dibuat. Silakan lakukan pembayaran melalui link berikut: 🔗 Bayar Sekarang. Link ini berlaku selama 60 menit. Terima kasih! 🙏

**Yang ditunjukkan ke juri:**
1. Klik tombol Bayar Sekarang → halaman checkout Doku terbuka di tab baru.
2. Buka DevTools → Network → tunjukkan request real ke `https://api-sandbox.doku.com/checkout/v1/payment`.

---

## Skenario Demo 2 – Tagihan Konsultasi

**Konteks naratif:**
"Sekarang saya konsultan bisnis. Klien saya namanya Pak Budi. Saya sudah selesai sesi konsultasi 1 jam dan ingin menagih beliau."

**Input demonstrator (ketik di chat):**

```
Buat tagihan untuk Budi Santoso senilai 750 ribu untuk sesi konsultasi bisnis 1 jam.
```

**Expected output:**
Payment link baru di-generate dengan nominal **Rp 750.000**. Perhatikan bahwa agent berhasil memahami:
- Format nominal informal ("750 ribu" → 750000)
- Nama klien personal (bukan badan usaha)
- Deskripsi item yang multi-kata

---

## Key Talking Points untuk Juri

- **Multi-step ReAct loop** — Agent berpikir secara eksplisit melalui siklus Thought → Action → Observation. Setiap kali tool dipanggil, model membaca hasilnya dan memutuskan langkah berikutnya. Ini bukan hanya prompt-response tunggal, melainkan reasoning chain yang dapat diaudit.

- **Real API integration ke Doku Sandbox** — Tidak ada mock atau hardcoded link. Setiap payment link adalah hasil request HTTP nyata dengan signature HMAC-SHA256 sesuai spesifikasi Doku, lengkap dengan digest body dan timestamped headers.

- **Natural language understanding berbahasa Indonesia** — Agent mengekstrak entitas (nama klien, item, nominal) dari kalimat bebas, termasuk format informal seperti "2.5 juta" atau "750 ribu". Tidak ada form field, tidak ada dropdown — hanya bahasa alami.

- **Production-ready error handling** — Setiap layer (Doku tool, agent executor, FastAPI endpoint) memiliki try-except eksplisit. Network error, signature mismatch, malformed response, dan agent parsing error semuanya ditangkap dan dikembalikan dalam pesan yang informatif untuk user.

- **Monetisasi yang jelas** — Target market: 5+ juta freelancer dan UMKM di Indonesia yang saat ini ribet menggunakan dashboard payment gateway. Model SaaS dengan tier gratis (X tagihan/bulan) dan paid plan untuk volume tinggi. PayGent jadi layer abstraksi di atas Doku, mempermudah onboarding merchant baru ke ekosistem Doku.

---

## Architecture Diagram (Text)

```
   User Input → Next.js Frontend → FastAPI Backend → LangChain ReAct Agent
                                                          ↓
                                                   Groq LLaMA-3 (LLM)
                                                          ↓
                                                  create_doku_payment_link (Tool)
                                                          ↓
                                                   Doku Sandbox API
                                                          ↓
                                              Payment Link URL → Response → UI
```

**Komponen kunci:**

| Layer            | Teknologi                        | Peran                                                                |
|------------------|----------------------------------|----------------------------------------------------------------------|
| Frontend         | Next.js 16 (App Router) + Tailwind v4 | Chat UI, state management, auto-detect URL untuk render payment link |
| Backend API      | FastAPI + CORS                   | Endpoint `/api/chat`, validasi input, error envelope                 |
| Agent Runtime    | LangChain ReAct + AgentExecutor  | Orkestrasi reasoning loop, max 5 iterations, parsing-error recovery  |
| LLM              | Groq + LLaMA-3 70B               | Inference cepat (sub-detik), Bahasa Indonesia native                 |
| Payment Tool     | `create_doku_payment_link`        | HTTP call + HMAC-SHA256 signing ke Doku Checkout API                 |
| Payment Provider | Doku Sandbox                     | Generate hosted checkout page dengan multi-channel support           |

---

## Recovery Plan (jika demo gagal)

1. **Backend down** → tunjukkan terminal log uvicorn, restart cepat dengan `Ctrl+C` lalu `uvicorn main:app --reload`.
2. **Doku API error 4xx** → buka file `tools/doku_tool.py`, tunjukkan implementasi HMAC-SHA256 — error envelope sudah pre-formatted dan tetap muncul di chat (bukan crash).
3. **Network lambat** → tunjukkan loading indicator (3 dots bouncing) dan jelaskan: "Inilah pengalaman real-world; kami punya feedback visual yang jelas saat agent sedang berpikir."

---

## Closing Statement

> "PayGent membuktikan bahwa payment gateway tidak harus selalu berbentuk dashboard. Dengan AI agent yang memahami bahasa, kami mengubah Doku menjadi infrastruktur conversational — sekali ketik, link siap dibagikan."
