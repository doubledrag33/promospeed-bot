interface ProductPageProps {
  params: { id: string };
}

export default function ProductPage({ params }: ProductPageProps) {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">Dettaglio prodotto {params.id}</h1>
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm text-slate-600">Confronto prezzi e offerte saranno caricati lato client.</p>
      </div>
    </div>
  );
}
