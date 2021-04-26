# Backend aplikacji - Zespół 7

### Dokumentacja

Dokumentacja jest oparta na SwaggerUI. Można tam sobie przetestować poszczególne endpointy. Dostępna jest pod adresem: [localhost:5000/api](http://localhost:5000/api). Jest to redirect na stronę parsującą wygenerowany dokument Swaggera.

### Korzystanie z Pip

Korzystamy z `pipenv`, żeby mieć zgodne wersje bibliotek. Wymagane paczki i ustawienia można podejrzeć w pliku `Pipfile`.

Po zainstalowaniu `pipenv` i pobraniu repozytorium trzeba wpisać:
```
pipenv shell      (uruchamia wirtualne srodowisko)
pipenv sync       (pobiera wszystkie dependencies z Pipfile.lock)
```

Potem jako, że korzystamy już z `pipenv` to aby uruchomić aplikację wystarczy wpisać
```
python run.py
```

### Baza

Domyślnie (dev) używamy `SQLite`, w produkcji jednak używamy `Postgres`. Jak zainstalować i obsługiwać sprawdźcie [DATABASE.md](DATABASE.md).

### Testy

Do testów używamy `unittest`. Testy podzielone są na kilka plików.

Uruchamianie (wszystkie testy na raz):
```
python -m unittest discover tests
```
Uruchamianie (pojedynczego przykladowego testu):
```
python -m unittest tests/test_users.py
```

### Kontrybucje

Ogólnie prośba, żeby commity pisać po angielsku (albo przynajmniej Pull Requesty, bo potem i tak to mergujemy do jednego commitu). Tak będzie czytelniej i łatwiej, nie będzie problemów z jakimś kodowaniem na kiju czy coś. Also trzymajmy się jednej funkcjonalności, nad którą akurat pracujemy, bo potem w razie jakichś problemów łatwiej będzie nam ewentualnie do tego wrócić. 
