# Traefik Quick Start Guide

## Start Everything

```bash
cd /home/lbesnard/github_repo/dotfiles/bfunk/docker-compose
docker compose up -d
```

## Check Status

```bash
# View Traefik logs (watch certificate generation)
docker compose logs -f traefik

# Verify all services started
docker compose ps

# Check certificate was created (wait 2-3 minutes)
ls -lh traefik/acme/acme.json
```

## Quick Access

### Local Network
- **Dashboard**: https://traefik.funkybrownfunk.duckdns.org (DuckDNS-only by design, not routed on `.lan`)
- **Jellyfin**: https://jellyfin.brownfunk.lan:443
- **Nextcloud**: https://nextcloud.brownfunk.lan:443
- **Homer**: https://home.brownfunk.lan:443

### Fallback (if DNS issues)
- **Jellyfin**: http://brownfunk.lan:8096
- **Nextcloud**: http://brownfunk.lan:9393
- **Homer**: http://brownfunk.lan:8080

### External (once DuckDNS updated)
- **Jellyfin**: https://jellyfin.funkybrownfunk.duckdns.org
- **Nextcloud**: https://nextcloud.funkybrownfunk.duckdns.org
- **Homer**: https://home.funkybrownfunk.duckdns.org

## Fix DNS Resolution

If `.brownfunk.lan` names don't resolve, add to `/etc/hosts`:
```
192.168.1.180 brownfunk.lan
192.168.1.180 jellyfin.brownfunk.lan
192.168.1.180 nextcloud.brownfunk.lan
```
(No entry needed for `traefik.brownfunk.lan` — the dashboard is not routed on `.lan`, only on the DuckDNS hostname.)

Or set device DNS to PiHole: `192.168.1.180`

## Stop Services

```bash
docker compose down
```

## View All Available Services

Run this command to see all 26 Traefik-enabled services:

```bash
docker compose config | grep -A 3 "traefik.enable"
```

## Troubleshooting

**Certificate warning in browser?**
- Expected for `.lan` names (self-signed)
- Add exception or use curl with `-k` flag

**Service not accessible?**
1. Check service is running: `docker compose ps`
2. Check service is in `proxy` network: `docker network inspect proxy`
3. Check Traefik logs: `docker compose logs traefik | tail -20`

**External access not working?**
1. Verify DuckDNS token is correct: check `traefik/acme/acme.json`
2. Check port 443 is open on WAN firewall
3. Verify DuckDNS domain is updated to your public IP
4. Wait for DNS propagation (can take 5-10 minutes)

## All Services

```
homer                 → https://home.brownfunk.lan
jellyfin              → https://jellyfin.brownfunk.lan
filebrowser           → https://filebrowser.brownfunk.lan
nextcloud             → https://nextcloud.brownfunk.lan
piwigo                → https://piwigo.brownfunk.lan
navidrome             → https://navidrome.brownfunk.lan
komga                 → https://komga.brownfunk.lan
radarr                → https://radarr.brownfunk.lan
radarr_fr             → https://radarr_fr.brownfunk.lan
sonarr                → https://sonarr.brownfunk.lan
prowlarr              → https://prowlarr.brownfunk.lan
jackett               → https://jackett.brownfunk.lan
bazarr                → https://bazarr.brownfunk.lan
calibre               → https://calibre.brownfunk.lan
calibre-web           → https://calibre-web.brownfunk.lan
hedgedoc              → https://hedgedoc.brownfunk.lan
wordpress             → https://wordpress.brownfunk.lan
wordpress_diary       → https://wordpress_diary.brownfunk.lan
tecmint-web           → https://tecmint-web.brownfunk.lan
portainer             → https://portainer.brownfunk.lan
phpmyadmin            → https://phpmyadmin.brownfunk.lan
crowdsec              → https://crowdsec.brownfunk.lan
scrutiny              → https://scrutiny.brownfunk.lan
firefox               → https://firefox.brownfunk.lan
taskchampion          → https://taskchampion.brownfunk.lan
unmanic               → https://unmanic.brownfunk.lan
traefik (admin)       → https://traefik.funkybrownfunk.duckdns.org (DuckDNS only, not on .lan)
pihole                → https://pihole.brownfunk.lan
```

Replace `brownfunk.lan` with `funkybrownfunk.duckdns.org` for external access.
