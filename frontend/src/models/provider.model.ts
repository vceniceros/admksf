export type ProviderType = 'servicios_mensuales' | 'reparaciones_mantenimientos';

export interface Provider {
  cuit: string;
  razon_social: string;
  telefono?: string | null;
  email?: string | null;
  calle: string;
  numero: number;
  codigo_postal: string;
  ciudad: string;
  tipo_proveedor: ProviderType;
  numero_cuenta?: string | null;
  numero_reclamo?: string | null;
}
