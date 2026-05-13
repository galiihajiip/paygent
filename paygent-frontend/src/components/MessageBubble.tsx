"use client";

import React from "react";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
}

function formatContent(text: string): React.ReactNode {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);

  return parts.map((part, index) => {
    if (urlRegex.test(part)) {
      // Reset lastIndex because regex has /g flag and is reused via .test()
      urlRegex.lastIndex = 0;
      return (
        <a
          key={index}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
          className="font-semibold underline decoration-2 underline-offset-2 text-[#2563EB] hover:text-[#1D4ED8] transition-colors break-all"
        >
          🔗 Bayar Sekarang
        </a>
      );
    }
    return <span key={index}>{part}</span>;
  });
}

export default function MessageBubble({ role, content }: MessageBubbleProps) {
  if (role === "user") {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[75%] bg-[#0F172A] text-white px-4 py-3 rounded-2xl rounded-br-sm text-sm leading-relaxed shadow-sm">
          {formatContent(content)}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start items-start gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-[#2563EB] flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-1">
        PG
      </div>
      <div className="max-w-[75%] bg-white border border-[#E2E8F0] text-[#0F172A] px-4 py-3 rounded-2xl rounded-bl-sm text-sm leading-relaxed shadow-sm">
        {formatContent(content)}
      </div>
    </div>
  );
}
