import Link from 'next/link';

const demoOffers = [
  { id: '1', store: 'Coop Ravenna', product: 'Pasta Integrale 500g', price: '0.89€', valid: 'Fino al 21/04' },
  { id: '2', store: 'Conad Ravenna', product: 'Latte Bio 1L', price: '1.19€', valid: 'Fino al 19/04' },
  { id: '3', store: 'Lidl Ravenna', product: 'Olio EVO 750ml', price: '5.49€', valid: 'Fino al 18/04' },
];

export default function OffersPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Offerte vicino a te</h1>
        <Link href="/cart" className="button-primary">
          Aggiungi al carrello
        </Link>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {demoOffers.map((offer) => (
          <div key={offer.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm font-semibold text-slate-800">{offer.store}</p>
            <p className="mt-2 text-lg font-bold text-slate-900">{offer.product}</p>
            <p className="text-sm text-slate-600">{offer.price}</p>
            <p className="text-xs text-slate-500">{offer.valid}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
