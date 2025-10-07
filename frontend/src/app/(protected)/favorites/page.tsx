'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useGroptStore } from '@/lib/store';

interface FavoriteResponse {
  items: Array<{ id: string; product_id: string; notes?: string }>;
}

export default function FavoritesPage() {
  const { favorites, addFavorite } = useGroptStore();
  const [remote, setRemote] = useState<FavoriteResponse['items']>([]);

  useEffect(() => {
    const fetchFavorites = async () => {
      const { data } = await api.get<FavoriteResponse>('/favorites');
      setRemote(data.items);
      data.items.forEach((item) => addFavorite(item.product_id));
    };
    fetchFavorites();
  }, [addFavorite]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Preferiti</h1>
      <div className="grid gap-4 md:grid-cols-2">
        {remote.map((fav) => (
          <div key={fav.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-800">Prodotto #{fav.product_id}</h2>
            <p className="text-sm text-slate-600">{fav.notes ?? 'Nessuna nota'}</p>
            <button className="button-primary mt-3">Aggiungi al carrello</button>
          </div>
        ))}
        {remote.length === 0 && <p>Nessun preferito salvato. Aggiungi prodotti dalla scheda dettaglio.</p>}
      </div>
    </div>
  );
}
