import type { Metadata } from "next";
import "./globals.css";
import { Shield } from "lucide-react";

export const metadata: Metadata = {
  title: "News Verifier",
  description: "Verify the authenticity of news articles and social media posts",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
          <div className="container mx-auto px-4 py-8">
            {/* Header */}
            <div className="text-center mb-12">
              <div className="flex items-center justify-center mb-4">
                <Shield className="h-12 w-12 text-blue-600 mr-3" />
                <h1 className="text-4xl font-bold text-gray-900">
                  News Verifier
                </h1>
              </div>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Verify the authenticity of news articles and social media posts
                using onotology based NLP system
              </p>
            </div>

            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
