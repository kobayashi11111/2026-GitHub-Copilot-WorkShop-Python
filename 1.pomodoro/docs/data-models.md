# データモデル仕様

## 概要

ポモドーロタイマーアプリケーションは、すべてのデータを JSON 形式で `pomodoro_data.json` ファイルに保存します。

## データ構造

### メインデータスキーマ

```json
{
  "xp": 0,
  "level": 1,
  "total_pomodoros": 0,
  "completed_dates": [],
  "badges": [],
  "sessions": [],
  "current_streak": 0,
  "best_streak": 0,
  "last_completion_date": null
}
```

## フィールド詳細

### `xp` (number)

**説明**: ユーザーの累計経験値

**型**: `float` または `int`

**初期値**: `0`

**計算式**: `(完了時間（分） / 25) * 100`

**例**:
- 25分のポモドーロ完了 → +100 XP
- 50分のポモドーロ完了 → +200 XP

### `level` (number)

**説明**: ユーザーの現在のレベル

**型**: `int`

**初期値**: `1`

**計算式**: `1 + floor(xp / 500)`

**レベルとXPの対応表**:

| レベル | 必要XP | 必要ポモドーロ数 |
|--------|--------|------------------|
| 1      | 0      | 0                |
| 2      | 500    | 5                |
| 3      | 1000   | 10               |
| 4      | 1500   | 15               |
| 5      | 2000   | 20               |
| ...    | ...    | ...              |
| n      | (n-1) * 500 | (n-1) * 5   |

### `total_pomodoros` (number)

**説明**: 完了したポモドーロの累計回数

**型**: `int`

**初期値**: `0`

**更新**: ポモドーロ完了ごとに +1

### `completed_dates` (array)

**説明**: ポモドーロを完了した日付のリスト（重複なし）

**型**: `array<string>`

**形式**: ISO 8601 日付形式（`YYYY-MM-DD`）

**初期値**: `[]`

**例**:
```json
["2026-02-20", "2026-02-21", "2026-02-22"]
```

**注意**: 
- 同じ日に複数回ポモドーロを完了しても、日付は1回のみ記録
- ストリーク計算には使用されない（`last_completion_date` を使用）

### `badges` (array)

**説明**: 獲得したバッジのIDリスト

**型**: `array<string>`

**初期値**: `[]`

**バッジID一覧**:

#### ストリークバッジ
- `"streak_3"`: 3日連続達成
- `"streak_7"`: 7日連続達成
- `"streak_30"`: 30日連続達成
- `"streak_100"`: 100日連続達成

#### 回数達成バッジ
- `"count_10"`: 10回達成
- `"count_25"`: 25回達成
- `"count_50"`: 50回達成
- `"count_100"`: 100回達成
- `"count_250"`: 250回達成

**例**:
```json
["streak_3", "count_10", "count_25"]
```

**制約**:
- 同じバッジIDは重複して記録されない
- バッジは取得後、削除されることはない

### `sessions` (array)

**説明**: 完了したポモドーロセッションの履歴

**型**: `array<SessionObject>`

**初期値**: `[]`

**SessionObject スキーマ**:
```json
{
  "date": "2026-02-24",
  "datetime": "2026-02-24T15:30:45.123456",
  "duration": 25,
  "xp_earned": 100.0
}
```

**フィールド**:
- `date` (string): セッション完了日（`YYYY-MM-DD`形式）
- `datetime` (string): セッション完了日時（ISO 8601形式）
- `duration` (number): セッション時間（分）
- `xp_earned` (number): 獲得したXP

**例**:
```json
[
  {
    "date": "2026-02-24",
    "datetime": "2026-02-24T10:25:00.000000",
    "duration": 25,
    "xp_earned": 100.0
  },
  {
    "date": "2026-02-24",
    "datetime": "2026-02-24T11:30:00.000000",
    "duration": 25,
    "xp_earned": 100.0
  }
]
```

### `current_streak` (number)

**説明**: 現在の連続日数

**型**: `int`

**初期値**: `0`

**更新ロジック**:
- 初回完了: `1`
- 前日に完了している場合: `+1`
- 2日以上空いた場合: `1` にリセット
- 同日に複数回完了: 変化なし

### `best_streak` (number)

**説明**: 最長連続日数の記録

**型**: `int`

**初期値**: `0`

**更新**: `current_streak` が `best_streak` を超えた場合に更新

### `last_completion_date` (string | null)

**説明**: 最後にポモドーロを完了した日付

**型**: `string` (ISO 8601 日付形式) または `null`

**形式**: `YYYY-MM-DD`

**初期値**: `null`

**例**: `"2026-02-24"`

**用途**: ストリーク計算に使用

## データ整合性ルール

### 1. セッション数と total_pomodoros の一致

```python
len(sessions) == total_pomodoros
```

常に真であるべき。

### 2. XPの一貫性

```python
xp == sum(session['xp_earned'] for session in sessions)
```

すべてのセッションのXPの合計が、現在のXPと一致するべき。

### 3. レベルとXPの関係

```python
level == 1 + int(xp / 500)
```

レベルは常にXPから計算可能。

### 4. ストリークの範囲

```python
0 <= current_streak <= best_streak
```

現在のストリークは必ずベストストリーク以下。

### 5. バッジの一意性

```python
len(badges) == len(set(badges))
```

バッジリストに重複がないこと。

### 6. 完了日付の一意性

```python
len(completed_dates) == len(set(completed_dates))
```

完了日付リストに重複がないこと。

## データ永続化

### 保存タイミング

- ポモドーロ完了時に `GamificationManager.save_data()` が自動的に呼ばれる
- データは即座にファイルに書き込まれる

### ファイル形式

- **ファイル名**: `pomodoro_data.json`
- **エンコーディング**: UTF-8
- **インデント**: 2スペース
- **ASCII以外の文字**: そのまま保存（`ensure_ascii=False`）

### データ読み込み

- アプリケーション起動時に `GamificationManager.__init__()` で自動読み込み
- ファイルが存在しない場合: デフォルトデータで初期化
- JSONが破損している場合: デフォルトデータで初期化
- 欠落フィールドがある場合: デフォルト値で補完

## データマイグレーション

### 後方互換性

現在の実装では、古いデータファイルを読み込む際に欠落フィールドを自動補完します：

```python
def _load_data(self) -> Dict:
    if os.path.exists(self.data_file):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # デフォルトデータとマージして欠落フィールドを補完
                default_data = self._create_default_data()
                default_data.update(loaded_data)
                return default_data
        except (json.JSONDecodeError, IOError, OSError):
            return self._create_default_data()
    return self._create_default_data()
```

このため、新しいフィールドを追加しても、既存のデータファイルは引き続き使用可能です。

## データサイズ見積もり

### 典型的な使用パターン

- 1日3回のポモドーロ実行
- 365日使用

**1セッションのデータサイズ**: 約150バイト

**1年間のデータサイズ**: 
```
3回/日 × 365日 × 150バイト ≈ 164 KB
```

**10年間のデータサイズ**: 約1.6 MB

→ ファイルサイズは実用上問題なし

## データエクスポート/インポート（将来対応）

現在の実装では、JSONファイルを直接コピーすることでデータのバックアップ/リストアが可能です。

将来的には以下の機能が考えられます：

- CSV形式でのエクスポート
- データの統計レポート生成（PDF）
- 複数デバイス間での同期
- クラウドバックアップ
