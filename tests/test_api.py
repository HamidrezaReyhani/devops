import pytest

@pytest.fixture
def client():
    from app.main import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """تست اندپوینت /health"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_data_endpoint(client, mock_db_connection):
    """تست اندپوینت /data با استفاده از mock دیتابیس"""
    response = client.get('/data')
    assert response.status_code == 200
    assert 'db_time' in response.json
    # این خط باید دقیقاً با مقداری که مک برمی‌گرداند مطابقت داشته باشد
    assert response.json['db_time'] == 'test_data'
    mock_db_connection.execute.assert_called_once_with("SELECT NOW();")

def test_data_endpoint_db_failure(client, mock_db_connection):
    """تست رفتار اپلیکیشن هنگام خطا در اتصال دیتابیس"""
    mock_db_connection.execute.side_effect = Exception("DB connection error")
    response = client.get('/data')
    assert response.status_code == 500
    assert response.json['error'] == "DB connection error"

def test_health_endpoint_no_db_connection(client):
    """تست endpoint /health بدون نیاز به دیتابیس"""
    response = client.get('/health')
    assert response.status_code == 200
    # مطمئن شوید health check به دیتابیس وابسته نیست