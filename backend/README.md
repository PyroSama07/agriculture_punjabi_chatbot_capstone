# Prerequisites

- Add secret key in main.py

to create secret key run= `openssl rand -hex 32` in your terminal.

- Change database url in database.py

- Rochak's service at get_responce_RAG() in main.py

## Run

`uvicorn main:app --reload`

## In code

database used in code -> db_example

tables in database -> chat, users

![Structure of tables](st.jpg)
