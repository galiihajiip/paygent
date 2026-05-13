"use client";

import ReactMarkdown from "react-markdown";
import { Bot, User } from "lucide-react";
import type { Message } from "./ChatWindow";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-brand-dark" : "bg-accent"
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Bubble */}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-brand-dark text-white rounded-tr-md"
            : "bg-accent-light text-text-primary rounded-tl-md"
        }`}
      >
        <div className="prose prose-sm max-w-none prose-p:my-1 prose-ul:my-1 prose-li:my-0">
          <ReactMarkdown
            components={{
              a: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`underline font-medium ${
                    isUser ? "text-accent-light" : "text-accent"
                  }`}
                >
                  {children}
                </a>
              ),
              strong: ({ children }) => (
                <strong className={isUser ? "text-white" : "text-text-primary"}>
                  {children}
                </strong>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Timestamp */}
        <p
          className={`text-xs mt-1 ${
            isUser ? "text-gray-300" : "text-text-secondary"
          }`}
        >
          {message.timestamp.toLocaleTimeString("id-ID", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}
