'use client';

import { useState } from 'react';

const demoStores = [
  { id: 'store-1', name: 'Coop Ravenna', isPartner: true },
  { id: 'store-2', name: 'Conad Ravenna', isPartner: false },
];

export default function AdminPage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Admin dashboard</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800">Negozi</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {demoStores.map((store) => (
              <li key={store.id} className="flex items-center justify-between">
                <span>{store.name}</span>
                <button className="text-sky-600" onClick={() => setSelected(store.id)}>
                  Modifica
                </button>
              </li>
            ))}
          </ul>
        </section>
        <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800">Upload prezzi/offerte</h2>
          <p className="text-sm text-slate-600">Funzionalità demo: carica un CSV per aggiornare i listini.</p>
          <button className="button-primary mt-4">Carica CSV</button>
        </section>
      </div>
      {selected && (
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-800">Modifica store {selected}</h3>
          <p className="text-sm text-slate-600">TODO: form completo di gestione.</p>
        </div>
      )}
    </div>
  );
}
