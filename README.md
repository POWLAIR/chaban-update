# Pont Chaban-Delmas — Calendrier ICS automatique

Génère automatiquement un fichier `.ics` avec les prévisions de fermeture du
[Pont Chaban-Delmas](https://opendata.bordeaux-metropole.fr/explore/dataset/previsions_pont_chaban/)
à partir de l'open data de Bordeaux Métropole.

## Fonctionnement

| Étape | Détail |
|---|---|
| Source | API Bordeaux Métropole — dataset `previsions_pont_chaban` |
| Script | `generate_calendar.py` → génère `docs/pont_chaban.ics` |
| Automatisation | GitHub Actions, toutes les 48h (5h UTC) |
| Diffusion | GitHub Pages → URL publique du fichier `.ics` |
| Abonnement | Google Calendar / Apple Calendar / Outlook via l'URL |

## Installation locale

```bash
pip install -r requirements.txt
python generate_calendar.py
```

Le fichier `docs/pont_chaban.ics` est créé localement.

## Abonnement Google Calendar

*Autres agendas → Depuis l'URL → coller l'URL ci-dessous*

```
https://powlair.github.io/chaban-update/pont_chaban.ics
```

Google Calendar rafraîchit les agendas externes toutes les 12-24h environ.

## Mise en place sur GitHub (pour un fork)

1. Pusher ce repo sur GitHub (repo **public**)
2. Activer GitHub Pages : *Settings → Pages → Deploy from branch `master` → `/docs`*
3. Déclencher le premier workflow : *Actions → Update Pont Chaban Calendar → Run workflow*
4. L'URL du calendrier sera : `https://<ton-user>.github.io/<nom-repo>/pont_chaban.ics`
