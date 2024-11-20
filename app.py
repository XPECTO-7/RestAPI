from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data store
tasks = [
    {
    "description": "Learn Flask",
    "done": True,
    "id": 1,
    "title": "Task 1"
  },
  
  {
    "description": "Learn RestAPI",
    "done": True,
    "id": 2,
    "title": "Task 2"
  },
  {
    "description": "Learn Swagger",
    "done": True,
    "id": 3,
    "title": "Task 3"
  }
]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Get a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Invalid input"}), 400
    
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,  # Generate new ID
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "done": request.json.get("done", False),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    if not request.json:
        return jsonify({"error": "Invalid input"}), 400
    
    task["title"] = request.json.get("title", task["title"])
    task["description"] = request.json.get("description", task["description"])
    task["done"] = request.json.get("done", task["done"])
    return jsonify(task)

#Patch Method
@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.update(data)
    return jsonify(task)



# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"result": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
