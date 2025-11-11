import os
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=os.environ.get(
            "RUN_INTEGRATION", "false"
        ).lower() == "true",
        help="Run integration tests that require external network access.",
    )


def pytest_collection_modifyitems(config, items):
    run_integration = config.getoption("--run-integration")
    if not run_integration:
        skip_integration = pytest.mark.skip(
            reason="Integration tests are skipped by default in CI"
        )
        for item in items:
            # Mark tests whose nodeid includes 'multimodal' or
            # are explicitly marked 'integration'
            if ("integration" in item.keywords or
                    "multimodal" in item.nodeid.lower()):
                item.add_marker(skip_integration)
