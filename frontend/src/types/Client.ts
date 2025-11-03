export interface Client {
  id: number;
  name: string;
  billing_address: string;
  email: string;
  phone_number: string;
  created_at: string;
}

export interface ClientCreateRequest {
  name: string;
  billing_address: string;
  email: string;
  phone_number: string;
}
