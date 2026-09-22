import importlib

from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")
app = app_module.app
client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Soccer Club"
    email = "alice@mergington.edu"

    app_module.activities[activity_name]["participants"] = []

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_participant_returns_404_when_missing():
    activity_name = "Track and Field"
    email = "missing@mergington.edu"

    app_module.activities[activity_name]["participants"] = []

    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
