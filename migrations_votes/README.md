Operacje z wersjonowaniem baz (alembic, python)

1) stworzyć na bazie własny schemat (jeśli używamy inny niż "public")
2) w pliku .env ustawić schemat i dane logowania do bazy
3) jeśli projekt ma już migracje -- wykonać (w terminalu) `alembic upgrade head`
4) tworzyć migracje przez `alembic revision -m 'info co migracja robi` (1-line najlepiej)
5) znaleźć w migrations/versions nowy plik .py z migracją
    - wyedytować funkcję `upgrade()` i `downgrade`
    - można użyć >1 polecenia sql w każdej
6) starać się napisać migracje tak, by:
    - mogły współpracować z możliwymi aktualnymi stanami bazy
    - wykonanie upgrade/downgrade prowadziło do stanu początkowego, czyli m.in.
        - wykonanie up/down/up było również możliwe

7) zmieniać stan bazy przez
    - `alembic upgrade head`
    - `alembic downgrade -1`
   
8) plik migracji wolno zmieniać _jedynie_ jeśli baza wcześniej jest z-downgrade'owana, 
   czyli jeśli edytowana migracja nie została jeszcze wykonana (na żadnym ze środowisk)
