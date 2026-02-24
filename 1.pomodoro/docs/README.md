# ドキュメント概要

## 📚 ドキュメント一覧

このディレクトリには、ポモドーロタイマーアプリケーションの包括的なドキュメントが含まれています。

### ユーザー向けドキュメント

- **[user-guide.md](./user-guide.md)** - ユーザーガイド
  - アプリの使い方
  - 基本操作
  - ゲーミフィケーション要素の説明
  - よくある質問
  - トラブルシューティング

### 開発者向けドキュメント

- **[architecture.md](./architecture.md)** - アーキテクチャ概要
  - システム構成
  - レイヤー構造
  - データフロー
  - 技術仕様
  - 設計の特徴

- **[api-reference.md](./api-reference.md)** - API リファレンス
  - PomodoroTimer クラス
  - GamificationManager クラス
  - 全メソッドの詳細説明
  - 使用例

- **[data-models.md](./data-models.md)** - データモデル仕様
  - データ構造
  - フィールド詳細
  - データ整合性ルール
  - 永続化方法

- **[testing.md](./testing.md)** - テスト仕様書
  - テスト戦略
  - テストケース一覧
  - カバレッジ
  - テストの実行方法

## 🚀 クイックスタート

### 使い始める

1. **インストール**: [user-guide.md - インストールと起動](./user-guide.md#インストールと起動)
2. **基本的な使い方**: [user-guide.md - 基本的な使い方](./user-guide.md#基本的な使い方)
3. **ゲーミフィケーション**: [user-guide.md - ゲーミフィケーション要素](./user-guide.md#ゲーミフィケーション要素)

### 開発を始める

1. **アーキテクチャを理解**: [architecture.md](./architecture.md)
2. **API を確認**: [api-reference.md](./api-reference.md)
3. **テストを実行**: [testing.md - テストの実行](./testing.md#テストの実行)

## 📖 読む順番の推奨

### 初めてのユーザー

```
1. README.md（プロジェクトルート）
2. user-guide.md - はじめに
3. user-guide.md - 基本的な使い方
4. user-guide.md - ゲーミフィケーション要素
```

### 開発者

```
1. README.md（プロジェクトルート）
2. architecture.md - システム構成
3. data-models.md - データ構造
4. api-reference.md - API 概要
5. testing.md - テスト戦略
```

### 機能拡張を検討している開発者

```
1. architecture.md - 設計の特徴
2. architecture.md - 今後の拡張可能性
3. api-reference.md - 内部メソッド
4. data-models.md - データマイグレーション
```

## 🔍 トピック別インデックス

### ゲーミフィケーション

- **XPシステム**: [user-guide.md - 経験値システム](./user-guide.md#経験値xpシステム)
- **レベル計算**: [data-models.md - level](./data-models.md#level-number)
- **レベルアップロジック**: [api-reference.md - _check_level_up()](./api-reference.md#gamificationmanager_check_level_up)

### ストリーク

- **ストリークとは**: [user-guide.md - ストリーク](./user-guide.md#ストリーク連続日数)
- **ストリーク計算**: [data-models.md - current_streak](./data-models.md#current_streak-number)
- **ストリーク更新ロジック**: [api-reference.md - _update_streak()](./api-reference.md#gamificationmanager_update_streak)

### バッジ

- **バッジ一覧**: [user-guide.md - バッジシステム](./user-guide.md#バッジシステム)
- **バッジデータ**: [data-models.md - badges](./data-models.md#badges-array)
- **バッジ判定ロジック**: [api-reference.md - _check_badges()](./api-reference.md#gamificationmanager_check_badges)

### データ管理

- **データ構造**: [data-models.md - データ構造](./data-models.md#データ構造)
- **データ保存**: [api-reference.md - save_data()](./api-reference.md#save_data)
- **データ読み込み**: [api-reference.md - _load_data()](./api-reference.md#gamificationmanager_load_data)

### テスト

- **テスト実行**: [testing.md - テストの実行](./testing.md#テストの実行)
- **カバレッジ**: [testing.md - カバレッジ目標](./testing.md#カバレッジ目標)
- **モック戦略**: [testing.md - モック戦略](./testing.md#モック戦略)

## 📝 ドキュメントの更新

### ドキュメント管理方針

1. **コードと同期**: コード変更時にドキュメントも更新
2. **正確性**: 実装と一致する情報のみを記載
3. **包括性**: すべての公開APIを文書化
4. **例示**: 実際の使用例を含める

### 更新が必要なタイミング

- 新機能の追加
- APIの変更
- データ構造の変更
- バグ修正（動作が変わる場合）
- テストケースの追加

### ドキュメント作成者へのガイド

1. **Markdown形式**: GitHub Flavored Markdown を使用
2. **日本語**: すべてのドキュメントは日本語で記述
3. **構造化**: 見出しを適切に使用して階層化
4. **コード例**: 実際に動作するコードを記載
5. **リンク**: 関連するドキュメントへのリンクを含める

## 🔗 外部リソース

### プロジェクト関連

- **リポジトリ**: [GitHub Repository](../..)
- **Issues**: [GitHub Issues](../../issues)
- **メインREADME**: [README.md](../README.md)

### 関連技術

- **Python 公式ドキュメント**: https://docs.python.org/3/
- **pytest ドキュメント**: https://docs.pytest.org/
- **ポモドーロ・テクニック**: https://ja.wikipedia.org/wiki/ポモドーロ・テクニック

## 📞 サポート

### ドキュメントに関する質問

ドキュメントが不明瞭な場合や、追加の情報が必要な場合は、以下の方法でお問い合わせください：

1. **GitHub Issues**: 質問やドキュメントの改善提案を投稿
2. **Pull Request**: ドキュメントの修正を直接提案

### バグ報告

アプリケーションのバグを発見した場合：

1. **確認**: [user-guide.md - トラブルシューティング](./user-guide.md#トラブルシューティング) を確認
2. **報告**: GitHub Issues でバグレポートを作成

## 📄 ライセンス

ドキュメントはソースコードと同じライセンスの下で提供されます。

---

## バージョン履歴

### v1.0.0 (2026-02-24)

- 初回ドキュメント作成
- ユーザーガイド
- アーキテクチャ概要
- API リファレンス
- データモデル仕様
- テスト仕様書

---

**最終更新**: 2026-02-24

**更新者**: GitHub Copilot CLI

**更新内容**: ソースコードと同期した包括的なドキュメントを作成
