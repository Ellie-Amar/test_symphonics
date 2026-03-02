from app.api.health import health_check
from app.main import create_app


def test_health_handler_returns_ok():
    assert health_check() == {"status": "ok"}


