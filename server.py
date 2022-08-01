from socket import *
import json

serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))
serverSocket.listen(1)

accounts = {}


def route_request(request):
    """
    Accepts JSON request, parses, and calls the appropriate function
    """
    if request["request"] == "create":
        print("\tRECEIVED request:: CREATE account")
        print("\t\t", request, "\n")
        create_account(request)
    elif request["request"] == "login":
        print("\tRECEIVED request:: LOG IN account")
        print("\t\t", request, "\n")
        login(request)
    elif request["request"] == "logout":
        print("\tRECEIVED request:: LOG OUT account")
        print("\t\t", request, "\n")
        logout(request)
    elif request["request"] == "edit":
        print("\tRECEIVED request:: EDIT account")
        print("\t\t", request, "\n")
        edit(request)
    elif request["request"] == "retrieve":
        print("\tRECEIVED request:: RETRIEVE account")
        print("\t\t", request, "\n")
        retrieve(request)

    return


def create_account(request):
    """
    Creates a new user account. Verifies username is not a duplicate.
    Requires: username, password, and user_data
    returns: 0 with "account created' msg on success, 1 with error message if unsuccessful
            ex. {"0": "account created"}
    Create account: verifies username is not duplicate, takes in account parameters, and creates account
    Returns =
    1 Error
    0 Account creation successful
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("Username required")
        return

    if username in accounts:
        error("Username already in use")
        return

    try:
        if request["password"]:
            password = request["password"]
    except KeyError:
        error("password required")
        return

    try:
        if request["user_data"]:
            user_data = request["user_data"]
    except KeyError:
        error("user_data required")
        return

    accounts[username] = {"password": password, "user_data": user_data, "logged_in": True}

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
        return

    if username not in accounts:
        error("invalid user")
        return

    try:
        if request["password"]:
            password = request["password"]
    except KeyError:
        error("password required")
        return

    if accounts[username]["password"] == password:
        accounts[username]["logged_in"] = True
        build_response({"0": "logged in"})
    else:
        build_response({"2": "incorrect password"})

    return


def logout(request):
    """
    Logs out the user specified in the request. Verifies existence of username and matching password
    for that username.
    Requires: username
    returns: 0 with "logged out" msg on success, 1 with "invalid user" msg
            ex. {"0": "logged in"}
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    if username not in accounts:
        error("invalid user")
    else:
        accounts[username]["logged_in"] = False
        build_response({"0": "logged Out"})


def edit(request):
    """
    Edits the user_data field for the specified user.
    Requires: username, new_user_data; User must be logged in
    returns: 0 with "updated user_data" msg on success, 1 with "invalid user" msg
            ex. {"0": "updated user_data"}
    """
    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    try:
        if request["new_user_data"]:
            new_user_data = request["new_user_data"]
    except KeyError:
        error("new user_data required")

    if accounts[username]["logged_in"]:
        accounts[username]["user_data"] = new_user_data
        build_response({"0": "updated user_data"})
    else:
        error("user not logged in")

    return


def retrieve(request):
    """
    Returns all account information for the specified user. Verifies existence of user.
    requires: username; User must be logged in
    Returns: on success returns account as JSON ex. {"username":{username}, "password":{password},
            "user_data":{user_data}"
            1 with "invalid user" msg on failure
    """

    try:
        if request["username"]:
            username = request["username"]
    except KeyError:
        error("username required")

    if accounts[username]["logged_in"]:
        build_response(accounts[username])
    else:
        error("user not logged in")

    return


def error(error_msg):
    response = {"1": error_msg}
    build_response(response)

    return


def format_response_header(pre_response):
    """
    Takes the encoded JSON response and creates the information that needs to be sent before it
    """
    response_len = len(pre_response)
    response_header = str(response_len).encode('utf-8')
    response_header += b' ' * (1024 - len(response_header))
    return response_header


def build_response(json_response):
    """
    Takes the unencoded JSON and encodes it and then retrieves the response header
    """
    encoded_json = json.dumps(json_response).encode('utf-8')
    response_header = format_response_header(encoded_json)
    print("\tSENDING RESPONSE: \n\t\t", json_response)
    send_response(response_header, encoded_json)

    return


def send_response(response_header, response_body):
    connectionSocket.send(response_header)
    connectionSocket.send(response_body)

    return


while True:
    print("\nServer waiting for message...")
    connectionSocket, addr = serverSocket.accept()

    # We expect the first 1024 bytes to tell us how long the next message will be
    msg_len = connectionSocket.recv(1024).decode('utf-8')
    msg_len = int(msg_len)

    # We receive the number of bytes we were told to expect (msg_len)
    receivedRaw = connectionSocket.recv(msg_len).decode('utf-8')
    received = json.loads(receivedRaw)
    route_request(received)