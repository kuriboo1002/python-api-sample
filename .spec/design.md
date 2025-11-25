# 設計書 (Design)

## 1. 概要

本システムは、商品の情報を管理するための基本的なCRUD機能を提供するWeb APIである。

## 2. アーキテクチャ

本システムは、クリーンアーキテクチャの原則に基づいたレイヤードアーキテクチャを採用している。依存関係の方向は、API層からドメイン層へと一方向に向かう。これにより、ビジネスロジックの独立性を高め、テスト容易性やメンテナンス性を向上させる。

各レイヤーの責務は以下の通り。

- **API層 (src/api):**
  - HTTPリクエストの受付、バリデーション、レスポンスの返却を担当する。
  - FastAPIのルーター機能を利用してエンドポイントを定義する。
  - アプリケーション層のサービスを呼び出し、処理を委譲する。
- **アプリケーション層 (src/application):**
  - システムのユースケースを実現する。
  - CQRS (Command Query Responsibility Segregation) パターンを実装しており、コマンド（登録・更新・削除）とクエリ（参照）の責務が明確に分離されている。
    - `ItemCommandService`: コマンド系のユースケースを担当する。
    - `ItemQueryService`: クエリ系のユースケースを担当する。
  - ドメインオブジェクトやリポジトリを利用してビジネスロジックを組み立てる。
  - `item_schemas.py` でAPIの入出力データ構造(DTO)を定義する。
- **ドメイン層 (src/domain):**
  - システムの核となるビジネスルールとエンティティを定義する。
  - `Item`エンティティ、`Name`や`Description`といった値オブジェクトが含まれる。
  - `ItemRepository`のように、インフラストラクチャ層が実装すべきインターフェースを定義する。
- **インフラストラクチャ層 (src/infrastructure):**
  - データベースへのアクセスなど、技術的な詳細を実装する。
  - ドメイン層で定義されたリポジトリインターフェースを実装する (`ItemRepositoryAdapter`, `ItemRepositoryImpl`)。
  - SQLAlchemyを利用してDBとの永続化を行う。

## 3. データモデル

### 3.1. ドメインモデル

- **Item:** 商品を表すエンティティ。
  - `id`: `int` (識別子)
  - `name`: `Name` (商品名)
  - `description`: `Description` (商品説明)
- **Name:** 商品名を表す値オブジェクト。
  - `value`: `str`
  - Validation:
    - 空でないこと
    - 禁止ワードを含まないこと (`禁止`, `NG`, `不適切`)
- **Description:** 商品説明を表す値オブジェクト。
  - `value`: `str`
  - Validation:
    - 255文字以下であること

### 3.2. データベーススキーマ

- **`items` テーブル**
  - `id`: `INT`, `AUTO_INCREMENT`, `PRIMARY KEY`
  - `name`: `VARCHAR(255)`, `NOT NULL`
  - `description`: `TEXT`

## 4. シーケンス図 (例: 商品作成)

```mermaid
sequenceDiagram
    participant Client
    participant API (item_api.py)
    participant AppService (item_command_service.py)
    participant Domain (item.py, value_objects.py)
    participant Repository (item_repository.py)
    participant DB

    Client->>+API: POST /items (name, description)
    API->>+AppService: create_item(req)
    AppService->>+Domain: Item(name, description)
    Note right of Domain: Name, Descriptionの<br>バリデーション実行
    Domain-->>-AppService: Itemインスタンス
    AppService->>+Repository: create(item)
    Repository->>+DB: INSERT INTO items ...
    DB-->>-Repository: 
    Repository-->>-AppService: 作成されたItem
    AppService-->>-API: ItemResponse
    API-->>-Client: 200 OK (id, name, description)
```
