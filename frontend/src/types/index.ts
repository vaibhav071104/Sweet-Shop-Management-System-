export interface Sweet {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
  description?: string;
}

export interface User {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
