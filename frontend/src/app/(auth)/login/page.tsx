'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useState } from 'react';
import api from '@/lib/api';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof schema>;

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const [message, setMessage] = useState<string | null>(null);

  const onSubmit = async (values: FormValues) => {
    setMessage(null);
    try {
      await api.post('/auth/login', values);
      setMessage('Login eseguito!');
    } catch (error) {
      setMessage('Credenziali non valide');
    }
  };

  return (
    <div className="mx-auto max-w-md space-y-6">
      <h1 className="text-2xl font-semibold text-slate-900">Accedi</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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
        <button type="submit" className="button-primary" disabled={isSubmitting}>
          {isSubmitting ? 'Accesso...' : 'Accedi'}
        </button>
      </form>
      {message && <p className="text-sm text-slate-700">{message}</p>}
    </div>
  );
}
