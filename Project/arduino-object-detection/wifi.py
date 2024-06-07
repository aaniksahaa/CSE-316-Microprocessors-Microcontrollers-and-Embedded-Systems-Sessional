import websocket
import requests
import time

def send_data():
    url = "ws://192.168.154.131:81/"  # replace with the WebSocket server URL

    # Connect to the WebSocket server
    ws = websocket.create_connection(url)

        
    while(True):
        message = "w"
        ws.send(message)
        print(f"Sent: {message}")
        time.sleep(1)
    

# Run the function
send_data()
