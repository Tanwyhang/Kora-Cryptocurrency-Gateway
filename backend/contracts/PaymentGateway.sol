// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract PaymentGateway {
    address public owner;
    
    struct Payment {
        string sessionId;
        address payer;
        address merchant;
        address token;
        uint256 amount;
        uint256 timestamp;
        bool completed;
    }
    
    mapping(string => Payment) public payments;
    mapping(address => bool) public allowedTokens;
    
    event PaymentReceived(
        string indexed sessionId,
        address indexed payer,
        address indexed merchant,
        address token,
        uint256 amount
    );
    
    event PaymentCompleted(string indexed sessionId);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    function addAllowedToken(address token) external onlyOwner {
        allowedTokens[token] = true;
    }
    
    function removeAllowedToken(address token) external onlyOwner {
        allowedTokens[token] = false;
    }
    
    function processPayment(
        string memory sessionId,
        address merchant,
        address token,
        uint256 amount
    ) external {
        require(allowedTokens[token], "Token not allowed");
        require(payments[sessionId].amount == 0, "Payment exists");
        require(amount > 0, "Invalid amount");
        
        IERC20(token).transferFrom(msg.sender, merchant, amount);
        
        payments[sessionId] = Payment({
            sessionId: sessionId,
            payer: msg.sender,
            merchant: merchant,
            token: token,
            amount: amount,
            timestamp: block.timestamp,
            completed: true
        });
        
        emit PaymentReceived(sessionId, msg.sender, merchant, token, amount);
        emit PaymentCompleted(sessionId);
    }
    
    function getPayment(string memory sessionId) external view returns (Payment memory) {
        return payments[sessionId];
    }
}
