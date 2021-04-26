# Jak podłączyć i używać bazy PostgreSQL

Gdy chcecie jej używać, to jest to wtedy config produkcyjny. Czyli normalnie polecam dalej korzystać z tej SQLite'owej. Also, z racji, że korzystam z MacOS nie ręczę, że wszystko będzie wyglądać identycznie. Ostatnia sprawa, póki co nazwę bazy danych hardcoduję, żeby nie komplikować działania CLI. Więc po prostu nazywajcie rzeczy tak samo jak ja i powinno być git. Jeśli jednak już by coś nie działało, to sprawdźcie `config.py`. Wracając:

## Instalacja

Jeżeli jeszcze nie macie, to zainstalujcie Postgresa [TUTAJ](https://www.postgresql.org/download/).

Polecam zainstalować też `pgAdmin 4`. Z tego co widzę, do pobrania jest pod Windowsa i MacOS (nie wiem jak pod Linuxem, też pewnie się da -- jak coś pisać). Ma bardzo ładny interfejs i można łatwo debugować połączenie i aktywność na bazie. Do pobrania [TUTAJ](https://www.pgadmin.org/download/).

Jak już odpalimy `pgAdmin 4` to po lewej w menu klikamy PPM na `Databases` i wybieramy `Create -> Database...`. Tam wprowadzamy nazwę `test_database` i klikamy `Save`. 

That's it. Teraz wystarczy odpalić aplikację z odpowiednim argumentem, a konkretnie
```
python run.py prod
```

Gdzie prod oznacza, że aplikacja wywoła się z konfigu `ProductionConfig`. Jeżeli chcemy wrócić do używania bazy SQLite'owej to po prostu uruchamiamy apkę normalnie:
```
python run.py
```

Oczywiście przypominam, że korzystamy z `pipenv` (`pipenv shell`) i jak wam coś nie działa, to prawdopodobnie nie pobraliście wszystkich rzeczy z `Pipfile` (komenda `pipenv sync`).

## Domyślne wartości

* Nazwa serwera: `postgres`
* Hasło: `1234`
* Połączenie: `localhost`
* Nazwa bazy: `test_database`
