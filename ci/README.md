# Jenkins — testy integracyjne

`Jenkinsfile` ładuje `ci/integration.groovy`. Pipeline buduje obraz z
`ci/Dockerfile`, dzieli wykonania testów między niezależne kontenery,
uruchamia je równolegle i zbiera raporty JUnit oraz logi.

## Uruchomienie

1. Przygotuj Jenkins i agenta Linux z etykietą `linux-docker`, Git, Docker CLI
   i dostępem do działającego demona Docker oraz rejestrów obrazów i pip.
   Pipeline używa `sh`, więc agent musi działać na Linuksie, także gdy hostem
   jest Windows. Kontener kontrolera Jenkins sam nie tworzy takiego agenta.
2. Zainstaluj wtyczki Pipeline, Git, Pipeline Utility Steps oraz JUnit.
   Docker Pipeline nie jest potrzebny, ponieważ używamy Docker CLI.
3. Zapisz pliki w repozytorium Git i wypchnij zmiany.
4. Utwórz zadanie Pipeline → Pipeline script from SCM. Wskaż repozytorium,
   branch i plik `Jenkinsfile`. Dla prywatnego repozytorium ustaw credentials.
5. Pierwszy build zarejestruje parametry i użyje wartości domyślnych.
   Kolejne uruchamiaj przez Build with Parameters.

Te pliki konfigurują zadanie CI; nie instalują serwera Jenkins ani agenta.
Agent z dostępem do Docker powinien wykonywać kod z zaufanych repozytoriów.

## Plan testów

Parametr `TEST_CONFIG` to ścieżka JSON w checkoutowanym repozytorium,
domyślnie `ci/tests.json`. Nie jest to upload pliku z komputera użytkownika.

```json
{
  "containers": 2,
  "timeout_minutes": 10,
  "tests": [
    {"nodeid": "tests/integration/test_cli.py::test_help", "repeat": 3},
    {"nodeid": "tests/integration/test_cli.py::test_unknown_command", "repeat": 1}
  ]
}
```

Przykład oznacza 4 wykonania, po 2 na kontener. Liczba wykonań jest sumą
`repeat`. Powtórzenia odbywają się niezależnie od wyniku poprzedniego testu.
Każdy kontener wykonuje przydzielone testy kolejno; kontenery działają
równolegle na jednym agencie. Nie są usługami wspólnego scenariusza.
Testy powinny izolować swoje dane, np. przez fixture `tmp_path`.

Obsługiwane są selektory pojedynczych funkcji `test_*` w plikach Python
pod `tests/integration`, również w podkatalogach. Selektory klas i pojedynczych
wariantów parametryzacji nie są obsługiwane. Funkcja parametryzowana uruchamia
wszystkie warianty w ramach jednego wykonania.

Limity: 1–32 kontenery (nie więcej niż wykonań), 1–100 powtórzeń na wpis,
1000 wykonań łącznie, 1–50 minut na kontener i 60 minut na cały pipeline.
Podział uwzględnia liczbę wykonań, a nie przewidywany czas testów.

## Wersja pyvcs

Parametr `PYVCS_VERSION` przyjmuje:

- `workspace`: instalacja kodu z checkoutu Jenkins. Aby testować konkretny
  tag lub commit, ustaw ten ref w konfiguracji SCM zadania. Ref musi zawierać
  pliki CI i testy.
- Dokładną wersję, np. `0.1.0`: instalacja `pyvcs==0.1.0` z publicznego
  rejestru pip. Pakiet musi być wcześniej opublikowany i należeć do tego
  projektu. Sam numer w `pyproject.toml` nie publikuje pakietu.

Jeśli projekt nie jest opublikowany, użyj `workspace` i taga/commita Git.
Prywatny rejestr wymaga dodatkowej konfiguracji adresu i credentials podczas
budowania obrazu. Nie zapisuj haseł w JSON ani Dockerfile.

Testy zawsze pochodzą z checkoutu zadania, także przy instalacji innej wersji.
Kod `src` nie trafia do katalogu wykonywania testów; testowana jest
zainstalowana dystrybucja. Obecne testy uruchamiają rzeczywistą komendę
`pyvcs` i sprawdzają pomoc oraz błędne argumenty. `init` nie implementuje
jeszcze tworzenia repozytorium.

## Wyniki

Jenkins publikuje raporty JUnit oraz archiwizuje `ci-results/`: plan,
przydział testów, logi/XML poszczególnych wykonań, wersję pyvcs i `pip freeze`.
Błąd testu lub infrastruktury powoduje niepowodzenie buildu. Pozostałe
kontenery mogą dokończyć testy. Częściowe raporty po timeout trafiają do
artefaktów, jeśli uda się je skopiować z kontenera.

Kontenery kończą się wraz z runnerem i są usuwane w `finally`, podobnie jak
obraz buildu. Nie wymagają `sleep infinity`. Utrata agenta lub awaria Docker
może wymagać ręcznego sprzątania.

## Sprawdzenie obrazu bez Jenkins

Z głównego katalogu repozytorium:

```sh
docker build -f ci/Dockerfile --build-arg PYVCS_VERSION=workspace -t pyvcs-ci:local .
docker run --rm pyvcs-ci:local python -m pytest -v tests/integration
```

Te polecenia wykonują wszystkie testy integracyjne raz. Plan JSON, powtórzenia
i podział na kontenery obsługuje pipeline Groovy.

Dokumentacja: [Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/),
[JSON](https://www.jenkins.io/doc/pipeline/steps/pipeline-utility-steps/),
[JUnit](https://www.jenkins.io/doc/pipeline/steps/junit/).
