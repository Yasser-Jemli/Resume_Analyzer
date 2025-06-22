export interface Post {
  id?: number; // optional
  title: string;
  skills?: string; // optional
  content: string;
  createdAt?: string; // optional
  status?: 'Opened' | 'InProgress' | 'Terminated';
  user?: {
    id: number;
    username?: string;
  };
}


