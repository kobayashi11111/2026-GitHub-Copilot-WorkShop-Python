# ポモドーロタイマー Web アプリケーション - プロジェクト計画書

**作成日**: 2026年2月24日  
**プロジェクト名**: Pomodoro Timer Web Application  
**技術スタック**: Flask (Backend) + HTML/CSS/JavaScript (Frontend)

---

## 📋 プロジェクト概要

添付の UI モックに基づいた、シンプルで実用的なポモドーロタイマー Web アプリケーションを開発します。クライアント側で正確なタイマー動作を実現し、サーバー側でセッション履歴を永続化・集計します。

**主要機能**:
- 25分の作業タイマーとカウントダウン表示
- 円形プログレスバーによる視覚的なフィードバック
- 今日の完了セッション数と合計時間の表示
- オフライン対応とローカル永続化
- ブラウザ通知とサウンド

---

## 🏗️ アーキテクチャ概要

### フロントエンド構成
```
static/
├── js/
│   ├── timerEngine.js      # 純粋ロジック（テスト可能）
│   ├── uiController.js     # DOM 操作層
│   ├── apiClient.js        # API 通信
│   ├── storage.js          # localStorage 抽象化
│   └── notifier.js         # 通知・サウンド
├── css/
│   └── style.css           # UI スタイル
```

### バックエンド構成
```
1.pomodoro/
├── app.py                  # Flask アプリファクトリ
├── api.py                  # REST API ブループリント
├── models.py               # SQLAlchemy モデル
├── repository.py           # DB アクセス抽象化
├── templates/
│   └── index.html
└── tests/
    ├── conftest.py
    └── test_*.py
```

### 主要設計原則
1. **純粋ロジックの分離**: `TimerEngine` は DOM に依存しない
2. **依存性注入**: 時刻（`clock`）や副作用を注入可能にしてテスト容易性を確保
3. **アプリファクトリ**: Flask は `create_app(config)` でテスト時の設定差し替え可能
4. **リポジトリパターン**: DB アクセスを抽象化してモック可能に

---

## 🎯 実装機能一覧

### コア機能（必須）
- [x] タイマー表示（MM:SS フォーマット）
- [x] 開始/一時停止/リセット操作
- [x] 円形プログレスバー（SVG/Canvas）
- [x] セッション記録（開始/完了/キャンセル）
- [x] 今日の進捗表示（完了数・合計時間）

### 拡張機能
- [ ] ブラウザ通知
- [ ] サウンド再生
- [ ] 時間設定のカスタマイズ（作業/短休憩/長休憩）
- [ ] ローカル永続化とオフライン対応
- [ ] 認証とユーザー管理（将来対応）

詳細は [features.md](features.md) を参照。

---

## 📅 段階的実装計画

### Phase 0: 環境構築（1-2時間）
- Flask プロジェクト構造の作成
- `requirements.txt` と依存パッケージのインストール
- 最小限の動作確認

### Phase 1: 基本タイマー UI（3-4時間）
- `TimerEngine` の実装（純粋ロジック）
- `UIController` の実装（DOM 操作）
- CSS スタイリングと円形プログレス
- フロントエンドユニットテストの作成

### Phase 2: バックエンド API（3-4時間）
- SQLAlchemy モデルの定義
- API エンドポイント実装（start/complete/cancel/stats）
- pytest テストの作成

### Phase 3: フロント・バックエンド統合（2-3時間）
- API 連携の実装
- 今日の進捗表示の動的更新
- エラーハンドリング

### Phase 4: ローカル永続化（2-3時間）
- `localStorage` による状態保存
- リロード時の状態復元
- オフラインキューと再送機能

### Phase 5: 通知・設定（2-3時間）
- ブラウザ通知とサウンド
- 設定画面の実装

### Phase 6: テスト拡充（3-4時間）
- カバレッジ向上
- エッジケースのテスト

### Phase 7: CI/CD（2-3時間）
- GitHub Actions 設定
- Dockerfile 作成

**総見積もり時間**: 約20-30時間（コア機能）

詳細なタスクとチェックリストは [implementation-plan.md](implementation-plan.md) を参照。

---

## 🧪 テスト戦略

### フロントエンド
- **ツール**: `vitest` + `jsdom`
- **対象**: `TimerEngine`, `storage.js`, `notifier.js`
- **方針**: `clock` と副作用をモックして純粋ロジックをテスト

### バックエンド
- **ツール**: `pytest` + `Flask test_client`
- **対象**: API エンドポイント、モデル、リポジトリ
- **方針**: in-memory SQLite (`sqlite:///:memory:`) を使用

### CI
- GitHub Actions で PR 毎に自動テスト実行
- カバレッジレポートの生成

---

## 🚀 デプロイ計画

### 開発環境
```bash
cd 1.pomodoro
pip install -r requirements.txt
python app.py
```

### 本番環境
- **コンテナ化**: Docker + Gunicorn
- **Web サーバー**: Nginx（リバースプロキシ）
- **データベース**: SQLite（小規模）/ PostgreSQL（スケール時）
- **ホスティング**: Heroku / GCP / Azure

---

## 📚 関連ドキュメント

- [architecture.md](architecture.md) - 詳細なアーキテクチャ設計
- [features.md](features.md) - 機能仕様一覧
- [implementation-plan.md](implementation-plan.md) - 段階的実装ガイド

---

## 🎬 次のステップ

**Phase 0（環境構築）** から開始することを推奨します。

```bash
# 1. プロジェクト構造の作成
mkdir -p 1.pomodoro/{templates,static/{css,js},tests}

# 2. 依存パッケージのインストール
cd 1.pomodoro
pip install flask flask-sqlalchemy pytest pytest-cov

# 3. 最小限のアプリを作成して動作確認
python app.py
```

準備ができたら Phase 1（基本タイマー UI）に進みます。
