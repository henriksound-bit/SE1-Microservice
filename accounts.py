import json
from server import *

accounts = {}
encoded_json = None
response_header = None

def route_request(request):
    """
    Takes the JSON request and parses it then calls the appropriate function based on
    the request type
    """
    if request["request"] == "create":
        create_account(request)
    elif request["request"] == "login":
        login(request)
    elif request["request"] == "edit":
        edit(request)
    elif request["request"] == "retrieve":
        retrieve(request)

    return


def create_account(request):
    """
    Creates a new user account. Verifies username is not a duplicate.
    Requires: username, password, and user_data
    returns: 0 with "account created' msg on success, 1 with error message if unsuccessful
            ex. {"0": "account created"}
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("Username required")

    if username in accounts:
        error("Username already in use")

    try:
        if request["password"]:
            password = request["password"]
    except KeyError:
        error("password required")

    try:
        if request["user_data"]:
            user_data = request["user_data"]
    except KeyError:
        error("user_data required")

    accounts[username] = {"password": password, "user_data": user_data}

    build_response({"0": "account created"})

    return


def login(request):
    """
    Logs in the user specified in the request. Verifies existence of username and matching password
    for that username.
    Requires: username, password
    returns: 0 with "logged in" msg on success, 1 with "invalid user" msg, 2 with "incorrect password" msg
            ex. {"0": "logged in"}
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    if username not in accounts:
        error("Username does not exist")

    try:
        if request["password"]:
            password = request["password"]
    except KeyError:
        error("password required")

    if accounts[username][password] == password:
        build_response({"0": "logged in"})
    else:
        build_response({"2": "incorrect password"})

    return


def edit(request):
    """
    Edits the user_data field for the specified user.
    Requires: username, new_user_data
    returns: 0 with "updated user_data" msg on success, 1 with "invalid user" msg
            ex. {"0": "updated user_data"}
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    try:
        if request["user_data"]:
            new_user_data = request["new_user_data"]
    except KeyError:
        error("new user_data required")

    accounts[username]["user_data"] = new_user_data


    return


def retrieve(request):
    """
    Returns all account information for the specified user. Verifies existence of user.
    requires: username
    Returns: on success returns account as JSON ex. {"username":{username}, "password":{password},
            "user_data":{user_data}"
            1 with "invalid user" msg on failure
    """

    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    build_response(accounts[username])

    return


def error(error_msg):
    response = {"1": error_msg}
    build_response(response)

    return


def format_response_header(pre_response):
    """
    Create JSON response header
    """
    response_len = len(pre_response)
    response_header = str(response_len).encode('utf-8')
    response_header += b' ' * (1024 - len(response_header))
    return response_header


def build_response(json_response):
    """
    Encodes unencoded JSON and then retrieves the response header
    """
    encoded_json = json.dumps(json_response).encode('utf-8')
    response_header = format_response_header(encoded_json)

    send_response(response_header, encoded_json)

    return