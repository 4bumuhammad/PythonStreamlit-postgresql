<p align="center">
    <img src="./gambar-petunjuk/streamlit_logo.png" alt="streamlit_logo" style="display: block; margin: 0 auto;">
</p>


# PythonStreamlit-postgresql
---

### Postgres dengan Docker Container

  ❯ docker run -d \
    --name postgres-container \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -p 5432:5432 \
    -v /Users/powercommerce/Documents/test/docker-mount/postgres:/var/lib/postgresql/data \
    postgres:16.1

- Test akses ke database postgresql

  ❯ psql -h <HOST-IP> -U postgres -d Superstore

### in host :

  ❯ pg_dump --version
    pg_dump (PostgreSQL) 16.1 (Homebrew)



---


### [PG_DUMP postgresql]

- Backup per-table:

    ❯ pg_dump -h <HOST-IP> -U postgres -W -d Superstore -t tablestatecity -F c -f /<path-directories>/dbpostgres_Superstore_tablestatecity_backup_$(date +"%Y%m%d_%H%M%S").dump

- Backup per-database:

    ❯ pg_dump -h <HOST-IP> -U postgres -d Superstore -F c -f /<path-directories>/dbpostgres_Superstore_backup_$(date +"%Y%m%d_%H%M%S").dump


- 

### [PG_RESTORE postgresql]

- Restore per-database

    ❯ pg_restore -h <HOST-IP> -U postgres -d Superstore /<path-directories>/dbpostgres_Superstore_backup_20240215_094515.dump



---


## BEGIN STREAMLIT PROJECT:

References : 
- components streamlit : --> https://components.streamlit.app


❯ cd <foldername-projects>

❯ python -m venv venv

❯ source ./venv/bin/activate


---

  ❯ pip install streamlit

  ❯ pip install streamlit-option-menu

  ❯ pip install streamlit-aggrid

---

### another packages for single compilations

  ❯ pip install opencv-python

  ❯ pip install qrcode

---

  ❯ pip install plotly 

  ❯ pip install openpyxl

  ❯ pip install matplotlib 


---

  ❯ pip install python-dotenv

  ❯ pip install psycopg2

  ❯ pip install sqlalchemy


---

### khusus untuk penggunaan Ubuntu 22.04 or latest

  ❯ python3 -m venv venvUbuntu

  ❯ source venvUbuntu/bin/activate

  ❯ pip install psycopg2-binary

  ❯ pip3 list | grep SQLAlchemy

      SQLAlchemy                        2.0.25


### menjalankan project:

  ❯ streamlit run ./<nama-file>.py  --server.port 8888