"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const welcomeMessage: Message = {
  id: "welcome-0",
  role: "assistant",
  content:
    'Halo! 👋 Saya PayGent, asisten penagihan AI Anda. Cukup beritahu saya siapa yang ingin Anda tagih, untuk apa, dan berapa nominalnya. Contoh: "Tagihkan CV Sentosa Digital 3 juta untuk jasa pembuatan website."',
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([welcomeMessage]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSendMessage = useCallback(async (userMessage: string) => {
    const newUserMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: userMessage,
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.reply,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setError(
        "Gagal terhubung ke server. Pastikan backend berjalan di port 8000."
      );
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content:
          "⚠️ Maaf, saya tidak dapat terhubung ke server saat ini. Silakan coba beberapa saat lagi.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="flex flex-col h-screen bg-[#F8FAFC]">
      {/* Header */}
      <header className="bg-[#0F172A] px-6 py-4 shadow-md flex-shrink-0">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-[#2563EB] rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-sm">PG</span>
            </div>
            <div>
              <h1 className="text-white font-semibold text-base leading-tight">
                PayGent
              </h1>
              <p className="text-[#94A3B8] text-xs">
                Auto-Biller AI · Powered by Doku
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#22C55E] animate-pulse" />
            <span className="text-[#94A3B8] text-xs">Online</span>
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="bg-[#FEF2F2] border-b border-[#FECACA] px-6 py-3 flex-shrink-0">
          <p className="text-[#EF4444] text-sm text-center max-w-3xl mx-auto">
            {error}
          </p>
        </div>
      )}

      {/* Chat Messages Area */}
      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
          ))}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex justify-start items-start gap-3 mb-4">
              <div className="w-8 h-8 rounded-full bg-[#2563EB] flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-1">
                PG
              </div>
              <div className="bg-white border border-[#E2E8F0] px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm">
                <div className="flex items-center gap-1.5">
                  <span
                    className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce"
                    style={{ animationDelay: "0ms" }}
                  />
                  <span
                    className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <span
                    className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </main>

      {/* Input Bar */}
      <InputBar onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
