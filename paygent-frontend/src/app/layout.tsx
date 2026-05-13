import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PayGent – Auto-Biller AI",
  description: "Asisten penagihan berbasis AI yang proaktif.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className={`${inter.className} bg-[#F8FAFC] text-[#0F172A] antialiased`}>
        {children}
      </body>
    </html>
  );
}
