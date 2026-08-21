"use client";

import React, { useState, useEffect } from "react";
import { useChat } from "@/context/ChatContext";

export default function ResearchAssistant() {
  const [query, setQuery] = useState("");
  const [width, setWidth] = useState(400);
  const [isResizing, setIsResizing] = useState(false);
  const { currentResponse: response, loading, error, askQuestion } = useChat();

  useEffect(() => {
    if (!response) {
      setQuery("");
    }
  }, [response]);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return;
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth > 300 && newWidth < 800) {
        setWidth(newWidth);
      }
    };
    const handleMouseUp = () => setIsResizing(false);

    if (isResizing) {
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    }
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing]);

  const handleSend = () => {
    if (query.trim() === "") return;
    askQuestion(query);
    setQuery("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <aside 
      className="fixed right-0 top-0 h-screen z-50 bg-surface-container/60 backdrop-blur-[30px] border-l border-white/10 shadow-2xl flex flex-col pt-16"
      style={{ width: `${width}px` }}
    >
      {/* Resizer Handle */}
      <div 
        className="absolute left-0 top-0 w-1.5 h-full cursor-col-resize hover:bg-primary/20 transition-colors z-50"
        onMouseDown={(e) => {
          e.preventDefault();
          setIsResizing(true);
        }}
      />
      {/* Header */}
      <div className="px-md py-sm border-b border-outline-variant/20 flex items-center gap-sm bg-surface-container/40">
        <div className="w-8 h-8 rounded-full bg-tertiary/20 border border-tertiary/50 flex items-center justify-center animate-pulse-slow">
          <span className="material-symbols-outlined text-tertiary text-[18px]">
            psychology
          </span>
        </div>
        <div>
          <h3 className="font-label-md text-label-md text-tertiary uppercase tracking-wider">
            AI Research
          </h3>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-md space-y-lg flex flex-col">


        {error && (
          <div className="flex justify-center">
            <div className="max-w-[85%] bg-error/20 border border-error/50 rounded-lg p-sm text-body-sm text-error">
              {error}
            </div>
          </div>
        )}

        {response && response.turns.map((turn, idx) => (
          <React.Fragment key={idx}>
            {/* User Message */}
            <div className="flex justify-end">
              <div className="max-w-[85%] bg-surface-container-high border border-outline-variant/30 rounded-2xl rounded-tr-sm p-sm text-body-sm text-on-surface shadow-sm">
                {turn.query}
              </div>
            </div>

            {/* AI Response */}
            <div className="flex justify-start">
              <div className="max-w-[95%] glass-panel rounded-2xl rounded-tl-sm p-md text-body-sm text-on-surface shadow-md relative">
                <div className="absolute top-0 left-0 w-1 h-full bg-tertiary rounded-l-2xl shadow-[0_0_10px_rgba(249,171,255,0.5)]"></div>
                <p className="text-on-surface-variant leading-relaxed">
                  {turn.answer}
                </p>
              </div>
            </div>
          </React.Fragment>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start opacity-50">
            <div className="flex items-center gap-1 p-sm">
              <div className="w-1.5 h-1.5 bg-tertiary rounded-full animate-bounce" style={{ animationDelay: "0s" }}></div>
              <div className="w-1.5 h-1.5 bg-tertiary rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
              <div className="w-1.5 h-1.5 bg-tertiary rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-md border-t border-outline-variant/20 bg-surface-container/80 backdrop-blur-md">
        <div className="relative bg-surface-container-lowest rounded-lg border-b border-outline-variant/50 focus-within:border-tertiary focus-within:shadow-[0_2px_10px_rgba(249,171,255,0.2)] transition-all">
          <textarea
            className="w-full bg-transparent border-none text-body-sm text-on-surface focus:ring-0 resize-none py-sm pl-sm pr-xl h-12 placeholder:text-outline-variant"
            placeholder="Ask the Research Assistant..."
            rows={1}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          ></textarea>
          <button 
            onClick={handleSend}
            disabled={loading}
            className="absolute right-sm bottom-sm p-1 rounded-md text-tertiary hover:bg-tertiary/10 transition-colors flex items-center justify-center"
          >
            <span
              className="material-symbols-outlined text-[20px]"
              style={{ fontVariationSettings: '"FILL" 1' }}
            >
              send
            </span>
          </button>
        </div>
        <div className="mt-xs text-center">
          <span className="text-[10px] text-outline-variant font-mono">
            Press Enter to send, Shift+Enter for new line
          </span>
        </div>
      </div>
    </aside>
  );
}
