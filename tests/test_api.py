import pytest
from httpx import AsyncClient, ASGITransport
from main import app


# --- Fixture ---
# זהו "כלי עזר" שרץ לפני כל טסט ומכין לנו את הקליינט
# חוסך לנו לכתוב את השורות האלו שוב ושוב בכל פונקציה
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# --- General Tests ---

@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "Welcome to Employee Management API" in response.json()["message"]


@pytest.mark.asyncio
async def test_health(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# --- Employee Tests ---

@pytest.mark.asyncio
async def test_create_employee(async_client):
    payload = {
        "id": "TEST_EMP_01",
        "first_name": "Test",
        "last_name": "User",
        "office_name": "Test Lab",
        "job_title": "Tester"
    }
    response = await async_client.post("/api/employees", json=payload)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"


@pytest.mark.asyncio
async def test_get_employees(async_client):
    response = await async_client.get("/api/employees")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Should have sample data + created test user


@pytest.mark.asyncio
async def test_get_employee_by_id(async_client):
    # נסתמך על העובד שיצרנו בטסט הקודם (או ניצור חדש אם הטסטים רצים במקביל)
    # לצורך הפשטות נניח שהם רצים סדרתית או נשתמש בנתוני דוגמה
    response = await async_client.get("/api/employees/E001")  # E001 קיים בנתוני דוגמה
    assert response.status_code == 200
    assert response.json()["id"] == "E001"


@pytest.mark.asyncio
async def test_update_employee(async_client):
    # נעדכן את E002
    payload = {"job_title": "Senior Manager"}
    response = await async_client.put("/api/employees/E002", json=payload)
    assert response.status_code == 200
    assert response.json()["job_title"] == "Senior Manager"


@pytest.mark.asyncio
async def test_delete_employee(async_client):
    # ניצור עובד זמני רק כדי למחוק אותו
    temp_emp = {
        "id": "DEL_ME", "first_name": "D", "last_name": "L", "office_name": "O", "job_title": "J"
    }
    await async_client.post("/api/employees", json=temp_emp)

    # נמחק אותו
    response = await async_client.delete("/api/employees/DEL_ME")
    assert response.status_code == 200

    # נוודא שהוא נמחק
    check = await async_client.get("/api/employees/DEL_ME")
    assert check.status_code == 404


# --- Mission Tests ---

@pytest.mark.asyncio
async def test_create_mission(async_client):
    payload = {
        "id": "TEST_MISSION_01",
        "title": "Test Mission",
        "assigned_to": "E001",  # חייב להיות עובד קיים
        "status": "Pending",
        "priority": "Low",
        "deadline": "2026-01-01"
    }
    response = await async_client.post("/api/missions", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Mission"


@pytest.mark.asyncio
async def test_get_missions(async_client):
    response = await async_client.get("/api/missions")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_mission_by_id(async_client):
    response = await async_client.get("/api/missions/M001")  # M001 קיים בדוגמה
    assert response.status_code == 200
    assert response.json()["id"] == "M001"


@pytest.mark.asyncio
async def test_get_missions_by_employee(async_client):
    response = await async_client.get("/api/missions/employee/E001")
    assert response.status_code == 200
    # E001 אמור לקבל לפחות משימה אחת מהדוגמה
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_mission(async_client):
    payload = {"status": "Completed"}
    response = await async_client.put("/api/missions/M002", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"


@pytest.mark.asyncio
async def test_delete_mission(async_client):
    # ניצור משימה למחיקה
    temp_mission = {
        "id": "DEL_MISS", "title": "T", "assigned_to": "E001",
        "status": "Pending", "priority": "Low", "deadline": "2025"
    }
    await async_client.post("/api/missions", json=temp_mission)

    response = await async_client.delete("/api/missions/DEL_MISS")
    assert response.status_code == 200

    check = await async_client.get("/api/missions/DEL_MISS")
    assert check.status_code == 404


# --- Analysis Tests ---

@pytest.mark.asyncio
async def test_analysis_employees(async_client):
    response = await async_client.get("/api/analysis/employees")
    assert response.status_code == 200
    data = response.json()
    assert "total_employees" in data
    assert "by_office" in data


@pytest.mark.asyncio
async def test_analysis_missions(async_client):
    response = await async_client.get("/api/analysis/missions")
    assert response.status_code == 200
    data = response.json()
    assert "total_missions" in data
    assert "by_status" in data


@pytest.mark.asyncio
async def test_analysis_workload(async_client):
    response = await async_client.get("/api/analysis/workload")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_analysis_summary(async_client):
    response = await async_client.get("/api/analysis/summary")
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert "missions" in data