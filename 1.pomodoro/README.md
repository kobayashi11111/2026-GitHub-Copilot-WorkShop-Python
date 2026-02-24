# Pomodoro Timer Web Application

シンプルで実用的なポモドーロタイマーアプリケーションです。

## 機能

- 25分の作業タイマー
- 円形プログレスバー表示
- 今日の完了セッション数と合計時間の表示
- セッション履歴の保存

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

## 開発

### テストの実行

```bash
pytest
```

### カバレッジ付きテスト

```bash
pytest --cov=. --cov-report=html
```

## プロジェクト構造

```
1.pomodoro/
├── app.py              # Flask アプリケーションエントリポイント
├── api.py              # REST API エンドポイント
├── models.py           # データベースモデル
├── templates/          # HTML テンプレート
├── static/             # 静的ファイル（CSS, JS, 画像）
│   ├── css/
│   ├── js/
│   └── images/
└── tests/              # テストファイル
```

## 技術スタック

- **Backend**: Flask 3.0
- **Database**: SQLite + SQLAlchemy
- **Frontend**: Vanilla JavaScript
- **Testing**: pytest
