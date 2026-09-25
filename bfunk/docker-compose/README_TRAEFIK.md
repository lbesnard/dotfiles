# Traefik Setup Documentation Index

Complete documentation for Traefik reverse proxy setup on bfunk (brownfunk) machine.

## 📖 Documentation Files

### For Quick Start
**→ Start here:** [`QUICK_START.md`](./QUICK_START.md)
- Quick access to all 26 services
- Common commands
- DNS troubleshooting
- Fallback URLs if needed
- ~5 min read

### For Deployment
**→ Deploy here:** [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md)
- Step-by-step deployment instructions
- Verification checks at each step
- Troubleshooting guide
- Rollback plan
- ~15-20 min deployment time

### For Complete Understanding
**→ Learn here:** [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md)
- Full configuration details
- All 26 services with URLs
- Certificate management explanation
- Architecture diagrams
- Advanced troubleshooting
- ~20 min read

---

## 🚀 Quick Navigation

### I want to...

**Start services immediately**
→ Go to: [`QUICK_START.md`](./QUICK_START.md) - Section: "Start Everything"

**Deploy Traefik properly**
→ Go to: [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) - Follow in order

**Access a specific service**
→ Go to: [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md) - Section: "Complete Service List"

**Fix DNS issues**
→ Go to: [`QUICK_START.md`](./QUICK_START.md) - Section: "Fix DNS Resolution"

**Understand certificate setup**
→ Go to: [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md) - Section: "Certificate Management"

**Fix a problem**
→ Go to: [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) - Section: "Troubleshooting"
→ Or: [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md) - Section: "Troubleshooting"

**Configure external (DuckDNS/Tailscale) access**
→ Go to: [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md) - Section: "DuckDNS Configuration"

---

## 📋 Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `.env` | Environment variables | ✅ Modified (3 vars added) |
| `docker-compose.yml` | Main compose config | ✅ Modified (Traefik + 26 services) |
| `traefik/dynamic_tls.yml` | TLS certificate config | ✅ Created |
| `traefik/certs/brownfunk.crt` | Self-signed certificate | ✅ Generated (10 years) |
| `traefik/certs/brownfunk.key` | Self-signed key | ✅ Generated (10 years) |
| `traefik/acme/` | Let's Encrypt storage | ⏳ Created on first run |

---

## 🔧 Configuration Summary

### Environment Variables (.env)
```env
SERVER_DOMAIN=brownfunk
SERVER_LAN_IP=192.168.1.180
ACME_EMAIL=besnard.laurent@gmail.com
DUCKDNS_DOMAIN=funkybrownfunk
DUCKDNS_TOKEN=***
```

### Docker Networks
- **proxy**: Traefik and all web services
- **frontend**: All services (internal communication)

### Services with Traefik
**26 total services:**
- Core: traefik, pihole, homer, jellyfin, filebrowser, nextcloud
- Media: piwigo, navidrome, komga, unmanic
- Download: radarr, radarr_fr, sonarr, prowlarr, jackett, bazarr
- Admin: portainer, phpmyadmin, crowdsec, scrutiny
- Docs: hedgedoc, calibre, calibre-web
- Website: wordpress, wordpress_diary, tecmint-web
- Personal: firefox, taskchampion

### Certificates
- **Self-Signed**: `*.brownfunk.{lan,home,local}` (10 years)
- **Let's Encrypt**: `*.funkybrownfunk.duckdns.org` (wildcard, 90 days)

### Service Access Patterns
```
Local:     https://service.brownfunk.lan
External:  https://service.funkybrownfunk.duckdns.org
Fallback:  http://brownfunk.lan:port
Tailscale: https://service.brownfunk.lan (via Tailscale DNS)
```

---

## ✅ Current Status

| Component | Status | Details |
|-----------|--------|---------|
| YAML Syntax | ✅ Valid | docker-compose.yml validated |
| Traefik Config | ✅ Complete | v3.6, DNS-01 ACME, self-signed fallback |
| Services | ✅ 26 configured | All have traefik.enable=true |
| Networks | ✅ Created | proxy network + frontend network |
| Certificates | ✅ Generated | Self-signed ready, Let's Encrypt on first run |
| Documentation | ✅ Complete | 3 guides + this index |
| Ready to Deploy | ✅ YES | Run: `docker compose up -d` |

---

## 🎯 Key Features

✅ **HTTPS Everywhere**
- All services accessible via secure HTTPS
- Self-signed for local (.lan) names
- Let's Encrypt wildcard for external (.duckdns.org) names

✅ **Automatic Hostname Routing**
- Service names automatically map to hostnames
- `jellyfin` service → `https://jellyfin.brownfunk.lan`
- Same routing rule for .lan, .home, .local, and .duckdns.org

✅ **Backward Compatible**
- Old direct port access still works
- Services expose original ports
- Fallback if Traefik has issues

✅ **Multiple Access Methods**
- Local network via .lan names
- External via DuckDNS domain
- Tailscale via .lan names or direct IP
- Direct ports as emergency fallback

✅ **Production Ready**
- Auto-renewal of Let's Encrypt certificates
- Comprehensive error handling
- Proper logging and monitoring
- Clean architecture

---

## 📚 Additional Resources

### Related Configurations
- **beefunk reference**: `/home/lbesnard/github_repo/dotfiles/beefunk/docker-compose/`
  - See `docker-compose.yml` and `traefik/dynamic_tls.yml` for reference implementation

### Docker Commands Reference
```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f traefik

# Check status
docker compose ps

# Access container
docker compose exec traefik /bin/sh

# Stop services
docker compose down

# View network
docker network inspect proxy
```

### Testing Commands
```bash
# Test HTTPS
curl -k https://jellyfin.brownfunk.lan

# Test HTTP redirect
curl -i http://jellyfin.brownfunk.lan

# Test DNS
nslookup jellyfin.brownfunk.lan 192.168.1.180

# Test direct port (fallback)
curl http://brownfunk.lan:8096

# Check certificate
openssl s_client -connect jellyfin.brownfunk.lan:443
```

---

## ⚠️ Important Notes

1. **Self-Signed Certificates**: Browser will warn for .lan names - this is expected and secure
2. **HTTP Redirect**: All HTTP → HTTPS (port 80 → 443)
3. **DNS Required**: `.lan` names need PiHole DNS (192.168.1.180) to resolve
4. **Certificate Renewal**: Let's Encrypt auto-renews every 90 days
5. **Fallback Access**: Direct ports still work if Traefik fails

---

## 🔄 Next Steps

1. **Review**: Read [`QUICK_START.md`](./QUICK_START.md) (5 min)
2. **Deploy**: Follow [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) (20 min)
3. **Test**: Verify services are accessible (5 min)
4. **Reference**: Keep [`TRAEFIK_SETUP.md`](./TRAEFIK_SETUP.md) for later

---

## 📞 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Certificate warning | Expected for .lan names, add exception |
| Can't reach services | Check DNS or use direct ports |
| Let's Encrypt fails | Verify DUCKDNS_TOKEN and internet access |
| Service not routing | Check service on proxy network |
| Traefik won't start | Check ports 80/443 aren't in use |
| Slow performance | Check Traefik logs for errors |

See [`DEPLOYMENT_CHECKLIST.md`](./DEPLOYMENT_CHECKLIST.md) for detailed troubleshooting.

---

**Version**: 1.0  
**Created**: 2026-09-25  
**Status**: Ready to Deploy ✅  
**Last Updated**: See git history  

For questions or issues, refer to the three main documentation files above.
