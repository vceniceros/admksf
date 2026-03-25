export type PaymentStatus = 'PAID' | 'PENDING' | 'Aprobado' | 'Pendiente' | 'Parcial';

export interface Payment {
  id: number;
  personName?: string;
  unit?: string;
  amount: number;
  status: PaymentStatus;
  numeroUnidad?: number;
  cuitConsorcio?: string;
  propietario?: string;
  fechaPago?: string;
}
