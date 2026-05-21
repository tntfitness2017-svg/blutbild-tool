import os
import base64
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import anthropic
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

TEMPLATE_SHEET_ID = os.environ.get("TEMPLATE_SHEET_ID", "1ZXptiINCbkZ2fBGNDQ5Qr-rrqor-IETSYbSFZ3xlUNI")
OUTPUT_FOLDER_ID = os.environ.get("OUTPUT_FOLDER_ID", "")
DASHBOARD_SHEET_NAME = "Blutbild Dashboard MUSTER"

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Alle 170 Parameter-Namen exakt wie im Template
TEMPLATE_PARAMETERS = [
    "Harnstoff (mg/dl)", "Harnsäure (mg/dl)", "Kreatinin (mg/dl)",
    "GFR CKD-EPI (ml/min/1.73m²)", "Cystatin C (mg/L)", "GFR Cystatin (mL/min)",
    "Gesamt-IgE (kU/l)", "Amylase, Lipase (U/l)",
    "Fettsäuren der Erythrozytenmembran", "Aminosäurestatus",
    "Vitamin C (mg/l)", "Biotin (Vitamin H) (ng/l)", "Vitamin K1/K2",
    "Methylgruppendonatoren", "8-Hydroxydesoxyguanosin (8-OHdG)",
    "BHI-PLUS (Bioenergetischer Gesundheitsindex)",
    "Ergänzende Biomarker (ursächliche Faktoren)", "mt/n-DNA-Ratio",
    "LDH + LDH-Isoenzyme (U/l)", "Lactat-Pyruvat-Ratio",
    "Organische Säuren des Zitronensäurezyklus", "TKTL-1 und APO-10", "M2PK Blut",
    "Oxidative Belastung", "Lipidperoxidation", "Crosslinks", "CK-MB (U/l)",
    "Lipoprotein (a) (nmol/l)", "Profil Glutathionstoffwechsel", "Thiol-Status",
    "Glutathionperoxidase (GPx)", "Superoxiddismutase (SOD)", "Basisprofil Darm",
    "Malabsorption: α1-AT, Calprotectin", "Schleimhautimmunität: sIgA",
    "Histamin im Stuhl", "Zonulin im Serum",
    "Mikrobiom Mini (Bakteriom + Mykobiom)", "Mikrobiom Midi (+ Parasiten)",
    "Mikrobiom Maxi (+ Parasiten)", "Maldigestion, Malabsorption (MIS)",
    "Mikrobolom 1.0 NEU", "RANTES (CCL5) (pg/ml)", "Histamin-Abbaukapazität (DAO)",
    "GPCR-Autoantikörper Basis", "Zellulärer Immunstatus",
    "sIL2R (T-Zellaktivierung) (U/ml)", "Neopterin", "TH1/TH2/TH17 (inkl. IL-17)",
    "IDO-Aktivität, TRP/KYN", "Pregnenolonsulfat (ng/ml)", "Östrogenmetabolite",
    "Somatomedin C / IGF-1 (ng/ml)", "Neurotransmitter Plus",
    "NT-Tryptophan-Metabolismus", "Neuronenspezifische Enolase (NSE)",
    "HOMA-Index", "HbA1c", "AGEs", "GPT", "NT-proBNP", "LDH 4 und 5",
    "LDL-Cholesterin", "Lipo(a)", "Zonulin", "I-FABP", "HPU (Pyrrole im Urin)",
    "TPO-AK", "TAK", "Nitrotyrosin", "CRP", "oxLDL", "MDA-LDL", "LDL",
    "Kreatinin", "Harnsäure", "Beta-Cross-Laps", "Trap 5b", "Lp-PLA2", "Apo-B",
    "Cystatin C", "CK", "Hämoglobin", "BDNF", "Serotonin", "Cortisol", "Calcium",
    "fT3", "PSA", "Homocystein", "MCV", "MCH", "Histamin", "PTH", "Calcitriol",
    "Mikronährstoff", "Vitamin A", "Vitamin B1", "Vitamin B2", "Vitamin B3",
    "Vitamin B5", "Vitamin B6", "Vitamin B7", "Vitamin B9", "Vitamin B12",
    "Calcidiol", "Vitamin E", "Vitamin K2",
    "Chrom", "Jod", "Molybdän", "Selen", "Bor", "Kupfer", "Zink", "Mangan",
    "Eisen",
    "Testosteron (gesamt)", "Freier Androgenindex (FAI)", "DHEA-S",
    "Freies Testosteron", "Estradiol (E2)", "Progesteron",
    "LH (Luteinisierendes Hormon)", "FSH (Follikelstimulierendes Hormon)",
    "SHBG", "Albumin",
    # Herz & Gefäße
    "Glucose nüchtern (mg/dL)", "Insulin Nüchtern", "HbA1c (%)", "AGE (Advanced Glycation Endproduct)",
    "Cholesterin (mg/dl)", "ApoB (mg/dL)", "Apo A1", "LDL-C (mg/dL)",
    "Non-HDL-Cholesterin (mg/dL)", "Triglyceride (mg/dL)", "HDL-C (mg/dL)",
    "Homocystein (μmol/L)", "Lipoprotein(a) / Lp(a) (nmol/l)",
    # Blutbild
    "Erythrozyten (Mio/μl)", "Hämatokrit (%)", "Hämoglobin / Hb (g/dl)",
    "MCH (pg)", "MCHC (g/dl)", "MCV (fl)", "RDW-CV (%)", "RDW-SD (fl)",
    "Leukozyten (G/l)", "Lymphozyten (G/l)", "Neutrophile (G/l)",
    # Hormone
    "Gesamt-Testosteron (ng/ml)", "Testosteron, frei (pg/ml)",
    "SHBG (nmol/l)", "Estradiol / E2 (pg/ml)",
]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_google_credentials():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    if not sa_json:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT Umgebungsvariable fehlt")
    sa_info = json.loads(sa_json)
    return service_account.Credentials.from_service_account_info(sa_info, scopes=GOOGLE_SCOPES)


def find_or_create_customer_tab(gc, customer_name):
    """Suche oder erstelle einen Tab für den Kunden im Template-Dokument."""
    sh = gc.open_by_key(TEMPLATE_SHEET_ID)
    tab_name = customer_name[:100]  # Google Sheets max tab name length

    # Prüfe ob Tab bereits existiert
    try:
        ws = sh.worksheet(tab_name)
        return sh, ws, False  # gefunden
    except gspread.WorksheetNotFound:
        pass

    # Template-Tab duplizieren
    template_ws = sh.worksheet(DASHBOARD_SHEET_NAME)
    sh.duplicate_sheet(
        source_sheet_id=template_ws.id,
        new_sheet_name=tab_name,
    )
    ws = sh.worksheet(tab_name)
    return sh, ws, True  # neu erstellt


def build_param_row_map(worksheet):
    """Erstellt Mapping: parameter_name → zeilen_index (1-basiert)."""
    all_values = worksheet.get_all_values()
    param_map = {}
    for i, row in enumerate(all_values):
        if row and row[0].strip():
            name = row[0].strip()
            if name not in param_map:  # nur erste Vorkommen
                param_map[name] = i + 1
    return param_map, all_values


def find_be_column(all_values):
    """Findet den Index der Kopfzeile und die nächste freie BE-Spalte."""
    header_row_idx = None
    be_col_map = {}

    for i, row in enumerate(all_values):
        if "BE 1" in row and "BE 2" in row:
            header_row_idx = i
            for j, cell in enumerate(row):
                if cell.strip() in ("BE 1", "BE 2", "BE 3", "BE 4"):
                    be_col_map[cell.strip()] = j
            break

    if header_row_idx is None:
        return None, None, None

    # Nächste freie BE-Spalte finden
    for be_name in ("BE 1", "BE 2", "BE 3", "BE 4"):
        if be_name not in be_col_map:
            continue
        col_idx = be_col_map[be_name]
        # Prüfe ob Spalte leer ist (Zeilen nach Header)
        col_vals = [
            row[col_idx] if col_idx < len(row) else ""
            for row in all_values[header_row_idx + 1:]
        ]
        if not any(v.strip() for v in col_vals):
            return header_row_idx, col_idx, be_name

    # Fallback: BE 4
    return header_row_idx, be_col_map.get("BE 4", 5), "BE 4"


def write_values_to_sheet(worksheet, param_row_map, all_values, col_idx, header_row_idx, mapped_values, test_date):
    """Schreibt die Blutwerte in die richtige Spalte."""
    updates = []

    # Datum in die Kopfzeile schreiben (Zeile über den Parametern, falls vorhanden)
    date_row = header_row_idx  # Header selbst
    # Schreibe Datum eine Zeile über dem Header, falls machbar
    if header_row_idx > 0:
        date_row_idx = header_row_idx - 1
        updates.append({
            "range": gspread.utils.rowcol_to_a1(date_row_idx + 1, col_idx + 1),
            "values": [[test_date]],
        })

    # Werte eintragen
    written = 0
    for param_name, value in mapped_values.items():
        if param_name in param_row_map:
            row_num = param_row_map[param_name]
            updates.append({
                "range": gspread.utils.rowcol_to_a1(row_num, col_idx + 1),
                "values": [[str(value)]],
            })
            written += 1

    if updates:
        worksheet.batch_update(updates)

    return written


def analyze_with_claude(file_content, file_type):
    """Claude analysiert das Blutbild und ordnet Werte den Template-Parametern zu."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    b64 = base64.standard_b64encode(file_content).decode("utf-8")

    if "pdf" in file_type:
        content_block = {
            "type": "document",
            "source": {"type": "base64", "media_type": "application/pdf", "data": b64},
        }
    else:
        media_type = file_type if file_type.startswith("image/") else "image/jpeg"
        content_block = {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": b64},
        }

    params_list = "\n".join(f"- {p}" for p in TEMPLATE_PARAMETERS)

    prompt = f"""Du analysierst ein medizinisches Blutbild für einen Fitness-Coach.

Unten findest du die vollständige Liste aller Parameter aus unserem Tracking-System.
Ordne jeden im Blutbild gefundenen Wert dem passenden Parameter aus dieser Liste zu.

PARAMETER-LISTE (verwende exakt diese Namen):
{params_list}

Antworte ausschließlich mit gültigem JSON – kein Text davor oder danach:

{{
  "werte": {{
    "Exakter Parameter-Name aus der Liste": "gemessener Wert als String (nur Zahl, keine Einheit)",
    ...
  }},
  "nicht_zugeordnet": [
    {{"parameter": "Name im Blutbild", "wert": "Wert", "einheit": "Einheit"}}
  ],
  "handlungsempfehlung": {{
    "zusammenfassung": "Medizinische Zusammenfassung in 2-3 Sätzen",
    "dringend": "Werte die sofortige Aufmerksamkeit brauchen – oder 'Keine auffälligen Werte'",
    "ernaehrung": "Konkrete Ernährungsempfehlungen basierend auf den Werten",
    "training": "Trainingsempfehlungen und eventuelle Einschränkungen",
    "supplements": "Empfohlene Supplements mit Begründung (z.B. Vitamin D, Magnesium)",
    "followup": "Empfehlung wann das nächste Blutbild sinnvoll ist"
  }}
}}

Regeln:
- Verwende im 'werte'-Objekt NUR Namen aus der obigen Liste
- Werte als reine Zahlen ohne Einheit (z.B. "14.5" nicht "14.5 g/dl")
- Nicht zuordenbare Werte kommen in 'nicht_zugeordnet'"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": [content_block, {"type": "text", "text": prompt}]}],
    )

    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    """Debug-Endpunkt um Konfiguration zu prüfen."""
    checks = {}
    checks["anthropic_key"] = bool(os.environ.get("ANTHROPIC_API_KEY"))
    checks["template_sheet_id"] = bool(os.environ.get("TEMPLATE_SHEET_ID"))
    checks["output_folder_id"] = bool(os.environ.get("OUTPUT_FOLDER_ID"))
    sa_raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT", "")
    checks["service_account_set"] = bool(sa_raw)
    if sa_raw:
        try:
            json.loads(sa_raw)
            checks["service_account_valid_json"] = True
        except Exception as e:
            checks["service_account_valid_json"] = False
            checks["service_account_error"] = str(e)[:100]
    try:
        creds = get_google_credentials()
        checks["google_credentials"] = "OK"
    except Exception as e:
        checks["google_credentials"] = str(e)[:150]
    return jsonify(checks)


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "Keine Datei hochgeladen"}), 400

    file = request.files["file"]
    customer_name = request.form.get("customer_name", "").strip()

    if not customer_name:
        return jsonify({"error": "Bitte Kundennamen eingeben"}), 400
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Nur PDF, JPG und PNG erlaubt"}), 400

    file_content = file.read()
    if len(file_content) > MAX_FILE_SIZE:
        return jsonify({"error": "Datei zu groß (max. 20 MB)"}), 400

    file_type = file.content_type or "application/octet-stream"
    test_date = datetime.now().strftime("%d.%m.%Y")

    try:
        # 1. Blutbild analysieren
        analysis = analyze_with_claude(file_content, file_type)
        mapped_values = analysis.get("werte", {})
        not_matched = analysis.get("nicht_zugeordnet", [])
        recommendation = analysis.get("handlungsempfehlung", {})

        if not mapped_values:
            return jsonify({"error": "Keine Blutwerte erkannt. Bitte prüfe die Qualität der Datei."}), 422

        # 2. Google Sheets
        creds = get_google_credentials()
        gc = gspread.authorize(creds)

        sh, ws, is_new = find_or_create_customer_tab(gc, customer_name)

        # 3. Parameter-Mapping aufbauen
        param_row_map, all_values = build_param_row_map(ws)
        header_row_idx, col_idx, be_name = find_be_column(all_values)

        if col_idx is None:
            return jsonify({"error": "BE-Spalten nicht gefunden. Bitte Template prüfen."}), 500

        # 4. Werte eintragen
        written = write_values_to_sheet(
            ws, param_row_map, all_values, col_idx, header_row_idx, mapped_values, test_date
        )

        # 5. Handlungsempfehlung in Notiz-Bereich schreiben (letztes Sheet oder eigene Zeile)
        # Suche nach freier Zeile am Ende des Sheets für die Empfehlung
        try:
            next_row = len(all_values) + 3
            empfehlung_text = (
                f"=== Handlungsempfehlung {test_date} ({be_name}) ===\n"
                f"ZUSAMMENFASSUNG: {recommendation.get('zusammenfassung', '')}\n"
                f"DRINGEND: {recommendation.get('dringend', '')}\n"
                f"ERNÄHRUNG: {recommendation.get('ernaehrung', '')}\n"
                f"TRAINING: {recommendation.get('training', '')}\n"
                f"SUPPLEMENTS: {recommendation.get('supplements', '')}\n"
                f"FOLLOW-UP: {recommendation.get('followup', '')}"
            )
            ws.update_cell(next_row, 1, empfehlung_text)
        except Exception:
            pass  # Empfehlung ist optional

        sheet_url = f"https://docs.google.com/spreadsheets/d/{TEMPLATE_SHEET_ID}/edit#gid={ws.id}"

        return jsonify({
            "success": True,
            "sheet_url": sheet_url,
            "sheet_name": customer_name,
            "be_column": be_name,
            "is_new_customer": is_new,
            "values_written": written,
            "not_matched_count": len(not_matched),
            "not_matched": not_matched[:5],
            "recommendation": recommendation,
        })

    except json.JSONDecodeError:
        return jsonify({"error": "Claude konnte das Blutbild nicht auslesen. Bitte Dateiqualität prüfen."}), 422
    except anthropic.APIError as e:
        return jsonify({"error": f"API-Fehler: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Fehler: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
