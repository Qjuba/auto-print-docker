# Współpraca przy AutoPrint

Dziękujemy za zainteresowanie projektem. Przed rozpoczęciem większej zmiany otwórz zgłoszenie i
opisz problem oraz proponowany kierunek rozwiązania.

## Środowisko lokalne

1. Utwórz środowisko Python 3.12 i zainstaluj `requirements-dev.txt`.
2. Uruchom `npm ci` oraz `npm run build:css`.
3. Przed wysłaniem zmiany wykonaj `ruff check app tests` i `pytest`.
4. Nie dodawaj pliku `.env`, bazy SQLite, uploadów, logów ani danych drukarki.

Zmiany interfejsu powinny działać na telefonie i komputerze, zachowywać obsługę klawiatury oraz
nie pobierać skryptów, stylów ani fontów z zewnętrznych CDN.

## Pull request

Pull request powinien zawierać krótki opis problemu, zakres zmiany, sposób weryfikacji i — przy
zmianach wizualnych — zrzut ekranu. Przed wysłaniem zmiany uruchom lokalnie testy i Ruff.
