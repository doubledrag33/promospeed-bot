import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="space-y-10">
      <section className="rounded-2xl bg-lime/40 p-8">
        <h1 className="text-3xl font-bold text-slate-900">Benvenuto su Gropt</h1>
        <p className="mt-4 text-lg text-slate-700">
          Crea la tua lista della spesa, confronta i prezzi e ottimizza il giro tra i tuoi negozi preferiti.
        </p>
        <div className="mt-6 flex flex-wrap gap-4">
          <Link href="/cart" className="button-primary">
            Vai al carrello
          </Link>
          <Link href="/offers" className="button-primary bg-sky text-white">
            Scopri le offerte
          </Link>
        </div>
      </section>
      <section>
        <h2 className="text-2xl font-semibold text-slate-900">Come funziona</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {[
            {
              title: 'Confronta prezzi',
              text: 'Ogni prodotto mostra il miglior prezzo disponibile, con fonte e data di rilevazione.',
            },
            {
              title: 'Ottimizza il giro',
              text: 'Ricevi tre piani personalizzati: economico, equilibrato e un solo negozio.',
            },
            {
              title: 'Prenota & Ritira',
              text: 'Per i partner puoi bloccare il ritiro con un codice pickup univoco.',
            },
          ].map((card) => (
            <div key={card.title} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-xl font-semibold text-slate-900">{card.title}</h3>
              <p className="mt-2 text-sm text-slate-600">{card.text}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
