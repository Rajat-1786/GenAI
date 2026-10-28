messages = {

}

def add_user_message(user_name, message):
    if user_name not in messages:
        messages[user_name] = []
    messages[user_name].append({"role":"user", "content": message})

def add_assistant_message(user_name, message):
    if user_name not in messages:
        messages[user_name] = []
    messages[user_name].append({"role":"assistant", "content": message})