"use client";

import ChatWindow from "@/components/ChatWindow";
import { CreditCard } from "lucide-react";

export default function Home() {
  return (
    <main className="flex flex-col h-screen">
      {/* Navbar */}
      <header className="bg-brand-dark text-white px-6 py-4 flex items-center gap-3 shadow-md">
        <div className="flex items-center gap-2">
          <CreditCard className="w-6 h-6 text-accent" />
          <h1 className="text-xl font-bold tracking-tight">PayGent</h1>
        </div>
        <span className="text-sm text-text-secondary ml-2 hidden sm:inline">
          AI Payment Assistant
        </span>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden">
        <ChatWindow />
      </div>
    </main>
  );
}
