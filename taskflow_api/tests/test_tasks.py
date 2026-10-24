def test_create_task(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
    })

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert response.status_code == 201

    response = client.get("/tasks")
    tasks = response.json()

    assert response.status_code == 200  
    assert len(tasks) == 1
    assert tasks[0]["id"] == data["id"]
    assert tasks[0]["title"] == data["title"]
    assert tasks[0]["description"] == data["description"]
    assert tasks[0]["status"] == data["status"]

def test_get_task_by_id(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
    })

    data = response.json()

    response = client.get(f"/tasks/{data['id']}")
    task = response.json()

    assert response.status_code == 200
    assert task["id"] == data["id"]
    assert task["title"] == data["title"]
    assert task["description"] == data["description"]
    assert task["status"] == data["status"]

def test_update_task(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
    })

    data = response.json()

    response = client.put(f"/tasks/{data['id']}", json={
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "completed",
    })

    updated_task = response.json()

    assert response.status_code == 200
    assert updated_task["id"] == data["id"]
    assert updated_task["title"] == "Updated Task"
    assert updated_task["description"] == "Updated Description"
    assert updated_task["status"] == "completed"

def test_delete_task(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
    })

    assert response.status_code == 201
    data = response.json()

    response = client.delete(f"/tasks/{data['id']}")

    assert response.status_code == 204

    response = client.get(f"/tasks/{data['id']}")
    assert response.status_code == 404

def test_update_non_existent_task(client):
    response = client.put("/tasks/999", json={
        "title": "Non Existent Task",
        "description": "Non Existent Description",
        "status": "pending",
    })  
    assert response.status_code == 404

def test_delete_non_existent_task(client):  
    response = client.delete("/tasks/999")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Task Not Found"

def test_get_non_existent_task(client):
    response = client.get("/tasks/999")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Task not found"

def test_create_task_empty_title(client):
    response = client.post("/tasks", json={
        "title": "",
        "description": "Test Description",
        "status": "pending",
    })  
    data = response.json()
    assert response.status_code == 422