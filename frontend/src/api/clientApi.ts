import client from './client';
import { Client, ClientCreateRequest } from '../types/Client';

export const clientApi = {
  // Create a new client
  async createClient(data: ClientCreateRequest): Promise<Client> {
    const response = await client.post<Client>('/clients', data);
    return response.data;
  },

  // Get all clients
  async getClients(): Promise<Client[]> {
    const response = await client.get<Client[]>('/clients');
    return response.data;
  },

  // Get a single client by ID
  async getClient(id: number): Promise<Client> {
    const response = await client.get<Client>(`/clients/${id}`);
    return response.data;
  },
};
