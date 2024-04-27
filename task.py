import requests
import socket
import agent

def get_ip(host):
    try:
        result = socket.getaddrinfo(host, None)
        return result
    except Exception as e:
        return f"Error in finding the IP: {e}"

def temp_room(room):
    return "Temp = 20, Humidity = 70"  # Fixed the return statement

def temp_city(city):
    url = "https://tomorrow-io1.p.rapidapi.com/v4/weather/forecast"
    querystring = {"location": city, "timesteps": "1h", "units": "metric"}
    headers = {
        "X-RapidAPI-Key": "2119d7e64emshe0d803918a72e30p1da392jsn72cff23ce386",
        "X-RapidAPI-Host": "tomorrow-io1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            hourly_forecast = data.get("timelines", {}).get("hourly", [])
            if hourly_forecast:
                first_hour_data = hourly_forecast[0]
                temperature = first_hour_data.get("values", {}).get("temperature")
                humidity = first_hour_data.get("values", {}).get("humidity")
                return f"Humidity: {humidity}, Temp in C: {temperature}"
            else:
                return "Hourly forecast data not available"
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def generate_content(query):
    key = "AIzaSyD_iEtIx2I9aA5zjS4Z-y1MCMdsdIcftV4"
    messages = [{"role": "user", "parts": [{"text": query}]}]
    data = {"contents": messages}
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + key
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            content = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
            print("Gemini Response:", content)
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Error: {e}")

 
definitions = [
    {
        "name": "generate_content",
        "description": "Generate content based on user query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Full query asked by user"
                }
            }
        }
    },
    {
        "name": "temp_city",
        "description": "Find weather and temperature of a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City to find weather"
                }
            }
        }
    },
    {
        "name": "temp_room",
        "description": "Find temperature of a room or home",
        "parameters": {
            "type": "object",
            "properties": {
                "room": {
                    "type": "string",
                    "description": "Room or home"
                }
            }
        }
    },
    {
        "name": "get_ip",
        "description": "Find IP address of a given URL or domain name",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "URL or domain name"
                }
            }
        }
    },
]

if __name__ == "__main__":
    print(temp_city("Kolkata"))  # Example usage of temp_city function