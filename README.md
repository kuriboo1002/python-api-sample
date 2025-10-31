# 社員商品管理API

## 概要
このアプリケーションはFastAPI＋MySQLによる社員商品管理APIです。  
日本語データも文字化けせず取得できます。

## 起動手順

1. DockerとDocker Composeがインストールされていることを確認してください。
2. プロジェクトディレクトリで以下を実行します。

```bash
docker compose up --build
```

3. ブラウザで http://localhost:8000/items にアクセスすると商品一覧が取得できます。

## APIエンドポイント

- `GET /`  
  サーバーの疎通確認（{"Hello": "World"}を返します）

  ```bash
  curl http://localhost:8000/
  ```

- `GET /items`  
  商品一覧を取得します。

  ```bash
  curl http://localhost:8000/items
  ```

- `GET /items/{item_id}`  
  商品IDで商品情報を取得します。

  ```bash
  curl http://localhost:8000/items/1
  ```

- `POST /items`  
  商品情報（name, description）を新規作成します。  
  リクエストBody:  
  ```
  {
    "name": "商品名",
    "description": "説明"
  }
  ```
  ```bash
  curl -X POST "http://localhost:8000/items" \
    -H "Content-Type: application/json" \
    -d '{"name": "商品名", "description": "説明"}'
  ```
  レスポンス例:
  ```
  {
    "id": 101,
    "name": "商品名",
    "description": "説明"
  }
  ```
  バリデーション:
  - name: 必須（空不可）
  - description: 255文字以内

- `PUT /items/{item_id}`  
  商品情報（name, description）を更新します。  
  リクエストBody:  
  ```
  {
    "name": "新しい商品名",
    "description": "新しい説明"
  }
  ```
  ```bash
  curl -X PUT "http://localhost:8000/items/1" \
    -H "Content-Type: application/json" \
    -d '{"name": "新しい商品名", "description": "新しい説明"}'
  ```
  バリデーション:
  - name: 必須（空不可）
  - description: 255文字以内

- `DELETE /items/{item_id}`  
  商品情報を削除します。

  ```bash
  curl -X DELETE http://localhost:8000/items/1
  ```

## models.py自動生成手順

1. MySQLサーバーを起動  
   （例：`docker compose up -d db`）

2. 以下コマンドを実行してmodels.pyを自動生成  
   ```
   sqlacodegen mysql+pymysql://root:root@localhost/employee_db --outfile employee/domain/generated_models/models.py
   ```

3. 自動生成されたmodels.pyは直接編集せず、  
   必要な拡張はラッパークラス（例：employee/domain/item.py等）で行ってください。

## データが投入できない場合の対処

MySQLの初期化SQL（init.sql）が反映されない場合、既存のDBボリュームが原因です。  
以下の手順でDBを再初期化してください。

1. コンテナとボリュームを削除

```bash
docker compose down
docker volume rm employee_db-data
```

2. 再度起動

```bash
docker compose up --build
```

これでinit.sqlが再度投入され、初期データが反映されます。

## 文字化け対策

- MySQLコンテナの環境変数に `MYSQL_CHARSET: utf8mb4` と `LANG: ja_JP.UTF-8` を追加しています。
- DB・テーブル・接続すべてUTF-8で統一しています。
