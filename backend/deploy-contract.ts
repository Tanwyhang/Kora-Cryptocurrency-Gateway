import { config } from "dotenv";
import { createThirdwebClient } from "thirdweb";
import { arbitrum } from "thirdweb/chains";
import { deployPublishedContract } from "thirdweb/deploys";
import { privateKeyToAccount } from "thirdweb/wallets";
import { readFileSync } from "fs";

config({ path: ".env.local" });

const deployContract = async () => {
  if (!process.env.WALLET_PRIVATE_KEY || !process.env.THIRDWEB_SECRET_KEY) {
    throw new Error("Missing environment variables");
  }

  const client = createThirdwebClient({
    secretKey: process.env.THIRDWEB_SECRET_KEY,
  });

  const account = privateKeyToAccount({
    client,
    privateKey: process.env.WALLET_PRIVATE_KEY,
  });

  console.log("Deploying from:", account.address);
  console.log("Chain: Arbitrum One");

  // Read contract source
  const contractSource = readFileSync("contracts/PaymentGateway.sol", "utf8");
  
  console.log("\n📝 Contract Source:");
  console.log(contractSource);
  
  console.log("\n⚠️  Manual Deployment Required:");
  console.log("1. Go to https://thirdweb.com/dashboard");
  console.log("2. Click 'Deploy Contract'");
  console.log("3. Select 'Arbitrum One' as the chain");
  console.log("4. Upload PaymentGateway.sol");
  console.log("5. Deploy the contract");
  console.log("6. After deployment, whitelist stablecoins:");
  console.log("   - USDC: 0xaf88d065e77c8cC2239327C5EDb3A432268e5831");
  console.log("   - USDT: 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9");
  console.log("   - DAI: 0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1");
  console.log("\n7. Update .env.local with PAYMENT_CONTRACT_ADDRESS");
};

deployContract().catch(console.error);
