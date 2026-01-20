export enum TipoGasto {
  MANTENIMIENTO = 'Mantenimiento',
  SERVICIOS = 'Servicios',
  LIMPIEZA = 'Limpieza',
  SEGURIDAD = 'Seguridad',
  ADMINISTRACION = 'Administracion',
  OTROS = 'Otros'
}

export enum EstadoPago {
  PENDIENTE = 'Pendiente',
  PAGADO = 'Pagado'
}

export interface Spend {
  idGasto: number;
  cuitConsorcio: string;
  cuitProveedor: string;
  periodo: string; // DATE format (YYYY-MM-DD)
  descripcion: string;
  monto: number;
  fechaRegistro: string; // TIMESTAMP format
  tipoGasto: TipoGasto;
  estadoPago: EstadoPago;
}
