@echo off
chcp 65001 >nul
echo ========================================
echo   Network Globe Scanner - Run Script
echo ========================================
echo.

set SYNC_POSTGRES=%1
if "%SYNC_POSTGRES%"=="--sync-postgres" (
    echo [*] PostgreSQL sync mode enabled
)

if not exist venv\Scripts\activate (
    echo [*] Creating virtual environment...
    python -m venv venv
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -r requirements.txt --quiet

if "%SYNC_POSTGRES%"=="--sync-postgres" (
    echo [*] PostgreSQL mode enabled
    set USE_POSTGRES=True
    set POSTGRES_DB=nslookupDB
    set POSTGRES_USER=postgres
    set POSTGRES_PASSWORD=Password09!
    set POSTGRES_HOST=localhost
    set POSTGRES_PORT=5008

    echo [!] Make sure PostgreSQL is running on port 5008
    echo [!] Or start it with: docker run -d -p 5008:5432 -e POSTGRES_DB=nslookupDB -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=Password09! postgres:15-alpine
)

echo [*] Running migrations...
python manage.py migrate --noinput

if "%SYNC_POSTGRES%"=="--sync-postgres" (
    echo [*] Syncing data from SQLite to PostgreSQL...
    python manage.py sync_databases --from=sqlite --to=postgres
)

echo [*] Checking database seeder...
python manage.py shell -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_globe.settings'); import django; django.setup(); from accounts.models import CustomUser; from datacenter.models import Datacenter; from servers.models import Server; 
if CustomUser.objects.count() == 0:
    print('[+] Seeding initial data...');
    user = CustomUser.objects.create_superuser(email='admin@example.com', password='admin123', role='super_admin', first_name='Admin', last_name='User');
    print('    Created superuser: ' + user.email);
else:
    print('[*] Database already has data, skipping seeder.');
if Datacenter.objects.count() == 0:
    print('[+] Seeding datacenters...');
    dc1 = Datacenter.objects.create(name='AWS Tokyo', provider='AWS', country='Japan', city='Tokyo', latitude=35.6762, longitude=139.6503, tier='TIER_1');
    dc2 = Datacenter.objects.create(name='Azure Singapore', provider='Azure', country='Singapore', city='Singapore', latitude=1.3521, longitude=103.8198, tier='TIER_1');
    dc3 = Datacenter.objects.create(name='Google Frankfurt', provider='Google Cloud', country='Germany', city='Frankfurt', latitude=50.1109, longitude=8.6821, tier='TIER_1');
    dc4 = Datacenter.objects.create(name='AWS Jakarta', provider='AWS', country='Indonesia', city='Jakarta', latitude=-6.2088, longitude=106.8456, tier='TIER_2');
    dc5 = Datacenter.objects.create(name='Azure Bali', provider='Azure', country='Indonesia', city='Bali', latitude=-8.4095, longitude=115.2922, tier='TIER_3');
    dc6 = Datacenter.objects.create(name='Cloudflare Batam', provider='Cloudflare', country='Indonesia', city='Batam', latitude=1.0456, longitude=104.0305, tier='TIER_3');
    print('    Created ' + str(Datacenter.objects.count()) + ' datacenters');
    print('[+] Seeding servers...');
    Server.objects.create(hostname='web-01', ip_address='10.0.0.1', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE');
    Server.objects.create(hostname='web-02', ip_address='10.0.0.2', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE');
    Server.objects.create(hostname='db-01', ip_address='10.0.1.1', datacenter=dc2, os='CentOS 8', status='ONLINE');
    Server.objects.create(hostname='db-02', ip_address='10.0.1.2', datacenter=dc2, os='CentOS 8', status='MAINTENANCE');
    Server.objects.create(hostname='cache-01', ip_address='10.0.2.1', datacenter=dc3, os='Debian 12', status='ONLINE');
    Server.objects.create(hostname='app-jkt-01', ip_address='10.0.3.1', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE');
    Server.objects.create(hostname='app-jkt-02', ip_address='10.0.3.2', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE');
    Server.objects.create(hostname='db-bali-01', ip_address='10.0.4.1', datacenter=dc5, os='CentOS 8', status='ONLINE');
    Server.objects.create(hostname='edge-batam-01', ip_address='10.0.5.1', datacenter=dc6, os='Debian 12', status='ONLINE');
    print('    Created ' + str(Server.objects.count()) + ' servers');
else:
    print('[*] Checking for missing datacenters...');
    existing_names = [d[0] for d in Datacenter.objects.values_list('name')];
    new_dcs = [];
    if 'AWS Tokyo' not in existing_names:
        new_dcs.append(Datacenter(name='AWS Tokyo', provider='AWS', country='Japan', city='Tokyo', latitude=35.6762, longitude=139.6503, tier='TIER_1'));
    if 'Azure Singapore' not in existing_names:
        new_dcs.append(Datacenter(name='Azure Singapore', provider='Azure', country='Singapore', city='Singapore', latitude=1.3521, longitude=103.8198, tier='TIER_1'));
    if 'Google Frankfurt' not in existing_names:
        new_dcs.append(Datacenter(name='Google Frankfurt', provider='Google Cloud', country='Germany', city='Frankfurt', latitude=50.1109, longitude=8.6821, tier='TIER_1'));
    if 'AWS Jakarta' not in existing_names:
        new_dcs.append(Datacenter(name='AWS Jakarta', provider='AWS', country='Indonesia', city='Jakarta', latitude=-6.2088, longitude=106.8456, tier='TIER_2'));
    if 'Azure Bali' not in existing_names:
        new_dcs.append(Datacenter(name='Azure Bali', provider='Azure', country='Indonesia', city='Bali', latitude=-8.4095, longitude=115.2922, tier='TIER_3'));
    if 'Cloudflare Batam' not in existing_names:
        new_dcs.append(Datacenter(name='Cloudflare Batam', provider='Cloudflare', country='Indonesia', city='Batam', latitude=1.0456, longitude=104.0305, tier='TIER_3'));
    if new_dcs:
        Datacenter.objects.bulk_create(new_dcs);
        print('    Added ' + str(len(new_dcs)) + ' missing datacenters');
    else:
        print('[*] All default datacenters exist.');
    if Server.objects.count() == 0:
        print('[+] Seeding servers for existing datacenters...');
        dc1 = Datacenter.objects.get(name='AWS Tokyo');
        dc2 = Datacenter.objects.get(name='Azure Singapore');
        dc3 = Datacenter.objects.get(name='Google Frankfurt');
        dc4 = Datacenter.objects.get(name='AWS Jakarta');
        dc5 = Datacenter.objects.get(name='Azure Bali');
        dc6 = Datacenter.objects.get(name='Cloudflare Batam');
        Server.objects.create(hostname='web-01', ip_address='10.0.0.1', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE');
        Server.objects.create(hostname='web-02', ip_address='10.0.0.2', datacenter=dc1, os='Ubuntu 22.04', status='ONLINE');
        Server.objects.create(hostname='db-01', ip_address='10.0.1.1', datacenter=dc2, os='CentOS 8', status='ONLINE');
        Server.objects.create(hostname='db-02', ip_address='10.0.1.2', datacenter=dc2, os='CentOS 8', status='MAINTENANCE');
        Server.objects.create(hostname='cache-01', ip_address='10.0.2.1', datacenter=dc3, os='Debian 12', status='ONLINE');
        Server.objects.create(hostname='app-jkt-01', ip_address='10.0.3.1', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE');
        Server.objects.create(hostname='app-jkt-02', ip_address='10.0.3.2', datacenter=dc4, os='Ubuntu 22.04', status='ONLINE');
        Server.objects.create(hostname='db-bali-01', ip_address='10.0.4.1', datacenter=dc5, os='CentOS 8', status='ONLINE');
        Server.objects.create(hostname='edge-batam-01', ip_address='10.0.5.1', datacenter=dc6, os='Debian 12', status='ONLINE');
        print('    Created ' + str(Server.objects.count()) + ' servers');
    else:
        print('[*] Servers already exist, skipping server seeder.');
print('[+] Seeder completed.');
"

echo.
echo ========================================
echo   Starting Network Globe Scanner
echo ========================================
echo.
echo   Dashboard : http://localhost:8000/api/dashboard/
echo   API Docs  : http://localhost:8000/swagger/
echo   Admin     : http://localhost:8000/admin/
echo.
echo   Default login: admin@example.com / admin123
echo.
if "%SYNC_POSTGRES%"=="--sync-postgres" (
    echo   Database: PostgreSQL (port 5008)
) else (
    echo   Database: SQLite (nslookupDB.sqlite3)
)
echo.
echo   Celery Beat: WAN scraper every 5 minutes
echo.
echo   Press Ctrl+C to stop
echo ========================================
echo.

start "Celery Worker" cmd /c "celery -A network_globe worker --loglevel=info"
start "Celery Beat" cmd /c "celery -A network_globe beat --loglevel=info"

python manage.py runserver 0.0.0.0:8000

pause
