import requests

# Supabase credentials
SUPABASE_URL = "https://okleposypaswgvqimllq.supabase.co"
API_KEY = "sb_publishable_4YoOqmfGglQjHflVyVk7LQ_SXt2Wblx"

# Headers for API request
headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# SQL query to alter the column
sql_query = """
ALTER TABLE bookings 
ALTER COLUMN booking_date TYPE TEXT;
"""

print("=" * 80)
print("FIXING BOOKING_DATE COLUMN")
print("=" * 80)
print(f"\nExecuting SQL query:")
print(f"  ALTER TABLE bookings ALTER COLUMN booking_date TYPE TEXT;")
print()

# Execute the SQL query via Supabase SQL Editor endpoint
url = f"{SUPABASE_URL}/rest/v1/rpc/query"

try:
    # Note: Supabase doesn't have a direct SQL execution endpoint via REST
    # We'll use the Python client method instead
    print("⚠️  To execute this SQL, you must:")
    print("1. Go to Supabase Dashboard: https://app.supabase.com")
    print("2. Select your project (okleposypaswgvqimllq)")
    print("3. Click 'SQL Editor' in the left sidebar")
    print("4. Click 'New Query'")
    print("5. Paste the following SQL and click 'Run':")
    print()
    print("─" * 80)
    print(sql_query)
    print("─" * 80)
    print()
    print("✅ The booking_date column will be changed from DATE to TEXT")
    print("✅ This allows storing JSON arrays with 5 dates for Privatkurs bookings")
    
except Exception as e:
    print(f"Error: {e}")
