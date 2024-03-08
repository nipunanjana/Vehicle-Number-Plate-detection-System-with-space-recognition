import socketio

authToken = "your_secret_token"  # Replace with your actual token
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def parkingStatus(data):
    # Handle parking status updates (replace with your logic)
    print("Parking space ID:", data["spaceId"], "Availability:", data["availability"])

# Function to simulate form submission (since Python doesn't have browser events)
def submit_form():
    spaceId = input("Enter space ID: ")
    availability = bool(input("Enter availability (True/False): "))
    sio.emit("parkingStatus", {"spaceId": spaceId, "availability": availability})

sio.connect("http://localhost:3000", auth={"token": authToken})

# Example usage:
submit_form()  # Call this to simulate form submission

# Keep the client running to handle events
sio.wait()
