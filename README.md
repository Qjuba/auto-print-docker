<p align="center">
  <img src="logo.svg" alt="AutoPrint" width="420">
</p>

# AutoPrint

AutoPrint to kompletna, samowystarczalna aplikacja do cyklicznego drukowania jednego wskazanego pliku. Działa w kontenerze Docker, przechowuje konfigurację i historię w SQLite, a zadania przekazuje do lokalnego CUPS przez IPP. Panel obsługuje PDF, PNG, JPG/JPEG i TXT.

> Projekt jest przeznaczony do samodzielnego hostowania na Linuxie lub NAS-ie. GitHub służy do
> publikacji kodu i budowania projektu — aplikacja wymaga lokalnego dostępu sieciowego do drukarki,
> dlatego nie działa jako GitHub Pages.

## Architektura

```text
Przeglądarka :8080
       │  formularz logowania + sesja cookie (opcjonalnie)
       ▼
FastAPI + responsywny panel Hallmark
       ├── upload i walidacja ──► /data/uploads
       ├── konfiguracja/historia ─► /data/autoprint.db
       ├── log aplikacji ─────────► /data/logs/app.log
       └── APScheduler (trwały job store w SQLite)
                         │
                         ▼
                 CUPS w kontenerze
                 lp / lpadmin / ippfind
                         │
                         ▼
           IPP / IPPS / IPP Everywhere
                 drukarka sieciowa
```

Kontener uruchamia dwa procesy o rozdzielonych rolach: systemowy `cupsd` startuje z uprawnieniami potrzebnymi usłudze drukowania i następnie sam je ogranicza, natomiast FastAPI działa jako nieuprzywilejowany użytkownik `autoprint` (UID 10001, grupy `lp`/`lpadmin`). Panel nie udostępnia interfejsu administracyjnego CUPS na zewnątrz.

Najważniejsze moduły:

- `app/main.py` — API, widoki i cykl życia aplikacji;
- `app/printers.py` — rzeczywiste wywołania CUPS/IPP, bez powłoki systemowej;
- `app/scheduler.py` — trwały harmonogram interwałowy i kalendarzowy;
- `app/tasks.py` — wykonanie wydruku i zapis wyniku;
- `app/files.py` — strumieniowy upload, limity, bezpieczne nazwy i walidacja treści;
- `app/static/` i `app/templates/` — panel w strukturze Hallmark „Workbench”;
- `config/` — zamknięta dla sieci konfiguracja CUPS.

## Uruchomienie

Wymagane są Docker Engine 24+ i Docker Compose v2 na Linuxie lub NAS-ie.

```bash
cp .env.example .env
```

Przed uruchomieniem zmień `ADMIN_PASSWORD` w `.env`. Pozostawienie obu pól `ADMIN_*` pustych wyłącza logowanie i jest odpowiednie wyłącznie w zaufanej, odizolowanej sieci LAN.

```bash
docker compose up -d --build
docker compose logs -f autoprint
```

Panel będzie dostępny pod `http://adres-serwera:8080/dashboard`. Widoki mają zwykłe adresy
`/dashboard`, `/settings`, `/history` i `/logs`; stare odnośniki z `#` są automatycznie zamieniane.
Stan kontenera można sprawdzić poleceniem:

```bash
docker compose ps
```

Konfiguracja, uploady, baza i kolejki CUPS pozostają w nazwanych wolumenach `autoprint-data`, `cups-config` i `cups-spool`, więc przeżywają odtworzenie kontenera.

### Aktualizacja z repozytorium

```bash
git pull
docker compose up -d --build
```

Plik `.env` oraz dane aplikacji są ignorowane przez Git i nie zostaną nadpisane przez aktualizację.

## Dodanie drukarki Canon / IPP Everywhere

W panelu przejdź do **Konfiguracja → Drukarka sieciowa**. Najpierw użyj **Wykryj w sieci**. Jeśli mDNS nie przechodzi przez sieć Dockera, wybierz **Dodaj przez IPP** i podaj adres ręcznie, najczęściej:

```text
ipp://192.168.1.40/ipp/print
ipps://192.168.1.40/ipp/print
```

Dokładna ścieżka zależy od drukarki; można ją odczytać z panelu WWW urządzenia. Kolejka jest tworzona poleceniem `lpadmin -m everywhere`, bez dedykowanego sterownika. Dotyczy to modeli Canon deklarujących AirPrint, Mopria lub IPP Everywhere. Starszy model bez driverless IPP może wymagać producenta PPD/sterownika, którego ten obraz celowo nie instaluje.

Dockerowa sieć bridge umożliwia druk pod bezpośredni adres IP, ale na części hostów blokuje wykrywanie mDNS. Na Linuxie można w takim przypadku usunąć sekcję `ports` i dodać do usługi:

```yaml
network_mode: host
```

Panel w kontenerze nasłuchuje na porcie 8080. W trybie host będzie więc dostępny na porcie 8080, niezależnie od mapowania `APP_PORT`. Tryb host nie jest przenośny na Docker Desktop.

## Harmonogram

Panel obsługuje:

- interwał co X minut, godzin, dni lub tygodni;
- wybraną godzinę w zaznaczone dni tygodnia;
- wiele wybranych dni miesiąca, opcjonalnie ostatni dzień miesiąca, oraz godzinę;
- strefy czasowe IANA, np. `Europe/Warsaw`.

Dla interwału liczonego w dniach lub tygodniach można wskazać godzinę pierwszego uruchomienia.
Dni nieistniejące w krótszym miesiącu są pomijane. Panel pokazuje pięć najbliższych terminów,
liczonych przez ten sam mechanizm co rzeczywiste zadanie.

Zadanie APScheduler i jego następny termin znajdują się w tej samej trwałej bazie SQLite. Po restarcie kontenera konfiguracja jest synchronizowana i zadanie wraca automatycznie. Nakładające się uruchomienia są blokowane, a opóźnione wywołania są scalane.

## Błędy i diagnostyka

Każda próba drukowania tworzy wpis historii. Sukces oznacza przyjęcie zadania przez CUPS i zawiera identyfikator kolejki; awaria zachowuje komunikat CUPS, np. brak kolejki, offline lub timeout. Fizyczny stan po przyjęciu zadania (papier, toner, zacięcie) zależy od informacji publikowanych przez drukarkę w IPP i pojawia się w stanie kolejki/logu CUPS.

Panel pokazuje ostatnie 250 linii rotowanego logu aplikacji. Pełniejsze logi kontenera:

```bash
docker compose logs --tail=200 autoprint
```

## Bezpieczeństwo

- nazwa uploadu nigdy nie jest używana jako ścieżka; plik dostaje losowy identyfikator;
- akceptowane są tylko PDF, PNG, JPEG i tekst UTF-8, a treść jest parsowana przed aktywacją;
- upload jest strumieniowany i ograniczony przez `MAX_UPLOAD_MB`;
- pliki mają tryb `0640`, nie są wykonywane ani serwowane przez WWW;
- polecenia CUPS dostają listę argumentów i nigdy nie używają `shell=True`;
- adres drukarki musi używać `ipp://` lub `ipps://`;
- mutacje z obcego `Origin` są odrzucane, a odpowiedzi mają CSP i nagłówki ochronne;
- logowanie używa formularza w panelu i podpisanej, 12-godzinnej sesji w cookie `HttpOnly`/`SameSite=Strict`;
- aplikacja WWW działa bez praw roota;
- `docker-compose.yml` usuwa capabilities i włącza `no-new-privileges`;
- dla dostępu spoza LAN należy bezwzględnie włączyć hasło i postawić TLS na reverse proxy (Caddy, Traefik lub Nginx). Nie wystawiaj portu bezpośrednio do Internetu.

## Rozwój lokalny i testy

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
npm install
npm run build:css
pytest
ruff check app tests
```

Źródłem stylów jest Tailwind CSS v4 w `app/static/tailwind.input.css`. Do kontenera trafia
skompilowany, statyczny `app.css` oraz lokalny Geist; panel nie pobiera CSS, fontów ani
skryptów z CDN.

Na Windows aktywacja środowiska to `.venv\Scripts\Activate.ps1`. Testy nie potrzebują działającego CUPS — warstwa poleceń jest izolowana i mockowana. Do rzeczywistego testu drukarki użyj kontenera Linux.

Każdy push i pull request uruchamia w GitHub Actions kompilację CSS, Ruff, testy Pytest oraz
kontrolny build obrazu Docker. Zasady współpracy opisuje [CONTRIBUTING.md](CONTRIBUTING.md),
a bezpieczne zgłaszanie podatności — [SECURITY.md](SECURITY.md).

## Licencja

Projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku [LICENSE](LICENSE).

## Aktualizacja i kopia zapasowa

Przed aktualizacją wykonaj kopię wolumenów, w szczególności pliku `/data/autoprint.db` i `/data/uploads`. Następnie:

```bash
docker compose build --pull
docker compose up -d
```

Usunięcie poleceniem `docker compose down` nie kasuje danych. `docker compose down -v` usuwa wszystkie wolumeny projektu i jest operacją nieodwracalną.
