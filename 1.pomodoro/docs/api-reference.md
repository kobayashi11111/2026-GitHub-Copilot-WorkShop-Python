# API リファレンス

## 概要

このドキュメントでは、ポモドーロタイマーアプリケーションの内部APIを説明します。現在はコマンドラインアプリケーションですが、各クラスとメソッドは明確なインターフェースを持っており、将来的なWeb化や他のインターフェースへの対応が可能です。

## PomodoroTimer クラス

**モジュール**: `app.py`

### 初期化

```python
PomodoroTimer(work_duration: int = 25, break_duration: int = 5)
```

**パラメータ**:
- `work_duration` (int, optional): 作業時間（分）。デフォルト: 25
- `break_duration` (int, optional): 休憩時間（分）。デフォルト: 5

**戻り値**: `PomodoroTimer` インスタンス

**例**:
```python
# デフォルト設定（25分作業 + 5分休憩）
timer = PomodoroTimer()

# カスタム設定（50分作業 + 10分休憩）
timer = PomodoroTimer(work_duration=50, break_duration=10)
```

---

### countdown()

```python
countdown(self, minutes: int, label: str) -> bool
```

**説明**: カウントダウンタイマーを実行

**パラメータ**:
- `minutes` (int): タイマー時間（分）
- `label` (str): 表示するラベル（例: "⏰ 作業時間"）

**戻り値**: 
- `True`: タイマーが完了した
- `False`: ユーザーが中断した（Ctrl+C）

**動作**:
- 指定された分数をカウントダウン
- `MM:SS` 形式で進捗を表示
- `Ctrl+C` で中断可能

**例**:
```python
# 25分のカウントダウン
completed = timer.countdown(25, "⏰ 作業時間")
if completed:
    print("完了！")
else:
    print("中断されました")
```

---

### start_pomodoro()

```python
start_pomodoro(self) -> bool
```

**説明**: ポモドーロセッションを開始

**戻り値**:
- `True`: ポモドーロが完了した
- `False`: 中断された

**処理フロー**:
1. 画面クリアとヘッダー表示
2. 作業時間のカウントダウン
3. 完了時、ゲーミフィケーション処理（XP付与、バッジチェック）
4. 結果表示（XP、レベル、ストリーク、新規バッジ）
5. 休憩するか確認
6. 休憩する場合、休憩時間のカウントダウン

**副作用**:
- `GamificationManager.add_pomodoro()` を呼び出し
- データファイルに保存

**例**:
```python
result = timer.start_pomodoro()
```

---

### show_status()

```python
show_status(self) -> None
```

**説明**: 現在のステータスを表示

**表示内容**:
- レベル
- 経験値（現在値 / 次のレベルまで）
- プログレスバー
- 合計ポモドーロ数
- 現在のストリーク
- 最長ストリーク
- 獲得バッジ数

**例**:
```python
timer.show_status()
```

**出力例**:
```
==================================================
📊 ステータス
==================================================
レベル: 3
経験値: 1250 / 1500
進捗: [████████████░░░░░░░░] 50.0%

合計ポモドーロ: 12回
現在のストリーク: 🔥 5日
最長ストリーク: 🔥 7日
獲得バッジ数: 3個
==================================================
```

---

### show_statistics()

```python
show_statistics(self, period: str = "week") -> None
```

**説明**: 統計情報を表示

**パラメータ**:
- `period` (str): 統計期間
  - `"week"`: 過去7日間
  - `"month"`: 過去30日間
  - `"all"`: 全期間

**表示内容**:
- 完了セッション数
- 総作業時間（分・時間）
- 1日平均セッション数
- 現在のストリーク
- 最長ストリーク
- 日別完了数のグラフ（テキストベース、最新7日分）

**例**:
```python
# 週間統計
timer.show_statistics("week")

# 月間統計
timer.show_statistics("month")
```

---

### show_badges()

```python
show_badges(self) -> None
```

**説明**: 獲得したバッジ一覧を表示

**例**:
```python
timer.show_badges()
```

**出力例**:
```
==================================================
🏆 バッジコレクション
==================================================
獲得バッジ:
  🔥 3日連続
  🔥🔥 7日連続
  ⭐ 10回達成
  ⭐⭐ 25回達成
==================================================
```

---

### clear_screen()

```python
clear_screen(self) -> None
```

**説明**: ターミナル画面をクリア

**動作**:
- Unix系: `clear` コマンドを実行
- Windows: `cls` コマンドを実行

---

### show_menu()

```python
show_menu(self) -> None
```

**説明**: メインメニューを表示し、ユーザー入力を処理

**メニュー項目**:
1. ポモドーロ開始
2. ステータス表示
3. 週間統計
4. 月間統計
5. バッジ一覧
0. 終了

**動作**: 
- ユーザーが選択するまでループ
- 各機能実行後、Enterキーで続行

---

## GamificationManager クラス

**モジュール**: `gamification.py`

### 初期化

```python
GamificationManager(data_file: str = "pomodoro_data.json")
```

**パラメータ**:
- `data_file` (str, optional): データファイルのパス。デフォルト: `"pomodoro_data.json"`

**戻り値**: `GamificationManager` インスタンス

**動作**:
- データファイルが存在する場合: 読み込み
- 存在しない場合: デフォルトデータで初期化
- JSONが破損している場合: デフォルトデータで初期化

**例**:
```python
# デフォルトのデータファイル
gm = GamificationManager()

# カスタムデータファイル
gm = GamificationManager(data_file="custom_data.json")
```

---

### add_pomodoro()

```python
add_pomodoro(self, duration_minutes: int = 25) -> Dict
```

**説明**: ポモドーロ完了時の処理を実行

**パラメータ**:
- `duration_minutes` (int, optional): ポモドーロの時間（分）。デフォルト: 25

**戻り値**: 辞書型（以下のキーを含む）
```python
{
    "xp_earned": float,        # 今回獲得したXP
    "total_xp": float,         # 累計XP
    "level": int,              # 現在のレベル
    "new_badges": List[str],   # 新しく獲得したバッジの表示名リスト
    "streak": int              # 現在のストリーク
}
```

**処理内容**:
1. XP計算と付与（`(duration_minutes / 25) * 100`）
2. ポモドーロ数のカウントアップ
3. セッション記録の追加
4. 完了日付の記録
5. ストリークの更新
6. レベルアップチェック
7. バッジ獲得チェック
8. データの保存

**副作用**:
- データファイルに保存

**例**:
```python
# 25分のポモドーロ完了
result = gm.add_pomodoro(25)
print(f"獲得XP: {result['xp_earned']}")
print(f"レベル: {result['level']}")

# 50分のポモドーロ完了
result = gm.add_pomodoro(50)
# → 200XPを獲得
```

---

### get_status()

```python
get_status(self) -> Dict
```

**説明**: 現在のステータスを取得

**戻り値**: 辞書型
```python
{
    "level": int,              # 現在のレベル
    "xp": float,               # 現在のXP
    "next_level_xp": int,      # 次のレベルに必要なXP
    "progress": float,         # 次のレベルまでの進捗率（0-100）
    "total_pomodoros": int,    # 累計ポモドーロ数
    "current_streak": int,     # 現在のストリーク
    "best_streak": int,        # 最長ストリーク
    "badges_count": int        # 獲得バッジ数
}
```

**計算式**:
- `next_level_xp` = `level * 500`
- `current_level_xp` = `(level - 1) * 500`
- `progress` = `((xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100`

**例**:
```python
status = gm.get_status()
print(f"レベル: {status['level']}")
print(f"XP: {status['xp']} / {status['next_level_xp']}")
print(f"進捗: {status['progress']:.1f}%")
```

---

### get_statistics()

```python
get_statistics(self, period: str = "week") -> Dict
```

**説明**: 統計情報を取得

**パラメータ**:
- `period` (str): 統計期間
  - `"week"`: 過去7日間
  - `"month"`: 過去30日間
  - `"all"`: 全期間

**戻り値**: 辞書型
```python
{
    "period": str,                        # 指定された期間
    "total_sessions": int,                # 期間内の完了セッション数
    "total_minutes": int,                 # 期間内の総作業時間（分）
    "average_per_day": float,             # 1日平均セッション数
    "daily_counts": Dict[str, int],       # 日別の完了数 {"2026-02-24": 3, ...}
    "current_streak": int,                # 現在のストリーク
    "best_streak": int                    # 最長ストリーク
}
```

**例**:
```python
# 週間統計
stats = gm.get_statistics("week")
print(f"完了セッション: {stats['total_sessions']}回")
print(f"総作業時間: {stats['total_minutes']}分")
print(f"1日平均: {stats['average_per_day']:.1f}回")

# 日別の完了数
for date, count in stats['daily_counts'].items():
    print(f"{date}: {count}回")
```

---

### display_badges()

```python
display_badges(self) -> str
```

**説明**: 獲得したバッジを表示用文字列として返す

**戻り値**: 文字列
- バッジがない場合: `"まだバッジを獲得していません"`
- バッジがある場合: バッジ一覧（複数行）

**例**:
```python
badges_text = gm.display_badges()
print(badges_text)
```

**出力例**:
```
獲得バッジ:
  🔥 3日連続
  🔥🔥 7日連続
  ⭐ 10回達成
  ⭐⭐ 25回達成
```

---

### save_data()

```python
save_data(self) -> None
```

**説明**: データをJSONファイルに保存

**副作用**:
- `self.data_file` に指定されたファイルに書き込み
- エンコーディング: UTF-8
- インデント: 2スペース
- `ensure_ascii=False` でUnicode文字をそのまま保存

**例**:
```python
gm.save_data()
```

**注意**: 
- `add_pomodoro()` 実行時に自動的に呼ばれるため、通常は手動で呼ぶ必要なし

---

## 内部メソッド（Private）

### GamificationManager._check_level_up()

```python
_check_level_up(self) -> None
```

**説明**: レベルアップのチェックと処理

**計算式**: `level = 1 + int(xp / 500)`

**副作用**: `self.data["level"]` を更新

---

### GamificationManager._update_streak()

```python
_update_streak(self) -> None
```

**説明**: ストリーク（連続日数）の更新

**ロジック**:
- 初回: ストリーク = 1
- 前日に完了している: ストリーク +1
- 2日以上空いている: ストリーク = 1 にリセット
- 同日に複数回完了: 変化なし
- ベストストリーク更新: `current_streak > best_streak` の場合

**副作用**:
- `self.data["current_streak"]` を更新
- `self.data["best_streak"]` を更新（必要に応じて）
- `self.data["last_completion_date"]` を更新

---

### GamificationManager._check_badges()

```python
_check_badges(self) -> List[str]
```

**説明**: 新しいバッジをチェックして獲得

**戻り値**: 新しく獲得したバッジの表示名リスト

**チェックするバッジ**:

| バッジID | 条件 | 表示名 |
|----------|------|--------|
| `streak_3` | ストリーク ≥ 3 | 🔥 3日連続達成！ |
| `streak_7` | ストリーク ≥ 7 | 🔥🔥 1週間連続達成！ |
| `streak_30` | ストリーク ≥ 30 | 🔥🔥🔥 30日連続達成！ |
| `streak_100` | ストリーク ≥ 100 | 🔥🔥🔥🔥 100日連続達成！ |
| `count_10` | 累計 ≥ 10 | ⭐ 10回達成！ |
| `count_25` | 累計 ≥ 25 | ⭐⭐ 25回達成！ |
| `count_50` | 累計 ≥ 50 | ⭐⭐⭐ 50回達成！ |
| `count_100` | 累計 ≥ 100 | ⭐⭐⭐⭐ 100回達成！ |
| `count_250` | 累計 ≥ 250 | ⭐⭐⭐⭐⭐ 250回達成！ |

**副作用**: `self.data["badges"]` に新しいバッジIDを追加

**例**:
```python
new_badges = gm._check_badges()
for badge in new_badges:
    print(badge)  # "🔥 3日連続達成！" など
```

---

### GamificationManager._create_default_data()

```python
_create_default_data(self) -> Dict
```

**説明**: デフォルトのデータ構造を作成

**戻り値**: デフォルトデータの辞書

---

### GamificationManager._load_data()

```python
_load_data(self) -> Dict
```

**説明**: データファイルから情報を読み込む

**エラーハンドリング**:
- ファイルが存在しない → デフォルトデータ
- JSONDecodeError → デフォルトデータ
- IOError / OSError → デフォルトデータ

**後方互換性**: 欠落フィールドはデフォルト値で補完

---

## 使用例

### 基本的な使用フロー

```python
from app import PomodoroTimer

# 1. タイマーを作成
timer = PomodoroTimer(work_duration=25, break_duration=5)

# 2. メニューを表示（対話型）
timer.show_menu()
```

### プログラマティックな使用

```python
from gamification import GamificationManager

# 1. ゲーミフィケーションマネージャーを作成
gm = GamificationManager()

# 2. ポモドーロを完了
result = gm.add_pomodoro(25)
print(f"XP獲得: {result['xp_earned']}")
print(f"レベル: {result['level']}")

if result['new_badges']:
    print("新しいバッジ:")
    for badge in result['new_badges']:
        print(f"  - {badge}")

# 3. ステータスを確認
status = gm.get_status()
print(f"累計: {status['total_pomodoros']}回")
print(f"ストリーク: {status['current_streak']}日")

# 4. 統計を取得
stats = gm.get_statistics("week")
print(f"今週の完了数: {stats['total_sessions']}回")
```

### カスタムデータファイルの使用

```python
# テスト用の一時データファイルを使用
gm = GamificationManager(data_file="test_data.json")

# 通常通り使用
gm.add_pomodoro(25)
```

---

## エラーと例外

### KeyboardInterrupt

**発生箇所**: `PomodoroTimer.countdown()`

**原因**: ユーザーが `Ctrl+C` を押した

**処理**: 
- カウントダウンを中断
- `False` を返す
- エラーメッセージを表示

### JSONDecodeError

**発生箇所**: `GamificationManager._load_data()`

**原因**: データファイルのJSONが破損

**処理**: デフォルトデータで初期化

### IOError / OSError

**発生箇所**: `GamificationManager._load_data()`, `save_data()`

**原因**: ファイルアクセスエラー

**処理**: デフォルトデータで初期化、またはエラー伝播

---

## 今後の拡張

現在のAPIは、以下のような拡張に対応可能です：

1. **REST API化**: 各メソッドをHTTPエンドポイントとして公開
2. **WebSocket対応**: リアルタイムタイマー通知
3. **マルチユーザー**: ユーザーIDをパラメータとして追加
4. **タスク連携**: `add_pomodoro()` にタスクIDを追加
5. **カスタマイズ**: バッジやレベルシステムの設定を外部化
