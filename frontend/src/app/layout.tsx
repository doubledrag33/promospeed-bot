import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Gropt',
  description: 'Spesa intelligente con ottimizzazione multi-negozio',
  manifest: '/manifest.json',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it">
      <body className="min-h-screen bg-white">
        <header className="border-b border-slate-200">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
            <span className="text-2xl font-bold text-slate-900">Gropt</span>
            <nav className="space-x-4 text-sm">
              <a href="/offers">Offerte</a>
              <a href="/cart">Carrello</a>
              <a href="/favorites">Preferiti</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
        <footer className="border-t border-slate-200 bg-slate-50 py-6 text-center text-sm text-slate-600">
          I prezzi online possono differire dai prezzi in negozio; mostriamo fonte e data rilevazione.
        </footer>
      </body>
    </html>
  );
}
