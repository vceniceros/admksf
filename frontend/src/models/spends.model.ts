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
  APROBADO = 'Aprobado',
  PARCIAL = 'Parcial'
}

export interface Spend {
  idGasto: number;
  cuitConsorcio: string;
  cuitProveedor: string;
  periodo: string;
  descripcion: string;
  monto: number;
  fechaRegistro: string;
  tipoGasto: TipoGasto;
  estadoPago: EstadoPago;
}
