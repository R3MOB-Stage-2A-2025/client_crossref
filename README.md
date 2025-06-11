# Client - Crossref API

[***Habanero***](https://github.com/sckott/habanero/) wrapper.

- backend: **Python** (*habanero*) using *socket-io Python*.

- frontend (tests only): **Javascript** using *socket-io JS*.

The goal of this repository is to code a wrapper on the *Crossref API* client
called *Habanero*.

## TODO

1. ``cd client_crossref/``

2. Initialize the backend:

```bash
# Open another terminal and do this:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src/backend/ && python app.py
```

3. Tests only, use the frontend:

```bash
# Open another terminal and do this:
cd src/frontend/ && npm install
```

### EOF

