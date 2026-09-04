# Supabase Database Setup for Lydbar

## Opprett Bookings Tabell

Gå til Supabase Dashboard → SQL Editor og kjør denne kommandoen:

```sql
CREATE TABLE IF NOT EXISTS bookings (
  id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  booking_date DATE NOT NULL,
  booking_time TIME NOT NULL,
  end_time TIME,
  duration_minutes INT DEFAULT 75,
  course_type VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Opprett indeks for raskere søk
CREATE INDEX IF NOT EXISTS idx_bookings_email ON bookings(email);
CREATE INDEX IF NOT EXISTS idx_bookings_course_type ON bookings(course_type);
CREATE INDEX IF NOT EXISTS idx_bookings_booking_date ON bookings(booking_date);
```

## Databaseskjema

**Tabell: `bookings`**

| Kolonne | Type | Beskrivelse |
|---------|------|-------------|
| id | BIGSERIAL | Unik booking-ID (auto-increment) |
| full_name | VARCHAR(255) | Kundens fullt navn |
| email | VARCHAR(255) | Kundens e-postadresse |
| phone | VARCHAR(20) | Kundens telefonnummer (valgfritt) |
| booking_date | DATE | Bookingsdato (YYYY-MM-DD) |
| booking_time | TIME | Starttidspunkt (HH:MM:SS) |
| end_time | TIME | Sluttidspunkt (HH:MM:SS) |
| duration_minutes | INT | Kurstid i minutter (standardverdi 75) |
| course_type | VARCHAR(255) | Kurstype som er booket |
| created_at | TIMESTAMP | Opprettelsestidspunkt |

## Aktiveer Row Level Security (RLS)

Hvis du vil beskytte dataene, kjør også:

```sql
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Tillat alle å lese sine egne bookinger
CREATE POLICY "Users can read own bookings" ON bookings
  FOR SELECT USING (email = current_user_email());

-- Tillat anon-brukere å sette inn bokinger
CREATE POLICY "Anyone can insert bookings" ON bookings
  FOR INSERT WITH CHECK (true);
```

## Status

✅ **Website oppdatert** - Alle bookinger lagres nå i Supabase med:
- Riktig kurstype (Gruppekurs, Privatkurs, osv.)
- Booking-dato og -tidspunkt
- Sluttidspunkt
- Kundinformasjon (navn, e-post, telefon)
- Opprettelsestidspunkt

Bookinger blir automatisk lagret når kunde klikker "Bekreft booking".
