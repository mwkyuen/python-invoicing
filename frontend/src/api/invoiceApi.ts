import client from './client';
import {
  Invoice,
  InvoiceCreateRequest,
  InvoiceUpdateStatusRequest,
} from '../types/Invoice';

export const invoiceApi = {
  // Create a new invoice
  async createInvoice(data: InvoiceCreateRequest): Promise<Invoice> {
    const response = await client.post<Invoice>('/invoices', data);
    return response.data;
  },

  // Get all invoices
  async getInvoices(): Promise<Invoice[]> {
    const response = await client.get<Invoice[]>('/invoices');
    return response.data;
  },

  // Get a single invoice by ID
  async getInvoice(id: number): Promise<Invoice> {
    const response = await client.get<Invoice>(`/invoices/${id}`);
    return response.data;
  },

  // Update invoice status
  async updateInvoiceStatus(
    id: number,
    data: InvoiceUpdateStatusRequest
  ): Promise<Invoice> {
    const response = await client.patch<Invoice>(`/invoices/${id}`, data);
    return response.data;
  },

  // Download invoice PDF
  async downloadInvoicePDF(id: number): Promise<Blob> {
    const response = await client.get(`/invoices/${id}/pdf`, {
      responseType: 'blob',
    });
    return response.data;
  },
};
