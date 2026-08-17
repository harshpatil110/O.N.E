import os
import socket
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

print("--- O.N.E. Database Diagnostic Tool ---")

if not db_url:
    print("❌ ERROR: DATABASE_URL is missing from your .env file.")
    exit(1)

# Extract host from postgresql://user:pass@host:port/dbname
try:
    host = db_url.split('@')[1].split(':')[0]
    port = int(db_url.split(':')[3].split('/')[0])
    print(f"🔍 Extracted Host: {host}")
    print(f"🔍 Extracted Port: {port}")
except Exception as e:
    print(f"❌ ERROR: DATABASE_URL is malformed. Cannot extract host/port. {e}")
    exit(1)

# Test 1: DNS Resolution
print("\n[Test 1] Attempting DNS Resolution...")
try:
    ip = socket.gethostbyname(host)
    print(f"✅ Success! Host resolves to IP: {ip}")
except socket.gaierror:
    print(f"❌ FAILED: Cannot resolve host '{host}'.")
    print("   Fix: Check your internet connection. If using Supabase, ensure the project is NOT paused in the dashboard.")
    exit(1)

# Test 2: Port Reachability
print(f"\n[Test 2] Attempting to reach Port {port}...")
try:
    s = socket.create_connection((host, port), timeout=5)
    print(f"✅ Success! Port {port} is open and reachable.")
    s.close()
except Exception as e:
    print(f"❌ FAILED: Cannot connect to port {port}. {e}")
    print("   Fix: Your ISP, VPN, or College Firewall might be blocking port 5432.")
    exit(1)

# Test 3: Authentication
print("\n[Test 3] Attempting Database Authentication...")
try:
    conn = psycopg2.connect(db_url, connect_timeout=5)
    print("✅ Success! Authenticated with PostgreSQL.")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: Authentication rejected. {e}")
    print("   Fix: Check your database password in the DATABASE_URL.")
    
print("\n--- Diagnostic Complete ---")
