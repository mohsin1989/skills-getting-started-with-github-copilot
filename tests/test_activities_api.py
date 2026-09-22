import importlib

from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")
app = app_module.app
client = TestClient(app)


def setup_function():
    app_module.activities["Soccer Club"]["participants"] = []
    app_module.activities["Track and Field"]["participants"] = []


def test_get_activities_returns_activity_data():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Soccer Club" in body
    assert "participants" in body["Soccer Club"]


def test_signup_for_activity_adds_participant():
    # Arrange
    email = "alice@mergington.edu"

    # Act
    response = client.post(f"/activities/Soccer Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Soccer Club"
    assert email in app_module.activities["Soccer Club"]["participants"]


def test_signup_rejects_duplicate_participant():
    # Arrange
    email = "alice@mergington.edu"
    app_module.activities["Soccer Club"]["participants"] = [email]

    # Act
    response = client.post(f"/activities/Soccer Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_missing_activity():
    # Arrange

    # Act
    response = client.post("/activities/Unknown Club/signup?email=test@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_unregisters_student():
    # Arrange
    email = "alice@mergington.edu"
    app_module.activities["Soccer Club"]["participants"] = [email]

    # Act
    response = client.delete(f"/activities/Soccer Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Soccer Club"
    assert email not in app_module.activities["Soccer Club"]["participants"]


def test_remove_participant_returns_404_for_missing_student():
    # Arrange

    # Act
    response = client.delete("/activities/Track and Field/participants/missing@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
