import httpx
import re
import json
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

def habanero_query(query: str, publisher: str = None) -> str:
    """
    :param query: `Title, author, DOI, ORCID iD, etc..`
    :param publisher: special parameter to find related publications.
        This parameter is usually the `container-title` of the response.
    :return: the result of ``habanero.Crossref.works()``. It is various *json*.
    :return: the result is a string, an error never starts with `{`.
    """
    # Detect if the query is actually a concatenation of *DOI*s.
    regex: str = r'10\.\d{4,9}/[\w.\-;()/:]+'
    ids: list[str] = re.findall(regex, query)

    filtering: dict = {
        #'type': 'journal-article',
    }

    # TODO: this thing does not work I don't know why.
    if publisher != None:
        filtering['container-title'] = publisher
    # </TODO>

    # "Don't use *rows* and *offset* in the */works* route.
    # They are very expansive and slow. Use cursors instead."
    offset: float = None

    limit: float = 10 # Default is 20
    sort: str = "relevance"
    order: str = "desc"

    # TODO: find a way to retrieve the publication abstract,
    #       there are too many retrieved publications for which only
    #       the title is public.
    #       Need to recursively retrieve publications from references etc..
    facet: str | bool | None = None # "relation-type:5"
    # </TODO>

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

    # TODO: add cursors on the *frontend*.
    cursor: str = "*"
    cursor: str = None # Cursor can't be combined with *offset* or *sample*.
    cursor_max: float = 10
    # <TODO>

    progress_bar: bool = False

    try:
        if len(ids) > 0:
            # Here, there is only one result (wo `items`),
            # but I want to get something generic in a `items` attribute.
            result: dict[str, dict] = cr.works(ids = ids)
            results: dict[str, dict] = { 'message': { 'items': [ result['message'] ] } }
            return json.dumps(results)

        return json.dumps(
                cr.works(
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
                progress_bar = progress_bar
            )
        )
    except httpx.HTTPStatusError as e:
        print(f'\n{e}\n')
        return e.__str__()[:92] + " ..."
    except RequestError as e:
        print(f'\n{e}\n')
        return e.__str__()[:92] + " ..."
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

    results: str = habanero_query(query, publisher)
    print(results)

    if not results.startswith('{'):
        emit("search_error", { 'error': results }, to=request.sid)
    else:
        emit("search_results", { 'results': results }, to=request.sid)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the backend"""
    print(f'client number {request.sid} is disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=BACKEND_PORT)

