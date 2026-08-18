const translations = {
  skipToContent: ["Skip to content", "Przejdź do treści"],
  connecting: ["Connecting…", "Łączenie…"],
  logout: ["Log out", "Wyloguj"],
  mainNavigation: ["Main navigation", "Główna nawigacja"],
  dashboard: ["Dashboard", "Przegląd"],
  settings: ["Settings", "Konfiguracja"],
  history: ["History", "Historia"],
  logs: ["Logs", "Logi"],
  dashboardDescription: ["Automatic printing status and recent jobs.", "Stan automatycznego drukowania i ostatnie zadania."],
  testPrint: ["Test print", "Druk testowy"],
  printNow: ["Print now", "Drukuj teraz"],
  automation: ["Automation", "Automatyzacja"],
  loading: ["Loading…", "Ładowanie…"],
  changeSettings: ["Change settings", "Zmień ustawienia"],
  nextPrint: ["Next print", "Następny wydruk"],
  notScheduled: ["Not scheduled", "Brak terminu"],
  lastResult: ["Last result", "Ostatni wynik"],
  noHistory: ["No history", "Brak historii"],
  printer: ["Printer", "Drukarka"],
  file: ["File", "Plik"],
  notSelected: ["Not selected", "Nie wybrano"],
  recentJobs: ["Recent jobs", "Ostatnie zadania"],
  viewHistory: ["View history", "Zobacz historię"],
  time: ["Time", "Czas"],
  mode: ["Mode", "Tryb"],
  result: ["Result", "Wynik"],
  settingsDescription: ["Choose a file, printer, and schedule.", "Wybierz plik, drukarkę i harmonogram."],
  save: ["Save", "Zapisz"],
  fileDescription: ["A new file will replace the currently selected one.", "Nowy plik zastąpi obecnie wybrany."],
  delete: ["Delete", "Usuń"],
  chooseOrDropFile: ["Choose or drop a file", "Wybierz lub upuść plik"],
  fileLimits: ["PDF, PNG, JPG, or TXT · max. {max} MB", "PDF, PNG, JPG lub TXT · maks. {max} MB"],
  printerDescription: ["Select a CUPS queue or add an IPP printer.", "Wybierz kolejkę CUPS albo dodaj drukarkę IPP."],
  activeQueue: ["Active queue", "Aktywna kolejka"],
  selectPrinter: ["Select a printer", "Wybierz drukarkę"],
  refresh: ["Refresh", "Odśwież"],
  discover: ["Discover", "Wykryj"],
  edit: ["Edit", "Edytuj"],
  addPrinter: ["Add printer", "Dodaj drukarkę"],
  discoveredDevices: ["Discovered devices", "Wykryte urządzenia"],
  schedule: ["Schedule", "Harmonogram"],
  scheduleDescription: ["Set the frequency and time zone.", "Ustaw częstotliwość i strefę czasową."],
  automaticPrinting: ["Automatic printing", "Automatyczne drukowanie"],
  automaticPrintingDescription: ["Enable the job using the settings below.", "Włącz zadanie według poniższych ustawień."],
  frequency: ["Frequency", "Częstotliwość"],
  atIntervals: ["At set intervals", "Co określony czas"],
  selectedWeekdays: ["On selected weekdays", "W wybrane dni tygodnia"],
  monthly: ["Monthly", "Co miesiąc"],
  repeatEvery: ["Repeat every", "Powtarzaj co"],
  unit: ["Unit", "Jednostka"],
  minutes: ["minutes", "minut"],
  hours: ["hours", "godzin"],
  days: ["days", "dni"],
  weeks: ["weeks", "tygodni"],
  weekdays: ["Weekdays", "Dni tygodnia"],
  mon: ["Mon", "Pn"], tue: ["Tue", "Wt"], wed: ["Wed", "Śr"], thu: ["Thu", "Cz"],
  fri: ["Fri", "Pt"], sat: ["Sat", "So"], sun: ["Sun", "Nd"],
  daysOfMonth: ["Days of the month", "Dni miesiąca"],
  lastDayOfMonth: ["Last day of the month", "Ostatni dzień miesiąca"],
  shortMonthHelp: ["Dates that do not exist in a shorter month are skipped.", "Terminy nieistniejące w krótszym miesiącu są pomijane."],
  crontabExpression: ["Crontab expression", "Wyrażenie crontab"],
  crontabHelp: ["Five fields: minute, hour, day of month, month, day of week. Example: 0 8 * * 1-5.", "Pięć pól: minuta, godzina, dzień miesiąca, miesiąc, dzień tygodnia. Przykład: 0 8 * * 1-5."],
  timeOfDay: ["Time", "Godzina"],
  intervalTimeHelp: ["For daily or weekly intervals, the first run starts at this time.", "Dla interwału dziennego lub tygodniowego pierwszy termin wypada o tej godzinie."],
  timezone: ["Time zone", "Strefa czasowa"],
  upcomingRuns: ["Upcoming runs", "Najbliższe terminy"],
  completeSchedule: ["Complete the schedule.", "Uzupełnij harmonogram."],
  historyDescription: ["Results of completed print jobs.", "Wyniki wykonanych zadań drukowania."],
  dateAndTime: ["Date and time", "Data i czas"],
  status: ["Status", "Status"],
  details: ["Details", "Informacja"],
  logsDescription: ["Latest application activity.", "Ostatnie wpisy z działania aplikacji."],
  printerDialogDescription: ["Enter the IPP Everywhere queue details.", "Podaj dane kolejki IPP Everywhere."],
  close: ["Close", "Zamknij"],
  queueName: ["Queue name", "Nazwa kolejki"],
  printerNamePlaceholder: ["Office_Canon", "Canon_biuro"],
  ippAddress: ["IPP address", "Adres IPP"],
  location: ["Location", "Lokalizacja"],
  office: ["Office", "Biuro"],
  cancel: ["Cancel", "Anuluj"],
  add: ["Add", "Dodaj"],
  login: ["Log in", "Logowanie"],
  loginDescription: ["Log in to the AutoPrint panel.", "Zaloguj się do panelu AutoPrint."],
  username: ["Username", "Nazwa użytkownika"],
  password: ["Password", "Hasło"],
  loginButton: ["Log in", "Zaloguj"],
  processing: ["Processing…", "Przetwarzanie…"],
  noSchedule: ["No schedule", "Brak harmonogramu"],
  last: ["last", "ostatni"],
  everyDay: ["Every day", "Codziennie"],
  accepted: ["Accepted", "Przyjęte"],
  error: ["Error", "Błąd"],
  noPrintJobs: ["No print jobs yet.", "Brak wykonanych wydruków."],
  automatic: ["Automatic", "Automatyczny"],
  manual: ["Manual", "Ręczny"],
  systemAvailable: ["System available", "System dostępny"],
  enabled: ["Enabled", "Włączona"],
  disabled: ["Disabled", "Wyłączona"],
  accordingToSchedule: ["According to schedule", "Według harmonogramu"],
  acceptedByCups: ["Accepted by CUPS", "Przyjęte przez CUPS"],
  failed: ["Failed", "Niepowodzenie"],
  noJobs: ["No jobs", "Brak zadań"],
  connectionUnavailable: ["Connection unavailable", "Brak połączenia"],
  calculating: ["Calculating…", "Obliczanie…"],
  noUpcomingRuns: ["No upcoming runs.", "Brak przyszłych terminów."],
  uploading: ["Uploading and validating…", "Wysyłanie i sprawdzanie…"],
  logEmpty: ["The log is empty.", "Log jest pusty."],
  use: ["Use", "Użyj"],
  noDevices: ["No devices found. Add an address manually.", "Nie znaleziono urządzeń. Dodaj adres ręcznie."],
  deleteFileConfirm: ["Delete the active file and disable automation?", "Usunąć aktywny plik i wyłączyć automatyzację?"],
  addedOn: ["added {date}", "dodano {date}"],
  startsAt: ["starts at {time}", "start o {time}"],
  dayOfMonthAt: ["{days} of the month at {time}", "{days} dnia miesiąca o {time}"],
  weekdaysAt: ["{days} at {time}", "{days} o {time}"],
  everyInterval: ["Every {value} {unit}{time}", "Co {value} {unit}{time}"],
  languageLabel: ["Current language: English. Switch to Polish", "Aktualny język: polski. Przełącz na angielski"],
  metaDescription: ["Automatic printing control panel for CUPS and IPP", "Panel automatycznego drukowania przez CUPS i IPP"],
};

let savedLanguage = "en";
try { savedLanguage = localStorage.getItem("autoprint-language") === "pl" ? "pl" : "en"; } catch (_) { /* storage may be unavailable */ }
const state = { dashboard: null, printers: [], started: false, language: savedLanguage };
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const viewRoutes = { dashboard: "/dashboard", setup: "/settings", history: "/history", logs: "/logs" };
const routeViews = Object.fromEntries(Object.entries(viewRoutes).map(([view, route]) => [route, view]));
let previewTimer;

function t(key, values = {}) {
  const value = translations[key]?.[state.language === "pl" ? 1 : 0] ?? key;
  return Object.entries(values).reduce(
    (text, [name, replacement]) => text.split(`{${name}}`).join(String(replacement)),
    value,
  );
}

function localizeBackendMessage(message) {
  if (!message) return message;
  const exact = {
    "Zadanie zostało przyjęte przez CUPS": "The print job was accepted by CUPS",
    "Nie wybrano drukarki": "No printer selected",
    "Wybrana drukarka nie jest dostępna w CUPS": "The selected printer is not available in CUPS",
    "Nie wybrano pliku do drukowania": "No file selected for printing",
    "Wybrany plik nie istnieje w magazynie": "The selected file does not exist in storage",
    "Brak informacji o stanie": "No status information",
    "Adres IPP drukarki jest nieprawidłowy": "The printer IPP address is invalid",
    "Port w adresie IPP drukarki jest nieprawidłowy": "The port in the printer IPP address is invalid",
    "Drukarka jest osiągalna": "The printer is reachable",
    "Nieprawidłowa nazwa użytkownika lub hasło": "Invalid username or password",
    "Prześlij plik przed włączeniem automatycznego drukowania": "Upload a file before enabling automatic printing",
    "Wybrana kolejka drukarki nie istnieje w CUPS": "The selected printer queue does not exist in CUPS",
    "Nazwy istniejącej kolejki nie można zmienić": "An existing queue cannot be renamed",
    "Kolejka drukarki nie istnieje": "The printer queue does not exist",
    "Odrzucono żądanie z innego źródła": "A request from another origin was rejected",
    "Nieobsługiwany rodzaj harmonogramu": "Unsupported schedule type",
    "Nieobsługiwana jednostka interwału": "Unsupported interval unit",
    "Godzina musi mieć format HH:MM": "Time must use the HH:MM format",
    "Nieprawidłowy dzień tygodnia": "Invalid weekday",
    "Nieprawidłowy dzień miesiąca": "Invalid day of the month",
    "Wybierz co najmniej jeden dzień tygodnia": "Select at least one weekday",
    "Wybierz co najmniej jeden dzień miesiąca": "Select at least one day of the month",
    "Wybierz drukarkę przed włączeniem automatyzacji": "Select a printer before enabling automation",
    "Dozwolone są wyłącznie adresy ipp:// i ipps://": "Only ipp:// and ipps:// addresses are allowed",
    "Nieprawidłowy adres drukarki": "Invalid printer address",
    "Wyrażenie crontab musi zawierać dokładnie 5 pól": "The crontab expression must contain exactly 5 fields",
    "Strona testowa AutoPrint": "AutoPrint test page",
    "Przekroczono czas odpowiedzi usługi drukowania": "The printing service timed out",
    "Nieznany błąd CUPS": "Unknown CUPS error",
  };
  if (state.language === "en" && exact[message]) return exact[message];
  if (state.language === "pl") {
    const translated = Object.entries(exact).find(([, english]) => english === message);
    if (translated) return translated[0];
    const unreachable = message.match(/^The printer is not responding at (.+)\. Check that it is powered on and connected to the network\.$/);
    if (unreachable) return `Drukarka nie odpowiada pod adresem ${unreachable[1]}. Sprawdź, czy jest włączona i połączona z siecią.`;
  }
  const prefixes = [
    ["Drukarka jest wyłączona:", "The printer is disabled:"],
    ["Drukarka nie odpowiada w sieci.", "The printer is not responding on the network."],
    ["CUPS odrzucił drukarkę:", "CUPS rejected the printer:"],
    ["CUPS odrzucił zmiany:", "CUPS rejected the changes:"],
    ["Nieprawidłowy lub uszkodzony plik:", "Invalid or corrupted file:"],
    ["Brak narzędzia systemowego:", "Missing system tool:"],
  ];
  const match = prefixes.find(pair => message.startsWith(pair[state.language === "pl" ? 1 : 0]));
  if (!match) return message;
  return message.replace(
    match[state.language === "pl" ? 1 : 0],
    match[state.language === "pl" ? 0 : 1],
  );
}

function applyLanguage() {
  document.documentElement.lang = state.language;
  document.querySelector('meta[name="description"]').content = t("metaDescription");
  $$('[data-i18n]').forEach(element => {
    const values = element.dataset.i18n === "fileLimits" ? { max: element.textContent.match(/\d+(?:\.\d+)?/)?.[0] || "" } : {};
    element.textContent = t(element.dataset.i18n, values);
  });
  $$('[data-i18n-aria-label]').forEach(element => { element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel)); });
  $$('[data-i18n-placeholder]').forEach(element => { element.placeholder = t(element.dataset.i18nPlaceholder); });
  [$("#language-button"), $("#login-language-button")].filter(Boolean).forEach(button => {
    button.textContent = state.language.toUpperCase();
    button.setAttribute("aria-label", t("languageLabel"));
  });
}

async function toggleLanguage() {
  state.language = state.language === "en" ? "pl" : "en";
  try { localStorage.setItem("autoprint-language", state.language); } catch (_) { /* storage may be unavailable */ }
  applyLanguage();
  if (state.started) {
    await loadPrinters();
    await loadDashboard();
    if ($("#view-history").classList.contains("active")) await loadHistory();
  }
}

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
    throw new Error(localizeBackendMessage(detail) || `${t("error")} HTTP ${response.status}`);
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
    button.textContent = t("processing");
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
  return new Intl.DateTimeFormat(state.language === "pl" ? "pl-PL" : "en-GB", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

function scheduleText(data) {
  if (!data) return t("noSchedule");
  if (data.type === "crontab") return `Crontab: ${data.cron_expression} · ${data.timezone}`;
  if (data.type === "interval") {
    const units = state.language === "pl"
      ? { minutes: "min", hours: "godz.", days: "dni", weeks: "tyg." }
      : { minutes: "min", hours: "hr", days: "days", weeks: "weeks" };
    const time = ["days", "weeks"].includes(data.interval_unit) ? ` · ${t("startsAt", { time: data.time_of_day })}` : "";
    return t("everyInterval", { value: data.interval_value, unit: units[data.interval_unit] || data.interval_unit, time });
  }
  if (data.type === "monthly") {
    const days = data.days_of_month.map(day => String(day));
    if (data.last_day_of_month) days.push(t("last"));
    return t("dayOfMonthAt", { days: days.join(", "), time: data.time_of_day });
  }
  const names = [t("mon"), t("tue"), t("wed"), t("thu"), t("fri"), t("sat"), t("sun")];
  const days = data.days_of_week.length === 7 ? t("everyDay") : data.days_of_week.map(day => names[day]).join(", ");
  return t("weekdaysAt", { days, time: data.time_of_day });
}

function statusBadge(item) {
  const label = item.status === "submitted" ? t("accepted") : t("error");
  return `<span class="badge ${item.status}">${label}</span>`;
}

function safe(value) {
  const node = document.createElement("span");
  node.textContent = value ?? "—";
  return node.innerHTML;
}

function historyRows(items, compact = false) {
  if (!items.length) return `<tr><td class="empty-row" colspan="${compact ? 4 : 6}">${t("noPrintJobs")}</td></tr>`;
  return items.map(item => compact
    ? `<tr><td>${formatDate(item.created_at)}</td><td>${safe(localizeBackendMessage(item.file_name))}</td><td>${item.trigger === "automatic" ? t("automatic") : t("manual")}</td><td>${statusBadge(item)}</td></tr>`
    : `<tr><td>${formatDate(item.created_at)}</td><td>${safe(localizeBackendMessage(item.file_name))}</td><td>${safe(item.printer_name)}</td><td>${item.trigger === "automatic" ? t("automatic") : t("manual")}</td><td>${statusBadge(item)}</td><td>${safe(localizeBackendMessage(item.message))}${item.cups_job_id ? `<br><small>${safe(item.cups_job_id)}</small>` : ""}</td></tr>`
  ).join("");
}

async function loadDashboard() {
  try {
    const data = await api("/api/dashboard");
    state.dashboard = data;
    $("#header-pulse").classList.add("ok");
    $("#header-status").textContent = t("systemAvailable");
    $("#auto-dot").classList.toggle("ok", data.enabled);
    $("#auto-state").textContent = data.enabled ? t("enabled") : t("disabled");
    $("#schedule-summary").textContent = data.enabled ? scheduleText(data.schedule) : `${t("disabled")} · ${scheduleText(data.schedule)}`;
    $("#next-run").textContent = formatDate(data.next_run);
    $("#next-run-relative").textContent = data.next_run ? t("accordingToSchedule") : t("notScheduled");
    $("#last-result").textContent = data.last_print ? (data.last_print.status === "submitted" ? t("acceptedByCups") : t("failed")) : t("noJobs");
    $("#last-result-time").textContent = data.last_print ? formatDate(data.last_print.created_at) : t("noHistory");
    $("#printer-name").textContent = data.printer_name || t("notSelected");
    $("#printer-state").textContent = data.printer_status ? localizeBackendMessage(data.printer_status.message) : "—";
    $("#file-name").textContent = data.file?.name || t("notSelected");
    $("#file-meta").textContent = data.file ? `${formatSize(data.file.size)} · ${data.file.media_type}` : "—";
    populateConfig(data);
    const recent = await api("/api/history?limit=5");
    $("#recent-history").innerHTML = historyRows(recent.items, true);
  } catch (error) {
    $("#header-status").textContent = t("connectionUnavailable");
    if (!$("#login-screen").classList.contains("grid")) toast(error.message, true);
  }
}

function populateConfig(data) {
  $("#enabled").checked = data.enabled;
  $("#interval-value").value = data.schedule.interval_value;
  $("#interval-unit").value = data.schedule.interval_unit;
  $("#cron-expression").value = data.schedule.cron_expression;
  $("#time-of-day").value = data.schedule.time_of_day;
  $("#timezone").value = data.schedule.timezone;
  $$("#week-days input").forEach(input => { input.checked = data.schedule.days_of_week.includes(Number(input.value)); });
  $$("#month-days input").forEach(input => { input.checked = data.schedule.days_of_month.includes(Number(input.value)); });
  $("#last-day-of-month").checked = data.schedule.last_day_of_month;
  setScheduleType(data.schedule.type === "daily" ? "weekly" : data.schedule.type);
  $("#file-current").classList.toggle("hidden", !data.file);
  if (data.file) {
    $("#current-file-name").textContent = data.file.name;
    $("#current-file-meta").textContent = `${formatSize(data.file.size)} · ${t("addedOn", { date: formatDate(data.file.created_at) })}`;
  }
  if (data.printer_name) $("#printer-select").value = data.printer_name;
  updateEditButton();
}

function setScheduleType(type) {
  $("#schedule-type").value = type;
  $("#interval-fields").classList.toggle("hidden", type !== "interval");
  $("#weekly-fields").classList.toggle("hidden", type !== "weekly");
  $("#monthly-fields").classList.toggle("hidden", type !== "monthly");
  $("#crontab-fields").classList.toggle("hidden", type !== "crontab");
  updateTimeField();
  schedulePreview();
}

function updateTimeField() {
  const type = $("#schedule-type").value;
  const needsTime = ["weekly", "monthly"].includes(type) || (type === "interval" && ["days", "weeks"].includes($("#interval-unit").value));
  $("#time-field").classList.toggle("hidden", !needsTime);
  $("#interval-time-help").classList.toggle("hidden", type !== "interval");
}

function schedulePayload() {
  return {
    schedule_type: $("#schedule-type").value,
    cron_expression: $("#cron-expression").value.trim(),
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
    list.innerHTML = `<li>${t("calculating")}</li>`;
    try {
      const data = await api("/api/schedule/preview", { method: "POST", body: JSON.stringify(schedulePayload()) });
      list.innerHTML = data.occurrences.map(value => `<li>${formatDate(value)}</li>`).join("") || `<li>${t("noUpcomingRuns")}</li>`;
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
    select.innerHTML = `<option value="">${t("selectPrinter")}</option>` + data.items.map(printer => `<option value="${safe(printer.name)}">${safe(printer.name)} — ${safe(localizeBackendMessage(printer.state))}</option>`).join("");
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
  $("#upload-progress").textContent = t("uploading");
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
    toast(localizeBackendMessage(result.message), result.status !== "submitted");
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
    $("#log-content").textContent = data.lines.join("\n") || t("logEmpty");
    $("#log-content").scrollTop = $("#log-content").scrollHeight;
  } catch (error) { toast(error.message, true); }
}

function openPrinterDialog(mode, printer = null) {
  $("#printer-form-mode").value = mode;
  $("#printer-dialog-title").textContent = mode === "edit" ? `${t("edit")} ${t("printer").toLocaleLowerCase(state.language === "pl" ? "pl" : "en")}` : t("addPrinter");
  $("#printer-submit").textContent = mode === "edit" ? t("save") : t("add");
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
    list.innerHTML = data.items.length ? data.items.map(item => `<div class="flex items-center justify-between gap-3 border-t border-neutral-200 py-2"><code class="min-w-0 break-all text-xs">${safe(item.uri)}</code><button class="link-button" type="button" data-uri="${safe(item.uri)}">${t("use")}</button></div>`).join("") : `<p class="text-sm text-neutral-600">${t("noDevices")}</p>`;
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
  applyLanguage();
  $("#language-button").addEventListener("click", toggleLanguage);
  $("#login-language-button").addEventListener("click", toggleLanguage);
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
  $("#delete-file").addEventListener("click", async () => { if (!confirm(t("deleteFileConfirm"))) return; try { await api("/api/files/current", { method: "DELETE" }); await loadDashboard(); } catch (error) { toast(error.message, true); } });
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
