export type ServiceStatus = 'OK' | 'WARNING' | 'ERROR';

export interface ServiceStatusItem {
  id: string;
  name: string;
  company: string;
  phoneNumber: string;
  status: ServiceStatus;
}
