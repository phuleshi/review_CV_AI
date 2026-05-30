import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI CV Review",
  description: "Minimal local UI for testing the CV review product."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
