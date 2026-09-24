Network Architecture & DNS Resolution Guide
---


# Network Architecture: Traefik, Pi-hole, Tailscale & Wireguard
┌───────────────────────────────┐     ┌───────────────────────────────┐
│         Client Device         │     │         Client Device         │
│     (Via Tailscale VPN)       │     │      (Via Wireguard VPN)      │
└──────────────┬────────────────┘     └──────────────┬────────────────┘
               │                                     │
               │ (Points to Tailscale IP)            │ (Connects to WG Port)
               ▼                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────┐
│       Tailscale Network       │     │    Wireguard Docker Container │
│ • Split DNS Nameserver:       │     │    (Running on Host Server)   │
│   *.funkybeefunk.duckdns.org  │     │ • Uses Pi-hole Docker IP for  │
│   ──► Forwards to Pi-hole     │     │   internal DNS resolution     │
└──────────────┬────────────────┘     └──────────────┬────────────────┘
               │                                     │
               └──────────────────┬──────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 Docker Host Server ("beefunk")                      │
│                                                                     │
│  ┌───────────────────────────────┐         ┌─────────────────────┐  │
│  │ Pi-hole Container + Dnsmasq   │         │       Traefik       │  │
│  │ (Docker Container IP)         │         │  (Reverse Proxy &   │  │
│  │ • Matches:                    │         │   ACME SSL Handler) │  │
│  │   *.funkybeefunk.duckdns.org  │         │                     │  │
│  │ • Resolves to: Local LAN IP   │         │                     │  │
│  └──────────────┬────────────────┘         └──────────┬──────────┘  │
│                 │                                     │             │
│                 │ (DNS Resolution Answer)             │ (Proxy Req) │
│                 └──────────────────┬──────────────────┘             │
│                                    ▼                                │
│                     [ Backend Docker Services ]                     │
└─────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ (Certificate Challenge: 
                                     │  TLS-ALPN / HTTP-01 or DNS-01)
                                     ▼
                        ┌─────────────────────────┐
                        │  Let's Encrypt (ACME)   │
                        └─────────────────────────┘


## Overview
This infrastructure routes internal and external traffic for `*.funkybeefunk.duckdns.org` and `*.beefunk.lan` securely to your Docker host server running Traefik and Pi-hole.

Traffic & Resolution Flow
1. External / VPN Entry Points:

  • Tailscale: DuckDNS points to your Tailscale IP. Tailscale Split DNS forwards `*.funkybeefunk.duckdns.org` queries directly to Pi-hole.

  • Wireguard: A Docker container running on the host server configured to use the Pi-hole container IP for internal DNS resolution.

2. DNS Interception (Pi-hole + Dnsmasq):

  • Dnsmasq matches requests for `*.beefunk.lan` and `*.funkybeefunk.duckdns.org` and resolves them directly to the Local LAN IP of the server, avoiding external routing latency.

3. Reverse Proxy & SSL (Traefik & ACME):

  • Traefik receives traffic on ports 80/443, handles automatic SSL/TLS certificate generation via Let's Encrypt (ACME) (using HTTP-01, TLS-ALPN, or DNS-01 challenges), and routes requests to the appropriate backend Docker services.

---

## Useful Diagnostic Commands
1. Test DNS Resolution via Pi-hole

Check how a specific domain resolves when querying your Pi-hole directly:

```

nslookup app.funkybeefunk.duckdns.org <PIHOLE_DOCKER_IP>

```

Or using `dig`:

```

dig @<PIHOLE_DOCKER_IP> app.funkybeefunk.duckdns.org

```

2. Verify Local Resolution on Host

```

dig app.funkybeefunk.duckdns.org +short

```

3. Check Traefik Container Logs

To inspect routing, incoming requests, or ACME certificate issuance errors:

```

docker logs -f traefik

```

4. Check Pi-hole / Dnsmasq Logs

To see if Dnsmasq is properly intercepting your wildcard domains:

```

docker logs -f pihole | grep dnsmasq

```
