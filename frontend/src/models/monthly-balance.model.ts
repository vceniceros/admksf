export interface MonthlyBalance {
  id: number;
  numeroUnidad: number;
  cuitConsorcio: string;
  mesAnio: string;
  saldoInicial: number;
  totalGastos: number;
  totalPagos: number;
  saldoFinal: number;
  fechaCierre?: string | null;
}
