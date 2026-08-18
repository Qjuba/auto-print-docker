# AutoPrint

AutoPrint pomaga zapobiegać zasychaniu tuszu w drukarkach atramentowych, m.in. typu inkjet. Automatycznie drukuje
wybrany plik według ustalonego harmonogramu, dzięki czemu drukarka jest regularnie używana nawet
wtedy, gdy przez dłuższy czas niczego nie drukujesz.

Aplikacja działa w lokalnej sieci, współpracuje z drukarkami obsługującymi IPP, AirPrint lub Mopria
i udostępnia prosty panel działający na komputerze oraz telefonie.

<img width="1252" height="752" alt="image" src="https://github.com/user-attachments/assets/b2c8b54b-3623-4f83-84d1-2b9192731fdb" />


## Co potrafi

- automatycznie drukuje jeden wybrany plik;
- obsługuje PDF, PNG, JPG i TXT;
- pozwala drukować co określoną liczbę minut, godzin, dni lub tygodni;
- obsługuje wybrane dni tygodnia oraz wiele dni miesiąca;
- obsługuje reguły w standardowej, pięciopolowej składni crontab;
- pozwala ustawić godzinę i strefę czasową;
- pokazuje najbliższe terminy, historię wydruków i komunikaty błędów;
- umożliwia ręczny wydruk oraz wydruk strony testowej;
- może być zabezpieczona formularzem logowania.

## Szybkie uruchomienie

Potrzebujesz urządzenia z Linuxem lub NAS-a, na którym działają Docker i Docker Compose. Urządzenie
musi pozostać włączone i mieć dostęp do drukarki w sieci lokalnej.

### 1. Pobierz projekt

Przez SSH:

```bash
git clone git@github.com:Qjuba/auto-print-docker.git
cd auto-print-docker
```

Lub przez HTTPS:

```bash
git clone https://github.com/Qjuba/auto-print-docker.git
cd auto-print-docker
```

### 2. Przygotuj konfigurację

```bash
cp .env.example .env
```

Otwórz plik `.env` i ustaw własne hasło:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu-wpisz-dlugie-losowe-haslo
```

Zamiast `.env` możesz użyć pliku `stack.env`, np. przy wdrożeniu przez Portainer:

```bash
cp .env.example stack.env
```

Jeśli istnieją oba pliki, wartości ze `stack.env` mają pierwszeństwo.

### 3. Uruchom aplikację

```bash
docker compose up -d --build
```

Panel będzie dostępny pod adresem:

```text
http://adres-twojego-serwera:8080/dashboard
```

Przykład dla serwera o adresie `192.168.1.20`:

```text
http://192.168.1.20:8080/dashboard
```

## Pierwsza konfiguracja

1. Zaloguj się danymi zapisanymi w `.env`.
2. Przejdź do **Konfiguracja**.
3. Wybierz wykrytą drukarkę lub dodaj jej adres IPP, np.:

   ```text
   ipp://192.168.1.40/ipp/print
   ```

4. Prześlij niewielki plik testowy zawierający kolory używane przez drukarkę.
5. Ustaw harmonogram i sprawdź podgląd najbliższych terminów.
6. Zapisz ustawienia i wykonaj ręczny wydruk testowy.

Na początek można ustawić jeden wydruk tygodniowo. Odpowiednia częstotliwość zależy jednak od
modelu drukarki, rodzaju tuszu, temperatury i wilgotności. AutoPrint nie zastępuje zaleceń
producenta dotyczących konserwacji urządzenia.

## Harmonogram crontab

Tryb **Crontab** przyjmuje pięć pól w kolejności: minuta, godzina, dzień miesiąca, miesiąc i dzień
tygodnia. Na przykład poniższa reguła uruchamia wydruk od poniedziałku do piątku o 08:00:

```text
0 8 * * 1-5
```

Obsługiwane są gwiazdki, listy, zakresy i kroki. Niedzielę można zapisać jako `0` lub `7`. Gdy
ograniczony jest zarówno dzień miesiąca, jak i dzień tygodnia, AutoPrint stosuje zgodną z cronem
regułę OR. Aliasy takie jak `@daily` oraz część zawierająca użytkownika lub komendę nie są
obsługiwane. Zadanie jest wykonywane przez harmonogram AutoPrint w wybranej strefie czasowej;
aplikacja nie modyfikuje pliku crontab hosta.

## Dodawanie drukarki

Najpierw użyj przycisku **Wykryj** w panelu. Jeśli drukarka nie zostanie znaleziona automatycznie,
podaj jej adres IPP ręcznie. Najczęściej jest to jeden z poniższych adresów:

```text
ipp://ADRES_IP/ipp/print
ipps://ADRES_IP/ipp/print
```

Dokładny adres można zwykle znaleźć w panelu internetowym drukarki. Urządzenie powinno obsługiwać
IPP Everywhere, AirPrint lub Mopria. Starsze drukarki wymagające dedykowanego sterownika mogą nie
działać z aplikacją.

## Aktualizacja

```bash
git pull
docker compose up -d --build
```

Ustawienia, historia, przesłany plik i kolejki drukarek są przechowywane poza kodem aplikacji i
pozostają zachowane po aktualizacji.

## Podstawowa diagnostyka

Sprawdź, czy aplikacja działa:

```bash
docker compose ps
```

Wyświetl ostatnie komunikaty:

```bash
docker compose logs --tail=100 autoprint
```

Jeśli wydruk nie dochodzi do drukarki, sprawdź kolejno:

- czy drukarka jest włączona i dostępna w tej samej sieci;
- czy jej adres IP nie uległ zmianie;
- czy wybrany adres IPP jest poprawny;
- czy w panelu AutoPrint wybrano plik i właściwą kolejkę drukarki;
- czy historia wydruków zawiera komunikat błędu.

## Zatrzymanie aplikacji

```bash
docker compose down
```

To polecenie nie usuwa zapisanych danych. Polecenie `docker compose down -v` usuwa wszystkie
wolumeny projektu i powoduje utratę konfiguracji oraz historii.

## Licencja

AutoPrint jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku [LICENSE](LICENSE).

---

# AutoPrint (English)

AutoPrint helps prevent ink from drying out in inkjet printers. It automatically prints a selected
file on a configured schedule, keeping the printer in regular use even when you do not print
anything else for a long time.

The application runs on your local network, works with printers that support IPP, AirPrint, or
Mopria, and provides a simple control panel for desktop and mobile devices. The web panel uses
English by default and can be switched between English and Polish.

## Features

- automatically prints one selected file;
- supports PDF, PNG, JPG, and TXT files;
- can print every configured number of minutes, hours, days, or weeks;
- supports selected weekdays and multiple days of the month;
- supports rules using the standard five-field crontab syntax;
- lets you configure the time and time zone;
- shows upcoming runs, print history, and error messages;
- supports manual printing and printing a test page;
- can be protected with a login form.

## Quick start

You need a Linux device or NAS with Docker and Docker Compose. The device must remain powered on
and have access to the printer on the local network.

### 1. Download the project

Using SSH:

```bash
git clone git@github.com:Qjuba/auto-print-docker.git
cd auto-print-docker
```

Or using HTTPS:

```bash
git clone https://github.com/Qjuba/auto-print-docker.git
cd auto-print-docker
```

### 2. Prepare the configuration

```bash
cp .env.example .env
```

Open `.env` and set your own password:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=enter-a-long-random-password-here
```

Instead of `.env`, you can use `stack.env`, for example when deploying through Portainer:

```bash
cp .env.example stack.env
```

If both files exist, values from `stack.env` take precedence.

### 3. Start the application

```bash
docker compose up -d --build
```

The panel will be available at:

```text
http://your-server-address:8080/dashboard
```

For example, for a server at `192.168.1.20`:

```text
http://192.168.1.20:8080/dashboard
```

## Initial setup

1. Log in using the credentials from `.env`.
2. Open **Settings**.
3. Select a discovered printer or add its IPP address, for example:

   ```text
   ipp://192.168.1.40/ipp/print
   ```

4. Upload a small test file containing the colors used by your printer.
5. Configure the schedule and review the upcoming run preview.
6. Save the settings and run a manual test print.

One print per week can be a reasonable starting point. The appropriate frequency depends on the
printer model, ink type, temperature, and humidity. AutoPrint does not replace the manufacturer's
maintenance recommendations.

## Crontab schedule

The **Crontab** mode accepts five fields in this order: minute, hour, day of month, month, and day
of week. For example, the following rule prints from Monday to Friday at 08:00:

```text
0 8 * * 1-5
```

Asterisks, lists, ranges, and steps are supported. Sunday can be written as `0` or `7`. When both
the day of month and day of week are restricted, AutoPrint applies the standard cron OR rule.
Aliases such as `@daily`, and entries containing a user or command, are not supported. Jobs are
run by the AutoPrint scheduler in the selected time zone; the application does not modify the
host's crontab file.

## Adding a printer

Start with the **Discover** button in the panel. If the printer is not found automatically, enter
its IPP address manually. It is usually one of the following:

```text
ipp://IP_ADDRESS/ipp/print
ipps://IP_ADDRESS/ipp/print
```

The exact address is usually available in the printer's web interface. The device should support
IPP Everywhere, AirPrint, or Mopria. Older printers that require a dedicated driver may not work
with the application.

## Updating

```bash
git pull
docker compose up -d --build
```

Settings, history, the uploaded file, and printer queues are stored outside the application code
and remain available after an update.

## Basic troubleshooting

Check whether the application is running:

```bash
docker compose ps
```

Show the latest messages:

```bash
docker compose logs --tail=100 autoprint
```

If the print job does not reach the printer, check:

- whether the printer is powered on and available on the same network;
- whether its IP address has changed;
- whether the selected IPP address is correct;
- whether a file and the correct printer queue are selected in AutoPrint;
- whether the print history contains an error message.

## Stopping the application

```bash
docker compose down
```

This command does not delete saved data. Running `docker compose down -v` deletes all project
volumes and permanently removes the configuration and history.

## License

AutoPrint is available under the MIT License. See [LICENSE](LICENSE) for details.
