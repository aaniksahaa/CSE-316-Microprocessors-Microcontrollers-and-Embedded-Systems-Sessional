import websocket
import json

# Define the WebSocket server address
server_address = "ws://192.168.154.131:81/"

# Define the callback function to handle WebSocket events
def on_message(ws, message):
    # print("Received message:", message)
    pass

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed")

# Define the callback function to handle the WebSocket open event
def on_open(ws):
    print("WebSocket connection established")
    # Send data to the WebSocket server
    cnt = 0
    while True:
        if(cnt == 50):
            ws.send("")
            break
        ws.send("w")
        cnt += 1

# Create a WebSocket connection
ws = websocket.WebSocketApp(server_address,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Keep the WebSocket connection open
ws.run_forever()


