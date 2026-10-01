# Traefik Setup for bfunk (brownfunk)

## Overview

Traefik has been configured as a reverse proxy for **26 web services** on bfunk. This provides:

- **HTTPS everywhere**: All services accessible via secure HTTPS
- **Automatic hostname routing**: Services accessible via `.brownfunk.{lan,home,local}` and `.funkybrownfunk.duckdns.org`
- **Let's Encrypt certificates**: Wildcard certificate for `*.funkybrownfunk.duckdns.org` (external access)
- **Self-signed certificates**: For local `.lan`/`.home`/`.local` names (local access)
- **Backward compatibility**: Old direct port access still works as fallback

## Configuration Files

### .env Variables Added
```env
SERVER_DOMAIN=brownfunk
SERVER_LAN_IP=192.168.1.180
ACME_EMAIL=besnard.laurent@gmail.com
```

### Certificates
- **Self-signed**: `traefik/certs/brownfunk.{crt,key}`
  - Valid for 10 years
  - Covers: `*.brownfunk.{lan,home,local}`
- **Let's Encrypt**: Stored in `traefik/acme/acme.json`
  - Wildcard: `*.funkybrownfunk.duckdns.org`
  - DNS-01 challenge via DuckDNS

### Dynamic TLS Configuration
- **File**: `traefik/dynamic_tls.yml`
- **Purpose**: Serves self-signed certs for local names, LE wildcard for DuckDNS
- **Local services**: Use Traefik's default rule + labels (no custom routers needed)
- **Remote services**: Add routers here for apps on other machines

## Networks

### Docker Networks
```
proxy (bridge)
  ├─ traefik
  ├─ pihole
  ├─ homer
  ├─ jellyfin
  ├─ filebrowser
  ├─ [26 web services]
  └─ ...

frontend (172.20.0.0/24)
  ├─ pihole (172.20.0.31)
  └─ [all services]
```

## Complete Service List with URLs

All these services are now accessible via Traefik:

| Service | External Port | Local HTTPS | External HTTPS |
|---------|---------------|-------------|-----------------|
| traefik | 80/443 (via duckdns host only) | _not routed on .lan (by design)_ | https://traefik.funkybrownfunk.duckdns.org |
| pihole | 53/455 | https://pihole.brownfunk.lan | https://pihole.funkybrownfunk.duckdns.org |
| homer | 8080 | https://home.brownfunk.lan | https://home.funkybrownfunk.duckdns.org |
| jellyfin | 8096 | https://jellyfin.brownfunk.lan | https://jellyfin.funkybrownfunk.duckdns.org |
| filebrowser | 9295 | https://filebrowser.brownfunk.lan | https://filebrowser.funkybrownfunk.duckdns.org |
| **Media & Management** |
| piwigo | 8282 | https://piwigo.brownfunk.lan | https://piwigo.funkybrownfunk.duckdns.org |
| nextcloud | 9393 | https://nextcloud.brownfunk.lan | https://nextcloud.funkybrownfunk.duckdns.org |
| navidrome | 8082 | https://navidrome.brownfunk.lan | https://navidrome.funkybrownfunk.duckdns.org |
| komga | 9981 | https://komga.brownfunk.lan | https://komga.funkybrownfunk.duckdns.org |
| **Download & Indexing** |
| sonarr | 8989 | https://sonarr.brownfunk.lan | https://sonarr.funkybrownfunk.duckdns.org |
| radarr | 7878 | https://radarr.brownfunk.lan | https://radarr.funkybrownfunk.duckdns.org |
| radarr_fr | 7879 | https://radarr_fr.brownfunk.lan | https://radarr_fr.funkybrownfunk.duckdns.org |
| prowlarr | 9696 | https://prowlarr.brownfunk.lan | https://prowlarr.funkybrownfunk.duckdns.org |
| jackett | 9117 | https://jackett.brownfunk.lan | https://jackett.funkybrownfunk.duckdns.org |
| bazarr | 6768 | https://bazarr.brownfunk.lan | https://bazarr.funkybrownfunk.duckdns.org |
| **Books & Documents** |
| calibre | 7080 | https://calibre.brownfunk.lan | https://calibre.funkybrownfunk.duckdns.org |
| calibre-web | 8083 | https://calibre-web.brownfunk.lan | https://calibre-web.funkybrownfunk.duckdns.org |
| hedgedoc | 3000 | https://hedgedoc.brownfunk.lan | https://hedgedoc.funkybrownfunk.duckdns.org |
| **Website & Blogs** |
| wordpress | 5555 | https://wordpress.brownfunk.lan | https://wordpress.funkybrownfunk.duckdns.org |
| wordpress_diary | 5556 | https://wordpress_diary.brownfunk.lan | https://wordpress_diary.funkybrownfunk.duckdns.org |
| tecmint-web | 1021 | https://tecmint-web.brownfunk.lan | https://tecmint-web.funkybrownfunk.duckdns.org |
| **Administration & Monitoring** |
| portainer | 6767 | https://portainer.brownfunk.lan | https://portainer.funkybrownfunk.duckdns.org |
| phpmyadmin | 3002 | https://phpmyadmin.brownfunk.lan | https://phpmyadmin.funkybrownfunk.duckdns.org |
| crowdsec | 8890 | https://crowdsec.brownfunk.lan | https://crowdsec.funkybrownfunk.duckdns.org |
| scrutiny | 8033 | https://scrutiny.brownfunk.lan | https://scrutiny.funkybrownfunk.duckdns.org |
| **Personal** |
| firefox | 3008 | https://firefox.brownfunk.lan | https://firefox.funkybrownfunk.duckdns.org |
| taskchampion | 9008 | https://taskchampion.brownfunk.lan | https://taskchampion.funkybrownfunk.duckdns.org |
| unmanic | 8877 | https://unmanic.brownfunk.lan | https://unmanic.funkybrownfunk.duckdns.org |

## Traefik Labels Applied

Every service above has been configured with:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.{service}.entrypoints=websecure"
  - "traefik.http.routers.{service}.tls=true"
  - "traefik.http.services.{service}.loadbalancer.server.port={internal_port}"
```

## Access Methods

### Local Network (brownfunk.lan)

**Option 1: Via Traefik HTTPS (recommended)**
```
https://jellyfin.brownfunk.lan
https://nextcloud.brownfunk.lan
https://radarr.brownfunk.lan
```
- **Pro**: HTTPS, works with Traefik rules/auth
- **Con**: Self-signed cert (browser warning)
- **Requires**: PiHole DNS configured on your device, or `/etc/hosts` entry

**Option 2: Direct Port (fallback)**
```
http://brownfunk.lan:8096       (jellyfin)
http://brownfunk.lan:9393       (nextcloud)
http://brownfunk.lan:7878       (radarr)
```
- **Pro**: No DNS needed, no cert warning
- **Con**: HTTP (not HTTPS), direct port access only

### External - Internet

**Via DuckDNS** (requires public IP forwarding)
```
https://jellyfin.funkybrownfunk.duckdns.org
https://nextcloud.funkybrownfunk.duckdns.org
https://radarr.funkybrownfunk.duckdns.org
```
- **Certificate**: Let's Encrypt wildcard (valid, no warning)
- **Requires**: DuckDNS updated to your public IP
- **Ports**: 80→443 redirect + 443 exposed on WAN

### Tailscale Network

**Option 1: Via .lan hostname + Tailscale DNS**
```
https://jellyfin.brownfunk.lan     (via Tailscale DNS resolution)
https://nextcloud.brownfunk.lan
```
- **Access**: Any Tailscale peer can reach .lan names
- **Requires**: Tailscale DNS magic working (nameserver pointing to PiHole)
- **Note**: The Traefik dashboard is intentionally NOT routed on `.lan`/`.home`/`.local`
  (matches the beefunk reference design) - only via the DuckDNS hostname below.

**Option 2: Via Tailscale IP direct**
```
https://100.92.18.39:443           (Traefik on Tailscale IP)
```
- **Access**: Direct IP works, certificates don't validate
- **Use case**: System checks, automation

## Next Steps

### 1. Start Traefik (with other services)
```bash
cd /home/lbesnard/github_repo/dotfiles/bfunk/docker-compose
docker compose up -d traefik pihole homer jellyfin filebrowser
```

### 2. Wait for Certificate Generation
Let's Encrypt DNS-01 challenge takes ~2-3 minutes:
```bash
# Monitor Traefik logs
docker compose logs -f traefik

# Check certificate status
ls -lh traefik/acme/acme.json
```

### 3. Test Local Access
```bash
# Assuming PiHole DNS is configured
curl -k https://jellyfin.brownfunk.lan
curl -k https://homer.brownfunk.lan   # (rule uses "home.brownfunk.lan" - see labels)
```

Note: the Traefik dashboard itself is only routed on
`https://traefik.funkybrownfunk.duckdns.org` (by design, matching beefunk) -
`https://traefik.brownfunk.lan` will return 404 from Traefik.

### 4. Add Hosts Entry (if PiHole DNS not available)
Edit `/etc/hosts` on your client machine:
```
192.168.1.180 brownfunk.lan
192.168.1.180 jellyfin.brownfunk.lan
192.168.1.180 nextcloud.brownfunk.lan
192.168.1.180 home.brownfunk.lan
# ... add all services you want to access
```

### 5. Test External Access (DuckDNS)
Once DuckDNS is updated to your public IP:
```bash
curl https://jellyfin.funkybrownfunk.duckdns.org
curl https://traefik.funkybrownfunk.duckdns.org
```

### 6. Configure Traefik Authentication (Optional Security)
Add Basic Auth or OAuth2 middleware to sensitive services:
```yaml
labels:
  - "traefik.http.routers.portainer.middlewares=basic-auth"
  - "traefik.http.middlewares.basic-auth.basicauth.users=admin:$$2y$$10$$..."
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Self-signed cert warning | Browser security | Expected for .lan names, add to exceptions or use `-k` flag |
| Service not routing to Traefik | Service not on `proxy` network | Add `networks: - proxy` to service config |
| Can't reach `*.brownfunk.lan` | DNS not resolving | Configure PiHole DNS (53) or add `/etc/hosts` entry |
| Let's Encrypt certificate fails | DuckDNS not accessible | Check DUCKDNS_TOKEN, ensure outbound DNS works |
| Traefik dashboard inaccessible | Dashboard router not configured | Use port 455 → 80 on pihole instead, or configure dashboard auth |
| Service shows `502 Bad Gateway` | Service not listening on configured port | Check service port in labels matches actual internal port |

## Important Notes

⚠️ **Self-Signed Certificates**
- Browser will warn about untrusted certificates for `.lan` names
- This is expected and secure (self-signed = no external validation)
- Add exception in browser or use tools that accept self-signed (curl -k, wget --no-check-certificate)

⚠️ **HTTP Redirect**
- All HTTP requests on port 80 are permanently redirected to HTTPS on port 443
- Disable this in Traefik config if needed for specific use cases

⚠️ **Certificate Renewal**
- Let's Encrypt wildcards are valid 90 days
- Traefik auto-renews before expiration (check logs every 2-3 months)

⚠️ **DNS Resolution**
- For local .lan access, configure your device to use PiHole DNS (192.168.1.180:53)
- Without DNS, fall back to direct port access (http://brownfunk.lan:8096)

## Architecture

```
Internet (Public IP)
    │
    ├─ DuckDNS Container ──→ Updates *.funkybrownfunk.duckdns.org → Public IP
    │
    ├─ Ports 80/443 (Host)
    │
    └─ Traefik Container
       ├─ Cert: Let's Encrypt wildcard *.funkybrownfunk.duckdns.org
       ├─ Cert: Self-signed *.brownfunk.{lan,home,local}
       │
       ├─ Router http → websecure redirect
       │
       ├─ Service: homer (8080)
       ├─ Service: jellyfin (8096)
       ├─ Service: nextcloud (443)
       ├─ Service: piwigo (80)
       ├─ Service: radarr (7878)
       ├─ Service: sonarr (8989)
       ├─ Service: [26 total services]
       │
       └─ Networks: proxy + frontend
           │
           └─ All services accessible on both networks
```

## Files Modified

- `.env` - Added SERVER_DOMAIN, SERVER_LAN_IP, ACME_EMAIL
- `docker-compose.yml` - Added traefik service, updated 26 services with Traefik labels and networks
- `traefik/dynamic_tls.yml` - New file for TLS certificate configuration
- `traefik/certs/brownfunk.{crt,key}` - New self-signed certificates

## Services NOT Using Traefik

These services intentionally excluded (backend/system services):
- `mariadb` - Database (internal only, port 3306)
- `redis` - Cache (internal only, port 6379)
- `gluetun` - VPN tunnel (system service)
- `flaresolverr` - Cloudflare solver (internal)
- `wireguard` / `wireguard2` - VPN (external port, not HTTP)
- `samba` - File sharing (SMB protocol)
- `rsync-server` - Rsync (SSH protocol)
- `duckdns` - System service
- `swag` - Legacy (commented out, superseded by Traefik)
