#!/usr/bin/env python3
"""
Query Supabase bookings table to verify JSON-list storage
"""
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

print("=" * 100)
print("CHECKING SUPABASE BOOKINGS TABLE - VERIFYING JSON-LIST STORAGE")
print("=" * 100)
print()

# Query the bookings table - get latest booking for privatekurs
url = f"{SUPABASE_URL}/rest/v1/bookings?course_type=eq.Privatkurs for nybegynnere - Fysisk&order=created_at.desc&limit=1"

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        bookings = response.json()
        
        if bookings:
            booking = bookings[0]
            
            print("✅ LATEST PRIVATKURS BOOKING FOUND!")
            print()
            print("-" * 100)
            print(f"ID:           {booking.get('id')}")
            print(f"Full Name:    {booking.get('full_name')}")
            print(f"Email:        {booking.get('email')}")
            print(f"Phone:        {booking.get('phone')}")
            print(f"Course Type:  {booking.get('course_type')}")
            print(f"Created At:   {booking.get('created_at')}")
            print()
            print("BOOKING_DATE (JSON-LIST):")
            print("-" * 100)
            
            # Try to parse JSON
            booking_date = booking.get('booking_date')
            
            if isinstance(booking_date, str):
                print(f"Type: STRING (correctly stored as TEXT)")
                print()
                
                try:
                    dates_list = json.loads(booking_date)
                    print(f"✅ Valid JSON-list with {len(dates_list)} dates:")
                    print()
                    
                    for i, date_slot in enumerate(dates_list, 1):
                        print(f"   Day {i}:")
                        print(f"     Date:    {date_slot.get('date')}")
                        print(f"     Time:    {date_slot.get('time')}")
                        print(f"     End Time: {date_slot.get('endTime')}")
                        print()
                    
                    print("FULL JSON:")
                    print("-" * 100)
                    print(json.dumps(dates_list, indent=2, ensure_ascii=False))
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON: {e}")
                    print(f"Raw value: {booking_date}")
            else:
                print(f"Type: {type(booking_date).__name__}")
                print(f"Value: {booking_date}")
            
            print()
            print("-" * 100)
            print("BOOKING_TIME: ", booking.get('booking_time'))
            print("END_TIME:     ", booking.get('end_time'))
            print("-" * 100)
            print()
            print("✅ SUCCESS! JSON-list storage is working correctly!")
            print()
            
        else:
            print("❌ No Privatkurs bookings found")
            print()
            print("Fetching ALL bookings...")
            url_all = f"{SUPABASE_URL}/rest/v1/bookings?order=created_at.desc&limit=5"
            response_all = requests.get(url_all, headers=headers)
            
            if response_all.status_code == 200:
                all_bookings = response_all.json()
                
                if all_bookings:
                    print(f"Found {len(all_bookings)} bookings:")
                    for b in all_bookings:
                        print(f"  - {b.get('full_name')} ({b.get('course_type')})")
                else:
                    print("No bookings found at all")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
