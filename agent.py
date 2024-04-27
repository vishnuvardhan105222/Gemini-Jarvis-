import requests
import task

# Define the API key
key = "AIzaSyD_iEtIx2I9aA5zjS4Z-y1MCMdsdIcftV4"

def parse_function_response(message):
    function_call = message[0].get("functionCall")
    if not function_call:
        return "No function call in the message"

    function_name = function_call.get("name")
    arguments = function_call.get("args", {})

    try:
        # Dynamically call the function based on the function name
        func = getattr(task, function_name)
        function_response = func(**arguments)
    except AttributeError:
        return f"Function '{function_name}' not found in task module"
    except Exception as e:
        return f"Error: {e}"
    
    return function_response

def run_conversation(user_message):
    messages = []  # List to store all messages

    system_message = """You are an AI bot that can do everything using function calls. 
                       When you are asked to do something, use the available function calls and 
                       then respond with a message"""
    message = {"role": "user", "parts": [{"text": system_message + "\n" + user_message}]}
    messages.append(message)

    data = {"contents": messages, "tools": [{"functionDeclarations": task.definitions}]}

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + key
    response = requests.post(url, json=data)

    if response.status_code != 200:
        print("Error:", response.text)
        return

    t1 = response.json()
    if "candidates" not in t1 or not t1["candidates"]:
        print("Error: No content in response")
        return

    message = t1["candidates"][0].get("content", {}).get("parts", [])
    if not message:
        print("Error: No content in response")
        return

    if "functionCall" in message[0]:
        # Call the function to parse the response
        resp1 = parse_function_response(message)
        print("Actual response:", resp1)
        return resp1
    else:
        print("No function call in response")

if __name__ == "__main__":
    user_message = "find the ip address of google.com"
    print(run_conversation(user_message))