# Bezpieczeństwo

Nie publikuj podatności w zwykłym zgłoszeniu. Użyj prywatnego zgłoszenia bezpieczeństwa GitHub:
**Security → Advisories → New draft security advisory** w publicznym repozytorium projektu.

W zgłoszeniu podaj wersję lub identyfikator commita, opis wpływu, kroki reprodukcji i — jeśli jest
znane — proponowane rozwiązanie. Nie dołączaj prawdziwych haseł, plików `.env`, adresów urządzeń ani
danych wydruków.

Projekt nie jest przeznaczony do bezpośredniego wystawiania w Internecie. Przy dostępie spoza
zaufanej sieci należy włączyć logowanie, HTTPS i reverse proxy oraz ustawić
`SESSION_COOKIE_SECURE=true`.
