# AutoPrint

AutoPrint pomaga zapobiegać zasychaniu tuszu w drukarkach atramentowych. Automatycznie drukuje
wybrany plik według ustalonego harmonogramu, dzięki czemu drukarka jest regularnie używana nawet
wtedy, gdy przez dłuższy czas niczego nie drukujesz.

Aplikacja działa we własnej sieci, współpracuje z drukarkami obsługującymi IPP, AirPrint lub Mopria
i udostępnia prosty panel działający na komputerze oraz telefonie.

## Co potrafi

- automatycznie drukuje jeden wybrany plik;
- obsługuje PDF, PNG, JPG i TXT;
- pozwala drukować co określoną liczbę minut, godzin, dni lub tygodni;
- obsługuje wybrane dni tygodnia oraz wiele dni miesiąca;
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

## Rozwój projektu

Informacje dla osób rozwijających kod znajdują się w [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencja

AutoPrint jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku [LICENSE](LICENSE).
