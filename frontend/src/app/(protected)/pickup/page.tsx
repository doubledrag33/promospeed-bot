'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function PickupPage() {
  const [pickupCode, setPickupCode] = useState<string | null>(null);

  const handleReservation = async () => {
    const { data } = await api.post('/pandr/create', { cart_id: 'demo-cart' });
    setPickupCode(data.reservations[0]);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Prenota & Ritira</h1>
      <p className="text-sm text-slate-600">
        Scegli i negozi partner disponibili e conferma la prenotazione. Per la demo usiamo dati fittizi.
      </p>
      <button className="button-primary" onClick={handleReservation}>
        Prenota adesso
      </button>
      {pickupCode && (
        <div className="rounded-xl border border-slate-200 bg-white p-6 text-center shadow-sm">
          <p className="text-sm text-slate-600">Il tuo codice pickup</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{pickupCode}</p>
        </div>
      )}
    </div>
  );
}
