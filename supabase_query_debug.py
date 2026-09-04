import requests
import json

# Supabase credentials
SUPABASE_URL = "https://okleposypaswgvqimllq.supabase.co"
API_KEY = "sb_publishable_4YoOqmfGglQjHflVyVk7LQ_SXt2Wblx"

# Headers for API request
headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_table(table_name):
    """Query a Supabase table with debugging"""
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    print(f"\n🔍 Querying: {url}")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text[:200]}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying {table_name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        return []

print("\n" + "=" * 100)
print("SUPABASE DATABASE QUERY WITH DEBUGGING")
print("=" * 100)

# Query users table
users = query_table("users")
print(f"\n✓ Users Retrieved: {len(users)}")

# Query bookings table
bookings = query_table("bookings")
print(f"✓ Bookings Retrieved: {len(bookings)}")

if users:
    print("\n📋 USERS:")
    for user in users:
        print(json.dumps(user, indent=2))

if bookings:
    print("\n📋 BOOKINGS:")
    for booking in bookings:
        print(json.dumps(booking, indent=2))
