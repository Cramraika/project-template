# {{ORCHESTRATOR_NAME}} — Makefile
#
# Standard targets per orchestrator-tier scaffold (ADR-068 template).
# Universal §52 unattended-mode contract: each target returns non-zero on hard fail.

PY      ?= python3
PKG_DIR ?= scripts/{{ORCHESTRATOR_NAME}}
PKG     ?= {{ORCHESTRATOR_PKG}}

.PHONY: help install lint test reconcile apply list-live clean

help:
	@echo "Targets:"
	@echo "  install     — pip install -e ${PKG_DIR}"
	@echo "  lint        — ruff check ${PKG_DIR}"
	@echo "  test        — pytest -v ${PKG_DIR}/tests"
	@echo "  reconcile   — ${PKG} reconcile (read-only diff)"
	@echo "  apply       — ${PKG} apply  (mutating; needs --confirm)"
	@echo "  list-live   — ${PKG} list-live"

install:
	cd ${PKG_DIR} && $(PY) -m pip install -e .

lint:
	cd ${PKG_DIR} && ruff check ${PKG}

test:
	cd ${PKG_DIR} && $(PY) -m pytest -v tests/

reconcile:
	cd ${PKG_DIR} && $(PY) -m ${PKG} reconcile

apply:
	cd ${PKG_DIR} && $(PY) -m ${PKG} apply $(ARGS)

list-live:
	cd ${PKG_DIR} && $(PY) -m ${PKG} list-live

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
