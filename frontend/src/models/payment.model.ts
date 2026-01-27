export type PaymentStatus = 'PAID' | 'PENDING';

export interface Payment {
  id: number;
  personName: string;
  unit: string;
  amount: number;
  status: PaymentStatus;
}
