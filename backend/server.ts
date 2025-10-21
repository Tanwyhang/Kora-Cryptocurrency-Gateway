import { config } from "dotenv";
import express, { type RequestHandler } from "express";
import cors from "cors";
import { v4 as uuidv4 } from "uuid";
import { CreatePaymentRequest, CreatePaymentResponse, PaymentStatusResponse } from "./types";
import { paymentStorage } from "./storage";
import { STABLECOINS } from "./constants";

config({ path: ".env.local" });

const app = express();
app.use(express.json());

// CORS
app.use(
  cors({
    origin: "*",
    allowedHeaders: ["Content-Type"],
  })
);

// Health check
type HealthResponse = { status: string };
const healthHandler: RequestHandler<{}, HealthResponse> = (req, res) => {
  res.json({ status: "ok" });
};
app.get("/health", healthHandler);

// Create payment session
const createPaymentHandler: RequestHandler<{}, CreatePaymentResponse | any, CreatePaymentRequest> = (req, res) => {
  try {
    const { merchant_id, amount, currency, customer_email, callback_url } = req.body;

    if (!merchant_id || !amount || !currency || !callback_url) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    if (!STABLECOINS[currency]) {
      return res.status(400).json({ error: "Invalid currency" });
    }

    const sessionId = `sess_${uuidv4()}`;
    const now = new Date();
    const expiresAt = new Date(now.getTime() + 30 * 60 * 1000); // 30 minutes

    paymentStorage.create({
      sessionId,
      merchantId: merchant_id,
      amount,
      currency,
      customerEmail: customer_email,
      callbackUrl: callback_url,
      status: "pending",
      createdAt: now,
      expiresAt,
    });

    const response: CreatePaymentResponse = {
      session_id: sessionId,
      payment_url: `${process.env.FRONTEND_URL || "http://localhost:3000"}/payment/${sessionId}`,
      expires_at: expiresAt.toISOString(),
    };

    res.json(response);
  } catch (error) {
    console.error("Error creating payment:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
app.post("/api/payments/create", createPaymentHandler);

// Get payment status
const getPaymentStatusHandler: RequestHandler<{ sessionId: string }, PaymentStatusResponse | any> = (req, res) => {
  try {
    const { sessionId } = req.params;
    const session = paymentStorage.get(sessionId);

    if (!session) {
      return res.status(404).json({ error: "Payment session not found" });
    }

    const response: PaymentStatusResponse = {
      session_id: session.sessionId,
      status: session.status,
      amount: session.amount,
      currency: session.currency,
      transaction_hash: session.transactionHash,
    };

    res.json(response);
  } catch (error) {
    console.error("Error fetching payment:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
app.get("/api/payments/:sessionId", getPaymentStatusHandler);

// Update payment status (called by frontend after transaction)
const confirmPaymentHandler: RequestHandler<
  { sessionId: string },
  { success: boolean } | any,
  { transaction_hash?: string }
> = (req, res) => {
  try {
    const { sessionId } = req.params;
    const { transaction_hash } = req.body;

    const session = paymentStorage.get(sessionId);
    if (!session) {
      return res.status(404).json({ error: "Payment session not found" });
    }

    paymentStorage.update(sessionId, {
      status: "completed",
      transactionHash: transaction_hash,
    });

    // TODO: Trigger merchant callback
    console.log(`Payment completed: ${sessionId}, tx: ${transaction_hash}`);

    res.json({ success: true });
  } catch (error) {
    console.error("Error confirming payment:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
app.post("/api/payments/:sessionId/confirm", confirmPaymentHandler);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Kora Gateway API running on port ${PORT}`);
});
