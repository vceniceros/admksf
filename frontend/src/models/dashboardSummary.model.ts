export interface FinancialMetrics {
  monthlyIncome: number;
  monthlyExpenses: number;
  incomeTrend: number;
  expenseTrend: number;
}

export interface CollectionMetrics {
  percentage: number;
  collectedAmount: number;
  pendingAmount: number;
}

export interface OccupancyMetrics {
  total: number;
  occupied: number;
  rented: number;
  empty: number;
}

export interface DashboardSummary {
  consortiumId: number;
  financials: FinancialMetrics;
  collection: CollectionMetrics;
  occupancy: OccupancyMetrics;
}
