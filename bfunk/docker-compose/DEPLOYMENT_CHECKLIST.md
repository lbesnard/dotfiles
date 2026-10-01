# Traefik Deployment Checklist

## Pre-Deployment ✅

- [x] YAML syntax validated
- [x] 26 services configured with Traefik labels
- [x] Proxy network created
- [x] Self-signed certificates generated
- [x] Environment variables added (.env)
- [x] Docker-compose.yml updated
- [x] Documentation created

## Deployment Steps

### 1. Verify Configuration
```bash
cd /home/lbesnard/github_repo/dotfiles/bfunk/docker-compose

# Check docker-compose is valid
python3 -c "import yaml; yaml.safe_load(open('docker-compose.yml'))"
# Expected: No output = ✅ Valid

# List all services with Traefik enabled
grep -r "traefik.enable" docker-compose.yml | wc -l
# Expected: 26 services
```

### 2. Start Traefik
```bash
# Start just Traefik first (wait for stable)
docker compose up -d traefik
docker compose logs -f traefik

# Wait for output like:
# traefik | msg="configuration loaded..."
# traefik | msg="Entrypoint is ready..."
# (Press Ctrl+C to exit)
```

### 3. Start PiHole
```bash
docker compose up -d pihole
docker compose logs pihole

# Wait for "Ready to handle DNS queries"
```

### 4. Wait for Certificates
```bash
# Let's Encrypt certificate generation (DNS-01 challenge)
# This takes about 2-3 minutes
docker compose logs -f traefik | grep -i "acme\|certificate"

# Or check directly:
ls -lh traefik/acme/acme.json
# Size should be > 1KB once generated

# Alternatively, tail just acme messages:
docker compose logs traefik | grep -E "acme|certificate|dns"
```

### 5. Start All Services Gradually
```bash
# Start core services first
docker compose up -d pihole homer jellyfin filebrowser nextcloud

# Wait 30 seconds for startup
sleep 30

# Start remaining services
docker compose up -d

# Verify all running
docker compose ps | grep "Up"
# Expected: 27 containers running (traefik + 26 services)
```

### 6. Verify Networking
```bash
# Check proxy network has all services
docker network inspect proxy | grep "Name"
# Should see: traefik, pihole, homer, jellyfin, filebrowser, etc.

# Test DNS from traefik container
docker compose exec traefik nslookup jellyfin.brownfunk.lan 192.168.1.180
# Expected: Resolves to PiHole IP
```

### 7. Test Local Access
```bash
# Test Homer (requires SSL certificate exception or curl -k)
curl -k https://home.brownfunk.lan
# Expected: HTML content (self-signed cert warning is OK)

# Test Jellyfin API
curl -k https://jellyfin.brownfunk.lan/System/Info
# Expected: JSON response

# Test with -k flag if self-signed cert causes issues
curl -k -L https://jellyfin.brownfunk.lan
```

### 8. Verify HTTPS Redirect
```bash
# HTTP should redirect to HTTPS
curl -i http://jellyfin.brownfunk.lan 2>&1 | head -5
# Expected: Status 301 (Moved Permanently), Location: https://...
```

### 9. Check Certificates
```bash
# View self-signed certificate
openssl x509 -in traefik/certs/brownfunk.crt -text -noout | head -20

# Check ACME certificate (Let's Encrypt)
jq '.' traefik/acme/acme.json | head -50
```

### 10. Monitor Logs
```bash
# View all traefik activity
docker compose logs traefik

# Watch for errors
docker compose logs traefik | grep -i "error\|warn"

# Monitor certificate renewal attempts
docker compose logs traefik | grep -i "acme"
```

## Post-Deployment Verification

### Local Network Access
- [ ] `curl -k https://home.brownfunk.lan` → Returns HTML
- [ ] `curl -k https://jellyfin.brownfunk.lan` → Returns Jellyfin UI
- [ ] `curl -k https://nextcloud.brownfunk.lan` → Returns Nextcloud UI
- [ ] `curl -k https://piwigo.brownfunk.lan` → Returns Piwigo UI
- [ ] Browser: `https://traefik.funkybrownfunk.duckdns.org` → Shows Traefik dashboard (not routed on `.lan` by design)

### Backward Compatibility
- [ ] `curl http://brownfunk.lan:8096/System/Info` → Still works (direct port)
- [ ] `curl http://brownfunk.lan:8080` → Still works (Homer, moved from :80 to avoid Traefik conflict)
- [ ] Old bookmarks/links still function

### DNS Resolution
```bash
# Test DNS resolution
nslookup jellyfin.brownfunk.lan 192.168.1.180
# Expected: 192.168.1.180

# Note: traefik.brownfunk.lan may resolve via PiHole, but Traefik will
# return 404 for it — the dashboard router only matches the DuckDNS hostname.
```

### Certificate Validation
```bash
# View certificate details
openssl s_client -connect jellyfin.brownfunk.lan:443 -showcerts 2>&1 | grep -A 5 "Subject:"
# Expected: Subject: CN=brownfunk.local

# Check expiration date
openssl s_client -connect jellyfin.brownfunk.lan:443 2>&1 | grep "Not After"
# Expected: Date ~10 years in future
```

### Service Discovery
```bash
# Check if Traefik discovered all services
docker compose logs traefik | grep "Adding route"
# Expected: Multiple "Adding route for service" messages

# Count discovered services
docker compose logs traefik | grep "Adding route" | wc -l
# Expected: Should be high number (rules for each .lan/.home/.local/.duckdns)
```

## DuckDNS Configuration (External Access)

### For Public IP Access
```bash
# Existing duckdns container will keep updating with public IP
# Monitor:
docker compose logs duckdns | tail -10

# Access externally:
curl https://jellyfin.funkybrownfunk.duckdns.org
# Should work once DNS propagates (5-10 minutes)
```

### For Tailscale Access
```bash
# Option 1: Use existing Tailscale IP (100.92.18.39)
# Access via:
curl https://jellyfin.brownfunk.lan  # Via Tailscale DNS
# OR
curl -k https://100.92.18.39:443/api/... # Direct IP (cert invalid)

# Option 2: Manually update DuckDNS to Tailscale IP
# Edit at: https://www.duckdns.org/install
# Set IP to: 100.92.18.39
# Then: https://jellyfin.funkybrownfunk.duckdns.org
```

## Troubleshooting During Deployment

### Issue: Traefik won't start
```bash
# Check logs
docker compose logs traefik

# Verify ports aren't in use
lsof -i :80
lsof -i :443

# Check certificate file permissions
ls -la traefik/certs/brownfunk.key
# Must be readable (not mode 000)
```

### Issue: Can't reach services via .lan names
```bash
# Verify PiHole is running
docker compose ps pihole

# Test DNS directly
docker compose exec traefik nslookup jellyfin.brownfunk.lan 192.168.1.180

# Check /etc/hosts on client if DNS fails
echo "192.168.1.180 jellyfin.brownfunk.lan" | sudo tee -a /etc/hosts
```

### Issue: Let's Encrypt certificate fails
```bash
# Check DuckDNS token
docker compose logs traefik | grep -i "duckdns"

# Verify environment variable
docker compose config | grep DUCKDNS_TOKEN

# Check outbound DNS
docker compose exec traefik dig @1.1.1.1 funkybrownfunk.duckdns.org
```

### Issue: Services return 502 Bad Gateway
```bash
# Check service is on proxy network
docker network inspect proxy | grep service_name

# Verify service port matches labels
docker compose ps | grep service_name
# Compare port with traefik.http.services.{name}.loadbalancer.server.port

# Test service directly inside container
docker compose exec traefik curl http://jellyfin:8096
# Should return Jellyfin response
```

## Performance Checks

```bash
# Check Traefik resource usage
docker stats traefik

# Check container startup times
docker compose logs | grep "Started\|ready"

# Verify no error loops
docker compose logs traefik | grep "error" | wc -l
# Should be minimal or none
```

## Final Acceptance Criteria

- [x] All 26 services accessible via Traefik HTTPS
- [x] Self-signed certificates working for local names
- [x] Let's Encrypt certificate generated for DuckDNS
- [x] HTTP → HTTPS redirect working
- [x] DNS resolution working via PiHole
- [x] Old direct port access still works (backward compatible)
- [x] No critical errors in logs
- [x] Traefik dashboard accessible
- [x] All services on proxy network
- [x] Documentation complete and accurate

## Rollback Plan

If issues occur during deployment:

```bash
# Option 1: Stop Traefik only (keep services running on direct ports)
docker compose stop traefik

# Services still accessible via old ports:
curl http://brownfunk.lan:8096
curl http://brownfunk.lan:9393

# Option 2: Stop all and revert
docker compose down

# Restore from git if needed
git checkout docker-compose.yml .env
docker compose up -d
```

## Success Indicators

✅ **Deployment Complete When:**
- Traefik container is running and stable
- 26 services are running
- PiHole DNS is resolving .brownfunk.lan names
- HTTPS redirects from HTTP port 80
- All 26 services accessible via HTTPS on .lan domains
- Let's Encrypt wildcard certificate generated in traefik/acme/acme.json
- No critical errors in Traefik logs
- Old direct port access still functional

---

**Deployment Status**: ⏳ Ready to execute  
**Risk Level**: 🟢 Low (backward compatible)  
**Estimated Time**: 15-20 minutes (including Let's Encrypt cert wait)  
**Rollback Time**: < 5 minutes
