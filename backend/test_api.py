import requests
import json
from datetime import datetime
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3001")
SUPPORTED_CURRENCIES = ["USDC", "USDT", "DAI", "MYRC"]
TEST_MERCHANT_ID = "merchant_test_001"
TEST_AMOUNT = "50.00"
TEST_EMAIL = "test@example.com"
TEST_CALLBACK_URL = "https://example.com/webhook"
TEST_TX_HASH = "0x" + "a" * 64
FAKE_SESSION_ID = "sess_nonexistent_test"

test_results = []

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_request(method, endpoint, payload=None):
    print(f"\n📤 REQUEST:")
    print(f"   Method: {method}")
    print(f"   Endpoint: {endpoint}")
    if payload:
        print(f"   Payload:")
        print(f"   {json.dumps(payload, indent=6)}")

def print_response(status, data, expected_status=200):
    success = status == expected_status
    icon = "✅" if success else "❌"
    print(f"\n📥 RESPONSE:")
    print(f"   Status Code: {status} {icon}")
    print(f"   Expected: {expected_status}")
    print(f"   Body:")
    print(f"   {json.dumps(data, indent=6)}")
    return success

def test_health():
    print_section("TEST 1: Health Check")
    print("Description: Verify API server is running and responsive")
    
    endpoint = f"{BASE_URL}/health"
    print_request("GET", endpoint)
    
    response = requests.get(endpoint)
    success = print_response(response.status_code, response.json())
    
    test_results.append({"test": "Health Check", "passed": success})
    return response.status_code == 200

def test_create_payment():
    print_section("TEST 2: Create Payment Session (USDC)")
    print("Description: Create a new payment session for $50 USDC")
    
    payload = {
        "merchant_id": TEST_MERCHANT_ID,
        "amount": TEST_AMOUNT,
        "currency": SUPPORTED_CURRENCIES[0],
        "customer_email": TEST_EMAIL,
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data)
    
    if success:
        print(f"\n💡 ANALYSIS:")
        print(f"   ✓ Session ID generated: {data.get('session_id')}")
        print(f"   ✓ Payment URL: {data.get('payment_url')}")
        print(f"   ✓ Expires at: {data.get('expires_at')}")
    
    test_results.append({"test": "Create Payment (USDC)", "passed": success})
    return data.get("session_id") if response.status_code == 200 else None

def test_get_payment_status(session_id, test_num, description):
    print_section(f"TEST {test_num}: Get Payment Status")
    print(f"Description: {description}")
    
    endpoint = f"{BASE_URL}/api/payments/{session_id}"
    print_request("GET", endpoint)
    
    response = requests.get(endpoint)
    data = response.json()
    success = print_response(response.status_code, data)
    
    if success:
        print(f"\n💡 ANALYSIS:")
        print(f"   ✓ Session ID: {data.get('session_id')}")
        print(f"   ✓ Status: {data.get('status')}")
        print(f"   ✓ Amount: {data.get('amount')} {data.get('currency')}")
        if data.get('transaction_hash'):
            print(f"   ✓ Transaction Hash: {data.get('transaction_hash')}")
    
    test_results.append({"test": f"Get Payment Status ({test_num})", "passed": success})
    return response.status_code == 200

def test_confirm_payment(session_id):
    print_section("TEST 4: Confirm Payment")
    print("Description: Simulate payment confirmation with transaction hash")
    
    payload = {
        "transaction_hash": TEST_TX_HASH
    }
    
    endpoint = f"{BASE_URL}/api/payments/{session_id}/confirm"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data)
    
    if success:
        print(f"\n💡 ANALYSIS:")
        print(f"   ✓ Payment confirmed successfully")
        print(f"   ✓ Status should change from 'pending' to 'completed'")
    
    test_results.append({"test": "Confirm Payment", "passed": success})
    return response.status_code == 200

def test_myrc_payment():
    print_section("TEST 6: Create Payment Session (MYRC)")
    print("Description: Test MYRC token support - Create payment for 100 MYRC")
    
    payload = {
        "merchant_id": f"{TEST_MERCHANT_ID}_myrc",
        "amount": "100.00",
        "currency": "MYRC",
        "customer_email": TEST_EMAIL,
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data)
    
    if success:
        print(f"\n💡 ANALYSIS:")
        print(f"   ✓ MYRC token is whitelisted")
        print(f"   ✓ Session created: {data.get('session_id')}")
    
    test_results.append({"test": "Create Payment (MYRC)", "passed": success})
    return response.status_code == 200

def test_invalid_currency():
    print_section("TEST 7: Invalid Currency Validation")
    print("Description: Verify API rejects unsupported currencies (BTC)")
    
    payload = {
        "merchant_id": TEST_MERCHANT_ID,
        "amount": TEST_AMOUNT,
        "currency": "BTC",
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    if success:
        print(f"\n💡 ANALYSIS:")
        print(f"   ✓ API correctly rejected invalid currency")
        print(f"   ✓ Supported currencies: {', '.join(SUPPORTED_CURRENCIES)}")
    
    test_results.append({"test": "Invalid Currency", "passed": success})
    return response.status_code == 400

def test_missing_merchant_id():
    print_section("TEST 8: Missing Merchant ID")
    print("Description: Verify API rejects payment without merchant_id")
    
    payload = {
        "amount": TEST_AMOUNT,
        "currency": SUPPORTED_CURRENCIES[0],
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    test_results.append({"test": "Missing Merchant ID", "passed": success})
    return response.status_code == 400

def test_missing_amount():
    print_section("TEST 9: Missing Amount")
    print("Description: Verify API rejects payment without amount")
    
    payload = {
        "merchant_id": TEST_MERCHANT_ID,
        "currency": SUPPORTED_CURRENCIES[0],
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    test_results.append({"test": "Missing Amount", "passed": success})
    return response.status_code == 400

def test_missing_currency():
    print_section("TEST 10: Missing Currency")
    print("Description: Verify API rejects payment without currency")
    
    payload = {
        "merchant_id": TEST_MERCHANT_ID,
        "amount": TEST_AMOUNT,
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    test_results.append({"test": "Missing Currency", "passed": success})
    return response.status_code == 400

def test_missing_callback_url():
    print_section("TEST 11: Missing Callback URL")
    print("Description: Verify API rejects payment without callback_url")
    
    payload = {
        "merchant_id": TEST_MERCHANT_ID,
        "amount": TEST_AMOUNT,
        "currency": SUPPORTED_CURRENCIES[0]
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    test_results.append({"test": "Missing Callback URL", "passed": success})
    return response.status_code == 400

def test_nonexistent_session():
    print_section("TEST 12: Get Non-existent Session")
    print("Description: Verify API returns 404 for invalid session ID")
    
    endpoint = f"{BASE_URL}/api/payments/{FAKE_SESSION_ID}"
    print_request("GET", endpoint)
    
    response = requests.get(endpoint)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=404)
    
    test_results.append({"test": "Non-existent Session", "passed": success})
    return response.status_code == 404

def test_confirm_nonexistent_session():
    print_section("TEST 13: Confirm Non-existent Session")
    print("Description: Verify API returns 404 when confirming invalid session")
    
    payload = {
        "transaction_hash": TEST_TX_HASH
    }
    
    endpoint = f"{BASE_URL}/api/payments/{FAKE_SESSION_ID}/confirm"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=404)
    
    test_results.append({"test": "Confirm Non-existent Session", "passed": success})
    return response.status_code == 404

def test_empty_fields():
    print_section("TEST 14: Empty String Fields")
    print("Description: Verify API rejects empty string values")
    
    payload = {
        "merchant_id": "",
        "amount": TEST_AMOUNT,
        "currency": SUPPORTED_CURRENCIES[0],
        "callback_url": TEST_CALLBACK_URL
    }
    
    endpoint = f"{BASE_URL}/api/payments/create"
    print_request("POST", endpoint, payload)
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    success = print_response(response.status_code, data, expected_status=400)
    
    test_results.append({"test": "Empty String Fields", "passed": success})
    return response.status_code == 400

def test_all_supported_currencies():
    print_section("TEST 15: All Supported Currencies")
    print("Description: Test USDT and DAI token support")
    
    currencies = [c for c in SUPPORTED_CURRENCIES if c not in ["USDC", "MYRC"]]
    all_passed = True
    
    for currency in currencies:
        payload = {
            "merchant_id": f"{TEST_MERCHANT_ID}_{currency.lower()}",
            "amount": "75.00",
            "currency": currency,
            "customer_email": TEST_EMAIL,
            "callback_url": TEST_CALLBACK_URL
        }
        
        endpoint = f"{BASE_URL}/api/payments/create"
        response = requests.post(endpoint, json=payload)
        
        if response.status_code != 200:
            all_passed = False
            print(f"   ✗ {currency} failed")
        else:
            print(f"   ✓ {currency} accepted")
    
    test_results.append({"test": "All Supported Currencies", "passed": all_passed})
    return all_passed

def print_summary():
    print("\n" + "=" * 70)
    print("  TEST SUMMARY REPORT")
    print("=" * 70)
    
    passed = sum(1 for r in test_results if r["passed"])
    total = len(test_results)
    
    print(f"\n📊 Results: {passed}/{total} tests passed\n")
    
    for i, result in enumerate(test_results, 1):
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"   {i}. {result['test']:<30} {status}")
    
    print("\n" + "=" * 70)
    if passed == total:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print(f"  ⚠️  {total - passed} TEST(S) FAILED")
    print("=" * 70 + "\n")

def main():
    print("\n" + "#" * 70)
    print("#" + "" * 68 + "#")
    print("#" + "  KORA GATEWAY API TEST SUITE".center(68) + "#")
    print("#" + "" * 68 + "#")
    print("#" * 70)
    print(f"\n🕐 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Create payment
        session_id = test_create_payment()
        
        if session_id:
            # Test 3: Get payment status (pending)
            test_get_payment_status(session_id, 3, "Check initial payment status (should be pending)")
            
            # Test 4: Confirm payment
            test_confirm_payment(session_id)
            
            # Test 5: Get updated status (completed)
            test_get_payment_status(session_id, 5, "Verify status changed to completed after confirmation")
        
        # Test 6: MYRC payment
        test_myrc_payment()
        
        # Test 7: Invalid currency
        test_invalid_currency()
        
        # Test 8-11: Missing required fields
        test_missing_merchant_id()
        test_missing_amount()
        test_missing_currency()
        test_missing_callback_url()
        
        # Test 12-13: Non-existent sessions
        test_nonexistent_session()
        test_confirm_nonexistent_session()
        
        # Test 14: Empty fields
        test_empty_fields()
        
        # Test 15: All supported currencies
        test_all_supported_currencies()
        
        # Print summary
        print_summary()
        
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 70)
        print("❌ CONNECTION ERROR")
        print("=" * 70)
        print("Cannot connect to backend server.")
        print("Make sure the server is running: npm run server")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}\n")

if __name__ == "__main__":
    main()
