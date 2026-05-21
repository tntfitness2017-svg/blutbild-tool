<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blutbild-Analyse – TNT Fitness</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --orange: #e04a00;
      --orange-dark: #b83c00;
      --dark: #1a1a2e;
      --gray: #f4f4f6;
      --gray-mid: #e2e2e8;
      --text: #1a1a2e;
      --text-light: #6b7280;
      --green: #16a34a;
      --green-bg: #f0fdf4;
      --red: #dc2626;
    }

    body {
      font-family: "Inter", "Segoe UI", system-ui, sans-serif;
      background: var(--gray);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: var(--dark);
      padding: 0 2rem;
      height: 64px;
      display: flex;
      align-items: center;
    }
    .logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .logo-icon {
      width: 36px; height: 36px;
      background: var(--orange);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 18px; font-weight: 900; color: white;
    }
    .logo-text { font-size: 1.1rem; font-weight: 700; color: white; }
    .logo-sub { font-size: 0.7rem; color: rgba(255,255,255,0.5); letter-spacing: 1px; text-transform: uppercase; }

    main {
      flex: 1;
      max-width: 660px;
      width: 100%;
      margin: 3rem auto;
      padding: 0 1rem;
    }

    .hero { text-align: center; margin-bottom: 2rem; }
    .hero h1 { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .hero h1 span { color: var(--orange); }
    .hero p { font-size: 0.95rem; color: var(--text-light); line-height: 1.6; }

    .steps {
      display: flex; gap: 0.5rem; margin-bottom: 2rem; justify-content: center;
    }
    .step { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; color: var(--text-light); }
    .step-num {
      width: 20px; height: 20px; background: var(--gray-mid); border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.7rem; font-weight: 700; color: var(--text-light);
    }
    .step.active .step-num { background: var(--orange); color: white; }
    .step-sep { color: var(--gray-mid); font-size: 0.7rem; }

    .card {
      background: white;
      border-radius: 16px;
      padding: 2rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.05);
    }

    .field { margin-bottom: 1.5rem; }
    label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem; }

    input[type="text"] {
      width: 100%; padding: 0.75rem 1rem;
      border: 1.5px solid var(--gray-mid); border-radius: 10px;
      font-size: 1rem; color: var(--text); outline: none; transition: border-color 0.2s;
    }
    input[type="text"]:focus { border-color: var(--orange); }
    input[type="text"]::placeholder { color: var(--text-light); }

    .upload-zone {
      border: 2px dashed var(--gray-mid); border-radius: 12px;
      padding: 2.5rem 1.5rem; text-align: center; cursor: pointer;
      transition: border-color 0.2s, background 0.2s; position: relative;
    }
    .upload-zone:hover, .upload-zone.dragover { border-color: var(--orange); background: #fff5f2; }
    .upload-zone input[type="file"] {
      position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%;
    }
    .upload-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
    .upload-zone p { font-size: 0.9rem; color: var(--text-light); }
    .upload-zone strong { color: var(--orange); }
    .upload-hint { font-size: 0.75rem; margin-top: 0.4rem; color: #9ca3af; }

    .file-selected {
      display: none; align-items: center; gap: 0.75rem;
      padding: 0.75rem 1rem;
      background: var(--green-bg); border: 1.5px solid #86efac;
      border-radius: 10px; margin-top: 0.75rem;
    }
    .file-selected.visible { display: flex; }
    .file-name { font-size: 0.85rem; font-weight: 600; color: var(--green); word-break: break-all; }
    .remove-file {
      margin-left: auto; background: none; border: none;
      cursor: pointer; font-size: 1.1rem; color: #6b7280;
    }

    .btn {
      width: 100%; padding: 0.9rem;
      background: var(--orange); color: white;
      border: none; border-radius: 12px;
      font-size: 1rem; font-weight: 700; cursor: pointer;
      transition: background 0.2s, transform 0.1s; letter-spacing: 0.3px;
    }
    .btn:hover { background: var(--orange-dark); }
    .btn:active { transform: scale(0.99); }
    .btn:disabled { background: #d1d5db; cursor: not-allowed; }

    /* LOADING */
    .loading { display: none; text-align: center; padding: 2rem 0 0.5rem; }
    .loading.visible { display: block; }
    .spinner {
      width: 44px; height: 44px;
      border: 4px solid var(--gray-mid); border-top-color: var(--orange);
      border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1rem;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading p { font-size: 0.9rem; color: var(--text-light); }
    .loading-steps { font-size: 0.8rem; color: #9ca3af; margin-top: 0.5rem; }

    /* RESULT */
    .result { display: none; }
    .result.visible { display: block; }

    .result-success {
      background: var(--green-bg); border: 1.5px solid #86efac;
      border-radius: 12px; padding: 1.5rem; margin-bottom: 1.25rem;
    }
    .result-success h3 { font-size: 1rem; font-weight: 700; color: var(--green); margin-bottom: 0.5rem; }
    .result-meta { font-size: 0.82rem; color: #374151; margin-bottom: 1rem; line-height: 1.7; }
    .result-meta span { font-weight: 600; }

    .sheet-link {
      display: flex; align-items: center; gap: 0.6rem;
      background: var(--green); color: white;
      padding: 0.75rem 1.25rem; border-radius: 10px;
      text-decoration: none; font-weight: 700; font-size: 0.9rem;
      transition: background 0.2s;
    }
    .sheet-link:hover { background: #15803d; }

    .recommendation {
      background: #f9fafb; border: 1px solid var(--gray-mid);
      border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem;
    }
    .recommendation h3 {
      font-size: 0.9rem; font-weight: 700; color: var(--dark);
      margin-bottom: 1rem; padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--gray-mid);
    }
    .rec-item { margin-bottom: 0.9rem; }
    .rec-label {
      font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.5px; color: var(--text-light); margin-bottom: 0.2rem;
    }
    .rec-label.urgent { color: var(--red); }
    .rec-label.zusammenhaenge { color: #7c3aed; }
    .rec-text { font-size: 0.875rem; color: var(--text); line-height: 1.5; }

    .not-matched {
      background: #fffbeb; border: 1px solid #fcd34d;
      border-radius: 10px; padding: 1rem; font-size: 0.82rem;
    }
    .not-matched h4 { font-weight: 700; margin-bottom: 0.4rem; color: #92400e; }
    .not-matched li { color: #78350f; margin-left: 1.2rem; line-height: 1.8; }

    .btn-again {
      width: 100%; padding: 0.75rem;
      background: white; color: var(--orange);
      border: 2px solid var(--orange); border-radius: 12px;
      font-size: 0.95rem; font-weight: 700; cursor: pointer;
      transition: background 0.15s; margin-top: 1rem;
    }
    .btn-again:hover { background: #fff5f2; }

    /* ERROR */
    .error-box {
      display: none; background: #fef2f2;
      border: 1.5px solid #fca5a5; border-radius: 10px;
      padding: 1rem 1.25rem; margin-top: 1.25rem;
      font-size: 0.875rem; color: var(--red);
    }
    .error-box.visible { display: block; }

    footer { text-align: center; padding: 2rem 1rem; font-size: 0.78rem; color: #9ca3af; }
  </style>
</head>
<body>

<header>
  <a href="https://tntfitness.de" class="logo">
    <div class="logo-icon">T</div>
    <div>
      <div class="logo-text">TNT Fitness</div>
      <div class="logo-sub">Coach-Tool</div>
    </div>
  </a>
</header>

<main>
  <div class="hero">
    <h1>Blutbild <span>analysieren</span></h1>
    <p>PDF oder Foto hochladen → Werte werden automatisch in das<br>Google Sheets Tracking des Kunden eingetragen.</p>
  </div>

  <div class="steps" id="steps">
    <div class="step active" id="step1"><div class="step-num">1</div><span>Hochladen</span></div>
    <div class="step-sep">›</div>
    <div class="step" id="step2"><div class="step-num">2</div><span>Analyse</span></div>
    <div class="step-sep">›</div>
    <div class="step" id="step3"><div class="step-num">3</div><span>Fertig in Google Sheets</span></div>
  </div>

  <div class="card">

    <!-- FORMULAR -->
    <form id="uploadForm">
      <div class="field">
        <label for="customer_name">Name des Kunden</label>
        <input type="text" id="customer_name" name="customer_name"
               placeholder="z.B. Max Mustermann" required autocomplete="off" />
      </div>

      <div class="field">
        <label>Blutbild hochladen</label>
        <div class="upload-zone" id="dropZone">
          <input type="file" id="fileInput" name="file" accept=".pdf,.jpg,.jpeg,.png" required />
          <div class="upload-icon">📋</div>
          <p><strong>Klicken</strong> oder Datei hier reinziehen</p>
          <p class="upload-hint">PDF, JPG oder PNG · max. 20 MB</p>
        </div>
        <div class="file-selected" id="fileSelected">
          <span>📄</span>
          <span class="file-name" id="fileName"></span>
          <button type="button" class="remove-file" id="removeFile">✕</button>
        </div>
      </div>

      <button type="submit" class="btn" id="submitBtn">Blutbild analysieren →</button>
      <div class="error-box" id="errorBox"></div>
    </form>

    <!-- LOADING -->
    <div class="loading" id="loading">
      <div class="spinner"></div>
      <p><strong>Blutbild wird ausgewertet…</strong></p>
      <p class="loading-steps">Claude liest Werte · Ordnet Template-Parameter zu · Trägt in Google Sheets ein</p>
    </div>

    <!-- ERGEBNIS -->
    <div class="result" id="result">

      <div class="result-success">
        <h3>✓ Fertig eingetragen</h3>
        <div class="result-meta" id="resultMeta"></div>
        <a href="#" class="sheet-link" id="sheetLink" target="_blank">
          📊 Google Sheet öffnen →
        </a>
      </div>

      <div class="recommendation" id="recommendationBox">
        <h3>Handlungsempfehlung</h3>
        <div id="recommendationContent"></div>
      </div>

      <div class="not-matched" id="notMatchedBox" style="display:none; margin-bottom:1.25rem;">
        <h4>⚠️ Nicht zugeordnete Werte</h4>
        <ul id="notMatchedList"></ul>
      </div>

      <button class="btn-again" id="btnAgain">Weiteres Blutbild analysieren</button>
    </div>

  </div>
</main>

<footer>© 2025 TNT Fitness · Nur für interne Coach-Verwendung</footer>

<script>
  const form = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const dropZone = document.getElementById('dropZone');
  const fileSelected = document.getElementById('fileSelected');
  const fileName = document.getElementById('fileName');
  const removeFile = document.getElementById('removeFile');
  const submitBtn = document.getElementById('submitBtn');
  const loading = document.getElementById('loading');
  const errorBox = document.getElementById('errorBox');
  const result = document.getElementById('result');

  function showFile(file) {
    fileName.textContent = file.name;
    fileSelected.classList.add('visible');
    dropZone.style.display = 'none';
  }

  function clearFile() {
    fileInput.value = '';
    fileSelected.classList.remove('visible');
    dropZone.style.display = '';
  }

  fileInput.addEventListener('change', () => { if (fileInput.files[0]) showFile(fileInput.files[0]); });
  removeFile.addEventListener('click', clearFile);

  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
      const dt = new DataTransfer(); dt.items.add(file);
      fileInput.files = dt.files; showFile(file);
    }
  });

  function setStep(n) {
    [1,2,3].forEach(i => {
      document.getElementById('step'+i).classList.toggle('active', i === n);
    });
  }

  function showResult(data) {
    setStep(3);
    const isNew = data.is_new_customer;
    document.getElementById('resultMeta').innerHTML =
      `<span>${data.values_written} Werte</span> eingetragen in Spalte <span>${data.be_column}</span> · ` +
      (isNew ? `<span>Neues Sheet erstellt</span>` : `<span>Bestehendes Sheet aktualisiert</span>`);

    document.getElementById('sheetLink').href = data.sheet_url;

    // Empfehlung
    const rec = data.recommendation || {};
    const recHtml = [
      rec.dringend && rec.dringend !== 'Keine auffälligen Werte' ? `<div class="rec-item"><div class="rec-label urgent">⚠ Dringend</div><div class="rec-text">${rec.dringend}</div></div>` : '',
      rec.zusammenfassung ? `<div class="rec-item"><div class="rec-label">Zusammenfassung</div><div class="rec-text">${rec.zusammenfassung}</div></div>` : '',
      rec.zusammenhaenge ? `<div class="rec-item"><div class="rec-label zusammenhaenge">🔗 Zusammenhänge</div><div class="rec-text">${rec.zusammenhaenge}</div></div>` : '',
      rec.ernaehrung ? `<div class="rec-item"><div class="rec-label">Ernährung</div><div class="rec-text">${rec.ernaehrung}</div></div>` : '',
      rec.training ? `<div class="rec-item"><div class="rec-label">Training</div><div class="rec-text">${rec.training}</div></div>` : '',
      rec.supplements ? `<div class="rec-item"><div class="rec-label">Supplements</div><div class="rec-text">${rec.supplements}</div></div>` : '',
      rec.followup ? `<div class="rec-item"><div class="rec-label">Follow-up</div><div class="rec-text">${rec.followup}</div></div>` : '',
    ].filter(Boolean).join('');
    document.getElementById('recommendationContent').innerHTML = recHtml;

    // Nicht zugeordnete Werte
    if (data.not_matched && data.not_matched.length > 0) {
      const box = document.getElementById('notMatchedBox');
      box.style.display = '';
      const list = document.getElementById('notMatchedList');
      list.innerHTML = data.not_matched.map(
        m => `<li><strong>${m.parameter}</strong>: ${m.wert} ${m.einheit || ''} → bitte manuell eintragen</li>`
      ).join('');
    }

    result.classList.add('visible');
  }

  document.getElementById('btnAgain').addEventListener('click', () => {
    result.classList.remove('visible');
    form.reset(); clearFile();
    form.style.display = '';
    document.getElementById('notMatchedBox').style.display = 'none';
    errorBox.classList.remove('visible');
    setStep(1);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorBox.classList.remove('visible');
    setStep(2);
    form.style.display = 'none';
    loading.classList.add('visible');

    try {
      const res = await fetch('/analyze', { method: 'POST', body: new FormData(form) });
      const data = await res.json();

      loading.classList.remove('visible');

      if (!res.ok) throw new Error(data.error || 'Unbekannter Fehler');

      showResult(data);
    } catch (err) {
      loading.classList.remove('visible');
      form.style.display = '';
      setStep(1);
      errorBox.textContent = err.message;
      errorBox.classList.add('visible');
    }
  });
</script>
</body>
</html>
