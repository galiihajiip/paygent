"use client";

import React, { useState } from "react";

interface InputBarProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export default function InputBar({ onSendMessage, isLoading }: InputBarProps) {
  const [inputValue, setInputValue] = useState<string>("");

  const handleSend = () => {
    const trimmed = inputValue.trim();
    if (trimmed && !isLoading) {
      onSendMessage(trimmed);
      setInputValue("");
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-[#E2E8F0] bg-white px-4 py-4">
      <div className="flex items-end gap-3 max-w-3xl mx-auto">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Contoh: Tagihkan PT Maju Bersama 2.5 juta untuk jasa konsultasi..."
          rows={1}
          disabled={isLoading}
          className="flex-1 resize-none border border-[#E2E8F0] rounded-2xl px-4 py-3 text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all max-h-32"
        />
        <button
          onClick={handleSend}
          disabled={isLoading || inputValue.trim() === ""}
          className="w-11 h-11 bg-[#2563EB] hover:bg-[#1D4ED8] disabled:bg-[#93C5FD] disabled:cursor-not-allowed text-white rounded-2xl flex items-center justify-center transition-all duration-200 flex-shrink-0 shadow-sm"
        >
          {isLoading ? (
            <svg
              className="animate-spin w-5 h-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          )}
        </button>
      </div>
      <p className="text-center text-[#94A3B8] text-xs mt-2">
        Tekan Enter untuk kirim · Shift+Enter untuk baris baru
      </p>
    </div>
  );
}
