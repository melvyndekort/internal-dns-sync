.PHONY: clean install update-deps test build full-build pylint run
.DEFAULT_GOAL: build

clean:
	@rm -rf .pytest_cache dist __pycache__ */__pycache__

install: clean
	@uv sync --all-extras

update-deps:
	@uv sync --upgrade --all-extras

test: install
	@uv run pytest

build: test
	@uv build

full-build: clean
	@docker image build -t internal-dns-sync .

pylint:
	@uv run pylint internal_dns_sync

run: install
	@uv run python3 -m internal_dns_sync.main
