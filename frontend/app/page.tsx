"use client";

import React from "react";
import { GlassCard } from "@/components/ui/GlassCard";
import { Activity, Database, CheckCircle, Clock } from "lucide-react";
import { QueryInterface } from "@/components/ui/QueryInterface";

export default function DashboardPage() {
  const metrics = [
    { name: "Total Rows Processed", value: "1.2M", change: "+14.5%", icon: Database, color: "text-blue-400" },
    { name: "Active Pipelines", value: "24", change: "+2", icon: Activity, color: "text-purple-400" },
    { name: "Success Rate", value: "99.8%", change: "+0.1%", icon: CheckCircle, color: "text-emerald-400" },
    { name: "Avg Processing Time", value: "1.2s", change: "-0.3s", icon: Clock, color: "text-amber-400" },
  ];

  return (
    <div className="flex flex-col gap-8 pb-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">
            Welcome back, Admin
          </h1>
          <p className="text-slate-400">
            Here's what's happening with your data pipelines today.
          </p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-sm font-medium hover:bg-white/10 transition-colors">
            Download Report
          </button>
          <button className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium transition-colors shadow-lg shadow-purple-500/20">
            New Pipeline
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => (
          <GlassCard key={metric.name} className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className={`p-2 rounded-xl bg-white/5 ${metric.color}`}>
                <metric.icon className="h-5 w-5" />
              </div>
              <span className={`text-sm font-medium ${metric.change.startsWith("+") ? "text-emerald-400" : "text-amber-400"}`}>
                {metric.change}
              </span>
            </div>
            <div>
              <p className="text-slate-400 text-sm font-medium mb-1">{metric.name}</p>
              <p className="text-2xl font-bold text-white">{metric.value}</p>
            </div>
          </GlassCard>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main AI Chat Area */}
        <div className="lg:col-span-2 shadow-2xl shadow-purple-900/20 rounded-2xl">
          <QueryInterface />
        </div>

        {/* Side Panel Area */}
        <div className="space-y-6">
          <GlassCard className="h-full min-h-[400px] flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-white">Recent Activity</h2>
              <button className="text-xs text-purple-400 hover:text-purple-300">View All</button>
            </div>
            <div className="flex-1 overflow-y-auto pr-2 space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex gap-4 items-start relative pb-4 border-b border-white/5 last:border-0 last:pb-0">
                  <div className="mt-1 flex-shrink-0 h-2 w-2 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.8)]" />
                  <div>
                    <p className="text-sm font-medium text-slate-200">ETL Job "Customer Sync" completed.</p>
                    <p className="text-xs text-slate-500 mt-1">{i * 15} minutes ago</p>
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
