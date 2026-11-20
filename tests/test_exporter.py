from prometheus_client import CollectorRegistry, generate_latest

from exporter.metrics_exporter import (
    build_metrics,
    calculate_success_rate,
    load_config,
    update_metrics,
)


def test_success_rate_normal():
    assert calculate_success_rate(8, 10) == 80.0


def test_success_rate_zero_total():
    assert calculate_success_rate(0, 0) == 0.0


def test_config_has_port():
    assert load_config()["port"] == 8000


def test_metrics_are_exposed():
    registry = CollectorRegistry()
    metrics = build_metrics(registry)
    update_metrics(metrics)
    output = generate_latest(registry).decode()
    assert "delivery_build_duration_seconds" in output
    assert "delivery_deployments_total" in output
