import React from "react";

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  dark?: boolean;
}

export function GlassCard({ children, className = "", dark = false }: GlassCardProps) {
  // Use the utility classes we defined in globals.css
  const baseStyle = dark ? "glass-panel-dark" : "glass-panel";
  
  return (
    <div className={`${baseStyle} rounded-2xl p-6 transition-all duration-300 hover:shadow-xl hover:border-white/30 ${className}`}>
      {children}
    </div>
  );
}
