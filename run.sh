#!/bin/bash
set -e

echo "========================================"
echo "  Network Globe Scanner - Run Script"
echo "========================================"

# Check for --sync-postgres flag
SYNC_POSTGRES=false
if [ "$1" = "--sync-postgres" ]; then
    SYNC_POSTGRES=true
    echo "[*] PostgreSQL sync mode enabled"
fi

if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python -m venv venv
fi

echo "[*] Activating virtual environment..."
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERROR: Cannot find venv activation script"
    exit 1
fi

echo "[*] Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if PostgreSQL is requested and available
if [ "$SYNC_POSTGRES" = "true" ]; then
    echo "[*] PostgreSQL mode enabled"
    export USE_POSTGRES=True
    export POSTGRES_DB=nslookupDB
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=Password09!
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5008

    # Check if PostgreSQL is running
    if command -v pg_isready &> /dev/null; then
        if ! pg_isready -h localhost -p 5008; then
            echo "[!] PostgreSQL is not running on port 5008"
            echo "[!] Starting PostgreSQL with Docker..."
            docker run -d --name nslookup-postgres \
                -e POSTGRES_DB=nslookupDB \
                -e POSTGRES_USER=postgres \
                -e POSTGRES_PASSWORD=Password09! \
                -p 5008:5432 \
                postgres:15-alpine || true
            echo "[*] Waiting for PostgreSQL to start..."
            sleep 5
        fi
    else
        echo "[!] PostgreSQL client not found, using Docker..."
        docker run -d --name nslookup-postgres \
            -e POSTGRES_DB=nslookupDB \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=Password09! \
            -p 5008:5432 \
            postgres:15-alpine || true
        echo "[*] Waiting for PostgreSQL to start..."
        sleep 5
    fi
fi

echo "[*] Running migrations..."
python manage.py migrate --noinput

# Sync data if PostgreSQL mode
if [ "$SYNC_POSTGRES" = "true" ]; then
    echo "[*] Syncing data from SQLite to PostgreSQL..."
    python manage.py sync_databases --from=sqlite --to=postgres
fi

echo "[*] Checking database seeder..."
python manage.py shell -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_globe.settings')
import django
django.setup()

from accounts.models import CustomUser
from datacenter.models import Datacenter
from servers.models import Server

if CustomUser.objects.count() == 0:
    print('[+] Seeding initial data...')
    user = CustomUser.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        role='super_admin',
        first_name='Admin',
        last_name='User'
    )
    print(f'    Created superuser: {user.email}')
else:
    print('[*] Database already has data, skipping seeder.')

if Datacenter.objects.count() == 0:
    print('[+] Seeding datacenters...')
    dc1 = Datacenter.objects.create(
        name='AWS Tokyo',
        provider='AWS',
        country='Japan',
        city='Tokyo',
        latitude=35.6762,
        longitude=139.6503,
        tier='TIER_1'
    )
    dc2 = Datacenter.objects.create(
        name='Azure Singapore',
        provider='Azure',
        country='Singapore',
        city='Singapore',
        latitude=1.3521,
        longitude=103.8198,
        tier='TIER_1'
    )
    dc3 = Datacenter.objects.create(
        name='Google Frankfurt',
        provider='Google Cloud',
        country='Germany',
        city='Frankfurt',
        latitude=50.1109,
        longitude=8.6821,
        tier='TIER_1'
    )
    dc4 = Datacenter.objects.create(
        name='AWS Jakarta',
        provider='AWS',
        country='Indonesia',
        city='Jakarta',
        latitude=-6.2088,
        longitude=106.8456,
        tier='TIER_2'
    )
    dc5 = Datacenter.objects.create(
        name='Azure Bali',
        provider='Azure',
        country='Indonesia',
        city='Bali',
        latitude=-8.4095,
        longitude=115.2922,
        tier='TIER_3'
    )
    dc6 = Datacenter.objects.create(
        name='Cloudflare Batam',
        provider='Cloudflare',
        country='Indonesia',
        city='Batam',
        latitude=1.0456,
        longitude=104.0305,
        tier='TIER_3'
    )
    print(f'    Created {Datacenter.objects.count()} datacenters')

    print('[+] Seeding servers...')
    Server.objects.create(hostname='web-01', ip_address='10.0.0.1', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE')
    Server.objects.create(hostname='web-02', ip_address='10.0.0.2', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE')
    Server.objects.create(hostname='db-01', ip_address='10.0.1.1', datacenter=dc2, os='CentOS 8', status='ONLINE')
    Server.objects.create(hostname='db-02', ip_address='10.0.1.2', datacenter=dc2, os='CentOS 8', status='MAINTENANCE')
    Server.objects.create(hostname='cache-01', ip_address='10.0.2.1', datacenter=dc3, os='Debian 12', status='ONLINE')
    Server.objects.create(hostname='app-jkt-01', ip_address='10.0.3.1', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE')
    Server.objects.create(hostname='app-jkt-02', ip_address='10.0.3.2', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE')
    Server.objects.create(hostname='db-bali-01', ip_address='10.0.4.1', datacenter=dc5, os='CentOS 8', status='ONLINE')
    Server.objects.create(hostname='edge-batam-01', ip_address='10.0.5.1', datacenter=dc6, os='Debian 12', status='ONLINE')
    print(f'    Created {Server.objects.count()} servers')
else:
    print('[*] Checking for missing datacenters...')
    existing_names = set(Datacenter.objects.values_list('name', flat=True))
    new_dcs = []
    if 'AWS Tokyo' not in existing_names:
        new_dcs.append(Datacenter(name='AWS Tokyo', provider='AWS', country='Japan', city='Tokyo', latitude=35.6762, longitude=139.6503, tier='TIER_1'))
    if 'Azure Singapore' not in existing_names:
        new_dcs.append(Datacenter(name='Azure Singapore', provider='Azure', country='Singapore', city='Singapore', latitude=1.3521, longitude=103.8198, tier='TIER_1'))
    if 'Google Frankfurt' not in existing_names:
        new_dcs.append(Datacenter(name='Google Frankfurt', provider='Google Cloud', country='Germany', city='Frankfurt', latitude=50.1109, longitude=8.6821, tier='TIER_1'))
    if 'AWS Jakarta' not in existing_names:
        new_dcs.append(Datacenter(name='AWS Jakarta', provider='AWS', country='Indonesia', city='Jakarta', latitude=-6.2088, longitude=106.8456, tier='TIER_2'))
    if 'Azure Bali' not in existing_names:
        new_dcs.append(Datacenter(name='Azure Bali', provider='Azure', country='Indonesia', city='Bali', latitude=-8.4095, longitude=115.2922, tier='TIER_3'))
    if 'Cloudflare Batam' not in existing_names:
        new_dcs.append(Datacenter(name='Cloudflare Batam', provider='Cloudflare', country='Indonesia', city='Batam', latitude=1.0456, longitude=104.0305, tier='TIER_3'))
    if new_dcs:
        Datacenter.objects.bulk_create(new_dcs)
        print(f'    Added {len(new_dcs)} missing datacenters')
    else:
        print('[*] All default datacenters exist.')

    if Server.objects.count() == 0:
        print('[+] Seeding servers for existing datacenters...')
        dc1 = Datacenter.objects.get(name='AWS Tokyo')
        dc2 = Datacenter.objects.get(name='Azure Singapore')
        dc3 = Datacenter.objects.get(name='Google Frankfurt')
        dc4 = Datacenter.objects.get(name='AWS Jakarta')
        dc5 = Datacenter.objects.get(name='Azure Bali')
        dc6 = Datacenter.objects.get(name='Cloudflare Batam')
        Server.objects.create(hostname='web-01', ip_address='10.0.0.1', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE')
        Server.objects.create(hostname='web-02', ip_address='10.0.0.2', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE')
        Server.objects.create(hostname='db-01', ip_address='10.0.1.1', datacenter=dc2, os='CentOS 8', status='ONLINE')
        Server.objects.create(hostname='db-02', ip_address='10.0.1.2', datacenter=dc2, os='CentOS 8', status='MAINTENANCE')
        Server.objects.create(hostname='cache-01', ip_address='10.0.2.1', datacenter=dc3, os='Debian 12', status='ONLINE')
        Server.objects.create(hostname='app-jkt-01', ip_address='10.0.3.1', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE')
        Server.objects.create(hostname='app-jkt-02', ip_address='10.0.3.2', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE')
        Server.objects.create(hostname='db-bali-01', ip_address='10.0.4.1', datacenter=dc5, os='CentOS 8', status='ONLINE')
        Server.objects.create(hostname='edge-batam-01', ip_address='10.0.5.1', datacenter=dc6, os='Debian 12', status='ONLINE')
        print(f'    Created {Server.objects.count()} servers')
    else:
        print('[*] Servers already exist, skipping server seeder.')

print('[+] Seeder completed.')
"

echo ""
echo "========================================"
echo "  Starting Network Globe Scanner"
echo "========================================"
echo ""
echo "  Dashboard : http://localhost:8000/api/dashboard/"
echo "  API Docs  : http://localhost:8000/swagger/"
echo "  Admin     : http://localhost:8000/admin/"
echo ""
echo "  Default login: admin@example.com / admin123"
echo ""
if [ "$SYNC_POSTGRES" = "true" ]; then
    echo "  Database: PostgreSQL (port 5008)"
else
    echo "  Database: SQLite (nslookupDB.sqlite3)"
fi
echo ""
echo "  Celery Beat: WAN scraper every 5 minutes"
echo ""
echo "  Press Ctrl+C to stop"
echo "========================================"
echo ""

celery -A network_globe worker --loglevel=info &
celery -A network_globe beat --loglevel=info &

python manage.py runserver 0.0.0.0:8000
