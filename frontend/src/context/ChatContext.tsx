"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";
import { ResearchQueryResponse } from "@/hooks/useResearch";

export interface ChatTurn extends ResearchQueryResponse {}

export interface ChatSession {
  id: string;
  turns: ChatTurn[];
}

interface ChatContextType {
  recentChats: ChatSession[];
  currentResponse: ChatSession | null;
  loading: boolean;
  error: string | null;
  askQuestion: (query: string) => Promise<void>;
  startNewAnalysis: () => void;
  loadChat: (chat: ChatSession) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [recentChats, setRecentChats] = useState<ChatSession[]>([]);
  const [currentResponse, setCurrentResponse] = useState<ChatSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/research/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }
      const data: ResearchQueryResponse = await res.json();
      
      let session: ChatSession;
      if (currentResponse) {
        session = {
          ...currentResponse,
          turns: [...currentResponse.turns, data],
        };
      } else {
        session = {
          id: Date.now().toString(),
          turns: [data],
        };
      }
      
      setCurrentResponse(session);
      
      setRecentChats((prev) => {
        const filtered = prev.filter(c => c.id !== session.id);
        return [session, ...filtered];
      });
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const startNewAnalysis = () => {
    setCurrentResponse(null);
  };

  const loadChat = (chat: ChatSession) => {
    setCurrentResponse(chat);
  };

  return (
    <ChatContext.Provider
      value={{
        recentChats,
        currentResponse,
        loading,
        error,
        askQuestion,
        startNewAnalysis,
        loadChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
}
