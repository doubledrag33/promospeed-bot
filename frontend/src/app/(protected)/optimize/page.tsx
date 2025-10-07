'use client';

import { useState } from 'react';
import api from '@/lib/api';

interface Plan {
  kind: string;
  total: number;
  stores_used: number;
  km_est?: number;
  details: Array<{ store: { id: string; name: string }; subtotal: string }>;
}

export default function OptimizePage() {
  const [slider, setSlider] = useState(5);
  const [plans, setPlans] = useState<Plan[]>([]);

  const handleOptimize = async () => {
    const { data } = await api.post<{ plans: Plan[] }>('/list/optimize', {
      cart_id: 'demo-cart',
      slider,
    });
    setPlans(data.plans);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Ottimizza il tuo giro</h1>
        <button className="button-primary" onClick={handleOptimize}>
          Calcola piani
        </button>
      </div>
      <div>
        <label className="text-sm font-medium text-slate-700">Risparmio ↔ Sbattimento</label>
        <input
          type="range"
          min={0}
          max={10}
          value={slider}
          onChange={(event) => setSlider(Number(event.target.value))}
          className="w-full"
        />
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {plans.map((plan) => (
          <div key={plan.kind} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">{plan.kind}</h2>
            <p className="text-sm text-slate-600">Totale: €{plan.total.toFixed(2)}</p>
            <p className="text-sm text-slate-600">Negozi: {plan.stores_used}</p>
            <p className="text-sm text-slate-600">Km stimati: {plan.km_est ?? '—'}</p>
          </div>
        ))}
        {plans.length === 0 && <p>Avvia l&apos;ottimizzazione per vedere i piani suggeriti.</p>}
      </div>
    </div>
  );
}
