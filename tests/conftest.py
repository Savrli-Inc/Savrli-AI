import os
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=os.environ.get("RUN_INTEGRATION", "false").lower() == "true",
        help="Run integration tests that require external network access.",
    )
