# Client - Crossref API

[***Habanero***](https://github.com/sckott/habanero/) wrapper.

- backend: **Python** (*habanero*) using *flask_socketio* and *flask*.

- frontend (tests only): **Javascript** using *socket.io* and *express*.

The goal of this repository is to code a wrapper on the *Crossref API* client
called *Habanero*.

## Environment variables

TODO

## Production mode

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

# TODO
```

## Security

1. **HTTPS**:

TODO (certificates)

2. **Token authentication JWT**:

TODO

3. **CORS**:

TODO

### EOF

