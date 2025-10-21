export const ARBITRUM_ONE_CHAIN_ID = 42161;

export const STABLECOINS = {
  USDC: {
    address: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    decimals: 6,
    symbol: "USDC"
  },
  USDT: {
    address: "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    decimals: 6,
    symbol: "USDT"
  },
  DAI: {
    address: "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    decimals: 18,
    symbol: "DAI"
  },
  MYRC: {
    address: "0x3eD03E95DD894235090B3d4A49E0C3239EDcE59e",
    decimals: 18,
    symbol: "MYRC"
  }

} as const;

export type StablecoinSymbol = keyof typeof STABLECOINS;
