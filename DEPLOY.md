# Deployment-Anleitung: blut.tntfitness.de

## Was du brauchst
- GitHub Account (kostenlos): https://github.com
- Railway Account (kostenlos): https://railway.app
- Deinen Claude API Key: https://console.anthropic.com
- Google Cloud Account (kostenlos): https://console.cloud.google.com

---

## Schritt 1 – Google Service Account einrichten (einmalig)

Ein Service Account ist ein technischer Google-Zugang, mit dem die App auf dein Google Sheet zugreifen kann.

### 1a. Google Cloud Projekt erstellen
1. Gehe auf https://console.cloud.google.com
2. Oben links: "Projekt auswählen" → "Neues Projekt"
3. Name: `tnt-blutbild` → "Erstellen"

### 1b. APIs aktivieren
1. Linkes Menü → "APIs & Dienste" → "Bibliothek"
2. Suche nach "Google Drive API" → "Aktivieren"
3. Zurück zur Bibliothek → "Google Sheets API" → "Aktivieren"

### 1c. Service Account erstellen
1. Linkes Menü → "APIs & Dienste" → "Anmeldedaten"
2. "+ Anmeldedaten erstellen" → "Dienstkonto"
3. Name: `blutbild-app` → "Erstellen und fortfahren" → "Fertig"
4. Klicke auf das neue Dienstkonto in der Liste
5. Reiter "Schlüssel" → "Schlüssel hinzufügen" → "Neuen Schlüssel erstellen"
6. Format: **JSON** → "Erstellen"
7. Die JSON-Datei wird heruntergeladen – gut aufbewahren!

### 1d. Template-Sheet mit Service Account teilen
1. Öffne dein Google Sheet (Blutbild-Vorlage)
2. Oben rechts: "Teilen"
3. Die E-Mail-Adresse des Service Accounts einfügen
   (steht in der JSON-Datei unter `"client_email"`, z.B. `blutbild-app@tnt-blutbild.iam.gserviceaccount.com`)
4. Berechtigung: **Bearbeiter** → Senden

### 1e. Ergebnis-Ordner in Google Drive erstellen
1. Öffne Google Drive
2. Neuen Ordner erstellen: `TNT Blutbilder Kunden`
3. Ordner mit dem Service Account teilen (wie in 1d, gleiche E-Mail)
4. Rechtsklick auf den Ordner → "Informationen" → die Ordner-ID aus der URL kopieren
   (URL: `drive.google.com/drive/folders/XXXX` → `XXXX` ist die ID)

---

## Schritt 2 – Projekt auf GitHub hochladen

1. Gehe auf https://github.com → "New repository"
2. Name: `blutbild-tool` → "Create repository"
3. Lade alle Dateien aus diesem Ordner hoch ("uploading an existing file")

---

## Schritt 3 – App auf Railway deployen

1. Gehe auf https://railway.app → "New Project"
2. "Deploy from GitHub repo" → GitHub verbinden → `blutbild-tool` auswählen
3. Railway erkennt Python automatisch → einfach bestätigen

### Umgebungsvariablen in Railway eintragen:
Projekt → "Variables" → folgende Variablen anlegen:

| Variable | Wert |
|---|---|
| `ANTHROPIC_API_KEY` | Dein Claude API Key (`sk-ant-...`) |
| `TEMPLATE_SHEET_ID` | `1ZXptiINCbkZ2fBGNDQ5Qr-rrqor-IETSYbSFZ3xlUNI` |
| `OUTPUT_FOLDER_ID` | Die Ordner-ID aus Schritt 1e |
| `GOOGLE_SERVICE_ACCOUNT` | Den gesamten Inhalt der JSON-Datei (als eine Zeile) |

**Wichtig für `GOOGLE_SERVICE_ACCOUNT`:** Öffne die heruntergeladene JSON-Datei mit einem Texteditor, markiere alles und füge es als Wert ein.

4. "Deploy" klicken → nach 2–3 Minuten läuft die App

---

## Schritt 4 – blut.tntfitness.de einrichten

### In Railway:
1. Projekt → "Settings" → "Domains" → "Custom Domain"
2. Eingeben: `blut.tntfitness.de`
3. Railway zeigt dir einen CNAME-Wert

### Bei deinem Domain-Anbieter:
1. DNS-Einstellungen öffnen
2. Neuen CNAME-Eintrag:
   - Host: `blut`
   - Wert: den CNAME aus Railway
3. Speichern → nach 5–30 Minuten aktiv

---

## Fertig!

Die App läuft unter `blut.tntfitness.de`.

**So funktioniert es für jeden Coach:**
- Kundennamen eingeben
- Blutbild (PDF oder Foto) hochladen
- Claude analysiert und trägt Werte automatisch in Google Sheets ein
- Direkt-Link zum fertigen Sheet erscheint auf der Seite

**Für jeden Kunden:**
- Erstes Blutbild → neues Sheet wird automatisch aus der Vorlage erstellt
- Folgeblutbilder → werden in BE 2, BE 3, BE 4 eingetragen (Verlauf sichtbar)

---

## Kosten

| Dienst | Kosten |
|---|---|
| GitHub | Kostenlos |
| Railway | $5/Monat (Hobby Plan) |
| Google Cloud | Kostenlos (API-Nutzung im Rahmen der Free Tier) |
| Claude API | ca. $0.01–0.05 pro Analyse |
