import { StablecoinSymbol } from "./constants";

export interface PaymentSession {
  sessionId: string;
  merchantId: string;
  amount: string;
  currency: StablecoinSymbol;
  customerEmail?: string;
  callbackUrl: string;
  status: "pending" | "processing" | "completed" | "failed" | "expired";
  createdAt: Date;
  expiresAt: Date;
  transactionHash?: string;
}

export interface CreatePaymentRequest {
  merchant_id: string;
  amount: string;
  currency: StablecoinSymbol;
  customer_email?: string;
  callback_url: string;
}

export interface CreatePaymentResponse {
  session_id: string;
  payment_url: string;
  expires_at: string;
}

export interface PaymentStatusResponse {
  session_id: string;
  status: PaymentSession["status"];
  amount: string;
  currency: StablecoinSymbol;
  transaction_hash?: string;
}
