#!/usr/bin/env python3
"""Build pygen/webui/index.html — self-contained single-page app."""

import json, os

TEMPLATES_JSON = os.path.join(os.path.dirname(__file__) or '.', 'all_templates.json')
OUTPUT = os.path.join(os.path.dirname(__file__) or '.', 'pygen', 'webui', 'index.html')

with open(TEMPLATES_JSON) as f:
    data = json.load(f)

templates_js = json.dumps(data['templates'], ensure_ascii=False)
domains_js = json.dumps(data['domains'], ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PyGen — Generator Fungsi Python Deterministik</title>
<style>
:root {{
  --bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9;
  --text-dim: #8b949e; --accent: #58a6ff; --accent2: #3fb950; --accent3: #d2991d;
  --danger: #f85149; --code-bg: #0d1117; --radius: 8px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
a {{ color: var(--accent); }}

/* Header */
.header {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 12px 24px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 10; }}
.header .logo {{ font-size: 1.3em; font-weight: 700; color: var(--accent2); white-space: nowrap; }}
.header .logo span {{ color: var(--text-dim); font-weight: 400; font-size: .7em; }}
.header .search {{ flex: 1; max-width: 420px; }}
.header .search input {{ width: 100%; padding: 8px 14px; border-radius: 20px; border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: .9em; outline: none; }}
.header .search input:focus {{ border-color: var(--accent); }}
.header .stats {{ font-size: .8em; color: var(--text-dim); white-space: nowrap; }}
.header .actions {{ display: flex; gap: 8px; }}

/* Layout */
.layout {{ display: flex; height: calc(100vh - 57px); }}
.sidebar {{ width: 260px; background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 12px; flex-shrink: 0; }}
.main {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}
.main-top {{ padding: 16px 24px 8px; flex-shrink: 0; }}
.main-body {{ flex: 1; overflow-y: auto; padding: 8px 24px 24px; display: flex; flex-direction: column; gap: 16px; }}

/* Sidebar */
.domain-group {{ margin-bottom: 6px; }}
.domain-header {{ font-weight: 600; font-size: .85em; padding: 6px 8px; color: var(--text-dim); cursor: pointer; border-radius: 4px; display: flex; align-items: center; gap: 6px; }}
.domain-header:hover {{ background: rgba(88,166,255,.08); }}
.domain-header .arrow {{ font-size: .7em; transition: transform .15s; }}
.domain-header.open .arrow {{ transform: rotate(90deg); }}
.domain-items {{ padding-left: 12px; display: none; }}
.domain-header.open + .domain-items {{ display: block; }}
.cat-header {{ font-size: .8em; color: var(--text-dim); padding: 4px 8px 2px; text-transform: uppercase; letter-spacing: .5px; }}
.tpl-item {{ font-size: .82em; padding: 4px 8px 4px 16px; cursor: pointer; border-radius: 3px; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.tpl-item:hover {{ background: rgba(88,166,255,.12); }}
.tpl-item.active {{ background: rgba(88,166,255,.2); color: var(--accent); }}

/* Top bar: path + buttons */
.breadcrumb {{ display: flex; align-items: center; gap: 8px; font-size: .85em; color: var(--text-dim); margin-bottom: 8px; flex-wrap: wrap; }}
.breadcrumb .sep {{ color: var(--border); }}
.breadcrumb .active {{ color: var(--accent); font-weight: 600; }}
.current-template {{ font-size: 1.1em; font-weight: 600; margin-bottom: 4px; }}
.current-template-desc {{ font-size: .85em; color: var(--text-dim); }}
.mode-tabs {{ display: flex; gap: 2px; margin-top: 10px; }}
.mode-tab {{ padding: 6px 16px; border: 1px solid var(--border); background: none; color: var(--text-dim); cursor: pointer; font-size: .85em; border-radius: var(--radius) var(--radius) 0 0; border-bottom: none; }}
.mode-tab.active {{ background: var(--surface); color: var(--accent); }}

/* Form */
.form-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.form-grid .full {{ grid-column: 1 / -1; }}
.form-group {{ }}
.form-group label {{ display: block; font-size: .8em; color: var(--text-dim); margin-bottom: 4px; }}
.form-group label .type-badge {{ font-size: .75em; background: var(--border); padding: 1px 6px; border-radius: 3px; margin-left: 6px; color: var(--accent2); }}
.form-group input, .form-group select, .form-group textarea {{
  width: 100%; padding: 8px 12px; border: 1px solid var(--border); border-radius: 4px;
  background: var(--bg); color: var(--text); font-size: .9em; font-family: inherit;
}}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {{ border-color: var(--accent); outline: none; }}
.form-group input.error {{ border-color: var(--danger); }}
.form-group .error-msg {{ font-size: .75em; color: var(--danger); margin-top: 2px; display: none; }}
.form-group input.error + .error-msg {{ display: block; }}

/* Code */
.code-section {{ flex: 1; display: flex; flex-direction: column; min-height: 200px; }}
.code-toolbar {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }}
.code-toolbar .label {{ font-size: .8em; color: var(--text-dim); }}
.code-toolbar .btns {{ display: flex; gap: 6px; }}
.code-output {{ flex: 1; background: var(--code-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; overflow: auto; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: .85em; line-height: 1.5; white-space: pre-wrap; position: relative; }}
.code-output .kw {{ color: #ff7b72; }}
.code-output .str {{ color: #a5d6ff; }}
.code-output .cmt {{ color: #8b949e; font-style: italic; }}
.code-output .fn {{ color: #d2a8ff; }}
.code-output .num {{ color: #79c0ff; }}

/* Buttons */
.btn {{ padding: 6px 14px; border-radius: 6px; border: 1px solid var(--border); background: var(--surface); color: var(--text); cursor: pointer; font-size: .85em; display: inline-flex; align-items: center; gap: 6px; transition: all .15s; }}
.btn:hover {{ background: #21262d; }}
.btn.primary {{ background: #238636; border-color: #238636; color: #fff; }}
.btn.primary:hover {{ background: #2ea043; }}
.btn.accent {{ background: #1f6feb; border-color: #1f6feb; color: #fff; }}
.btn.accent:hover {{ background: #388bfd; }}
.btn.small {{ padding: 3px 10px; font-size: .78em; }}
.btn:disabled {{ opacity: .4; cursor: not-allowed; }}

/* Composed units list */
.units-list {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.unit-chip {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 3px 10px; font-size: .78em; display: flex; align-items: center; gap: 6px; }}
.unit-chip .remove {{ cursor: pointer; color: var(--text-dim); font-weight: bold; font-size: 1.1em; }}
.unit-chip .remove:hover {{ color: var(--danger); }}

/* Toast */
.toast {{ position: fixed; bottom: 20px; right: 20px; background: #238636; color: #fff; padding: 10px 20px; border-radius: 8px; font-size: .85em; z-index: 100; animation: fadeInOut 2.5s forwards; }}
@keyframes fadeInOut {{ 0% {{ opacity: 0; transform: translateY(10px); }} 10% {{ opacity: 1; transform: translateY(0); }} 80% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}

/* Mobile */
@media (max-width: 768px) {{
  .layout {{ flex-direction: column; }}
  .sidebar {{ width: 100%; max-height: 40vh; border-right: none; border-bottom: 1px solid var(--border); }}
  .form-grid {{ grid-template-columns: 1fr; }}
  .header .search {{ max-width: 200px; }}
  .header .stats {{ display: none; }}
}}

/* Empty state */
.empty {{ text-align: center; padding: 60px 20px; color: var(--text-dim); }}
.empty h3 {{ font-size: 1.2em; margin-bottom: 8px; color: var(--text); }}
.empty p {{ font-size: .9em; max-width: 400px; margin: 0 auto; }}

/* Highlight current mode */
.panel {{ display: none; }}
.panel.active {{ display: flex; flex-direction: column; gap: 16px; flex: 1; }}
.compose-panel {{ display: none; }}
.compose-panel.active {{ display: flex; flex-direction: column; gap: 16px; flex: 1; }}
</style>
</head>
<body>

<header class="header">
  <div class="logo">PyGen <span>v2</span></div>
  <div class="search"><input type="text" id="searchInput" placeholder="🔍 Cari template... (contoh: csv, http, json)" /></div>
  <div class="stats" id="statsBar">0 fungsi | 4 domain</div>
  <div class="actions">
    <button class="btn accent small" onclick="switchMode('wizard')" id="btnWizard">Wizard</button>
    <button class="btn small" onclick="switchMode('compose')" id="btnCompose">Compose (<span id="unitCount">0</span>)</button>
  </div>
</header>

<div class="layout">
  <nav class="sidebar" id="sidebar"></nav>

  <div class="main">
    <!-- Wizard panel -->
    <div class="panel active" id="wizardPanel">
      <div class="main-top">
        <div class="breadcrumb" id="breadcrumb"><span class="active">Pilih template dari sidebar</span></div>
        <div class="current-template" id="currentTitle"></div>
        <div class="current-template-desc" id="currentDesc"></div>
      </div>
      <div class="main-body" id="wizardBody">
        <div class="empty">
          <h3>👋 Selamat datang di PyGen Web UI</h3>
          <p>Pilih domain dan template dari sidebar kiri, atau gunakan search bar di atas untuk mencari template. Setiap template akan menampilkan form isian untuk menghasilkan kode Python siap pakai.</p>
        </div>
      </div>
    </div>

    <!-- Compose panel -->
    <div class="compose-panel" id="composePanel">
      <div class="main-top">
        <div style="font-weight:600;margin-bottom:4px">📦 Fungsi Terpilih</div>
        <div class="units-list" id="unitsList">
          <span style="color:var(--text-dim);font-size:.85em">Belum ada fungsi. Kembali ke tab Wizard dan tambahkan fungsi.</span>
        </div>
      </div>
      <div class="main-body">
        <div id="composeOutput" style="flex:1"></div>
      </div>
    </div>
  </div>
</div>

<!-- Toast -->
<div id="toast" class="toast" style="display:none"></div>

<script>
// ══════════════════════════════════════════════════════
// DATA
// ══════════════════════════════════════════════════════
const DOMAINS = {domains_js};
const TEMPLATES = {templates_js};

// ══════════════════════════════════════════════════════
// ENGINE (ported from Python)
// ══════════════════════════════════════════════════════
const PLACEHOLDER_RE = /\{{\{{(\\w+)\}}\}}/g;
const CONDITIONAL_RE = /\{{\{{#(\\w+)\}}\}}([\\s\\S]*?)\{{\{{\\/\\1\}}\}}/g;
const VALID_FIELD_TYPES = new Set(['identifier','text','int','list','choice','bool','multi_line','args','optional']);

function _isTruthy(val) {{
  if (val == null) return false;
  if (typeof val === 'string') return val.trim() !== '';
  if (typeof val === 'boolean') return val;
  if (Array.isArray(val)) return val.length > 0;
  return true;
}}

function coerceValue(field, rawValue) {{
  const ftype = field.type, name = field.name;
  switch (ftype) {{
    case 'identifier': {{
      const v = String(rawValue || '').trim();
      if (!v) throw new Error(`Field '${{name}}' tidak boleh kosong`);
      if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(v)) throw new Error(`Field '${{name}}' harus nama variabel Python valid, dapat: "${{v}}"`);
      return v;
    }}
    case 'text': return String(rawValue ?? '');
    case 'int': {{
      const n = parseInt(rawValue, 10);
      if (isNaN(n)) throw new Error(`Field '${{name}}' harus angka bulat, dapat: "${{rawValue}}"`);
      return String(n);
    }}
    case 'list': {{
      if (Array.isArray(rawValue)) return JSON.stringify(rawValue.map(String));
      const s = String(rawValue || '').trim();
      const items = s ? s.split(',').map(x => x.trim()).filter(Boolean) : [];
      return JSON.stringify(items);
    }}
    case 'choice': {{
      const opts = field.options || [];
      const v = String(rawValue || '').trim();
      if (opts.length > 0 && !opts.includes(v)) throw new Error(`Field '${{name}}' harus salah satu dari ${{JSON.stringify(opts)}}, dapat: "${{v}}"`);
      return v;
    }}
    case 'bool': {{
      if (typeof rawValue === 'boolean') return rawValue ? 'True' : 'False';
      const v = String(rawValue || '').trim().toLowerCase();
      if (['true','1','yes','y'].includes(v)) return 'True';
      return 'False';
    }}
    case 'multi_line': return String(rawValue ?? '');
    case 'args': return String(rawValue ?? '').trim();
    case 'optional': return String(rawValue ?? '').trim();
    default: throw new Error(`Tipe field tidak dikenal: ${{ftype}}`);
  }}
}}

function render(template, values) {{
  let code = template.code;
  const resolved = {{}}, rawResolved = {{}};
  for (const field of template.fields) {{
    const name = field.name;
    let raw = values[name] !== undefined ? values[name] : field.default;
    if (field.type === 'list' && !Array.isArray(raw) && typeof raw === 'string') {{
      raw = raw || field.default;
    }}
    rawResolved[name] = raw;
    resolved[name] = coerceValue(field, raw);
  }}

  // Conditional blocks
  code = code.replace(CONDITIONAL_RE, (match, key, body) => {{
    if (!_isTruthy(rawResolved[key])) return '';
    return body.replace(PLACEHOLDER_RE, (m, k) => resolved[k] !== undefined ? resolved[k] : m);
  }});

  // Placeholder substitution
  code = code.replace(PLACEHOLDER_RE, (match, key) => {{
    if (!(key in resolved)) throw new Error(`Placeholder {{{{'${{key}}'}}}} tidak punya definisi field`);
    return resolved[key];
  }});

  return code;
}}

function compose(units) {{
  if (!units.length) return '';
  const allImports = new Set();
  const allPackages = new Set();
  for (const u of units) {{
    (u.imports || []).forEach(i => allImports.add(i));
    const req = u.requires || {{}};
    (req.packages || []).forEach(p => allPackages.add(p));
  }}

  const header = `"""\\nFile ini dihasilkan otomatis oleh PyGen Web UI.\\nDibuat: ${{new Date().toISOString().slice(0, 19).replace('T', ' ')}}\\nJumlah fungsi/komponen: ${{units.length}}\\n\\nPyGen adalah generator kode deterministik berbasis template —\\nTIDAK ada AI/LLM yang terlibat dalam pembuatan kode ini.\\n"""\\n`;
  const reqHeader = allPackages.size ? `# Requirements:\\n# pip install ${{[...allPackages].sort().join(' ')}}\\n\\n` : '';
  const importBlock = allImports.size ? [...allImports].sort().map(i => `import ${{i}}`).join('\\n') + '\\n\\n' : '';

  const blocks = units.map(u => {{
    let info = `# --- ${{u.title}} (template: ${{u.id}})\\n`;
    if (u.requires && u.requires.packages && u.requires.packages.length) {{
      info += `#     requires: ${{u.requires.packages.join(', ')}}\\n`;
    }}
    return info + `\\n${{u.code.trim()}}\\n`;
  }});

  return (header + reqHeader + importBlock + blocks.join('\\n')).trim() + '\\n';
}}

// ══════════════════════════════════════════════════════
// STATE
// ══════════════════════════════════════════════════════
let state = {{
  currentTemplate: null,
  units: [], // {{id, title, imports, code, requires}}
  mode: 'wizard', // 'wizard' | 'compose'
  activeDomain: null,
  renderedCode: '',
}};

// ══════════════════════════════════════════════════════
// RENDER SIDEBAR
// ══════════════════════════════════════════════════════
function buildSidebar(filter = '') {{
  const sidebar = document.getElementById('sidebar');
  const q = filter.toLowerCase().trim();

  // Filter templates
  const matchingIds = new Set();
  if (q) {{
    TEMPLATES.forEach(t => {{
      if (t.id.toLowerCase().includes(q) || t.title.toLowerCase().includes(q) || (t.description||'').toLowerCase().includes(q)) {{
        matchingIds.add(t.id);
      }}
    }});
  }}

  let html = '';
  for (const dm of DOMAINS) {{
    const domainTmpls = TEMPLATES.filter(t => t._domain === dm.key);
    if (!domainTmpls.length) continue;

    // Group by category
    const cats = {{}};
    for (const t of domainTmpls) {{
      const ck = t._category_key;
      if (!cats[ck]) cats[ck] = {{ label: t._category, items: [] }};
      cats[ck].items.push(t);
    }}

    // Check if any template in this domain matches filter
    let domainMatch = !q;
    if (q) {{
      domainMatch = domainTmpls.some(t => matchingIds.has(t.id));
    }}
    if (q && !domainMatch) continue;

    const isOpen = !q ? (state.activeDomain === dm.key) : true;
    html += `<div class="domain-group">
      <div class="domain-header ${{isOpen ? 'open' : ''}}" data-domain="${{dm.key}}" onclick="toggleDomain(this)">
        <span class="arrow">▶</span> ${{dm.label}} <span style="font-size:.7em;color:var(--text-dim)">(${{domainTmpls.length}})</span>
      </div>
      <div class="domain-items">`;

    for (const [ck, cat] of Object.entries(cats)) {{
      const matchItems = q ? cat.items.filter(t => matchingIds.has(t.id)) : cat.items;
      if (!matchItems.length) continue;
      html += `<div class="cat-header">${{cat.label}}</div>`;
      for (const t of matchItems) {{
        const active = state.currentTemplate && state.currentTemplate.id === t.id ? ' active' : '';
        const dmBadge = `<span style="color:var(--accent3);font-size:.7em">[${{dm.key}}]</span> `;
        html += `<div class="tpl-item${{active}}" data-id="${{t.id}}" onclick="selectTemplate('${{t.id}}')" title="${{t.title}}">${{q ? dmBadge : ''}}${{t.title}}</div>`;
      }}
    }}
    html += `</div></div>`;
  }}

  if (!html.trim()) {{
    html = '<div class="empty" style="padding:20px"><p>Tidak ada template yang cocok.</p></div>';
  }}

  sidebar.innerHTML = html;
}}

// ══════════════════════════════════════════════════════
// DOMAIN TOGGLE
// ══════════════════════════════════════════════════════
function toggleDomain(el) {{
  el.classList.toggle('open');
  state.activeDomain = el.dataset.domain;
}}

// ══════════════════════════════════════════════════════
// TEMPLATE SELECTION
// ══════════════════════════════════════════════════════
function selectTemplate(id) {{
  const tpl = TEMPLATES.find(t => t.id === id);
  if (!tpl) return;
  state.currentTemplate = tpl;
  state.renderedCode = '';
  renderWizard(tpl);
  buildSidebar(document.getElementById('searchInput').value);
  switchMode('wizard');
  document.getElementById('wizardBody').scrollIntoView({{ behavior: 'smooth' }});
}}

function renderWizard(tpl) {{
  // Breadcrumb
  document.getElementById('breadcrumb').innerHTML = `
    <span>${{DOMAINS.find(d => d.key === tpl._domain)?.label || tpl._domain}}</span>
    <span class="sep">▸</span>
    <span>${{tpl._category}}</span>
    <span class="sep">▸</span>
    <span class="active">${{tpl.title}}</span>
  `;
  document.getElementById('currentTitle').textContent = tpl.title;
  document.getElementById('currentDesc').textContent = tpl.description || '';

  // Form
  let formHtml = '<div class="form-grid">';
  for (const field of tpl.fields) {{
    const fn = field.name, fl = field.label, ft = field.type;
    const defVal = field.default !== undefined ? field.default : '';
    const typeBadge = `<span class="type-badge">${{ft}}</span>`;
    const isWide = ['multi_line', 'args', 'optional'].includes(ft);

    let input;
    if (ft === 'choice') {{
      const opts = field.options || [];
      input = `<select id="field_${{fn}}" data-type="${{ft}}" data-name="${{fn}}">
        ${{opts.map(o => `<option value="${{o}}"${{o === defVal ? ' selected' : ''}}>${{o}}</option>`).join('')}}
      </select>`;
    }} else if (ft === 'bool') {{
      input = `<select id="field_${{fn}}" data-type="${{ft}}" data-name="${{fn}}">
        <option value="false"${{defVal === false || defVal === 'false' ? ' selected' : ''}}>False</option>
        <option value="true"${{defVal === true || defVal === 'true' ? ' selected' : ''}}>True</option>
      </select>`;
    }} else if (ft === 'multi_line') {{
      const dv = Array.isArray(defVal) ? defVal.join('\\n') : defVal;
      input = `<textarea id="field_${{fn}}" data-type="${{ft}}" data-name="${{fn}}" rows="4" placeholder="Masukkan teks...">${{dv}}</textarea>`;
    }} else if (ft === 'list') {{
      const dv = Array.isArray(defVal) ? defVal.join(', ') : defVal;
      input = `<input id="field_${{fn}}" data-type="${{ft}}" data-name="${{fn}}" value="${{dv}}" placeholder="pisahkan dengan koma">`;
    }} else {{
      input = `<input id="field_${{fn}}" data-type="${{ft}}" data-name="${{fn}}" value="${{defVal}}">`;
    }}

    formHtml += `<div class="form-group${{isWide ? ' full' : ''}}">
      <label>${{fl}}${{typeBadge}}</label>
      ${{input}}
      <div class="error-msg" id="err_${{fn}}"></div>
    </div>`;
  }}
  formHtml += '</div>';

  // Action buttons
  formHtml += `
    <div style="display:flex;gap:8px;margin-top:12px;align-items:center">
      <button class="btn primary" onclick="generateCode()">⚡ Generate</button>
      <button class="btn" onclick="generateAndAddUnit()">➕ Generate & Tambah ke Compose</button>
      <button class="btn" onclick="fillDefaults()">↺ Reset ke Default</button>
    </div>`;

  const wizardBody = document.getElementById('wizardBody');
  wizardBody.innerHTML = formHtml + `
    <div class="code-section" id="codeSection" style="display:none">
      <div class="code-toolbar">
        <span class="label">✨ Kode Dihasilkan</span>
        <div class="btns">
          <button class="btn" onclick="copyCode()">📋 Copy</button>
          <button class="btn accent" onclick="downloadCode()">💾 Download .py</button>
          <button class="btn" onclick="clearCode()">✕ Tutup</button>
        </div>
      </div>
      <div class="code-output" id="codeOutput"></div>
    </div>`;
}}

// ══════════════════════════════════════════════════════
// CODE GENERATION
// ══════════════════════════════════════════════════════
function collectValues() {{
  const tpl = state.currentTemplate;
  if (!tpl) return null;
  const values = {{}};
  let hasError = false;
  for (const field of tpl.fields) {{
    const el = document.getElementById('field_' + field.name);
    if (!el) continue;
    const raw = el.value;
    // Clear error
    el.classList.remove('error');
    const errEl = document.getElementById('err_' + field.name);
    if (errEl) errEl.textContent = '';

    try {{
      coerceValue(field, raw);
    }} catch (e) {{
      el.classList.add('error');
      if (errEl) errEl.textContent = e.message;
      hasError = true;
    }}
    values[field.name] = raw;
  }}
  if (hasError) return null;
  return values;
}}

function generateCode() {{
  const values = collectValues();
  if (!values) return;

  const tpl = state.currentTemplate;
  let code;
  try {{
    code = render(tpl, values);
  }} catch (e) {{
    showToast('❌ Error: ' + e.message, true);
    return;
  }}

  state.renderedCode = code;
  document.getElementById('codeSection').style.display = 'flex';
  document.getElementById('codeOutput').innerHTML = syntaxHighlight(code);
  document.getElementById('codeOutput').parentElement.scrollIntoView({{ behavior: 'smooth' }});
}}

function generateAndAddUnit() {{
  const values = collectValues();
  if (!values) return;

  const tpl = state.currentTemplate;
  let code;
  try {{
    code = render(tpl, values);
  }} catch (e) {{
    showToast('❌ Error: ' + e.message, true);
    return;
  }}

  state.units.push({{
    id: tpl.id,
    title: tpl.title,
    imports: tpl.imports || [],
    code: code,
    requires: tpl.requires || {{}},
  }});

  state.renderedCode = code;
  document.getElementById('codeSection').style.display = 'flex';
  document.getElementById('codeOutput').innerHTML = syntaxHighlight(code);
  updateUnitsUI();
  showToast('✅ Ditambahkan ke Compose (' + state.units.length + ' fungsi)');
}}

function clearCode() {{
  document.getElementById('codeSection').style.display = 'none';
  state.renderedCode = '';
}}

// ══════════════════════════════════════════════════════
// COMPOSE
// ══════════════════════════════════════════════════════
function updateUnitsUI() {{
  document.getElementById('unitCount').textContent = state.units.length;
  const list = document.getElementById('unitsList');
  if (!state.units.length) {{
    list.innerHTML = '<span style="color:var(--text-dim);font-size:.85em">Belum ada fungsi. Kembali ke tab Wizard dan tambahkan fungsi.</span>';
  }} else {{
    list.innerHTML = state.units.map((u, i) => `
      <span class="unit-chip">
        <span style="color:var(--accent2)">#${{i+1}}</span> ${{u.title}}
        <span class="remove" onclick="removeUnit(${{i}})" title="Hapus">×</span>
      </span>`).join('');
  }}
  updateComposePanel();
}}

function removeUnit(idx) {{
  state.units.splice(idx, 1);
  updateUnitsUI();
}}

function updateComposePanel() {{
  const out = document.getElementById('composeOutput');
  if (!state.units.length) {{
    out.innerHTML = '<div class="empty"><h3>📦 Belum ada fungsi</h3><p>Klik tab Wizard, pilih template, lalu klik "Generate & Tambah ke Compose" untuk menambahkan fungsi.</p></div>';
    return;
  }}
  try {{
    const final = compose(state.units);
    out.innerHTML = `
      <div class="code-toolbar">
        <span class="label">✨ ${{state.units.length}} fungsi dirangkai (siap diimpor/dijalankan)</span>
        <div class="btns">
          <button class="btn" onclick="copyCompose()">📋 Copy</button>
          <button class="btn accent" onclick="downloadCompose()">💾 Download .py</button>
          <button class="btn" onclick="state.units=[];updateUnitsUI();">🗑 Clear All</button>
        </div>
      </div>
      <div class="code-output">${{syntaxHighlight(final)}}</div>`;
  }} catch (e) {{
    out.innerHTML = `<div class="empty"><p style="color:var(--danger)">❌ Error: ${{e.message}}</p></div>`;
  }}
}}

function switchMode(mode) {{
  state.mode = mode;
  document.getElementById('wizardPanel').classList.toggle('active', mode === 'wizard');
  document.getElementById('composePanel').classList.toggle('active', mode === 'compose');
  document.getElementById('btnWizard').classList.toggle('accent', mode === 'wizard');
  document.getElementById('btnCompose').classList.toggle('accent', mode === 'compose');
  if (mode === 'compose') updateComposePanel();
}}

// ══════════════════════════════════════════════════════
// COPY / DOWNLOAD
// ══════════════════════════════════════════════════════
function copyCode() {{
  copyToClipboard(state.renderedCode);
}}

function downloadCode() {{
  const fn = (state.currentTemplate?.id || 'function') + '.py';
  downloadFile(fn, state.renderedCode);
}}

function copyCompose() {{
  try {{
    copyToClipboard(compose(state.units));
  }} catch(e) {{ showToast('❌ Error: ' + e.message, true); }}
}}

function downloadCompose() {{
  try {{
    downloadFile('generated_functions.py', compose(state.units));
  }} catch(e) {{ showToast('❌ Error: ' + e.message, true); }}
}}

function copyToClipboard(text) {{
  navigator.clipboard.writeText(text).then(() => showToast('📋 Disalin ke clipboard!')).catch(() => showToast('❌ Gagal menyalin', true));
}}

function downloadFile(filename, content) {{
  const blob = new Blob([content], {{ type: 'text/x-python' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
  showToast('💾 Diunduh: ' + filename);
}}

// ══════════════════════════════════════════════════════
// SYNTAX HIGHLIGHT (simple regex-based)
// ══════════════════════════════════════════════════════
function syntaxHighlight(code) {{
  // Escape HTML
  let esc = code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  // Keywords
  esc = esc.replace(/\\b(def|class|import|from|return|if|else|elif|for|while|try|except|raise|with|as|in|not|and|or|is|None|True|False|yield|pass|break|continue|lambda|async|await|self)\\b/g, '<span class="kw">$1</span>');
  // Strings (triple, single, f-strings)
  esc = esc.replace(/(f?"""[\\s\\S]*?""")/g, '<span class="str">$1</span>');
  esc = esc.replace(/(f?"[^"]*")/g, '<span class="str">$1</span>');
  esc = esc.replace(/(f?'[^']*')/g, '<span class="str">$1</span>');
  // Comments
  esc = esc.replace(/(#.*)/g, '<span class="cmt">$1</span>');
  // Numbers
  esc = esc.replace(/\\b(\\d+\\.?\\d*)\\b/g, '<span class="num">$1</span>');
  // Function calls
  esc = esc.replace(/\\b([a-zA-Z_]\\w*)(?=\\()/g, '<span class="fn">$1</span>');
  return esc;
}}

// ══════════════════════════════════════════════════════
// HELPERS
// ══════════════════════════════════════════════════════
function fillDefaults() {{
  const tpl = state.currentTemplate;
  if (!tpl) return;
  for (const field of tpl.fields) {{
    const el = document.getElementById('field_' + field.name);
    if (!el) continue;
    const def = field.default;
    if (field.type === 'list' && Array.isArray(def)) el.value = def.join(', ');
    else if (field.type === 'bool') el.value = def === true || def === 'true' ? 'true' : 'false';
    else el.value = def !== undefined ? def : '';
    el.classList.remove('error');
    const errEl = document.getElementById('err_' + field.name);
    if (errEl) errEl.textContent = '';
  }}
  showToast('↺ Field di-reset ke default');
}}

function showToast(msg, isError) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.background = isError ? '#f85149' : '#238636';
  t.style.display = 'block';
  t.style.animation = 'none';
  t.offsetHeight;
  t.style.animation = 'fadeInOut 2.5s forwards';
  setTimeout(() => t.style.display = 'none', 2500);
}}

function updateStats() {{
  document.getElementById('statsBar').textContent = `${{TEMPLATES.length}} template | ${{DOMAINS.length}} domain`;
}}

// ══════════════════════════════════════════════════════
// SEARCH
// ══════════════════════════════════════════════════════
document.getElementById('searchInput').addEventListener('input', function(e) {{
  const q = e.target.value;
  if (q.length >= 2 || q.length === 0) {{
    buildSidebar(q);
    if (q && TEMPLATES.length) {{
      const hits = TEMPLATES.filter(t =>
        t.id.toLowerCase().includes(q.toLowerCase()) ||
        t.title.toLowerCase().includes(q.toLowerCase())
      );
      if (hits.length > 0 && hits.length <= 5 && hits[0].id) {{
        // Don't auto-select, just filter
      }}
    }}
  }}
}});

// ══════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════
function init() {{
  updateStats();
  buildSidebar();
  updateUnitsUI();

  // Keyboard shortcut: Ctrl+Enter to generate
  document.addEventListener('keydown', function(e) {{
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {{
      e.preventDefault();
      generateCode();
    }}
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
      e.preventDefault();
      document.getElementById('searchInput').focus();
    }}
  }});
}}

init();
</script>
</body>
</html>'''

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'✅ Written {len(html):,} bytes → {OUTPUT}')
