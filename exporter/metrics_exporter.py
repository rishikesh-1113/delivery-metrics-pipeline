"""Delivery metrics exporter (Prometheus format)."""
import json
import random
import time
from pathlib import Path

from prometheus_client import CollectorRegistry, Counter, Gauge, start_http_server

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"


def load_config(path=CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calculate_success_rate(successful, total):
    if total == 0:
        return 0.0
    return round(successful / total * 100, 2)


def build_metrics(registry):
    return {
        "deployments": Counter(
            "delivery_deployments_total", "Total deployments", registry=registry
        ),
        "build_duration": Gauge(
            "delivery_build_duration_seconds", "Last build duration", registry=registry
        ),
        "success_rate": Gauge(
            "delivery_success_rate_percent", "Deployment success rate", registry=registry
        ),
    }


def update_metrics(metrics):
    metrics["deployments"].inc()
    metrics["build_duration"].set(round(random.uniform(30, 120), 2))
    metrics["success_rate"].set(calculate_success_rate(random.randint(8, 10), 10))


def main():
    config = load_config()
    registry = CollectorRegistry()
    metrics = build_metrics(registry)
    start_http_server(config["port"], registry=registry)
    print(f"Exporter running on port {config['port']}")
    while True:
        update_metrics(metrics)
        time.sleep(config["interval_seconds"])


if __name__ == "__main__":
    main()
