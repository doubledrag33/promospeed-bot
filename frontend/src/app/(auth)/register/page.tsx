'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import api from '@/lib/api';

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
  cap: z.string().min(5).max(5),
  consent_geoloc: z.boolean().optional(),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { consent_geoloc: false },
  });
  const [message, setMessage] = useState<string | null>(null);

  const onSubmit = async (values: FormValues) => {
    setMessage(null);
    try {
      await api.post('/auth/register', values);
      setMessage('Registrazione completata! Controlla la tua email.');
    } catch (error) {
      setMessage('Registrazione fallita. Riprovare.');
    }
  };

  return (
    <div className="mx-auto max-w-md space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Crea un account</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700">Nome</label>
          <input className="w-full rounded-lg border border-slate-300 p-2" {...register('name')} />
          {errors.name && <p className="text-sm text-rose-500">{errors.name.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">Email</label>
          <input className="w-full rounded-lg border border-slate-300 p-2" type="email" {...register('email')} />
          {errors.email && <p className="text-sm text-rose-500">{errors.email.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">Password</label>
          <input className="w-full rounded-lg border border-slate-300 p-2" type="password" {...register('password')} />
          {errors.password && <p className="text-sm text-rose-500">{errors.password.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">CAP</label>
          <input className="w-full rounded-lg border border-slate-300 p-2" {...register('cap')} />
          {errors.cap && <p className="text-sm text-rose-500">{errors.cap.message}</p>}
        </div>
        <label className="flex items-center gap-2 text-sm text-slate-600">
          <input type="checkbox" {...register('consent_geoloc')} />
          Acconsento alla geolocalizzazione per ottimizzare il percorso
        </label>
        <button type="submit" className="button-primary" disabled={isSubmitting}>
          {isSubmitting ? 'Invio...' : 'Registrati'}
        </button>
      </form>
      {message && <p className="text-sm text-slate-700">{message}</p>}
    </div>
  );
}
