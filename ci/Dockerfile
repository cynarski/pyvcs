FROM python:3.12-slim

ARG PYVCS_VERSION=workspace
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

COPY pyproject.toml README.md /opt/source/
COPY src /opt/source/src
RUN if [ "$PYVCS_VERSION" = "workspace" ]; then \
        python -m pip install --no-cache-dir /opt/source; \
    else \
        python -m pip install --no-cache-dir "pyvcs==$PYVCS_VERSION"; \
    fi
RUN python -m pip install --no-cache-dir "pytest==9.1.1"

WORKDIR /suite
COPY pyproject.toml /suite/pyproject.toml
COPY tests/integration /suite/tests/integration
COPY ci/run_tests.py /suite/run_tests.py
RUN mkdir /results && python -m pip freeze > /results/packages.txt
CMD ["python", "run_tests.py", "/suite/jobs.json"]
