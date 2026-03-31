# Data Directory

This directory contains all runtime data files created by DAVID CIS.
**Do not manually delete files here** unless resetting the application.

---

## Files Created at Runtime

| File | Module | Contents |
|------|--------|----------|
| `threat_intel.db` | Threat Intelligence | IOC cache, AbuseIPDB/OTX/ThreatFox results, local events |
| `siem.db` | Local SIEM | Security events, alert stats, brute force tracking |
| `bounty.db` | Bug Bounty | Submitted reports, CVSS scores, researcher leaderboard |
| `scan_results.db` | All engines | Pentest, malware, OSINT scan results |
| `scheduler.db` | Automation | Scheduled job definitions and run history |

---

## Seeding Threat Intel Data

Run this once to pre-populate the threat intel database from free bulk feeds:

```bash
python -c "
from intelligence.threat_intel import ThreatIntelEngine
engine = ThreatIntelEngine()
engine.update_feeds()
print(engine.db.stats())
"
```

This downloads:
- **ThreatFox** — recent malware IOCs (IPs, domains, hashes)
- **URLhaus** — active malware URLs
- **FeodoTracker** — C2 server IP blocklist
- **Emerging Threats** — IP reputation blocklist

All stored locally. Future lookups are instant and offline.

---

## Backup

```bash
# Backup all data
cp -r data/ data_backup_$(date +%Y%m%d)/

# Restore
cp -r data_backup_20260331/ data/
```

## Reset

```bash
# Delete all cached data (fresh start)
rm -f data/*.db
```
