export enum ConsortiumStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  PENDING = 'PENDING'
}

export interface Consortium {
  id: string;
  name: string;
  status: ConsortiumStatus;
  address: string;
  units: number;
  owners: number;
  imageUrl: string;
}
