# Team Management System

Jest to aplikacja służąca do zarządzania zespołami projektowymi. Umożliwia zarządzanie użytkownikami, projektami,
członkami projektu, tablicami projektowymi oraz zadaniami. Zaimplementowana została funkcjonalność, która pozwala 
na ewaluacje efektywności pracy członków projektów, co ułatwi dobór osób dla nowych projektów.

W celu uruchomienia aplikacji należy posiadać zainstalowane narzędzie docker compose.

Zmienne środowiskowe zostały zdefiniowane w plikach *docker/.db.env* oraz *docker/.django.env*. 
Zmienne, które mają wartość `PLEASE_CHANGE_THIS` należy zmodyfikować.
Należy również zmodyfikować nazwę oraz domenę dla aplikacji. Ich wartości są określone w pliku 
`backend/accounts/fixtures/sites.json`. 

Wymagane zależności dla serwera można zmodyfikować, w tym celu wymagane jest zainstalowanie narzędzia Poetry, 
przykłady użycia dostępne są w jego [dokumentacji](https://python-poetry.org/docs/).

Sposoby instalacji:
1. Instancja lokalna
   1. Wersja z danymi demonstracyjnymi:
   Uruchomienie skryptu inicjalizującego poprzez komendę `bash bin/dev_init.sh` z poziomu katalogu głównego projektu.
   
   2. Wersja bez danych demonstracyjnych:
   Polega na uruchomieniu ciągu komend z poziomu katalogu głównego projektu. Pierwsza z nich odpowiada za budowę 
   kontenera `docker compose build`. Następnie należy przeprowadzić migrację do bazy danych
   `docker compose run --rm django python manage.py migrate`. Kolejno możemy załadować instancję modelu witryny 
   `docker compose run --rm django python manage.py loaddata sites.json` oraz utworzyć super użytkownika na podstawie 
   zmiennych środowiskowych `docker compose run --rm django python manage.py createsuperuser --no-input`. 
   
2. Instancja bazująca na gotowym obrazie - w planach na przyszłość 

Uruchomienie zainstalowanej instancji sprowadza się jedynie do uruchomienia konteneru `docker compose up` lub 
`docker compose up --detach`. Ustawienie flagi detach uruchamia kontener w tle i nie mamy bezpośrednio dostępu
do informacji generowanych przez serwer.

Administracja systemu sprowadza się do dwóch przypadków:
1. Instancja lokalna:
   1. W celu modyfikacji kodu aplikacji wystarczy zmodyfikować lokalnie kod źródłowy aplikacji, a zmiany powinny
   się automatycznie przeładować na serwerze. Jeśli tak sie nie dzieje, należy uruchomić ponownie kontener:
   `docker compose stop`, a następnie `docker compose up`.
   
   2. W celu usunięcia konteneru i wyczyszczenia powiązanych danych należy wykonać komendę `bash bin/dev_clear.sh`.
   
2. Instancja bazująca na gotowym obrazie - w planach na przyszłość
