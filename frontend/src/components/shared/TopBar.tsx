import React from "react";

export default function TopBar() {
  return (
    <header className="fixed top-0 right-0 w-[calc(100%-var(--spacing-sidebar-width))] z-40 bg-surface/80 backdrop-blur-xl border-b border-white/5 shadow-sm flex justify-between items-center h-16 px-xl">
      <div className="flex items-center gap-lg">
        <nav className="hidden md:flex items-center gap-md ml-lg">
          {/* Add nav links if necessary */}
        </nav>
      </div>

      <div className="flex items-center gap-md">
        {/* Search */}
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-sm flex items-center pointer-events-none">
            <span className="material-symbols-outlined text-outline-variant group-focus-within:text-primary transition-colors">
              search
            </span>
          </div>
        </div>

        {/* Icons */}
        <div className="flex items-center gap-xs border-l border-outline-variant/30 pl-md ml-xs">
          <button className="p-sm rounded-full text-on-surface-variant hover:bg-surface-variant/50 hover:text-primary transition-all relative">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-error border border-background"></span>
          </button>
          <button className="p-sm rounded-full text-on-surface-variant hover:bg-surface-variant/50 hover:text-primary transition-all">
            <span className="material-symbols-outlined">history</span>
          </button>
        </div>

        {/* Primary Action */}
        <button className="ml-sm px-md py-xs rounded-lg accent-gradient text-background font-label-md text-label-md shadow-[0_0_15px_rgba(255,79,116,0.2)] hover:shadow-[0_0_20px_rgba(255,79,116,0.4)] transition-all flex items-center gap-xs">
          <span className="material-symbols-outlined text-[16px]">model_training</span>
          Deploy AI
        </button>
      </div>
    </header>
  );
}
