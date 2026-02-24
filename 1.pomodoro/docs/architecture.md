# アーキテクチャドキュメント

## システム概要

ポモドーロタイマーアプリケーションは、ゲーミフィケーション要素を統合したコマンドライン型のタイマーアプリケーションです。Python標準ライブラリのみを使用し、外部依存なしで動作します。

## システムアーキテクチャ

### レイヤー構成

```
┌─────────────────────────────────────┐
│     CLI Interface Layer             │
│     (app.py - PomodoroTimer)        │
├─────────────────────────────────────┤
│     Business Logic Layer            │
│  (gamification.py - Manager)        │
├─────────────────────────────────────┤
│     Data Persistence Layer          │
│     (JSON File Storage)             │
└─────────────────────────────────────┘
```

### 主要コンポーネント

#### 1. PomodoroTimer クラス (`app.py`)

**責務:**
- ユーザーインターフェースの提供（メニュー、画面表示）
- タイマー機能の実装（カウントダウン）
- セッション管理（作業/休憩サイクル）
- ゲーミフィケーションマネージャーとの連携

**主要メソッド:**
- `show_menu()`: メインメニューの表示とユーザー入力処理
- `start_pomodoro()`: ポモドーロセッションの開始・実行
- `countdown(minutes, label)`: カウントダウンタイマーの実装
- `show_status()`: 現在のステータス表示
- `show_statistics(period)`: 統計情報の表示
- `show_badges()`: バッジコレクションの表示
- `clear_screen()`: 画面クリア処理

#### 2. GamificationManager クラス (`gamification.py`)

**責務:**
- ゲーミフィケーション要素の管理
- データの永続化・読み込み
- XP/レベルシステムの計算
- バッジ・ストリークの管理
- 統計情報の集計

**主要メソッド:**
- `add_pomodoro(duration_minutes)`: ポモドーロ完了処理
- `_check_level_up()`: レベルアップ判定
- `_update_streak()`: ストリーク更新
- `_check_badges()`: バッジ解放チェック
- `get_statistics(period)`: 統計情報の取得
- `get_status()`: 現在の状態取得
- `save_data()`: データの保存
- `_load_data()`: データの読み込み

## データモデル

### データ構造 (`pomodoro_data.json`)

```json
{
  "xp": 0,
  "level": 1,
  "total_pomodoros": 0,
  "completed_dates": [],
  "badges": [],
  "sessions": [
    {
      "date": "YYYY-MM-DD",
      "datetime": "ISO8601形式",
      "duration": 25,
      "xp_earned": 100
    }
  ],
  "current_streak": 0,
  "best_streak": 0,
  "last_completion_date": "YYYY-MM-DD"
}
```

### フィールド説明

| フィールド | 型 | 説明 |
|-----------|---|------|
| `xp` | number | 累計経験値 |
| `level` | number | 現在のレベル |
| `total_pomodoros` | number | 完了したポモドーロの総数 |
| `completed_dates` | array | 完了日のリスト（YYYY-MM-DD形式） |
| `badges` | array | 獲得したバッジIDのリスト |
| `sessions` | array | セッション履歴の配列 |
| `current_streak` | number | 現在の連続日数 |
| `best_streak` | number | 最長連続日数記録 |
| `last_completion_date` | string | 最後に完了した日付 |

## 設計パターン

### 関心の分離 (Separation of Concerns)

- **UI層 (PomodoroTimer)**: ユーザーインターフェースとタイマー機能
- **ビジネスロジック層 (GamificationManager)**: ゲーミフィケーションロジック
- **データ層 (JSON)**: データの永続化

### 単一責任の原則 (Single Responsibility)

各クラスは明確に定義された単一の責務を持ちます：
- `PomodoroTimer`: CLI操作とタイマー機能
- `GamificationManager`: ゲーミフィケーション要素の管理

## データフロー

### ポモドーロ完了時のフロー

```
1. ユーザーがポモドーロセッションを開始
   ↓
2. PomodoroTimer.start_pomodoro() が実行
   ↓
3. countdown() でカウントダウン実行
   ↓
4. 完了時、GamificationManager.add_pomodoro() 呼び出し
   ↓
5. GamificationManager内で:
   - XP付与
   - レベルアップチェック
   - ストリーク更新
   - バッジチェック
   - データ保存
   ↓
6. 結果を返却（獲得XP、レベル、新規バッジ等）
   ↓
7. PomodoroTimerが結果を画面に表示
```

## ゲーミフィケーションロジック

### XPシステム

**計算式:**
- XP獲得量 = `(作業時間 / 25) * 100`
- レベル = `1 + floor(総XP / 500)`

**例:**
- 25分のポモドーロ完了 → +100 XP
- レベル1→2: 500 XP必要
- レベル2→3: 1000 XP必要

### ストリークシステム

**ロジック:**
1. 最後の完了日と今日の日付を比較
2. 同日: ストリーク値維持
3. 連続している（差分1日）: ストリーク+1
4. 連続が途切れた（差分2日以上）: ストリーク=1にリセット
5. ベストストリークの更新判定

### バッジシステム

**バッジタイプ:**

1. **ストリークバッジ**: 連続日数に基づく
   - `streak_3`: 3日連続
   - `streak_7`: 7日連続
   - `streak_30`: 30日連続
   - `streak_100`: 100日連続

2. **回数達成バッジ**: 累計ポモドーロ数に基づく
   - `count_10`: 10回達成
   - `count_25`: 25回達成
   - `count_50`: 50回達成
   - `count_100`: 100回達成
   - `count_250`: 250回達成

**判定ロジック:**
- `add_pomodoro()` 実行時に `_check_badges()` が呼ばれる
- 各バッジの条件を満たし、かつまだ獲得していない場合に解放
- 複数バッジを同時に獲得可能

## エラーハンドリング

### データ読み込みエラー

`GamificationManager._load_data()`:
- JSONファイルが存在しない → デフォルトデータで初期化
- JSON解析エラー → デフォルトデータで初期化
- IOエラー → デフォルトデータで初期化

### タイマー中断

`PomodoroTimer.countdown()`:
- `KeyboardInterrupt` をキャッチ
- 中断メッセージを表示してFalseを返却
- ポモドーロとしてカウントされない

## 技術的制約

### プラットフォーム

- **Python要件**: Python 3.x
- **OS互換性**: 
  - Unix系: `clear` コマンド使用
  - Windows: `cls` コマンド使用

### 外部依存

- **なし**: 標準ライブラリのみ使用
- 必要モジュール: `time`, `os`, `sys`, `datetime`, `json`, `typing`

### データ永続化

- **形式**: JSON（UTF-8エンコーディング）
- **ファイル名**: `pomodoro_data.json`
- **場所**: アプリケーション実行ディレクトリ
- **保存タイミング**: 各ポモドーロ完了時

## 拡張性

### 将来的な拡張ポイント

1. **Webインターフェース**: Flask/FastAPIでRESTful APIに変換
2. **データベース統合**: SQLiteやPostgreSQLへの移行
3. **複数ユーザー対応**: 認証・ユーザー管理機能の追加
4. **設定のカスタマイズ**: 作業時間・休憩時間の変更機能
5. **通知機能**: デスクトップ通知やサウンドの追加
6. **クラウド同期**: 複数デバイス間でのデータ同期
7. **より高度な統計**: グラフライブラリを使った可視化

### 現在のアーキテクチャの利点

- **シンプル**: 理解しやすく、メンテナンスしやすい
- **ポータブル**: 外部依存なしでどこでも動作
- **拡張可能**: レイヤー分離により機能追加が容易
- **テスト可能**: ビジネスロジックが分離されており、ユニットテスト作成が容易
