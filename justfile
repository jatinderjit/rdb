run:
    python main.py

# KEY should be url encoded
db_get KEY:
    @curl "http://localhost:4000/get?key={{ KEY }}"

# KEY and VALUE should be url encoded
db_set KEY VALUE:
    @curl "http://localhost:4000/set?{{ KEY }}={{ VALUE }}"
