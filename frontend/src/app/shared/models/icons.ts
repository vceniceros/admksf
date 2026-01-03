import {
  LayoutDashboard,
  Users,
  Building2,
  Receipt,
  CreditCard,
  FileText,
  Menu,
  X
} from 'lucide';

export type IconKey = 'dashboard' | 'owners' | 'units' | 'expenses' | 'payments' | 'reports' | 'menu' | 'close';

export const ICONS: Record<IconKey, any> = {
  dashboard: LayoutDashboard,
  owners: Users,
  units: Building2,
  expenses: Receipt,
  payments: CreditCard,
  reports: FileText,
  menu: Menu,
  close: X,
};