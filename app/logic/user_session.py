# user_session.py
current_user = {"user_id": None, "username": None}

def set_active_user(user_id, username):
    global current_user
    current_user["user_id"] = user_id
    current_user["username"] = username

def get_active_user_id():
    return current_user["user_id"]

def clear_active_user():
    global current_user
    current_user = {"user_id": None, "username": None}