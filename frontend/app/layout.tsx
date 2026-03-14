import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNav } from "@/components/layout/TopNav";
import Providers from "./providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DataWhisperer Admin",
  description: "Next Generation Data Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased selection:bg-purple-500/30`}>
        <Providers>
          <div className="flex min-h-screen">
            {/* Fixed Sidebar */}
            <Sidebar />
            
            {/* Main Content Wrapper - offset by sidebar width (w-64 = 16rem = 256px) */}
            <div className="flex flex-1 flex-col ml-64 min-w-0">
              <TopNav />
              <main className="flex-1 p-6 lg:p-8 w-full max-w-7xl mx-auto">
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out h-full">
                  {children}
                </div>
              </main>
            </div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
