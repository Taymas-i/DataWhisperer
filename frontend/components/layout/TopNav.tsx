"use client";

import React, { useEffect, useState } from "react";
import { Search, Bell, AlertCircle, CheckCircle2 } from "lucide-react";

export function TopNav() {
  const [apiStatus, setApiStatus] = useState<"checking" | "connected" | "error">("checking");

  useEffect(() => {
    // Test connection to FastAPI backend to verify CORS setup
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => {
        if (data.message) {
          setApiStatus("connected");
        } else {
          setApiStatus("error");
        }
      })
      .catch((err) => {
        console.error("FastAPI Connection Error:", err);
        setApiStatus("error");
      });
  }, []);

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full shrink-0 items-center justify-between border-b border-white/10 bg-black/20 backdrop-blur-md px-6 shadow-sm">
      <div className="flex flex-1 items-center gap-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search data sources, pipelines, or queries..."
            className="w-full rounded-full border border-white/10 bg-white/5 py-1.5 pl-10 pr-4 text-sm text-white placeholder:text-slate-400 focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500 transition-all"
          />
        </div>
      </div>
      <div className="flex items-center gap-x-4">
        <button className="relative text-slate-400 hover:text-white transition-colors">
          <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500 border border-black/20" />
          <Bell className="h-5 w-5" />
        </button>
        <div className="h-6 w-[1px] bg-white/10 mx-2" />
        <button className={`flex items-center gap-2 text-sm font-medium transition-colors ${
          apiStatus === "connected" ? "text-emerald-400" : 
          apiStatus === "error" ? "text-red-400" : "text-amber-500"
        }`}>
          {apiStatus === "connected" ? (
            <CheckCircle2 className="h-4 w-4" />
          ) : (
            <AlertCircle className="h-4 w-4" />
          )}
          <span className="hidden sm:inline">
            API: {apiStatus === "connected" ? "Connected" : apiStatus === "error" ? "Offline" : "Checking..."}
          </span>
        </button>
      </div>
    </header>
  );
}
