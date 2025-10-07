import Link from 'next/link';

const demoOrders = [
  { id: 'res-1', status: 'preparazione', pickupCode: 'ABC123' },
  { id: 'res-2', status: 'pronto', pickupCode: 'XYZ789' },
];

export default function MerchantDashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Ordini Prenota & Ritira</h1>
        <Link href="/" className="text-sm text-sky-600">
          Torna alla home
        </Link>
      </div>
      <div className="space-y-4">
        {demoOrders.map((order) => (
          <div key={order.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm font-semibold text-slate-800">{order.id}</p>
            <p className="text-sm text-slate-600">Stato: {order.status}</p>
            <p className="text-sm text-slate-600">Pickup code: {order.pickupCode}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
