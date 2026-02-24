# テスト仕様書

## 概要

ポモドーロタイマーアプリケーションのテストは、pytest フレームワークを使用して実装されています。本ドキュメントでは、テスト戦略、テストの実行方法、カバレッジ、およびテストケースの詳細を説明します。

## テスト環境

### 必要なパッケージ

```bash
pytest>=7.4.0          # テストフレームワーク
pytest-cov>=4.1.0      # カバレッジ測定
pytest-mock>=3.11.0    # モック機能
```

### インストール

```bash
pip install -r requirements.txt
```

## テストの実行

### 基本的な実行

```bash
# すべてのテストを実行
pytest

# 詳細な出力
pytest -v

# 特定のファイルのみ実行
pytest tests/test_app.py
pytest tests/test_gamification.py
```

### カバレッジ付きで実行

```bash
# カバレッジを測定
pytest --cov=. --cov-report=html

# カバレッジレポートをブラウザで表示
open htmlcov/index.html
```

### その他のオプション

```bash
# 失敗したテストのみ再実行
pytest --lf

# 特定のテストクラスのみ実行
pytest tests/test_app.py::TestPomodoroTimerInit

# 特定のテストメソッドのみ実行
pytest tests/test_app.py::TestPomodoroTimerInit::test_default_initialization

# 並列実行（pytest-xdist が必要）
pytest -n auto
```

## テスト構成

### ディレクトリ構造

```
1.pomodoro/
├── app.py
├── gamification.py
├── tests/
│   ├── __init__.py
│   ├── test_app.py              # PomodoroTimer のテスト
│   ├── test_gamification.py     # GamificationManager のテスト
│   └── test_integration.py      # 統合テスト
├── pytest.ini                    # pytest 設定
└── .coveragerc                   # カバレッジ設定
```

### pytest.ini 設定

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

## テスト戦略

### 1. ユニットテスト

**対象**: 個別のメソッドや関数

**方針**:
- 各メソッドを独立してテスト
- モックを使用して依存関係を分離
- エッジケースを網羅

### 2. 統合テスト

**対象**: 複数のコンポーネント間の連携

**方針**:
- 実際のファイルI/Oを含む
- エンドツーエンドのフローをテスト

### 3. エッジケーステスト

**対象**: 異常系や境界値

**方針**:
- 0、負の値、非常に大きな値
- ファイル破損、存在しないファイル
- 不正な入力

## test_app.py - PomodoroTimer のテスト

### TestPomodoroTimerInit

**目的**: 初期化のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_default_initialization` | デフォルト初期化 | work_duration=25, break_duration=5 |
| `test_custom_initialization` | カスタム時間設定 | 指定した時間が設定される |
| `test_gamification_manager_initialized` | GM初期化 | GamificationManager が作成される |

### TestShowStatus

**目的**: ステータス表示機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_show_status_calls_get_status` | get_status呼び出し | get_statusが1回呼ばれる |
| `test_show_status_displays_all_info` | 情報表示 | すべてのステータス情報が表示される |

### TestShowStatistics

**目的**: 統計表示機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_show_statistics_week` | 週間統計 | get_statistics("week")が呼ばれる |
| `test_show_statistics_month` | 月間統計 | get_statistics("month")が呼ばれる |
| `test_show_statistics_displays_info` | 情報表示 | 統計情報が表示される |

### TestShowBadges

**目的**: バッジ表示機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_show_badges_calls_display_badges` | display_badges呼び出し | display_badgesが1回呼ばれる |
| `test_show_badges_displays_result` | バッジ表示 | バッジ情報が表示される |

### TestCountdown

**目的**: カウントダウン機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_countdown_completion` | 正常完了 | Trueを返す |
| `test_countdown_interruption` | 中断 | Falseを返す |
| `test_countdown_duration_calculation` | 時間計算 | sleep が正しい回数呼ばれる |

### TestStartPomodoro

**目的**: ポモドーロ開始機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_start_pomodoro_success` | 正常完了 | add_pomodoroが呼ばれ、Trueを返す |
| `test_start_pomodoro_interrupted` | 中断 | add_pomodoroが呼ばれず、Falseを返す |
| `test_start_pomodoro_with_break` | 休憩込み | カウントダウンが2回呼ばれる |
| `test_start_pomodoro_displays_new_badges` | バッジ表示 | 新しいバッジが表示される |

### TestClearScreen

**目的**: 画面クリア機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_clear_screen_unix` | Unix系 | 'clear'コマンドが実行される |
| `test_clear_screen_windows` | Windows | 'cls'コマンドが実行される |

### TestEdgeCases

**目的**: エッジケースのテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_zero_work_duration` | 0分作業時間 | 正しく設定される |
| `test_zero_break_duration` | 0分休憩時間 | 正しく設定される |
| `test_large_duration` | 非常に長い時間 | 正しく設定される |

## test_gamification.py - GamificationManager のテスト

### TestGamificationManagerBasics

**目的**: 基本機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_initialization` | 初期化 | デフォルト値が設定される |
| `test_create_default_data` | デフォルトデータ | すべてのキーが存在する |
| `test_save_and_load_data` | 保存と読み込み | データが正しく永続化される |

### TestPomodoroCompletion

**目的**: ポモドーロ完了機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_add_pomodoro_basic` | 基本的な追加 | XP、レベル、回数が正しく更新される |
| `test_add_pomodoro_custom_duration` | カスタム時間 | XPが時間に応じて計算される |
| `test_add_pomodoro_session_recording` | セッション記録 | セッション情報が記録される |
| `test_add_multiple_pomodoros` | 複数回追加 | 累計が正しく更新される |

### TestLevelUpSystem

**目的**: レベルアップシステムのテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_level_up_at_500xp` | レベル2 | 500XPでレベル2になる |
| `test_level_up_at_1000xp` | レベル3 | 1000XPでレベル3になる |
| `test_level_up_notification` | レベルアップ通知 | 通知が返される |
| `test_check_level_up_formula` | 計算式 | レベル計算式が正しい |

### TestStreakSystem

**目的**: ストリークシステムのテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_first_streak` | 初回ストリーク | 1になる |
| `test_same_day_multiple_pomodoros` | 同日複数回 | ストリークは変わらない |
| `test_consecutive_days_streak` | 連続日数 | ストリークが増加する |
| `test_broken_streak` | ストリーク途切れ | 1にリセットされる |
| `test_best_streak_update` | ベスト更新 | ベストストリークが更新される |

### TestBadgeSystem

**目的**: バッジシステムのテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_streak_badge_3_days` | 3日連続バッジ | 獲得される |
| `test_streak_badge_7_days` | 7日連続バッジ | 獲得される |
| `test_count_badge_10` | 10回バッジ | 獲得される |
| `test_count_badge_25` | 25回バッジ | 獲得される |
| `test_badge_not_duplicated` | 重複防止 | 同じバッジは重複しない |
| `test_all_count_badges` | すべての回数バッジ | すべて正しく獲得される |

### TestStatistics

**目的**: 統計機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_statistics_week` | 週間統計 | 正しい形式で返される |
| `test_statistics_month` | 月間統計 | 正しい形式で返される |
| `test_statistics_all` | 全期間統計 | 正しい形式で返される |
| `test_statistics_with_data` | データあり | 統計が正しく計算される |
| `test_statistics_daily_counts` | 日別カウント | 日別の数が正しい |
| `test_statistics_average_calculation` | 平均計算 | 平均が正しく計算される |

### TestStatus

**目的**: ステータス機能のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_get_status_basic` | 基本ステータス | デフォルト値が返される |
| `test_get_status_with_progress` | 進捗あり | 進捗率が正しい |
| `test_get_status_level_2` | レベル2 | レベル2の情報が正しい |

### TestBadgeDisplay

**目的**: バッジ表示のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_display_badges_empty` | バッジなし | メッセージが表示される |
| `test_display_badges_with_badges` | バッジあり | バッジ一覧が表示される |

### TestEdgeCases

**目的**: エッジケースのテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_corrupted_json_file` | JSON破損 | デフォルトデータで初期化 |
| `test_empty_json_file` | 空ファイル | デフォルトデータで初期化 |
| `test_zero_duration_pomodoro` | 0分ポモドーロ | XP=0、回数+1 |
| `test_negative_duration_pomodoro` | 負の時間 | 負のXPが計算される（既知の制限） |
| `test_very_large_duration` | 非常に長い時間 | 正しく計算される |
| `test_concurrent_data_access` | 並行アクセス | データが正しく保存/読み込まれる |
| `test_data_persistence_after_multiple_operations` | 複数操作後の永続化 | データが正しく永続化される |

### TestDataIntegrity

**目的**: データ整合性のテスト

| テストケース | 内容 | 検証項目 |
|--------------|------|----------|
| `test_session_count_matches_total_pomodoros` | セッション数一致 | セッション数 = 累計回数 |
| `test_xp_calculation_consistency` | XP一貫性 | XP計算が一貫している |
| `test_completed_dates_unique` | 日付の一意性 | 日付が重複しない |
| `test_badges_unique` | バッジの一意性 | バッジが重複しない |

## test_integration.py - 統合テスト

### 統合テストの内容

統合テストでは、以下のシナリオをテストします：

1. **エンドツーエンドフロー**:
   - アプリ起動 → ポモドーロ実行 → データ保存 → アプリ再起動 → データ読み込み

2. **複数日のシミュレーション**:
   - 複数日にわたるポモドーロ実行
   - ストリークの連続性

3. **バッジ獲得フロー**:
   - 条件を満たしてバッジを獲得
   - バッジ表示の確認

## カバレッジ目標

### 現在のカバレッジ

- **app.py**: 95%以上
- **gamification.py**: 98%以上
- **全体**: 95%以上

### カバレッジの確認

```bash
pytest --cov=. --cov-report=term-missing
```

### カバーされていない箇所

1. **main() 関数**: エントリーポイントのため、テスト不要
2. **os.system() の実際の実行**: モックでテスト済み
3. **一部のエラーハンドリング**: 実際の発生が困難

## モック戦略

### 1. GamificationManager のモック

```python
from unittest.mock import patch, MagicMock

with patch('app.GamificationManager') as mock_gm:
    timer = PomodoroTimer()
    timer.gm = mock_gm.return_value
```

### 2. time.sleep のモック

```python
with patch('time.sleep'):
    timer.countdown(1, "テスト")
```

### 3. ユーザー入力のモック

```python
with patch('builtins.input', return_value='y'):
    timer.start_pomodoro()
```

### 4. ファイルI/O のモック

```python
@pytest.fixture
def temp_data_file(tmp_path):
    data_file = tmp_path / "test_data.json"
    return str(data_file)
```

## テストのベストプラクティス

### 1. Fixture の活用

```python
@pytest.fixture
def timer():
    with patch('app.GamificationManager'):
        return PomodoroTimer()
```

### 2. パラメータ化テスト

```python
@pytest.mark.parametrize("xp,expected_level", [
    (0, 1),
    (499, 1),
    (500, 2),
    (1000, 3),
])
def test_level_calculation(xp, expected_level):
    # テスト実装
```

### 3. テストの独立性

- 各テストは独立して実行可能
- 他のテストの実行順序に依存しない
- 一時ファイルを使用してファイルシステムを汚染しない

### 4. 明確なテスト名

```python
def test_add_pomodoro_with_custom_duration_calculates_xp_correctly():
    # テスト実装
```

## CI/CD 統合

### GitHub Actions 設定例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## 既知の制限事項

### 1. 負の時間のポモドーロ

**現状**: 負のXPが計算される

**テスト**: `test_negative_duration_pomodoro`

**TODO**: 入力検証を追加して負の値を拒否する

### 2. 非常に大きなデータセット

**現状**: メモリに全データを保持

**影響**: 長期間使用するとメモリ使用量が増大

**対策**: 将来的にはデータベース化を検討

## トラブルシューティング

### テストが失敗する

```bash
# 詳細な出力で実行
pytest -vv

# 失敗したテストのみ再実行
pytest --lf

# pdb でデバッグ
pytest --pdb
```

### カバレッジが低い

```bash
# カバレッジレポートを確認
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### モックが動かない

```python
# モックの呼び出しを確認
mock_obj.assert_called_once()
mock_obj.assert_called_with(expected_args)
```

## まとめ

- **包括的なテストスイート**: 95%以上のカバレッジ
- **ユニットテスト**: 各メソッドを独立してテスト
- **統合テスト**: エンドツーエンドのフローをテスト
- **エッジケーステスト**: 異常系や境界値をテスト
- **CI/CD対応**: 自動テスト実行に対応

テストを継続的に実行・更新することで、高品質なアプリケーションを維持できます。
