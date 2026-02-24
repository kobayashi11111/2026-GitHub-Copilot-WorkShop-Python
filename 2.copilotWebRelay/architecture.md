Pomodoro Web アプリケーション — アーキテクチャ & 実装機能一覧
=================================================

概要
- Flask（バックエンド） + HTML/CSS/JavaScript（フロントエンド）でポモドーロタイマーを実装します。
- クライアントは正確なタイマー表⽰と UI、サーバーはセッション永続化と日次集計を担当します。

主要コンポーネント
- `TimerEngine`（純粋ロジック）: 時刻依存を注入できる設計で `start() / pause() / reset()` を提供。
- `UIController`（DOM 層）: 描画・ユーザー操作ハンドリング。`TimerEngine` のイベントを受ける薄い層。
- `ApiClient`（副作用アダプタ）: サーバー通信を担い、失敗時は再送キュー化を行う。
- `Storage`（localStorage 抽象）: ローカルの状態永続化・オフライン復旧。
- Flask アプリ（`create_app()`）: API ブループリント、サービス層、リポジトリ（SQLAlchemy）を持つ。

実装する機能（優先度順）
1. プロジェクト骨組み
	- `create_app()` を持つ Flask エントリ、`requirements.txt`、README。
2. UI 基本画面
	- 添付モックに沿った `index.html`、`style.css`、SVG/Canvas の円形プログレス。
3. TimerEngine（純粋ロジック）
	- `start`, `pause`, `reset`、経過/残時間計算（`clock.now()` 注入）
	- ドリフト対策（時刻差計算ベース）
4. UIController（DOM レイヤ）
	- ボタン、表示、進捗リングの更新、通知トリガー
5. Storage & オフライン同期
	- `localStorage` 保存、未送信イベントのキュー、再接続時再送
6. ApiClient と API（サーバー）
	- `POST /api/session/start`, `/complete`, `/cancel`
	- `GET /api/stats/today`（今日の完了数・合計集中時間）
7. DB モデル & リポジトリ
	- `sessions` テーブル、`SessionRepository` による DB 抽象
8. セッション永続化・日次集計
	- 完了セッションの保存と日次集計ロジック
9. 通知・サウンド
	- ブラウザ通知・サウンド再生（Notifier 抽象で差替え可能）
10. 設定画面
	- 作業/短休憩/長休憩の変更・保存（local または server）
11. テスト実装
	- フロント: `TimerEngine` のユニットテスト（`vitest`/`jest` + `jsdom`）
	- バックエンド: `pytest` + in-memory SQLite（`conftest.py`）
12. CI / デプロイ
	- GitHub Actions でテスト実行、Dockerfile / Gunicorn + Nginx 設定

テスト容易性のための設計上の注意点
- 純粋ロジックと副作用を厳密に分離すること。
- 時刻や乱数などの外部依存は注入して固定可能にすること（`clock`、`Notifier`、`Storage`）。
- Flask はアプリファクトリで作成し、テスト用に DB 接続や設定を差し替えられるようにすること。

次の推奨アクション
- スキャフォールド作成（`1.pomodoro/` の雛形）
- `static/js/timerEngine.js` とそのユニットテスト雛形作成
- バックエンド `conftest.py` を含む pytest 雛形作成

