# Pomodoro テストガイド

## 概要
このディレクトリには、ポモドーロタイマーアプリケーションの包括的なテストスイートが含まれています。

## テスト構成

### テストファイル
- `test_gamification.py` - GamificationManagerクラスのユニットテスト
- `test_app.py` - PomodoroTimerクラスのユニットテスト
- `test_integration.py` - 統合テストとエンドツーエンドテスト

### テストカバレッジ

#### GamificationManagerテスト（test_gamification.py）
- **基本機能テスト**
  - 初期化
  - データの読み込みと保存
  - デフォルトデータの作成

- **ポモドーロ完了機能**
  - 基本的なポモドーロ追加
  - カスタム時間のポモドーロ
  - セッション記録
  - 複数のポモドーロ

- **レベルアップシステム**
  - 500XP、1000XPでのレベルアップ
  - レベルアップ通知
  - レベル計算式の検証

- **ストリークシステム**
  - 初回ストリーク
  - 同日複数回のポモドーロ
  - 連続日のストリーク
  - ストリークの途切れ
  - ベストストリークの更新

- **バッジシステム**
  - ストリークバッジ（3日、7日、30日、100日）
  - 回数達成バッジ（10回、25回、50回、100回、250回）
  - バッジの重複防止
  - すべてのバッジの検証

- **統計機能**
  - 週間統計
  - 月間統計
  - 全期間統計
  - 日別カウント
  - 平均計算

- **ステータス機能**
  - 基本ステータス取得
  - 進捗表示
  - レベル別ステータス

- **バッジ表示**
  - 空のバッジリスト
  - バッジ表示文字列

- **エッジケース**
  - 破損したJSONファイル
  - 空のJSONファイル
  - 0分のポモドーロ
  - 負の時間のポモドーロ
  - 非常に長い時間のポモドーロ
  - 並行データアクセス
  - 複数操作後のデータ永続化

- **データ整合性**
  - セッション数と合計ポモドーロ数の一致
  - XP計算の一貫性
  - 完了日付のユニーク性
  - バッジのユニーク性

#### PomodoroTimerテスト（test_app.py）
- **初期化**
  - デフォルト初期化
  - カスタム初期化
  - GamificationManagerの初期化

- **表示機能**
  - ステータス表示
  - 統計表示（週間・月間）
  - バッジ表示

- **カウントダウン機能**
  - 完了
  - 中断
  - 時間計算

- **ポモドーロ開始**
  - 正常完了
  - 中断
  - 休憩時間を含む実行
  - 新しいバッジの表示

- **画面クリア**
  - Unix系システム
  - Windowsシステム

- **エッジケース**
  - 0分の作業時間
  - 0分の休憩時間
  - 非常に長い時間

#### 統合テスト（test_integration.py）
- **統合テスト**
  - 完全なポモドーロワークフロー
  - レベルアップワークフロー
  - バッジ獲得ワークフロー
  - ストリークワークフロー
  - データ永続化
  - 統計ワークフロー

- **同時実行シナリオ**
  - 複数インスタンスでの順次アクセス
  - データ競合状態のシミュレーション

- **境界値テスト**
  - 最小値
  - 最大値
  - レベル境界
  - ストリーク境界

- **エラーハンドリング**
  - 不正なJSONからの回復
  - フィールド欠落からの回復
  - ファイル権限エラー

- **複雑なシナリオ**
  - 長期使用シミュレーション
  - 異なる時間のポモドーロ混在
  - バッジとレベルの同期

## テストの実行

### 前提条件
```bash
pip install -r requirements.txt
```

### すべてのテストを実行
```bash
pytest tests/
```

### 特定のテストファイルを実行
```bash
pytest tests/test_gamification.py
pytest tests/test_app.py
pytest tests/test_integration.py
```

### カバレッジレポート付きでテストを実行
```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
```

### 詳細モードでテストを実行
```bash
pytest tests/ -v
```

### 特定のテストクラスやメソッドを実行
```bash
pytest tests/test_gamification.py::TestGamificationManagerBasics
pytest tests/test_gamification.py::TestGamificationManagerBasics::test_initialization
```

## カバレッジレポート

### 現在のカバレッジ
> **Note**: 以下の数値は2024年2月24日時点（コミット63bac5a）のものです。コードの変更により変動する可能性があります。

- **全体**: 85%
- **gamification.py**: 99%
- **app.py**: 74%

### カバレッジレポートの確認
HTMLカバレッジレポートは `htmlcov/index.html` に生成されます。
```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

## テスト統計

- **総テスト数**: 84個
- **ユニットテスト**: 66個
- **統合テスト**: 18個
- **成功率**: 100%
- **平均実行時間**: 約30秒

## 継続的インテグレーション

pytest.iniファイルで設定された内容：
- テストディレクトリ: `tests/`
- カバレッジソース: `.`
- カバレッジレポート: HTML、XML、ターミナル
- 詳細モード（-v）がデフォルト

## トラブルシューティング

### テストが失敗する場合
1. 依存関係を再インストール: `pip install -r requirements.txt`
2. キャッシュをクリア: `pytest --cache-clear`
3. 詳細なエラー情報を確認: `pytest -v --tb=long`

### カバレッジが表示されない場合
1. pytest-covがインストールされているか確認: `pip show pytest-cov`
2. .coveragercファイルが正しく設定されているか確認

## ベストプラクティス

1. **新機能を追加する場合**: 対応するテストも追加してください
2. **バグを修正する場合**: バグを再現するテストを先に追加してください
3. **リファクタリングする場合**: テストがすべてパスすることを確認してください
4. **カバレッジを維持**: 新しいコードには適切なテストを書いてください

## 参考資料

- [pytest公式ドキュメント](https://docs.pytest.org/)
- [pytest-cov公式ドキュメント](https://pytest-cov.readthedocs.io/)
- [unittest.mockドキュメント](https://docs.python.org/3/library/unittest.mock.html)
