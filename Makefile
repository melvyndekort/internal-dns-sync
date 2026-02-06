.PHONY: clean install update-deps test test-cov build full-build lint pylint run
.DEFAULT_GOAL: build

clean:
	@rm -rf .pytest_cache dist __pycache__ */__pycache__ htmlcov .coverage

install: clean
	@uv sync --all-extras

update-deps:
	@uv sync --upgrade --all-extras

test: install
	@uv run pytest

test-cov: install
	@uv run pytest --cov=internal_dns_sync --cov-report=html --cov-report=term

build: test
	@uv build

full-build: clean
	@docker image build -t internal-dns-sync .

lint: install
	@uv run pylint internal_dns_sync

pylint: lint

run: install
	@uv run python3 -m internal_dns_sync.main
