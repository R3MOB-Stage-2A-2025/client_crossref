import httpx
import re
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Retrieve environment variables.
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
BACKEND_PORT: int = int(os.getenv("BACKEND_PORT"))
BACKEND_SECRETKEY: str = os.getenv("BACKEND_SECRETKEY")

HABANERO_BASEURL: str = os.getenv("HABANERO_BASEURL")
HABANERO_APIKEY: str = os.getenv("HABANERO_APIKEY")
HABANERO_MAILTO: str = os.getenv("HABANERO_MAILTO")
HABANERO_TIMEOUT: int = int(os.getenv("HABANERO_TIMEOUT")) # seconds
# </Retrieve environment variables>

# Habanero Initialization
from habanero import Crossref, RequestError

xrate_limit: str = "" "X-Rate-Limit-Limit: 100"
xrate_interval: str = "" "X-Rate-Limit-Interval: 1s"
ua_string: str = xrate_limit + ";" + xrate_interval

cr: Crossref = Crossref(
    base_url = HABANERO_BASEURL,
    api_key = HABANERO_APIKEY,
    mailto = HABANERO_MAILTO,
    ua_string = ua_string,
    timeout = HABANERO_TIMEOUT
)

def habanero_query(query: str, publisher: str = None) -> dict[str, dict] | str:
    """
    :param query: `Title, author, DOI, ORCID iD, etc..`
    :param publisher: special parameter to find related publications.
        This parameter is usually the `container-title` of the response.
    :return: the result of ``habanero.Crossref.works()``. It is various *json*.
    :return: the result is a string only if there is an error.
    """
    # Detect if the query is actually a concatenation of *DOI*s.
    regex: str = r'10\.\d{4,9}/[\w.\-;()/:]+'
    ids: list[str] = re.findall(regex, query)

    filtering: dict = {
        #'type': 'journal-article',
    }

    # "Don't use *rows* and *offset* in the */works* route.
    # They are very expansive and slow. Use cursors instead."
    offset: float = None

    limit: float = 10 # Default is 20
    sort: str = "relevance"
    order: str = "desc"

    facet: str | bool | None = None # "relation-type:5"

    # What could happen:
    #   - the *abstract* is located in the *title* section.
    #   - *subject* is almost never present.
    #   - the *issn-value*: is too generic. (ex: "Electronic")
    #   - there could be A LOT of authors. (too many).
    select: list[str] | str | None = [
        "DOI",
        "type",
        "container-title",
        "issn-type",
        "subject",
        "title",
        "abstract",
        "publisher",
        "author",
        "created",
        "URL",
        "references-count", # ]
        "reference",        # ] what the publication is citing.
    ]

    cursor: str = "*"
    cursor: str = None # Cursor can't be combined with *offset* or *sample*.
    cursor_max: float = 10

    progress_bar: bool = False

    try:
        if len(ids) > 0:
            return cr.works(
                ids = ids
            )

        return cr.works(
            query = query,
            filter = filtering,
            offset = offset,
            limit = limit,
            sort = sort,
            order = order,
            facet = facet,
            select = select,
            cursor = cursor,
            cursor_max = cursor_max,
            progress_bar = progress_bar,
            publisher = publisher
        )
    except httpx.HTTPStatusError as e:
        print(f'\n{e}\n')
        return e.__str__()
    except RequestError as e:
        print(f'\n{e}\n')
        return e.__str__()
    except RuntimeError as e:
        print(f'\n{e}\n')
        return e.__str__()

# </Habanero Initialization>

app = Flask(__name__)
app.config['SECRET_KEY'] = BACKEND_SECRETKEY
CORS(app, resources={r"/*": { "origins": "*" }})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def connected():
    """event listener when client connects to the backend"""
    print(f'client number {request.sid} is connected')

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))

@socketio.on("search_query")
def handle_search_query(query: str, publisher: str = None):
    print(f"Search query received: {query}")
    if publisher != None:
        print(f"Publisher received: {publisher}")

    results: dict[str, dict] = habanero_query(query, publisher)
    print(results)
    emit("search_results", { "results": results }, to=request.sid)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the backend"""
    print(f'client number {request.sid} is disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=BACKEND_PORT)

