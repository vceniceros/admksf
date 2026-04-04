export interface SettlementTemplate {
  id: number;
  consorcio?: string | null;
  nombre: string;
  version: number;
  activo: boolean;
  config?: any;
}

export interface SettlementColumn {
  id: string;
  label: string;
  visible: boolean;
  calc_type: string;
  help_text?: string;
}

export interface SettlementUnitRow {
  numero_unidad_funcional: number;
  propietario: string;
  apellido: string;
  valores: Record<string, string>;
}

export interface SettlementResponse {
  consorcio: string;
  periodo: string;
  template_id: number;
  columns: SettlementColumn[];
  unidades: SettlementUnitRow[];
  totales: Record<string, string>;
  cerrada?: boolean;
}

export interface SettlementTableRow {
  unidad_funcional: string;
  propietario: string;
  apellido: string;
  [key: string]: string;
}

export interface SettlementTableState {
  columns: SettlementColumn[];
  rows: SettlementTableRow[];
  totales: Record<string, string>;
  templateId: number;
  periodo: string;
  cerrada?: boolean;
}
