# Network Globe Scanner

A Django-based network monitoring and management platform with NVIDIA Neon themed dashboard.

## Features

- **Dashboard**: Unified monitoring dashboard with real-time stats, charts, and network topology animation
- **Traceroute**: Scan domains/IPs with hop-by-hop results (like Windows tracert)
- **DNS Lookup**: Query DNS records (A, AAAA, MX, TXT, CNAME, NS, PTR, SPF)
- **Animations**: Real-time traceroute path animation (Canvas) and DNS resolution animation (SVG+CSS)
- **Datacenter Management**: Add and manage global datacenters
- **Server Management**: Add and manage servers with status tracking
- **Admin Panel**: Professional Django admin with custom neon theme
- **API Documentation**: Swagger/OpenAPI docs
- **Real-time Updates**: Live stats refresh every 5 seconds
- **Network Topology**: Animated canvas showing datacenter connections

## Tech Stack

- **Backend**: Django 6.0.7, Django REST Framework
- **Task Queue**: Celery + Redis
- **Databases**: PostgreSQL (production), SQLite (development)
- **Frontend**: Django Templates, Tailwind CSS, Chart.js
- **API Docs**: drf-yasg (Swagger/ReDoc)

## Database Configuration

### SQLite (Development Default)
```
File: nslookupDB.sqlite3
Location: C:\www\nslookup\nslookupDB.sqlite3
```

### PostgreSQL (Production)
```
Name: nslookupDB
Port: 5008
User: postgres
Password: Password09!
Host: localhost
```

### Database Sync: SQLite → PostgreSQL

To sync all data from SQLite to PostgreSQL:

**Windows:**
```cmd
run.bat --sync-postgres
```

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh --sync-postgres
```

Or manually:
```bash
# Start PostgreSQL (if not running)
docker run -d -p 5008:5432 -e POSTGRES_DB=nslookupDB -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=Password09! postgres:15-alpine

# Run migrations on PostgreSQL
USE_POSTGRES=True python manage.py migrate

# Sync data from SQLite to PostgreSQL
python manage.py sync_databases --from=sqlite --to=postgres
```

**Sync specific models:**
```bash
python manage.py sync_databases --from=sqlite --to=postgres --models accounts.CustomUser datacenter.Datacenter servers.Server
```

### Redis
```
Host: localhost
Port: 6379
Memory: 2GB
```

## Quick Start

### Windows (SQLite - default)
```cmd
run.bat
```

### Windows (with PostgreSQL sync)
```cmd
run.bat --sync-postgres
```

### Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

The run scripts will:
1. Create virtual environment if missing
2. Install dependencies
3. Run migrations
4. Seed initial data (superuser, datacenters, servers)
5. Start dev server at `http://localhost:8000`

**Note:** Use `--sync-postgres` flag to sync SQLite data to PostgreSQL and run on PostgreSQL instead of SQLite.

## Default Login

```
Email: admin@example.com
Password: admin123
Role: Super Admin
```

## URLs

| URL | Description |
|-----|-------------|
| `/` | Unified Dashboard (redirects) |
| `/animations/` | Traceroute & DNS Resolution Animations |
| `/api/dashboard/unified/` | Main monitoring dashboard |
| `/admin/` | Django admin panel |
| `/swagger/` | API documentation |
| `/redoc/` | API documentation (ReDoc) |

## API Endpoints

### Authentication
```
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/register/
```

### Traceroute
```
POST /api/traceroute/traceroutes/
GET  /api/traceroute/traceroutes/
GET  /api/traceroute/traceroutes/{id}/
```

### DNS Lookup
```
POST /api/dns/dns/
GET  /api/dns/dns/
```

### Datacenters
```
GET  /api/datacenters/datacenters/
POST /api/datacenters/datacenters/
GET  /api/datacenters/datacenters/{id}/
```

### Servers
```
GET  /api/servers/servers/
POST /api/servers/servers/
GET  /api/servers/servers/{id}/
```

### Dashboard Stats
```
GET /api/dashboard/unified/api/stats/
GET /api/dashboard/api/stats/
```

## Project Structure

```
C:\www\nslookup\
├── network_globe/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── celery.py
│   └── routing.py
├── accounts/               # Custom user model & auth
├── core/                   # Base models, utilities
├── datacenter/             # Datacenter models & API
├── servers/                # Server models & API
├── traceroute/             # Traceroute models & Celery tasks
├── dnslookup/              # DNS query models & Celery tasks
├── dashboard/              # Dashboard views & templates
├── api/                    # Health check endpoint
├── sync/                   # Database sync utility
│   └── management/
│       └── commands/
│           └── sync_databases.py
├── templates/
│   ├── dashboard/
│   │   ├── unified.html    # Main dashboard
│   │   └── index.html      # Stats dashboard
│   └── admin/
│       ├── base_site.html  # Neon admin theme
│       ├── index.html      # Custom admin dashboard
│       └── dashboard.html  # Admin dashboard with topology
├── static/
│   ├── css/
│   │   └── animations.css        # DNS resolution animation styles
│   └── js/
│       ├── traceroute-animation.js       # Canvas traceroute path animation
│       └── dns-resolution-animation.js   # SVG+CSS DNS resolution animation
├── templates/
│   ├── dashboard/
│   │   ├── animations.html     # Traceroute & DNS animation page
│   │   ├── unified.html        # Main dashboard
│   │   └── index.html          # Stats dashboard
│   └── admin/
│       ├── base_site.html  # Neon admin theme
│       ├── index.html      # Custom admin dashboard
│       └── dashboard.html  # Admin dashboard with topology
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── run.sh                  # Linux/macOS run script
├── run.bat                 # Windows run script
└── manage.py
```

## Seeded Data

The run scripts automatically seed:

### Datacenters
1. AWS Tokyo (Japan) - TIER_1
2. Azure Singapore (Singapore) - TIER_1
3. Google Frankfurt (Germany) - TIER_1
4. AWS Jakarta (Indonesia) - TIER_2
5. Azure Bali (Indonesia) - TIER_3
6. Cloudflare Batam (Indonesia) - TIER_3

### Servers
- web-01, web-02 (Tokyo)
- db-01, db-02 (Singapore)
- cache-01 (Frankfurt)
- app-jkt-01, app-jkt-02 (Jakarta)
- db-bali-01 (Bali)
- edge-batam-01 (Batam)

## Admin Panel Features

- Custom NVIDIA neon theme
- Dashboard overview with stats cards
- **Animations page**: Real-time traceroute path (Canvas) and DNS resolution (SVG+CSS) visualizations
- **Direct CRUD tables**: Datacenters, Servers, Traceroutes, DNS Queries
- **Inline add forms**: Add datacenters and servers directly from dashboard
- **Animated network topology**: Interactive canvas showing worldwide datacenter connections
  - Scroll to zoom
  - Drag to pan
  - Animated packet scanning between nodes
- Quick Scan form for traceroute and DNS lookup
- Edit/Delete actions on every table row
- Status badges with colors
- Server count per datacenter
- Advanced search and filtering

## Docker Deployment

```bash
docker compose up -d
```

Services:
- PostgreSQL (port 5008)
- Redis (port 6379)
- Django web (port 8000)
- Celery worker
- Celery beat

## Environment Variables

Create `.env` file or set environment variables:

```
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite default)
USE_POSTGRES=False

# Database (PostgreSQL)
# USE_POSTGRES=True
# POSTGRES_DB=nslookupDB
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=Password09!
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5008

# Redis
REDIS_URL=redis://localhost:6379/0
```

## Database Sync Command

Sync data between SQLite and PostgreSQL:

```bash
# Sync all models from SQLite to PostgreSQL
python manage.py sync_databases --from=sqlite --to=postgres

# Sync specific models
python manage.py sync_databases --from=sqlite --to=postgres --models accounts.CustomUser datacenter.Datacenter servers.Server

# Sync from PostgreSQL to SQLite
python manage.py sync_databases --from=postgres --to=sqlite
```

## User Roles

1. **Super Admin** - Full access
2. **Network Admin** - Network operations
3. **Security Analyst** - Security monitoring
4. **Viewer** - Read-only access

## Celery Tasks

- `traceroute.run_traceroute` - Run traceroute scan
- `traceroute.run_dns_query` - Run DNS lookup
- `dnslookup.run_dns_query` - DNS query task

## License

MIT
