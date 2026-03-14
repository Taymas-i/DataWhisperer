"use client";

import React, { useState } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";
import { AIMetricCard } from "@/components/ui/AIMetricCard";

interface Message {
  role: "user" | "ai";
  content: string;
}

// A helper to parse the AI text and inject dynamic components
function MessageRenderer({ content }: { content: string }) {
  // Regex pattern to find metrics like "1588 reviews" or "42 users"
  const metricRegex = /(?:(\d+(?:,\d+)?(?:\.\d+)?(?:k|m|b)?))\s*(reviews|users|rows|pipelines|errors)/i;
  
  const match = content.match(metricRegex);

  if (match) {
    const [fullMatch, value, unit] = match;
    const parts = content.split(fullMatch);
    
    return (
      <div className="flex flex-col">
        {parts[0] && <p className="whitespace-pre-wrap text-sm leading-relaxed">{parts[0]}</p>}
        {/* Render our custom Metric Component right in the middle of the chat */}
        <AIMetricCard title={`Total ${unit}`} value={value} />
        {parts[1] && <p className="whitespace-pre-wrap text-sm leading-relaxed mt-2">{parts[1]}</p>}
      </div>
    );
  }

  // Fallback to normal text rendering
  return <p className="whitespace-pre-wrap text-sm leading-relaxed">{content}</p>;
}

export function QueryInterface() {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: query.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage.content }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessages((prev) => [
          ...prev,
          { role: "ai", content: data.answer || "No response generated." },
        ]);
      } else {
        throw new Error(data.error || "Failed to fetch AI response");
      }
    } catch (error) {
      console.error("Query Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Sorry, I encountered an error connecting to the backend. Please ensure the FastAPI server is running.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <GlassCard className="h-full min-h-[400px] flex flex-col p-0 overflow-hidden">
      <div className="border-b border-white/10 px-6 py-4 flex items-center justify-between bg-white/5">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center">
            <Bot className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">DataWhisperer AI</h2>
            <p className="text-xs text-slate-400">Ask questions about your data pipelines</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-50">
            <Bot className="h-12 w-12 text-slate-400 mb-4" />
            <p className="text-slate-300 max-w-sm">
              I'm ready to help you analyze your data. Try asking about recent errors, processing times, or pipeline statuses.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
            >
              <div
                className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
                  msg.role === "user" ? "bg-blue-500 text-white" : "bg-purple-500/20 text-purple-400"
                }`}
              >
                {msg.role === "user" ? <User className="h-5 w-5" /> : <Bot className="h-5 w-5" />}
              </div>
              <div
                className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                  msg.role === "user"
                    ? "bg-blue-500/20 text-white border border-blue-500/30 rounded-tr-none"
                    : "bg-white/5 text-slate-200 border border-white/10 rounded-tl-none"
                }`}
              >
                {msg.role === "user" ? (
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                ) : (
                  <MessageRenderer content={msg.content} />
                )}
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex gap-4">
            <div className="flex-shrink-0 h-8 w-8 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center">
              <Bot className="h-5 w-5" />
            </div>
            <div className="bg-white/5 border border-white/10 rounded-2xl rounded-tl-none px-5 py-3 flex items-center gap-2">
              <Loader2 className="h-4 w-4 text-purple-400 animate-spin" />
              <span className="text-sm text-slate-400">Analyzing...</span>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-black/20 border-t border-white/10 backdrop-blur-md">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            placeholder="Ask anything about your data..."
            className="w-full bg-white/5 border border-white/10 rounded-full py-3 pl-6 pr-14 text-white placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-purple-500 focus:border-purple-500 disabled:opacity-50 transition-all"
          />
          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="absolute right-2 h-9 w-9 rounded-full bg-purple-600 hover:bg-purple-700 flex items-center justify-center text-white disabled:opacity-50 disabled:hover:bg-purple-600 transition-colors"
          >
            <Send className="h-4 w-4 ml-0.5" />
          </button>
        </form>
      </div>
    </GlassCard>
  );
}
