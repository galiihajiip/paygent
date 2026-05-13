"use client";

import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Halo! 👋 Saya **PayGent**, asisten pembayaran AI Anda. Saya bisa membantu Anda:\n\n- 💳 Membuat link pembayaran\n- 📋 Mengecek status pembayaran\n\nSilakan beritahu saya apa yang bisa saya bantu!",
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: content, history }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.reply,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "Maaf, terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi. 🙏",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {/* Typing indicator */}
        {isLoading && (
          <div className="flex items-center gap-2 px-4 py-3">
            <div className="flex items-center gap-1 bg-accent-light rounded-2xl px-4 py-3">
              <span className="typing-dot w-2 h-2 bg-accent rounded-full inline-block" />
              <span className="typing-dot w-2 h-2 bg-accent rounded-full inline-block" />
              <span className="typing-dot w-2 h-2 bg-accent rounded-full inline-block" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <InputBar onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}
