# Team Management System

Wersja rozwojowa - ALPHA

Jest to aplikacja służąca do zarządzania zespołami projektowymi. Umożliwia zarządzanie użytkownikami, projektami,
członkami projektu, tablicami projektowymi oraz zadaniami. Zaimplementowana została funkcjonalność, która pozwala 
na ewaluacje efektywności pracy członków projektów, co ułatwi dobór osób dla nowych projektów.

W celu uruchomienia aplikacji należy posiadać zainstalowane narzędzie docker compose.

Zmienne środowiskowe o wartości `PLEASE_CHANGE_THIS` należy zmodyfikować w plikach *docker/.db.env* oraz *docker/.django.env*.
Wymagane zależności dla serwera można zmodyfikować, w tym celu wymagane jest zainstalowanie narzędzia Poetry, 
przykłady użycia dostępne są w jego [dokumentacji](https://python-poetry.org/docs/).

Do inicjalizacji działania aplikacji uruchamia się skrypt poprzez komendę `bash bin/dev_init.sh` z poziomu katalogu 
głównego projektu. W celu wyczyszczenia danych powiązanych z utworzonym kontenerem należy wykonać komendę
`bash bin/dev_clear.sh`. 