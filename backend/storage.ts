import { PaymentSession } from "./types";

// In-memory storage (replace with database in production)
class PaymentStorage {
  private sessions: Map<string, PaymentSession> = new Map();

  create(session: PaymentSession): void {
    this.sessions.set(session.sessionId, session);
  }

  get(sessionId: string): PaymentSession | undefined {
    return this.sessions.get(sessionId);
  }

  update(sessionId: string, updates: Partial<PaymentSession>): void {
    const session = this.sessions.get(sessionId);
    if (session) {
      this.sessions.set(sessionId, { ...session, ...updates });
    }
  }

  delete(sessionId: string): void {
    this.sessions.delete(sessionId);
  }

  getAll(): PaymentSession[] {
    return Array.from(this.sessions.values());
  }
}

export const paymentStorage = new PaymentStorage();
