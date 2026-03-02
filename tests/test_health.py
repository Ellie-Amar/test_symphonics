from app.interface.routes.health_route import health_check


def test_health_handler_returns_ok():
    assert health_check() == {"status": "ok"}
