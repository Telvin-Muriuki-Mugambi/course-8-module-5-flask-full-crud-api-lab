from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# List all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# Retrieve one event
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = next((item for item in events if item.id == event_id), None)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} was not found."}), 404

    return jsonify(event.to_dict()), 200

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    event_id = max((event.id for event in events), default=0) + 1
    event = Event(event_id, data["title"].strip())
    events.append(event)
    return jsonify(event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    event = next((item for item in events if item.id == event_id), None)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} was not found."}), 404

    event.title = data["title"].strip()
    return jsonify(event.to_dict()), 200

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((item for item in events if item.id == event_id), None)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} was not found."}), 404

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
