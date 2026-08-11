const API_BASE = ""; // same origin — FastAPI serves this file too

const runBtn = document.getElementById("run-btn");
const scopeInput = document.getElementById("scope-input");
const scopeRunBtn = document.getElementById("scope-run-btn");
const scopeBanner = document.getElementById("scope-banner");
const scopeBannerText = document.getElementById("scope-banner-text");
const scopeClearBtn = document.getElementById("scope-clear-btn");

const hero = document.getElementById("hero");
const heroRunBtn = document.getElementById("hero-run-btn");
const heroScopeInput = document.getElementById("hero-scope-input");
const heroScopeRunBtn = document.getElementById("hero-scope-run-btn");
const heroError = document.getElementById("hero-error");

const emptyState = document.getElementById("empty-state");
const loading = document.getElementById("loading");
const loadingText = document.getElementById("loading-text");
const report = document.getElementById("report");

const searchInput = document.getElementById("search-input");
const severityFilters = document.getElementById("severity-filters");
const showPassedCheckbox = document.getElementById("show-passed");
const paginationEl = document.getElementById("pagination");

const recSearchInput = document.getElementById("rec-search-input");
const recSeverityFilters = document.getElementById("rec-severity-filters");

const SEVERITY_COLOR = {
  CRITICAL: "var(--critical)",
  HIGH: "var(--high)",
  MEDIUM: "var(--medium)",
  LOW: "var(--low)",
};

const PAGE_SIZE = 25;

// Results table state
let allResults = [];
let activeSeverity = "ALL";
let searchTerm = "";
let showPassed = false;
let currentPage = 1;

// Recommendations state
let allGroups = [];
let recSearchTerm = "";
let recActiveSeverity = "ALL";

// Landing vs app-mode: before the first successful run, the hero
// panel is the primary UI and the compact top-bar controls stay
// hidden. Once a run succeeds, the hero is retired for the session
// and the top controls (already in the DOM) take over — matches
// "both bars should exist on top" once validation has been applied.
let hasEverSucceeded = false;

// --- top bar controls ---
runBtn.addEventListener("click", () => runValidation(null, { fromHero: false }));
scopeRunBtn.addEventListener("click", () => runValidation(parseScopeValue(scopeInput.value), { fromHero: false }));
scopeInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runValidation(parseScopeValue(scopeInput.value), { fromHero: false });
});
scopeClearBtn.addEventListener("click", () => {
  scopeInput.value = "";
  runValidation(null, { fromHero: false });
});

// --- hero controls ---
heroRunBtn.addEventListener("click", () => runValidation(null, { fromHero: true }));
heroScopeRunBtn.addEventListener("click", () => runValidation(parseScopeValue(heroScopeInput.value), { fromHero: true }));
heroScopeInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runValidation(parseScopeValue(heroScopeInput.value), { fromHero: true });
});

// --- results table controls ---
searchInput.addEventListener("input", (e) => {
  searchTerm = e.target.value.trim().toLowerCase();
  currentPage = 1;
  renderResultsTable();
});
showPassedCheckbox.addEventListener("change", (e) => {
  showPassed = e.target.checked;
  currentPage = 1;
  renderResultsTable();
});
severityFilters.addEventListener("click", (e) => {
  const btn = e.target.closest(".sev-chip");
  if (!btn) return;
  setActiveChip(severityFilters, btn);
  activeSeverity = btn.dataset.sev;
  currentPage = 1;
  renderResultsTable();
});

// --- recommendation controls ---
recSearchInput.addEventListener("input", (e) => {
  recSearchTerm = e.target.value.trim().toLowerCase();
  renderRecommendationGroups();
});
recSeverityFilters.addEventListener("click", (e) => {
  const btn = e.target.closest(".sev-chip");
  if (!btn) return;
  setActiveChip(recSeverityFilters, btn);
  recActiveSeverity = btn.dataset.sev;
  renderRecommendationGroups();
});

function setActiveChip(container, activeBtn) {
  container.querySelectorAll(".sev-chip").forEach((b) => b.classList.remove("active"));
  activeBtn.classList.add("active");
}

function parseScopeValue(raw) {
  raw = (raw || "").trim();
  if (!raw) return null;
  return raw.split(/[,\s]+/).map((s) => s.trim()).filter(Boolean);
}

async function runValidation(poNumbers, { fromHero }) {
  const buttons = [runBtn, scopeRunBtn, heroRunBtn, heroScopeRunBtn];
  buttons.forEach((b) => (b.disabled = true));
  heroError.classList.add("hidden");
  scopeBanner.classList.add("hidden");
  report.classList.add("hidden");
  emptyState.classList.add("hidden");

  if (fromHero) {
    hero.classList.add("hidden");
  }

  loadingText.textContent = poNumbers
    ? `Validating ${poNumbers.length} selected PO(s)…`
    : "Running validations and generating AI recommendations…";
  loading.classList.remove("hidden");

  try {
    let url = `${API_BASE}/api/report/procurement`;
    if (poNumbers && poNumbers.length) {
      url += `?po_numbers=${encodeURIComponent(poNumbers.join(","))}`;
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    const data = await res.json();

    loading.classList.add("hidden");

    if (!hasEverSucceeded) {
      hasEverSucceeded = true;
      enterAppMode();
    }

    // Keep the scope input in the top bar in sync with whatever was
    // just run, so a rerun/edit starts from the current scope.
    scopeInput.value = poNumbers ? poNumbers.join(", ") : "";

    renderReport(data);

  } catch (err) {
    loading.classList.add("hidden");

    if (fromHero && !hasEverSucceeded) {
      // Still on the landing screen — show the error inline in the
      // hero panel and bring the hero back so the user can retry.
      hero.classList.remove("hidden");
      heroError.textContent = `Could not run validation: ${err.message}. Check that the backend is running and DATABASE_URL is set.`;
      heroError.classList.remove("hidden");
    } else {
      emptyState.classList.remove("hidden");
      emptyState.querySelector("p").textContent =
        `Could not generate the report: ${err.message}. Check that the backend is running and DATABASE_URL is set.`;
    }
  } finally {
    buttons.forEach((b) => (b.disabled = false));
  }
}

function enterAppMode() {
  hero.classList.add("hidden");
  document.querySelectorAll(".top-control").forEach((el) => el.classList.remove("hidden"));
}

function renderReport(data) {
  report.classList.remove("hidden");

  if (data.scope === "SELECTED") {
    let text = `Scoped run — validating: <strong>${data.scoped_pos.join(", ")}</strong>`;
    if (data.scoped_pos_not_found.length) {
      text += ` <span style="color:var(--critical)">(not found: ${data.scoped_pos_not_found.join(", ")})</span>`;
    }
    scopeBannerText.innerHTML = text;
    scopeBanner.classList.remove("hidden");
  } else {
    scopeBanner.classList.add("hidden");
  }

  allResults = data.results;
  activeSeverity = "ALL";
  searchTerm = "";
  showPassed = false;
  currentPage = 1;
  searchInput.value = "";
  showPassedCheckbox.checked = false;
  resetChips(severityFilters);

  allGroups = data.recommendation_groups;
  recSearchTerm = "";
  recActiveSeverity = "ALL";
  recSearchInput.value = "";
  resetChips(recSeverityFilters);

  renderMetrics(data);
  renderSummary(data);
  renderRiskChart(data.risk_distribution);
  renderRecommendationGroups();
  renderResultsTable();
}

function resetChips(container) {
  container.querySelectorAll(".sev-chip").forEach((b) => b.classList.remove("active"));
  container.querySelector('[data-sev="ALL"]').classList.add("active");
}

function renderMetrics(data) {
  const m = data.metrics;

  const cells = [
    ["Purchase Requisitions", m.purchase_requisitions, m.purchase_requisitions],
    ["Purchase Orders", m.purchase_orders, m.purchase_orders],
    ["Goods Receipts", m.goods_receipts, m.goods_receipts],
    ["Invoices", m.invoices, m.invoices],
    ["Total Spend", formatCurrencyCompact(m.total_spend), formatCurrencyFull(m.total_spend)],
    ["Vendors Approved", `${m.approved_vendors}/${m.total_vendors}`, `${m.approved_vendors} of ${m.total_vendors} approved`],
  ];

  const grid = document.getElementById("metrics-grid");
  grid.innerHTML = cells
    .map(
      ([label, value, title]) => `
      <div class="metric-cell">
        <div class="metric-value" title="${escapeHtml(String(title))}">${value}</div>
        <div class="metric-label">${label}</div>
      </div>`
    )
    .join("");
}

function renderSummary(data) {
  document.getElementById("executive-summary").textContent = data.executive_summary;
  document.getElementById("stat-total").textContent = data.total_checks;
  document.getElementById("stat-passed").textContent = data.passed_checks;
  document.getElementById("stat-failed").textContent = data.failed_checks;
}

function renderRiskChart(distribution) {
  const chart = document.getElementById("risk-chart");
  const legend = document.getElementById("risk-legend");

  if (!distribution.length) {
    chart.style.background = "var(--pass)";
    legend.innerHTML = `<li><span class="swatch" style="background:var(--pass)"></span> No failures <span class="count">0</span></li>`;
    return;
  }

  const total = distribution.reduce((sum, d) => sum + d.count, 0);
  let acc = 0;
  const stops = [];

  distribution.forEach((d) => {
    const color = SEVERITY_COLOR[d.severity] || "var(--text-muted)";
    const start = (acc / total) * 100;
    acc += d.count;
    const end = (acc / total) * 100;
    stops.push(`${color} ${start}% ${end}%`);
  });

  chart.style.background = `conic-gradient(${stops.join(", ")})`;

  legend.innerHTML = distribution
    .map(
      (d) => `
      <li>
        <span class="swatch" style="background:${SEVERITY_COLOR[d.severity] || "var(--text-muted)"}"></span>
        ${d.severity}
        <span class="count">${d.count}</span>
      </li>`
    )
    .join("");
}

function getFilteredGroups() {
  return allGroups.filter((g) => {
    if (recActiveSeverity !== "ALL" && g.severity !== recActiveSeverity) return false;
    if (recSearchTerm) {
      const haystack = `${g.group_label} ${g.recommendation} ${g.rule_name}`.toLowerCase();
      if (!haystack.includes(recSearchTerm)) return false;
    }
    return true;
  });
}

function renderRecommendationGroups() {
  const container = document.getElementById("recommendations");
  const countLabel = document.getElementById("rec-group-count");
  const filtered = getFilteredGroups();

  if (!allGroups.length) {
    countLabel.textContent = "";
    container.innerHTML = `<p class="no-issues">✓ No issues found — every check passed.</p>`;
    return;
  }

  countLabel.textContent = `${filtered.length} of ${allGroups.length} pattern(s) shown`;

  container.innerHTML = filtered.length
    ? filtered
        .map((g) => {
          const extra = g.count - g.sample_entities.length;
          return `
      <div class="rec-card ${g.severity.toLowerCase()}">
        <div class="rec-head">
          <span class="rec-title">${escapeHtml(g.group_label)}</span>
          <span class="rec-severity">${g.severity}</span>
          <span class="rec-count">${g.count} record${g.count === 1 ? "" : "s"}</span>
        </div>
        <div class="rec-text">${escapeHtml(g.recommendation)}</div>
        <details class="rec-entities">
          <summary>View affected records</summary>
          <div class="entity-chips">
            ${g.sample_entities.map((e) => `<span class="entity-chip">${escapeHtml(e)}</span>`).join("")}
            ${extra > 0 ? `<span class="entity-chip more">+${extra} more</span>` : ""}
          </div>
        </details>
      </div>`;
        })
        .join("")
    : `<p class="no-issues" style="color:var(--text-muted)">No recommendations match the current filters.</p>`;
}

function getFilteredResults() {
  return allResults.filter((r) => {
    if (!showPassed && r.passed) return false;
    if (activeSeverity !== "ALL" && r.severity !== activeSeverity) return false;
    if (searchTerm) {
      const haystack = `${r.rule_name} ${r.entity} ${r.message}`.toLowerCase();
      if (!haystack.includes(searchTerm)) return false;
    }
    return true;
  });
}

function renderResultsTable() {
  const filtered = getFilteredResults();
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  currentPage = Math.min(currentPage, totalPages);

  const start = (currentPage - 1) * PAGE_SIZE;
  const pageItems = filtered.slice(start, start + PAGE_SIZE);

  document.getElementById("results-count").textContent =
    `${filtered.length} of ${allResults.length} shown`;

  const body = document.getElementById("results-body");
  body.innerHTML = pageItems.length
    ? pageItems
        .map(
          (r) => `
      <tr>
        <td><span class="status-dot ${r.passed ? "pass" : "fail"}"></span></td>
        <td class="rule-cell">${escapeHtml(r.rule_name)}</td>
        <td class="entity-cell">${escapeHtml(r.entity)}</td>
        <td><span class="severity-tag ${r.severity.toLowerCase()}">${r.severity}</span></td>
        <td>${escapeHtml(r.message)}</td>
      </tr>`
        )
        .join("")
    : `<tr><td colspan="5" class="empty-row">No results match the current filters.</td></tr>`;

  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  if (totalPages <= 1) {
    paginationEl.innerHTML = "";
    return;
  }

  const buttons = [];
  buttons.push(
    `<button class="page-btn" data-page="${currentPage - 1}" ${currentPage === 1 ? "disabled" : ""}>‹ Prev</button>`
  );
  buttons.push(`<span class="page-status">Page ${currentPage} of ${totalPages}</span>`);
  buttons.push(
    `<button class="page-btn" data-page="${currentPage + 1}" ${currentPage === totalPages ? "disabled" : ""}>Next ›</button>`
  );

  paginationEl.innerHTML = buttons.join("");
  paginationEl.querySelectorAll(".page-btn:not([disabled])").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentPage = parseInt(btn.dataset.page, 10);
      renderResultsTable();
      document.querySelector(".table-controls").scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });
}

function formatCurrencyCompact(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

function formatCurrencyFull(value) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

// ============================================================
// Module switching (Procurement <-> ABAP)
// ============================================================

const moduleNav = document.querySelector(".module-nav");
const abapWorkspace = document.getElementById("abap-workspace");
const ruleWorkspace = document.getElementById("rule-workspace");
const inventoryWorkspace = document.getElementById("inventory-workspace");
const homeWorkspace = document.getElementById("home-workspace");
let currentModule = "home";

const WORKSPACES = {
  home: homeWorkspace,
  abap: abapWorkspace,
  rules: ruleWorkspace,
  inventory: inventoryWorkspace,
};

moduleNav.addEventListener("click", (e) => {
  const btn = e.target.closest(".module-btn");
  if (!btn || btn.disabled) return;
  switchModule(btn.dataset.module);
});

function switchModule(module) {
  currentModule = module;

  document.querySelectorAll(".module-btn[data-module]").forEach((b) => {
    b.classList.toggle("active", b.dataset.module === module);
  });

  Object.values(WORKSPACES).forEach((ws) => ws && ws.classList.add("hidden"));

  if (module in WORKSPACES) {
    hero.classList.add("hidden");
    report.classList.add("hidden");
    emptyState.classList.add("hidden");
    scopeBanner.classList.add("hidden");
    loading.classList.add("hidden");
    document.querySelectorAll(".top-control").forEach((el) => el.classList.add("hidden"));
    WORKSPACES[module].classList.remove("hidden");
  } else {
    if (hasEverSucceeded) {
      document.querySelectorAll(".top-control").forEach((el) => el.classList.remove("hidden"));
      report.classList.remove("hidden");
    } else {
      hero.classList.remove("hidden");
    }
  }
}

// ============================================================
// ABAP Copilot
// ============================================================

const abapCodeInput = document.getElementById("abap-code-input");
const abapModeSelect = document.getElementById("abap-mode-select");
const abapTargetSelect = document.getElementById("abap-target-select");
const abapAnalyzeBtn = document.getElementById("abap-analyze-btn");
const abapError = document.getElementById("abap-error");
const abapEmpty = document.getElementById("abap-empty");
const abapLoading = document.getElementById("abap-loading");
const abapResults = document.getElementById("abap-results");

let abapMode = "review";

abapModeSelect.addEventListener("click", (e) => {
  const btn = e.target.closest(".mode-chip");
  if (!btn) return;
  abapModeSelect.querySelectorAll(".mode-chip").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  abapMode = btn.dataset.mode;
  abapTargetSelect.classList.toggle("hidden", abapMode !== "convert");
});

abapAnalyzeBtn.addEventListener("click", runAbapAnalysis);

async function runAbapAnalysis() {
  const code = abapCodeInput.value.trim();

  if (!code) {
    abapError.textContent = "Paste some ABAP code first.";
    abapError.classList.remove("hidden");
    return;
  }

  abapError.classList.add("hidden");
  abapEmpty.classList.add("hidden");
  abapResults.classList.add("hidden");
  abapLoading.classList.remove("hidden");
  abapAnalyzeBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/api/abap/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        mode: abapMode,
        target: abapMode === "convert" ? abapTargetSelect.value : null,
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Server returned ${res.status}`);
    }

    const data = await res.json();
    renderAbapResults(data);

  } catch (err) {
    abapLoading.classList.add("hidden");
    abapEmpty.classList.remove("hidden");
    abapError.textContent = `Analysis failed: ${err.message}`;
    abapError.classList.remove("hidden");
  } finally {
    abapAnalyzeBtn.disabled = false;
  }
}

function renderAbapResults(data) {
  abapLoading.classList.add("hidden");
  abapResults.classList.remove("hidden");

  let html = `<div class="abap-summary">${escapeHtml(data.summary)}</div>`;

  if (data.score) {
    html += renderAbapScore(data.score);
  }

  if (data.issues && data.issues.length) {
    html += `<div class="abap-issues-title">${data.issues.length} issue(s) found</div>`;
    html += `<div class="recommendations">` + data.issues.map((issue) => `
      <div class="rec-card ${issue.severity.toLowerCase()}">
        <div class="rec-head">
          <span class="rec-title">${escapeHtml(issue.title)}</span>
          <span class="rec-severity">${issue.severity}</span>
        </div>
        <div class="rec-text">${escapeHtml(issue.description)}</div>
      </div>`).join("") + `</div>`;
  }

  if (data.optimized_code) {
    html += renderCodeBlock("Optimized Code", data.optimized_code, "abap-optimized-code");
  }

  if (data.converted_code) {
    html += renderCodeBlock("Converted Code", data.converted_code, "abap-converted-code");
  }

  if (data.documentation) {
    html += renderAbapDocumentation(data.documentation);
  }

  abapResults.innerHTML = html;

  attachCopyHandlers(abapResults);
}

function renderAbapScore(score) {
  const cells = [
    ["Performance", score.performance],
    ["Readability", score.readability],
    ["Security", score.security],
    ["Complexity", score.complexity],
  ];

  return `<div class="abap-score-grid">` + cells.map(([label, value]) => {
    const cls = value >= 75 ? "good" : value >= 50 ? "ok" : "poor";
    return `
      <div class="abap-score-cell">
        <div class="abap-score-value ${cls}">${value}</div>
        <div class="abap-score-label">${label}</div>
      </div>`;
  }).join("") + `</div>`;
}

function renderCodeBlock(title, code, id) {
  return `
    <div class="abap-doc-section">
      <h3>${title}</h3>
      <div class="abap-code-block">
        <button class="copy-btn" data-target="${id}">Copy</button>
        <pre id="${id}">${escapeHtml(code)}</pre>
      </div>
    </div>`;
}

function renderAbapDocumentation(doc) {
  let html = "";

  if (doc.business_logic) {
    html += `<div class="abap-doc-section"><h3>Business Logic</h3><p class="abap-summary">${escapeHtml(doc.business_logic)}</p></div>`;
  }

  const tagSection = (label, items) => {
    if (!items || !items.length) return "";
    return `
      <div class="abap-doc-section">
        <h3>${label}</h3>
        <div class="abap-doc-tags">
          ${items.map((i) => `<span class="abap-doc-tag">${escapeHtml(i)}</span>`).join("")}
        </div>
      </div>`;
  };

  html += tagSection("Inputs", doc.inputs);
  html += tagSection("Outputs", doc.outputs);
  html += tagSection("Tables Used", doc.tables_used);
  html += tagSection("Function Modules / BAPIs", doc.function_modules);

  if (doc.flow && doc.flow.length) {
    html += `<div class="abap-doc-section"><h3>Flow</h3><div class="abap-flow">`;
    doc.flow.forEach((step, i) => {
      html += `
        <div class="abap-flow-step">
          <span class="abap-flow-num">${i + 1}</span>
          <span>${escapeHtml(step.step)}</span>
        </div>`;
      if (i < doc.flow.length - 1) {
        html += `<div class="abap-flow-arrow">↓</div>`;
      }
    });
    html += `</div></div>`;
  }

  return html;
}

function attachCopyHandlers(container) {
  container.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.dataset.target);
      if (!target) return;
      navigator.clipboard.writeText(target.textContent).then(() => {
        const original = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = original), 1500);
      });
    });
  });
}

// ============================================================
// AI Rule & Test Case Generator
// ============================================================

const ruleModuleSelect = document.getElementById("rule-module-select");
const ruleDescriptionInput = document.getElementById("rule-description-input");
const ruleGenerateBtn = document.getElementById("rule-generate-btn");
const ruleError = document.getElementById("rule-error");
const ruleEmpty = document.getElementById("rule-empty");
const ruleLoading = document.getElementById("rule-loading");
const ruleResults = document.getElementById("rule-results");

ruleGenerateBtn.addEventListener("click", runRuleGeneration);

async function runRuleGeneration() {
  const description = ruleDescriptionInput.value.trim();

  if (!description) {
    ruleError.textContent = "Describe the validation you want first.";
    ruleError.classList.remove("hidden");
    return;
  }

  ruleError.classList.add("hidden");
  ruleEmpty.classList.add("hidden");
  ruleResults.classList.add("hidden");
  ruleLoading.classList.remove("hidden");
  ruleGenerateBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/api/rules/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, module: ruleModuleSelect.value }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Server returned ${res.status}`);
    }

    const data = await res.json();
    renderRuleResults(data);

  } catch (err) {
    ruleLoading.classList.add("hidden");
    ruleEmpty.classList.remove("hidden");
    ruleError.textContent = `Generation failed: ${err.message}`;
    ruleError.classList.remove("hidden");
  } finally {
    ruleGenerateBtn.disabled = false;
  }
}

function renderRuleResults(data) {
  ruleLoading.classList.add("hidden");
  ruleResults.classList.remove("hidden");

  let html = `
    <div class="rec-head" style="margin-bottom:14px;">
      <span class="rec-title" style="font-size:15px;">${escapeHtml(data.rule_name)}</span>
      <span class="rec-severity">${data.severity}</span>
    </div>
    <div class="abap-summary">${escapeHtml(data.description)}</div>

    <div class="abap-doc-section"><h3>Expected Result</h3><p class="abap-summary">${escapeHtml(data.expected_result)}</p></div>
    <div class="abap-doc-section"><h3>Business Impact</h3><p class="abap-summary">${escapeHtml(data.business_impact)}</p></div>
    <div class="abap-doc-section"><h3>Recommendation Template</h3><p class="abap-summary">${escapeHtml(data.recommendation)}</p></div>
  `;

  html += renderCodeBlock("SQL Query", data.sql_query, "rule-sql-code");
  html += renderCodeBlock("Python Check", data.python_check, "rule-python-code");

  if (data.test_cases && data.test_cases.length) {
    html += `<div class="abap-issues-title">${data.test_cases.length} test case(s)</div>`;
    html += `<div class="recommendations">` + data.test_cases.map((tc) => {
      const typeClass = tc.type === "POSITIVE" ? "low" : tc.type === "NEGATIVE" ? "critical" : "medium";
      return `
        <div class="rec-card ${typeClass}">
          <div class="rec-head">
            <span class="rec-title">${escapeHtml(tc.scenario)}</span>
            <span class="rec-severity">${tc.type}</span>
          </div>
          <div class="rec-text">${escapeHtml(tc.expected_result)}</div>
        </div>`;
    }).join("") + `</div>`;
  }

  html += `
    <div class="abap-doc-section rule-save-row">
      <button id="rule-save-btn" class="scope-run-btn">Save to Rule Library</button>
      <span id="rule-save-status" class="rule-save-status"></span>
    </div>
  `;

  ruleResults.innerHTML = html;
  attachCopyHandlers(ruleResults);

  document.getElementById("rule-save-btn").addEventListener("click", () => saveGeneratedRule(data));
}

async function saveGeneratedRule(data) {
  const btn = document.getElementById("rule-save-btn");
  const status = document.getElementById("rule-save-status");

  btn.disabled = true;
  status.textContent = "Saving…";
  status.style.color = "var(--text-muted)";

  const categoryName = ruleModuleSelect.options[ruleModuleSelect.selectedIndex].text.replace("Module: ", "");

  try {
    const res = await fetch(`${API_BASE}/api/rules/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rule_name: data.rule_name,
        category_name: categoryName,
        description: data.description,
        rule_expression: data.sql_query,
        severity: data.severity,
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Server returned ${res.status}`);
    }

    const saved = await res.json();
    status.textContent = `Saved as rule #${saved.id} in "${saved.category_name}".`;
    status.style.color = "var(--pass)";

  } catch (err) {
    status.textContent = `Could not save: ${err.message}`;
    status.style.color = "var(--critical)";
    btn.disabled = false;
  }
}

// ============================================================
// Inventory module
// ============================================================

const invRunBtn = document.getElementById("inv-run-btn");
const invMaterialInput = document.getElementById("inv-material-input");
const invPlantInput = document.getElementById("inv-plant-input");
const invScopeRunBtn = document.getElementById("inv-scope-run-btn");
const invScopeBanner = document.getElementById("inv-scope-banner");
const invScopeBannerText = document.getElementById("inv-scope-banner-text");
const invScopeClearBtn = document.getElementById("inv-scope-clear-btn");
const invEmpty = document.getElementById("inv-empty");
const invLoading = document.getElementById("inv-loading");
const invReport = document.getElementById("inv-report");

const invSearchInput = document.getElementById("inv-search-input");
const invSeverityFilters = document.getElementById("inv-severity-filters");
const invShowPassedCheckbox = document.getElementById("inv-show-passed");
const invPaginationEl = document.getElementById("inv-pagination");

const invRecSearchInput = document.getElementById("inv-rec-search-input");
const invRecSeverityFilters = document.getElementById("inv-rec-severity-filters");

let invAllResults = [];
let invActiveSeverity = "ALL";
let invSearchTerm = "";
let invShowPassed = false;
let invCurrentPage = 1;

let invAllGroups = [];
let invRecSearchTerm = "";
let invRecActiveSeverity = "ALL";

invRunBtn.addEventListener("click", () => runInventoryValidation(null, null));
invScopeRunBtn.addEventListener("click", () => {
  runInventoryValidation(parseScopeValue(invMaterialInput.value), parseScopeValue(invPlantInput.value));
});
invScopeClearBtn.addEventListener("click", () => {
  invMaterialInput.value = "";
  invPlantInput.value = "";
  runInventoryValidation(null, null);
});

invSearchInput.addEventListener("input", (e) => {
  invSearchTerm = e.target.value.trim().toLowerCase();
  invCurrentPage = 1;
  renderInventoryResultsTable();
});
invShowPassedCheckbox.addEventListener("change", (e) => {
  invShowPassed = e.target.checked;
  invCurrentPage = 1;
  renderInventoryResultsTable();
});
invSeverityFilters.addEventListener("click", (e) => {
  const btn = e.target.closest(".sev-chip");
  if (!btn) return;
  setActiveChip(invSeverityFilters, btn);
  invActiveSeverity = btn.dataset.sev;
  invCurrentPage = 1;
  renderInventoryResultsTable();
});

invRecSearchInput.addEventListener("input", (e) => {
  invRecSearchTerm = e.target.value.trim().toLowerCase();
  renderInventoryRecommendationGroups();
});
invRecSeverityFilters.addEventListener("click", (e) => {
  const btn = e.target.closest(".sev-chip");
  if (!btn) return;
  setActiveChip(invRecSeverityFilters, btn);
  invRecActiveSeverity = btn.dataset.sev;
  renderInventoryRecommendationGroups();
});

async function runInventoryValidation(materialNames, plantNames) {
  invRunBtn.disabled = true;
  invScopeRunBtn.disabled = true;
  invEmpty.classList.add("hidden");
  invScopeBanner.classList.add("hidden");
  invReport.classList.add("hidden");
  invLoading.classList.remove("hidden");

  try {
    let url = `${API_BASE}/api/report/inventory`;
    const params = new URLSearchParams();
    if (materialNames && materialNames.length) params.set("materials", materialNames.join(","));
    if (plantNames && plantNames.length) params.set("plants", plantNames.join(","));
    if ([...params].length) url += `?${params.toString()}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    const data = await res.json();

    invMaterialInput.value = materialNames ? materialNames.join(", ") : "";
    invPlantInput.value = plantNames ? plantNames.join(", ") : "";

    renderInventoryReport(data);

  } catch (err) {
    invLoading.classList.add("hidden");
    invEmpty.classList.remove("hidden");
    invEmpty.querySelector("p").textContent =
      `Could not generate the report: ${err.message}. Check that the backend is running.`;
  } finally {
    invRunBtn.disabled = false;
    invScopeRunBtn.disabled = false;
  }
}

function renderInventoryReport(data) {
  invLoading.classList.add("hidden");
  invReport.classList.remove("hidden");
  document.getElementById("inv-intro").classList.add("hidden");

  if (data.scope === "SELECTED") {
    const parts = [];
    if (data.scoped_materials.length) parts.push(`materials: <strong>${data.scoped_materials.join(", ")}</strong>`);
    if (data.scoped_plants.length) parts.push(`plants: <strong>${data.scoped_plants.join(", ")}</strong>`);
    let text = `Scoped run — ${parts.join(" | ")}`;
    const notFound = [...data.scoped_materials_not_found, ...data.scoped_plants_not_found];
    if (notFound.length) {
      text += ` <span style="color:var(--critical)">(not found: ${notFound.join(", ")})</span>`;
    }
    invScopeBannerText.innerHTML = text;
    invScopeBanner.classList.remove("hidden");
  } else {
    invScopeBanner.classList.add("hidden");
  }

  invAllResults = data.results;
  invActiveSeverity = "ALL";
  invSearchTerm = "";
  invShowPassed = false;
  invCurrentPage = 1;
  invSearchInput.value = "";
  invShowPassedCheckbox.checked = false;
  resetChips(invSeverityFilters);

  invAllGroups = data.recommendation_groups;
  invRecSearchTerm = "";
  invRecActiveSeverity = "ALL";
  invRecSearchInput.value = "";
  resetChips(invRecSeverityFilters);

  const m = data.metrics;
  const cells = [
    ["Inventory Records", m.total_inventory_records],
    ["Materials Tracked", m.total_materials],
    ["Plants", m.total_plants],
    ["Low Stock Items", m.low_stock_count],
    ["Negative Stock Issues", m.negative_stock_count],
    ["Stock Movements Logged", m.total_stock_movements],
  ];
  document.getElementById("inv-metrics-grid").innerHTML = cells
    .map(([label, value]) => `
      <div class="metric-cell">
        <div class="metric-value">${value}</div>
        <div class="metric-label">${label}</div>
      </div>`)
    .join("");

  document.getElementById("inv-executive-summary").textContent = data.executive_summary;
  document.getElementById("inv-stat-total").textContent = data.total_checks;
  document.getElementById("inv-stat-passed").textContent = data.passed_checks;
  document.getElementById("inv-stat-failed").textContent = data.failed_checks;

  renderGenericRiskChart(data.risk_distribution, "inv-risk-chart", "inv-risk-legend");
  renderInventoryRecommendationGroups();
  renderInventoryResultsTable();
}

// Shared risk-chart renderer (Procurement's version stayed inline and
// tab-hardcoded to keep that first working flow untouched; this one
// is parameterized so Inventory can reuse the same conic-gradient
// donut logic without duplicating it a third time).
function renderGenericRiskChart(distribution, chartId, legendId) {
  const chart = document.getElementById(chartId);
  const legend = document.getElementById(legendId);

  if (!distribution.length) {
    chart.style.background = "var(--pass)";
    legend.innerHTML = `<li><span class="swatch" style="background:var(--pass)"></span> No failures <span class="count">0</span></li>`;
    return;
  }

  const total = distribution.reduce((sum, d) => sum + d.count, 0);
  let acc = 0;
  const stops = [];

  distribution.forEach((d) => {
    const color = SEVERITY_COLOR[d.severity] || "var(--text-muted)";
    const start = (acc / total) * 100;
    acc += d.count;
    const end = (acc / total) * 100;
    stops.push(`${color} ${start}% ${end}%`);
  });

  chart.style.background = `conic-gradient(${stops.join(", ")})`;

  legend.innerHTML = distribution
    .map((d) => `
      <li>
        <span class="swatch" style="background:${SEVERITY_COLOR[d.severity] || "var(--text-muted)"}"></span>
        ${d.severity}
        <span class="count">${d.count}</span>
      </li>`)
    .join("");
}

function getInventoryFilteredGroups() {
  return invAllGroups.filter((g) => {
    if (invRecActiveSeverity !== "ALL" && g.severity !== invRecActiveSeverity) return false;
    if (invRecSearchTerm) {
      const haystack = `${g.group_label} ${g.recommendation} ${g.rule_name}`.toLowerCase();
      if (!haystack.includes(invRecSearchTerm)) return false;
    }
    return true;
  });
}

function renderInventoryRecommendationGroups() {
  const container = document.getElementById("inv-recommendations");
  const countLabel = document.getElementById("inv-rec-group-count");
  const filtered = getInventoryFilteredGroups();

  if (!invAllGroups.length) {
    countLabel.textContent = "";
    container.innerHTML = `<p class="no-issues">✓ No issues found — every check passed.</p>`;
    return;
  }

  countLabel.textContent = `${filtered.length} of ${invAllGroups.length} pattern(s) shown`;

  container.innerHTML = filtered.length
    ? filtered.map((g) => {
        const extra = g.count - g.sample_entities.length;
        return `
      <div class="rec-card ${g.severity.toLowerCase()}">
        <div class="rec-head">
          <span class="rec-title">${escapeHtml(g.group_label)}</span>
          <span class="rec-severity">${g.severity}</span>
          <span class="rec-count">${g.count} record${g.count === 1 ? "" : "s"}</span>
        </div>
        <div class="rec-text">${escapeHtml(g.recommendation)}</div>
        <details class="rec-entities">
          <summary>View affected records</summary>
          <div class="entity-chips">
            ${g.sample_entities.map((e) => `<span class="entity-chip">${escapeHtml(e)}</span>`).join("")}
            ${extra > 0 ? `<span class="entity-chip more">+${extra} more</span>` : ""}
          </div>
        </details>
      </div>`;
      }).join("")
    : `<p class="no-issues" style="color:var(--text-muted)">No recommendations match the current filters.</p>`;
}

function getInventoryFilteredResults() {
  return invAllResults.filter((r) => {
    if (!invShowPassed && r.passed) return false;
    if (invActiveSeverity !== "ALL" && r.severity !== invActiveSeverity) return false;
    if (invSearchTerm) {
      const haystack = `${r.rule_name} ${r.entity} ${r.message}`.toLowerCase();
      if (!haystack.includes(invSearchTerm)) return false;
    }
    return true;
  });
}

function renderInventoryResultsTable() {
  const filtered = getInventoryFilteredResults();
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  invCurrentPage = Math.min(invCurrentPage, totalPages);

  const start = (invCurrentPage - 1) * PAGE_SIZE;
  const pageItems = filtered.slice(start, start + PAGE_SIZE);

  document.getElementById("inv-results-count").textContent =
    `${filtered.length} of ${invAllResults.length} shown`;

  const body = document.getElementById("inv-results-body");
  body.innerHTML = pageItems.length
    ? pageItems.map((r) => `
      <tr>
        <td><span class="status-dot ${r.passed ? "pass" : "fail"}"></span></td>
        <td class="rule-cell">${escapeHtml(r.rule_name)}</td>
        <td class="entity-cell">${escapeHtml(r.entity)}</td>
        <td><span class="severity-tag ${r.severity.toLowerCase()}">${r.severity}</span></td>
        <td>${escapeHtml(r.message)}</td>
      </tr>`).join("")
    : `<tr><td colspan="5" class="empty-row">No results match the current filters.</td></tr>`;

  renderInventoryPagination(totalPages);
}

function renderInventoryPagination(totalPages) {
  if (totalPages <= 1) {
    invPaginationEl.innerHTML = "";
    return;
  }

  const buttons = [];
  buttons.push(`<button class="page-btn" data-page="${invCurrentPage - 1}" ${invCurrentPage === 1 ? "disabled" : ""}>‹ Prev</button>`);
  buttons.push(`<span class="page-status">Page ${invCurrentPage} of ${totalPages}</span>`);
  buttons.push(`<button class="page-btn" data-page="${invCurrentPage + 1}" ${invCurrentPage === totalPages ? "disabled" : ""}>Next ›</button>`);

  invPaginationEl.innerHTML = buttons.join("");
  invPaginationEl.querySelectorAll(".page-btn:not([disabled])").forEach((btn) => {
    btn.addEventListener("click", () => {
      invCurrentPage = parseInt(btn.dataset.page, 10);
      renderInventoryResultsTable();
    });
  });
}

// ============================================================
// Home landing — card navigation + initial state
// ============================================================

document.querySelectorAll(".home-card[data-module]").forEach((card) => {
  card.addEventListener("click", () => switchModule(card.dataset.module));
});

// Establish the true initial state through the same code path as
// every other navigation, rather than relying on hand-set 'hidden'
// classes in the HTML matching this JS by coincidence.
switchModule("home");
