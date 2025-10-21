# Payment Gateway Smart Contract

## Contract: PaymentGateway.sol

Minimal smart contract for accepting stablecoin payments on Arbitrum One.

### Features
- Accept USDC, USDT, DAI payments
- Track payment sessions
- Direct merchant payouts
- Event emission for backend tracking

### Functions

**Owner Functions:**
- `addAllowedToken(address token)` - Whitelist stablecoin
- `removeAllowedToken(address token)` - Remove stablecoin

**Payment Functions:**
- `processPayment(sessionId, merchant, token, amount)` - Process payment
- `getPayment(sessionId)` - Get payment details

### Events
- `PaymentReceived` - Emitted when payment is processed
- `PaymentCompleted` - Emitted when payment is confirmed

## Deployment Steps

### Option 1: Thirdweb Dashboard (Recommended)

1. Go to https://thirdweb.com/dashboard
2. Click "Deploy Contract"
3. Select "Arbitrum One"
4. Upload `PaymentGateway.sol`
5. Click "Deploy"
6. After deployment, call `addAllowedToken()` for each stablecoin:
   - USDC: `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`
   - USDT: `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`
   - DAI: `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1`

### Option 2: Using Script

```bash
npm run deploy
```

## After Deployment

1. Copy the contract address
2. Update `.env.local`:
```
PAYMENT_CONTRACT_ADDRESS=0x...
```

3. Whitelist stablecoins using Thirdweb dashboard or script

## Contract Interaction

### From Frontend (with Account Abstraction)

```typescript
import { prepareContractCall } from "thirdweb";
import { useSendTransaction } from "thirdweb/react";

const transaction = prepareContractCall({
  contract,
  method: "processPayment",
  params: [sessionId, merchantAddress, tokenAddress, amount]
});

await sendTransaction(transaction);
```

### From Backend (verify payment)

```typescript
import { getContract, readContract } from "thirdweb";

const payment = await readContract({
  contract,
  method: "getPayment",
  params: [sessionId]
});
```
