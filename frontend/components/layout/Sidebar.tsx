"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession, signOut } from "next-auth/react";
import { LayoutDashboard, Database, Activity, Settings, Users, ArrowRightLeft } from "lucide-react";
import { GlassCard } from "@/components/ui/GlassCard";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Data Sources", href: "/sources", icon: Database },
  { name: "Transformations", href: "/transformations", icon: ArrowRightLeft },
  { name: "Monitoring", href: "/monitoring", icon: Activity },
  { name: "Team", href: "/team", icon: Users },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { data: session } = useSession();

  return (
    <div className="w-64 h-screen fixed inset-y-0 left-0 p-4 z-50">
      <GlassCard className="h-full flex flex-col pt-8 pb-4 px-4 bg-white/5 border-white/10 dark" dark>
        <div className="flex items-center gap-3 px-2 mb-10">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
            <span className="font-bold text-white tracking-tighter">DW</span>
          </div>
          <h1 className="text-xl font-bold tracking-tight text-white">
            DataWhisperer
          </h1>
        </div>
        
        <nav className="flex-1 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group relative
                  ${isActive 
                    ? "bg-white/10 text-white font-medium" 
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                  }`}
              >
                {isActive && (
                  <div className="absolute left-0 w-1 h-6 bg-purple-500 rounded-r-full" />
                )}
                <item.icon className={`h-5 w-5 ${isActive ? "text-purple-400" : "group-hover:text-purple-400 transition-colors"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="mt-auto px-2">
          {session ? (
            <div className="p-3 bg-white/5 rounded-xl border border-white/10 relative group">
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-full bg-slate-800 border-2 border-purple-500/50 flex flex-shrink-0 items-center justify-center font-bold text-white shadow-sm shadow-purple-500/20">
                  {session.user?.name?.charAt(0).toUpperCase() || "U"}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{session.user?.name}</p>
                  <p className="text-xs text-slate-400 truncate">{session.user?.email}</p>
                </div>
              </div>
              
              {/* Sign out hover button */}
              <button 
                onClick={() => signOut({ callbackUrl: '/login' })}
                className="absolute inset-0 bg-red-500/90 rounded-xl flex items-center justify-center text-white font-semibold opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-sm"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div className="p-3 bg-white/5 rounded-xl border border-white/10 text-center">
              <Link href="/login" className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors">
                Sign In
              </Link>
            </div>
          )}
        </div>
      </GlassCard>
    </div>
  );
}
