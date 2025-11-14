# ==============================================================================
# Makefile for Item Project
# ==============================================================================

# .PHONY はファイル名とターゲット名が衝突するのを防ぎます
.PHONY: help init up down build restart logs test lint format shell clean

# デフォルトターゲット
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help          このヘルプメッセージを表示します"
	@echo "  init          .env.sample から .env ファイルをコピーしてプロジェクトを初期化します"
	@echo "  up            Dockerコンテナをバックグラウンドで起動します"
	@echo "  down          Dockerコンテナを停止します"
	@echo "  build         Dockerイメージをビルドします"
	@echo "  restart       Dockerコンテナを再起動します"
	@echo "  logs          Dockerコンテナのログを表示します"
	@echo "  test          ローカルでpytestを実行します"
	@echo "  lint          ローカルでruffを使ったlintチェックを実行します"
	@echo "  format        ローカルでruffを使ったフォーマットを実行します"
	@echo "  shell         appコンテナ内でbashを起動します"
	@echo "  clean         Dockerコンテナを停止し、ボリュームも削除します"

# .envファイルが存在しない場合、.env.sampleからコピーする
init:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.sample..."; \
		cp .env.sample .env; \
	else \
		echo ".env file already exists."; \
	fi

# Docker Composeコマンド
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

restart: down up

logs:
	docker compose logs db app

test:
	poetry run python -m pytest --cov=src --cov-report=term-missing

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

shell:
	docker compose exec app /bin/bash

# クリーンアップ
clean:
	docker compose down -v --remove-orphans