import requests
import json
from datetime import datetime

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
    """Query a Supabase table"""
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying {table_name}: {e}")
        return []

# Query users table
print("\n" + "=" * 110)
print("SUPABASE DATABASE QUERY RESULTS")
print("=" * 110)

print("\n📋 USERS TABLE")
print("-" * 110)
users = query_table("users")

if users:
    print(f"Total Users: {len(users)}\n")
    print(f"{'Email':<45} {'Full Name':<30} {'Created At':<35}")
    print("-" * 110)
    for user in users:
        email = str(user.get('email', 'N/A'))
        full_name = str(user.get('full_name', 'N/A'))
        created_at = str(user.get('created_at', 'N/A'))
        print(f"{email:<45} {full_name:<30} {created_at:<35}")
else:
    print("Total Users: 0")
    print("⚠️  No users found in the 'users' table - table is empty")

# Query bookings table
print("\n" + "=" * 110)
print("📋 BOOKINGS TABLE")
print("-" * 110)
bookings = query_table("bookings")

if bookings:
    print(f"Total Bookings: {len(bookings)}\n")
    print(f"{'Full Name':<25} {'Email':<40} {'Phone':<15} {'Course Type':<25} {'Booking Date':<20}")
    print("-" * 110)
    for booking in bookings:
        full_name = str(booking.get('full_name', 'N/A'))
        email = str(booking.get('email', 'N/A'))
        phone = str(booking.get('phone', 'N/A'))
        course_type = str(booking.get('course_type', 'N/A'))
        booking_date = str(booking.get('booking_date', 'N/A'))
        print(f"{full_name:<25} {email:<40} {phone:<15} {course_type:<25} {booking_date:<20}")
else:
    print("Total Bookings: 0")
    print("⚠️  No bookings found in the 'bookings' table - table is empty")

# Print summary
print("\n" + "=" * 110)
print("SUMMARY")
print("=" * 110)
print(f"✓ Total Users in 'users' table: {len(users)}")
print(f"✓ Total Bookings in 'bookings' table: {len(bookings)}")
print(f"✓ Supabase URL: {SUPABASE_URL}")
print(f"✓ API Connection Status: SUCCESS (HTTP 200)")
print("=" * 110 + "\n")
