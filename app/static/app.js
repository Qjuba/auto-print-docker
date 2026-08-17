const state = { dashboard: null, printers: [], started: false };
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const viewRoutes = { dashboard: "/dashboard", setup: "/settings", history: "/history", logs: "/logs" };
const routeViews = Object.fromEntries(Object.entries(viewRoutes).map(([view, route]) => [route, view]));
let previewTimer;

function showLogin() {
  const screen = $("#login-screen");
  screen.classList.remove("hidden");
  screen.classList.add("grid");
  $("#app-shell").setAttribute("inert", "");
  requestAnimationFrame(() => $("#login-username").focus());
}

function hideLogin() {
  const screen = $("#login-screen");
  screen.classList.add("hidden");
  screen.classList.remove("grid");
  $("#app-shell").removeAttribute("inert");
  $("#login-error").textContent = "";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(options.headers || {}),
    },
  });
  let data = {};
  try { data = await response.json(); } catch (_) { /* response without JSON */ }
  if (response.status === 401 && path !== "/api/auth/login") showLogin();
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail.map(item => item.msg).join(", ") : data.detail;
    throw new Error(detail || `Błąd HTTP ${response.status}`);
  }
  return data;
}

function toast(message, error = false) {
  const item = document.createElement("div");
  item.className = `toast${error ? " error" : ""}`;
  item.textContent = message;
  $("#toasts").append(item);
  setTimeout(() => item.remove(), 5000);
}

function setBusy(button, busy) {
  button.disabled = busy;
  button.dataset.state = busy ? "loading" : "default";
  if (busy) {
    button.dataset.label = button.textContent;
    button.textContent = "Przetwarzanie…";
  } else if (button.dataset.label) {
    button.textContent = button.dataset.label;
  }
}

function showView(name, push = true) {
  $$(".view").forEach(view => view.classList.toggle("active", view.id === `view-${name}`));
  $$(".nav-link").forEach(link => link.classList.toggle("active", link.dataset.view === name));
  if (push && location.pathname !== viewRoutes[name]) window.history.pushState({ view: name }, "", viewRoutes[name]);
  if (name === "history") loadHistory();
  if (name === "logs") loadLogs();
  window.scrollTo(0, 0);
}

function formatDate(value) {
  if (!value) return "—";
  return new Intl.DateTimeFormat("pl-PL", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

function scheduleText(data) {
  if (!data) return "Brak harmonogramu";
  if (data.type === "interval") {
    const units = { minutes: "min", hours: "godz.", days: "dni", weeks: "tyg." };
    const time = ["days", "weeks"].includes(data.interval_unit) ? ` · start o ${data.time_of_day}` : "";
    return `Co ${data.interval_value} ${units[data.interval_unit] || data.interval_unit}${time}`;
  }
  if (data.type === "monthly") {
    const days = data.days_of_month.map(day => String(day));
    if (data.last_day_of_month) days.push("ostatni");
    return `${days.join(", ")} dnia miesiąca o ${data.time_of_day}`;
  }
  const names = ["Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd"];
  const days = data.days_of_week.length === 7 ? "Codziennie" : data.days_of_week.map(day => names[day]).join(", ");
  return `${days} o ${data.time_of_day}`;
}

function statusBadge(item) {
  const label = item.status === "submitted" ? "Przyjęte" : "Błąd";
  return `<span class="badge ${item.status}">${label}</span>`;
}

function safe(value) {
  const node = document.createElement("span");
  node.textContent = value ?? "—";
  return node.innerHTML;
}

function historyRows(items, compact = false) {
  if (!items.length) return `<tr><td class="empty-row" colspan="${compact ? 4 : 6}">Brak wykonanych wydruków.</td></tr>`;
  return items.map(item => compact
    ? `<tr><td>${formatDate(item.created_at)}</td><td>${safe(item.file_name)}</td><td>${item.trigger === "automatic" ? "Automatyczny" : "Ręczny"}</td><td>${statusBadge(item)}</td></tr>`
    : `<tr><td>${formatDate(item.created_at)}</td><td>${safe(item.file_name)}</td><td>${safe(item.printer_name)}</td><td>${item.trigger === "automatic" ? "Automatyczny" : "Ręczny"}</td><td>${statusBadge(item)}</td><td>${safe(item.message)}${item.cups_job_id ? `<br><small>${safe(item.cups_job_id)}</small>` : ""}</td></tr>`
  ).join("");
}

async function loadDashboard() {
  try {
    const data = await api("/api/dashboard");
    state.dashboard = data;
    $("#header-pulse").classList.add("ok");
    $("#header-status").textContent = "System dostępny";
    $("#auto-dot").classList.toggle("ok", data.enabled);
    $("#auto-state").textContent = data.enabled ? "Włączona" : "Wyłączona";
    $("#schedule-summary").textContent = data.enabled ? scheduleText(data.schedule) : `Wyłączona · ${scheduleText(data.schedule)}`;
    $("#next-run").textContent = formatDate(data.next_run);
    $("#next-run-relative").textContent = data.next_run ? "Według harmonogramu" : "Brak terminu";
    $("#last-result").textContent = data.last_print ? (data.last_print.status === "submitted" ? "Przyjęte przez CUPS" : "Niepowodzenie") : "Brak zadań";
    $("#last-result-time").textContent = data.last_print ? formatDate(data.last_print.created_at) : "Brak historii";
    $("#printer-name").textContent = data.printer_name || "Nie wybrano";
    $("#printer-state").textContent = data.printer_status ? data.printer_status.message : "—";
    $("#file-name").textContent = data.file?.name || "Nie wybrano";
    $("#file-meta").textContent = data.file ? `${formatSize(data.file.size)} · ${data.file.media_type}` : "—";
    populateConfig(data);
    const recent = await api("/api/history?limit=5");
    $("#recent-history").innerHTML = historyRows(recent.items, true);
  } catch (error) {
    $("#header-status").textContent = "Brak połączenia";
    if (!$("#login-screen").classList.contains("grid")) toast(error.message, true);
  }
}

function populateConfig(data) {
  $("#enabled").checked = data.enabled;
  $("#interval-value").value = data.schedule.interval_value;
  $("#interval-unit").value = data.schedule.interval_unit;
  $("#time-of-day").value = data.schedule.time_of_day;
  $("#timezone").value = data.schedule.timezone;
  $$("#week-days input").forEach(input => { input.checked = data.schedule.days_of_week.includes(Number(input.value)); });
  $$("#month-days input").forEach(input => { input.checked = data.schedule.days_of_month.includes(Number(input.value)); });
  $("#last-day-of-month").checked = data.schedule.last_day_of_month;
  setScheduleType(data.schedule.type === "daily" ? "weekly" : data.schedule.type);
  $("#file-current").classList.toggle("hidden", !data.file);
  if (data.file) {
    $("#current-file-name").textContent = data.file.name;
    $("#current-file-meta").textContent = `${formatSize(data.file.size)} · dodano ${formatDate(data.file.created_at)}`;
  }
  if (data.printer_name) $("#printer-select").value = data.printer_name;
  updateEditButton();
}

function setScheduleType(type) {
  $("#schedule-type").value = type;
  $("#interval-fields").classList.toggle("hidden", type !== "interval");
  $("#weekly-fields").classList.toggle("hidden", type !== "weekly");
  $("#monthly-fields").classList.toggle("hidden", type !== "monthly");
  updateTimeField();
  schedulePreview();
}

function updateTimeField() {
  const needsTime = $("#schedule-type").value !== "interval" || ["days", "weeks"].includes($("#interval-unit").value);
  $("#time-field").classList.toggle("hidden", !needsTime);
  $("#interval-time-help").classList.toggle("hidden", $("#schedule-type").value !== "interval");
}

function schedulePayload() {
  return {
    schedule_type: $("#schedule-type").value,
    interval_value: Number($("#interval-value").value),
    interval_unit: $("#interval-unit").value,
    time_of_day: $("#time-of-day").value,
    days_of_week: $$("#week-days input:checked").map(input => Number(input.value)),
    days_of_month: $$("#month-days input:checked").map(input => Number(input.value)),
    last_day_of_month: $("#last-day-of-month").checked,
    timezone: $("#timezone").value.trim(),
  };
}

function schedulePreview() {
  clearTimeout(previewTimer);
  previewTimer = setTimeout(async () => {
    const list = $("#schedule-preview");
    list.innerHTML = "<li>Obliczanie…</li>";
    try {
      const data = await api("/api/schedule/preview", { method: "POST", body: JSON.stringify(schedulePayload()) });
      list.innerHTML = data.occurrences.map(value => `<li>${formatDate(value)}</li>`).join("") || "<li>Brak przyszłych terminów.</li>";
    } catch (error) {
      list.innerHTML = `<li class="text-red-700">${safe(error.message)}</li>`;
    }
  }, 250);
}

function updateEditButton() {
  $("#edit-printer").disabled = !state.printers.some(printer => printer.name === $("#printer-select").value);
}

async function loadPrinters() {
  const select = $("#printer-select");
  const selected = select.value || state.dashboard?.printer_name || "";
  try {
    const data = await api("/api/printers");
    state.printers = data.items;
    select.innerHTML = `<option value="">Wybierz drukarkę</option>` + data.items.map(printer => `<option value="${safe(printer.name)}">${safe(printer.name)} — ${safe(printer.state)}</option>`).join("");
    select.value = selected;
    updateEditButton();
  } catch (error) { toast(error.message, true); }
}

async function saveConfig(event) {
  event.preventDefault();
  const button = $('[type="submit"][form="config-form"]');
  setBusy(button, true);
  const payload = {
    ...schedulePayload(),
    enabled: $("#enabled").checked,
    printer_name: $("#printer-select").value || null,
  };
  try {
    await api("/api/config", { method: "PUT", body: JSON.stringify(payload) });
    button.dataset.state = "success";
    await loadDashboard();
  } catch (error) {
    button.dataset.state = "error";
    toast(error.message, true);
  } finally { setBusy(button, false); }
}

async function uploadFile(file) {
  if (!file) return;
  const form = new FormData();
  form.append("file", file);
  $("#upload-progress").textContent = "Wysyłanie i sprawdzanie…";
  try {
    await api("/api/files", { method: "POST", body: form });
    $("#file-input").value = "";
    await loadDashboard();
  } catch (error) { toast(error.message, true); }
  finally { $("#upload-progress").textContent = ""; }
}

async function runPrint(path, button) {
  setBusy(button, true);
  try {
    const result = await api(path, { method: "POST" });
    toast(result.message, result.status !== "submitted");
    await loadDashboard();
  } catch (error) { toast(error.message, true); }
  finally { setBusy(button, false); }
}

async function loadHistory() {
  try { const data = await api("/api/history?limit=100"); $("#history-body").innerHTML = historyRows(data.items); }
  catch (error) { toast(error.message, true); }
}

async function loadLogs() {
  try {
    const data = await api("/api/logs?lines=250");
    $("#log-content").textContent = data.lines.join("\n") || "Log jest pusty.";
    $("#log-content").scrollTop = $("#log-content").scrollHeight;
  } catch (error) { toast(error.message, true); }
}

function openPrinterDialog(mode, printer = null) {
  $("#printer-form-mode").value = mode;
  $("#printer-dialog-title").textContent = mode === "edit" ? "Edytuj drukarkę" : "Dodaj drukarkę";
  $("#printer-submit").textContent = mode === "edit" ? "Zapisz" : "Dodaj";
  $("#printer-add-name").value = printer?.name || "";
  $("#printer-add-name").disabled = mode === "edit";
  $("#printer-add-uri").value = printer?.uri || "";
  $("#printer-add-location").value = printer?.location || "";
  $("#printer-dialog").showModal();
  requestAnimationFrame(() => (mode === "edit" ? $("#printer-add-uri") : $("#printer-add-name")).focus());
}

async function discover(button) {
  setBusy(button, true);
  try {
    const data = await api("/api/printers/discover");
    const box = $("#discovered"), list = $("#discovered-list");
    box.classList.remove("hidden");
    list.innerHTML = data.items.length ? data.items.map(item => `<div class="flex items-center justify-between gap-3 border-t border-neutral-200 py-2"><code class="min-w-0 break-all text-xs">${safe(item.uri)}</code><button class="link-button" type="button" data-uri="${safe(item.uri)}">Użyj</button></div>`).join("") : `<p class="text-sm text-neutral-600">Nie znaleziono urządzeń. Dodaj adres ręcznie.</p>`;
    $$('[data-uri]', list).forEach(use => use.addEventListener("click", () => { openPrinterDialog("add"); $("#printer-add-uri").value = use.dataset.uri; }));
  } catch (error) { toast(error.message, true); }
  finally { setBusy(button, false); }
}

async function bootstrapApp() {
  if (!state.started) state.started = true;
  await loadPrinters();
  await loadDashboard();
  const legacy = location.hash.slice(1);
  const legacyView = ["dashboard", "setup", "history", "logs"].includes(legacy) ? legacy : null;
  const initial = legacyView || routeViews[location.pathname] || "dashboard";
  if (legacyView) window.history.replaceState({ view: initial }, "", viewRoutes[initial]);
  showView(initial, false);
}

document.addEventListener("DOMContentLoaded", async () => {
  $$(".nav-link").forEach(link => link.addEventListener("click", event => { event.preventDefault(); showView(link.dataset.view); }));
  $$('[data-go]').forEach(link => link.addEventListener("click", event => { event.preventDefault(); showView(link.dataset.go); }));
  window.addEventListener("popstate", () => showView(routeViews[location.pathname] || "dashboard", false));
  $("#schedule-type").addEventListener("change", event => setScheduleType(event.target.value));
  $("#interval-unit").addEventListener("change", updateTimeField);
  $$("#config-form input, #config-form select").forEach(input => input.addEventListener("change", schedulePreview));
  $("#printer-select").addEventListener("change", updateEditButton);
  $("#config-form").addEventListener("submit", saveConfig);
  $("#file-input").addEventListener("change", event => uploadFile(event.target.files[0]));
  const drop = $("#drop-zone");
  ["dragenter", "dragover"].forEach(name => drop.addEventListener(name, event => { event.preventDefault(); drop.classList.add("drag"); }));
  ["dragleave", "drop"].forEach(name => drop.addEventListener(name, event => { event.preventDefault(); drop.classList.remove("drag"); }));
  drop.addEventListener("drop", event => uploadFile(event.dataTransfer.files[0]));
  $("#delete-file").addEventListener("click", async () => { if (!confirm("Usunąć aktywny plik i wyłączyć automatyzację?")) return; try { await api("/api/files/current", { method: "DELETE" }); await loadDashboard(); } catch (error) { toast(error.message, true); } });
  $("#manual-print").addEventListener("click", event => runPrint("/api/print/manual", event.currentTarget));
  $("#test-print").addEventListener("click", event => runPrint("/api/print/test", event.currentTarget));
  $("#refresh-printers").addEventListener("click", async event => { setBusy(event.currentTarget, true); await loadPrinters(); setBusy(event.currentTarget, false); });
  $("#discover-printers").addEventListener("click", event => discover(event.currentTarget));
  $("#open-printer-dialog").addEventListener("click", () => openPrinterDialog("add"));
  $("#edit-printer").addEventListener("click", () => openPrinterDialog("edit", state.printers.find(printer => printer.name === $("#printer-select").value)));
  $("#close-printer-dialog").addEventListener("click", () => $("#printer-dialog").close());
  $("#cancel-printer-dialog").addEventListener("click", () => $("#printer-dialog").close());
  $("#printer-form").addEventListener("submit", async event => {
    event.preventDefault();
    const mode = $("#printer-form-mode").value;
    const payload = { name: $("#printer-add-name").value, uri: $("#printer-add-uri").value, location: $("#printer-add-location").value };
    try {
      await api(mode === "edit" ? `/api/printers/${encodeURIComponent(payload.name)}` : "/api/printers", { method: mode === "edit" ? "PUT" : "POST", body: JSON.stringify(payload) });
      $("#printer-dialog").close();
      await loadPrinters();
      $("#printer-select").value = payload.name;
      updateEditButton();
    } catch (error) { toast(error.message, true); }
  });
  $("#refresh-history").addEventListener("click", loadHistory);
  $("#refresh-logs").addEventListener("click", loadLogs);
  $("#login-form").addEventListener("submit", async event => {
    event.preventDefault();
    const button = $("#login-submit");
    setBusy(button, true);
    try {
      await api("/api/auth/login", { method: "POST", body: JSON.stringify({ username: $("#login-username").value, password: $("#login-password").value }) });
      $("#login-password").value = "";
      hideLogin();
      $("#logout-button").classList.remove("hidden");
      await bootstrapApp();
    } catch (error) { $("#login-error").textContent = error.message; }
    finally { setBusy(button, false); }
  });
  $("#logout-button").addEventListener("click", async () => { await api("/api/auth/logout", { method: "POST" }); showLogin(); });

  try {
    const auth = await api("/api/auth/status");
    $("#logout-button").classList.toggle("hidden", !auth.enabled);
    if (auth.enabled && !auth.authenticated) showLogin(); else await bootstrapApp();
  } catch (error) { toast(error.message, true); }
});
