export interface LineItem {
  id: number;
  invoice_id: number;
  description: string;
  quantity: number;
  unit_price: number;
  amount: number;
}

export interface LineItemCreateRequest {
  description: string;
  quantity: number;
  unit_price: number;
}

export interface Invoice {
  id: number;
  invoice_number: string;
  client_id: number;
  issue_date: string;
  total_amount: number;
  status: string;
  pdf_path: string | null;
  line_items: LineItem[];
}

export interface InvoiceCreateRequest {
  client_id: number;
  line_items: LineItemCreateRequest[];
}

export interface InvoiceUpdateStatusRequest {
  status: string;
}
