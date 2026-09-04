#!/usr/bin/env python3
"""
Script to alter booking_date column from DATE to TEXT in Supabase
"""

import subprocess
import sys

print("=" * 80)
print("ATTEMPTING TO RUN SQL VIA SUPABASE CLI")
print("=" * 80)
print()

# First, check if supabase CLI is installed
try:
    result = subprocess.run(['which', 'supabase'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Supabase CLI not installed. Installing...")
        subprocess.run(['brew', 'install', 'supabase'], check=True)
    else:
        print("✅ Supabase CLI found")
except Exception as e:
    print(f"⚠️ Could not check for Supabase CLI: {e}")
    print()
    print("Manual Alternative - Use Supabase SQL Editor:")
    print("1. Go to: https://app.supabase.com")
    print("2. Select project 'okleposypaswgvqimllq'")
    print("3. Click 'SQL Editor'")
    print("4. Paste this SQL:")
    print()
    print("ALTER TABLE bookings ALTER COLUMN booking_date TYPE TEXT;")
    print()
    print("5. Check the console for errors - it might say something like:")
    print("   - 'column ... does not exist'")
    print("   - 'relation ... does not exist'")
    print("   - Permission errors")
    sys.exit(1)

print()
print("Trying alternative method using psql...")
print()

# Try using psql directly if available
sql_command = "ALTER TABLE bookings ALTER COLUMN booking_date TYPE TEXT;"

try:
    # This requires DATABASE_URL to be set
    result = subprocess.run(
        ['psql', '-U', 'postgres', '-c', sql_command],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print("✅ SUCCESS! Column altered successfully")
        print(result.stdout)
    else:
        print("❌ Error running command:")
        print(result.stderr)
        
except Exception as e:
    print(f"⚠️  Could not run psql: {e}")
    print()
    print("SOLUTION: Check Supabase Console for Errors")
    print("-" * 80)
    print()
    print("Possible issues:")
    print()
    print("1️⃣  TABLE DOESN'T EXIST")
    print("   - Run this first to create it:")
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
""")
    print()
    print("2️⃣  PERMISSION DENIED")
    print("   - Check if your API key has admin privileges")
    print("   - Use a service_role key instead of anon key")
    print()
    print("3️⃣  COLUMN ALREADY EXISTS")
    print("   - Just verify the column type is TEXT")
    print("   - Run: \\d bookings (in SQL Editor)")
