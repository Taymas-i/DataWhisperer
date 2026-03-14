"use client";

import React from "react";
import { TrendingUp } from "lucide-react";

interface AIMetricCardProps {
  title: string;
  value: string;
  trend?: string;
  className?: string;
}

export function AIMetricCard({ title, value, trend, className = "" }: AIMetricCardProps) {
  return (
    <div className={`mt-3 mb-2 w-full max-w-[300px] bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-5 shadow-xl transition-all hover:border-white/40 ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-slate-300 uppercase tracking-wider">{title}</h3>
        {trend && (
          <div className="flex items-center gap-1 text-emerald-400 text-xs font-semibold bg-emerald-400/10 px-2 py-1 rounded-full">
            <TrendingUp className="h-3 w-3" />
            {trend}
          </div>
        )}
      </div>
      <div className="flex items-baseline gap-2 mt-1">
        <span className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 tracking-tight">
          {value}
        </span>
      </div>
    </div>
  );
}
