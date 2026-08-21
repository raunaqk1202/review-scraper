"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import { useChat } from "@/context/ChatContext";

export default function Sidebar() {
  const { recentChats, startNewAnalysis, loadChat, currentResponse } = useChat();

  return (
    <nav className="fixed left-0 top-0 h-screen w-sidebar-width bg-surface-container-lowest border-r border-outline-variant/10 backdrop-blur-3xl flex flex-col py-lg px-md z-30">
      {/* Header */}
      <div className="flex items-center gap-sm mb-xl pl-sm">
        <Image
          alt="Myntra Logo"
          className="object-contain h-16 w-16 rounded-md"
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuA828KTKByyRYesL5blaRm_6J5LQOscoVCdmGyHhHvPNa1ksuFrkMOg_T-8ZqrvDs5HeWC-tJ6-8atcUAbuwv62mkmdiMoYmmifPrF0-H8ICmmdPG8Ecs9WWAISyWkPLFeRhIy5MWLmyXAWiqV96NK2pk6dxnE0_4LR2XAWJpNsHxz3gVGaFSA4InOwS17ItS6aiyo3yW8MZ0NtR1AAoj0Oey3BApSgGR3DSLdKVgNXCSXlxt3HxdKI"
          width={64}
          height={64}
        />
        <h2 className="font-headline-sm text-headline-sm font-bold text-on-surface tracking-tight">
          Myntra MindSight
        </h2>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 flex flex-col gap-sm">
        <button 
          onClick={startNewAnalysis}
          className="w-full py-sm px-md rounded-lg bg-surface-container-high border border-outline-variant/30 text-primary font-label-md text-label-md hover:bg-surface-variant hover:border-primary/50 transition-all shadow-sm flex items-center justify-center gap-xs mb-md"
        >
          <span className="material-symbols-outlined text-[16px]">add</span>
          New Analysis
        </button>

        <div className="mb-md mt-lg">
          <h3 className="px-md mb-xs text-[10px] uppercase font-bold tracking-widest text-on-surface-variant/70">
            Recents
          </h3>
          <div className="flex flex-col gap-xs">
            {recentChats.map((chat, idx) => (
              <button
                key={idx}
                onClick={() => loadChat(chat)}
                className={`flex items-center w-full text-left gap-md px-md py-sm rounded-lg text-on-surface-variant font-medium hover:bg-surface-variant/50 transition-colors active:scale-95 transition-transform group ${currentResponse?.id === chat.id ? 'bg-surface-variant/50 border border-outline-variant/30' : ''}`}
              >
                <span className="material-symbols-outlined text-[20px] group-hover:text-primary transition-colors">
                  chat_bubble
                </span>
                <span className="truncate text-body-sm">{chat.turns[0]?.query}</span>
              </button>
            ))}
            {recentChats.length === 0 && (
              <div className="px-md py-sm text-body-sm text-on-surface-variant/50 italic">
                No recent chats
              </div>
            )}
          </div>
        </div>
      </div>

      {/* CTA & Status */}
      <div className="mt-lg pt-lg border-t border-outline-variant/20">
        <div className="flex items-center gap-sm px-sm"></div>
      </div>
    </nav>
  );
}
