export type NotificationType = 'WARNING' | 'ERROR' | 'INFO';

export interface Notification {
  id: number;
  type: NotificationType;
  message: string;
  timestamp: string;
}
