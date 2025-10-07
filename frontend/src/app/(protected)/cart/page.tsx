'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useGroptStore } from '@/lib/store';

interface CartApiResponse {
  id: string;
  status: string;
  items: Array<{
    id: string;
    product_id: string;
    quantity: string;
    preferred_store_id?: string;
  }>;
}

export default function CartPage() {
  const { cart, setCart } = useGroptStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const { data } = await api.get<CartApiResponse>('/cart');
        setCart(
          data.items.map((item) => ({
            id: item.id,
            productId: item.product_id,
            name: 'Prodotto demo',
            quantity: Number(item.quantity),
          })),
        );
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchCart();
  }, [setCart]);

  if (loading) {
    return <p>Caricamento carrello...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Il tuo carrello</h1>
        <button className="button-primary">Ottimizza</button>
      </div>
      <div className="space-y-4">
        {cart.map((item) => (
          <div key={item.id} className="rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-800">{item.name}</h2>
                <p className="text-sm text-slate-600">Quantità: {item.quantity}</p>
              </div>
              <div className="text-right text-sm text-slate-600">
                <p>Miglior prezzo: TBD</p>
                <p className="text-xs">Aggiornato pochi giorni fa</p>
              </div>
            </div>
          </div>
        ))}
        {cart.length === 0 && <p>Il carrello è vuoto. Cerca un prodotto e aggiungilo!</p>}
      </div>
    </div>
  );
}
