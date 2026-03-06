# HEARTBEAT.md — Brrr Kadzin 🖨️

## Perioodilised kontrollid

### PRINTER 2 (iga heartbeat)
- Kontrolli kas PRINTER 2 protsessid jooksevad VPS-il
- Kontrolli kas on uusi logisid/vigu viimase tunni jooksul
- Kui midagi on mäda, teata Ristole kohe

### Git seis (iga heartbeat)
- Kontrolli kas brrr-printer2 repos on uncommitted muudatusi
- Kontrolli kas on lahendamata merge conflicte
- Kontrolli kas VPS ja GitHub on sünkis (git status)

### VPS tervis (iga heartbeat)
- `df -h` — alerti kui ketas üle 85%
- `free -h` — alerti kui mälu üle 90%

### Flux kanban (iga heartbeat)
- `python3 /home/brrr/bin/flux-tasks list --status=in_progress` — mis on töös
- Kui midagi on liiga kaua in_progress, teata

## Reeglid
- Ära saada sõnumeid kui kõik on korras — vasta HEARTBEAT_OK
- Teata AINULT kui midagi vajab tähelepanu
- Max 3 proaktiivset sõnumit päevas, ära tüüta Ristot
- Öösiti (23:00-07:00 EET) ära saada sõnumeid, välja arvatud kriitilised alertid
