#!/usr/bin/env python3
"""
Supabase - Fix booking_date column type
"""

import os
import sys

# Install dependencies if needed
try:
    from supabase import create_client
except ImportError:
    print("Installing supabase package...")
    os.system("pip install supabase")
    from supabase import create_client

SUPABASE_URL = "https://okleposypaswgvqimllq.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "your_service_role_key_here")

print("=" * 80)
print("SUPABASE BOOKING_DATE FIX")
print("=" * 80)
print()

if SERVICE_ROLE_KEY == "your_service_role_key_here":
    print("⚠️  STEPS TO FIX:")
    print()
    print("1. Go to Supabase Dashboard: https://app.supabase.com")
    print("2. Select project: okleposypaswgvqimllq")
    print("3. Go to Settings → API Tokens")
    print("4. Copy the 'service_role' (secret) key")
    print("5. Create a .env file with:")
    print()
    print('   SUPABASE_SERVICE_ROLE_KEY="your_secret_key_here"')
    print()
    print("6. Run this script again")
    print()
    print("=" * 80)
    print()
    print("OR DO IT MANUALLY:")
    print()
    print("1. Go to SQL Editor in Supabase")
    print("2. Click 'New Query'")
    print("3. Paste this:")
    print()
    print("   -- First, check if table exists:")
    print("   SELECT * FROM information_schema.tables WHERE table_name = 'bookings';")
    print()
    print("   -- Then run:")
    print("   ALTER TABLE bookings ALTER COLUMN booking_date TYPE TEXT;")
    print()
    print("4. Look for any error messages at the bottom of the screen")
    print()
    sys.exit(1)

print(f"Connecting to Supabase...")
print(f"URL: {SUPABASE_URL}")
print()

try:
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    
    # Test connection by fetching table info
    print("Testing connection...")
    response = supabase.table('bookings').select('*', count='exact').limit(1).execute()
    
    print("✅ Connected to database!")
    print(f"   Bookings table found: {response.count} records")
    print()
    
except Exception as e:
    print(f"❌ Error connecting: {e}")
    print()
    print("This likely means:")
    print("1. The 'bookings' table doesn't exist yet")
    print("2. The service role key is invalid")
    print()
    print("SOLUTION:")
    print("Go to Supabase SQL Editor and run:")
    print()
    print("""
CREATE TABLE IF NOT EXISTS bookings (
  id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  booking_date TEXT NOT NULL,
  booking_time TIME NOT NULL,
  end_time TIME,
  duration_minutes INT DEFAULT 75,
  course_type VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_bookings_email ON bookings(email);
CREATE INDEX idx_bookings_course_type ON bookings(course_type);
CREATE INDEX idx_bookings_booking_date ON bookings(booking_date);
""")
    sys.exit(1)
