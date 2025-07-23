import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["short_url"].endswith(data["short_code"])

def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={"url": "not-a-url"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_redirect_to_original_url(client):
    # Shorten URL
    post = client.post('/api/shorten', json={"url": "https://example.com"})
    code = post.get_json()["short_code"]

    # Redirect
    response = client.get(f'/{code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com"

def test_get_stats(client):
    # Shorten URL
    post = client.post('/api/shorten', json={"url": "https://example.com"})
    code = post.get_json()["short_code"]

    # Trigger two redirects
    client.get(f'/{code}')
    client.get(f'/{code}')

    # Check stats
    response = client.get(f'/api/stats/{code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["url"] == "https://example.com"
    assert data["clicks"] == 2
    assert "created_at" in data

def test_redirect_not_found(client):
    response = client.get('/abcdef')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_stats_not_found(client):
    response = client.get('/api/stats/abcdef')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
