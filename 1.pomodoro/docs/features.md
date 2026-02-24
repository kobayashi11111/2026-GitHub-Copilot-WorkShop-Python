# 機能仕様

## 概要

このドキュメントでは、ポモドーロタイマーアプリケーションの各機能の仕様と実装詳細を説明します。

## コア機能

### 1. ポモドーロタイマー

#### 1.1 基本タイマー機能

**クラス**: `PomodoroTimer`  
**メソッド**: `countdown(minutes: int, label: str) -> bool`

**仕様**:
- 指定した分数のカウントダウンタイマーを実行
- 1秒ごとに画面を更新（MM:SS形式）
- `\r` を使用して同じ行を上書き更新

**パラメータ**:
- `minutes`: カウントダウンの分数
- `label`: 表示ラベル（例: "⏰ 作業時間"）

**返り値**:
- `True`: 正常完了
- `False`: 中断（KeyboardInterrupt）

**表示形式**:
```
⏰ 作業時間: 24:35
```

**実装詳細**:
```python
total_seconds = minutes * 60
for remaining in range(total_seconds, 0, -1):
    mins, secs = divmod(remaining, 60)
    timer = f'{mins:02d}:{secs:02d}'
    print(f'\r{label}: {timer}', end='', flush=True)
    time.sleep(1)
```

---

#### 1.2 作業セッション

**メソッド**: `start_pomodoro() -> bool`

**フロー**:
1. 画面クリア
2. 開始メッセージ表示
3. 作業時間のカウントダウン（デフォルト25分）
4. 完了時、ゲーミフィケーションマネージャーに通知
5. 結果表示（XP、レベル、バッジ）
6. 休憩確認
7. 休憩タイマー実行（選択時）

**中断処理**:
- `Ctrl+C` で中断可能
- 中断時はポモドーロとしてカウントされない
- `countdown()` が `False` を返した場合、処理を中止

**デフォルト設定**:
- 作業時間: 25分
- 休憩時間: 5分

---

#### 1.3 休憩セッション

**トリガー**: 作業セッション完了後のユーザー選択

**仕様**:
- 作業完了後、休憩するか確認（y/n）
- `y` を選択すると休憩タイマー開始
- 休憩時間はデフォルト5分
- 休憩完了後、メインメニューに戻る

---

### 2. ゲーミフィケーション要素

#### 2.1 経験値（XP）システム

**クラス**: `GamificationManager`  
**メソッド**: `add_pomodoro(duration_minutes: int = 25)`

**XP獲得計算**:
```python
xp_earned = (duration_minutes / 25) * 100
```

**例**:
- 25分完了 → 100 XP
- 50分完了 → 200 XP
- 12.5分完了 → 50 XP

**累計XP更新**:
```python
self.data["xp"] += xp_earned
```

---

#### 2.2 レベルシステム

**メソッド**: `_check_level_up()`

**計算式**:
```python
new_level = 1 + int(self.data["xp"] / 500)
```

**レベルテーブル**:

| レベル | 必要XP（累計） | 必要XP（前レベルから） |
|--------|---------------|---------------------|
| 1      | 0             | -                   |
| 2      | 500           | 500                 |
| 3      | 1000          | 500                 |
| 4      | 1500          | 500                 |
| 5      | 2000          | 500                 |
| ...    | ...           | 500                 |

**レベルアップ通知**:
- レベルアップ時、新規バッジリストに追加
- 完了画面で「レベルX到達！」と表示

---

#### 2.3 ストリークシステム

**メソッド**: `_update_streak()`

**ロジック**:

```python
today = datetime.now().date()
last_date = datetime.fromisoformat(self.data["last_completion_date"]).date()
days_diff = (today - last_date).days

if days_diff == 0:
    # 同じ日 → 変更なし
    pass
elif days_diff == 1:
    # 連続している → +1
    self.data["current_streak"] += 1
else:
    # 途切れた → リセット
    self.data["current_streak"] = 1
```

**初回処理**:
```python
if last_date is None:
    self.data["current_streak"] = 1
```

**ベストストリーク更新**:
```python
if self.data["current_streak"] > self.data["best_streak"]:
    self.data["best_streak"] = self.data["current_streak"]
```

**更新タイミング**: ポモドーロ完了時（`add_pomodoro()` 内）

---

#### 2.4 バッジシステム

**メソッド**: `_check_badges() -> List[str]`

**バッジタイプ**:

1. **ストリークバッジ**

```python
streak_badges = {
    3: "🔥 3日連続達成！",
    7: "🔥🔥 1週間連続達成！",
    30: "🔥🔥🔥 30日連続達成！",
    100: "🔥🔥🔥🔥 100日連続達成！"
}
```

2. **回数達成バッジ**

```python
count_badges = {
    10: "⭐ 10回達成！",
    25: "⭐⭐ 25回達成！",
    50: "⭐⭐⭐ 50回達成！",
    100: "⭐⭐⭐⭐ 100回達成！",
    250: "⭐⭐⭐⭐⭐ 250回達成！"
}
```

**判定ロジック**:
```python
for days, badge in streak_badges.items():
    badge_id = f"streak_{days}"
    if self.data["current_streak"] >= days and badge_id not in self.data["badges"]:
        self.data["badges"].append(badge_id)
        new_badges.append(badge)
```

**特徴**:
- 条件を満たした瞬間に解放
- 一度獲得したバッジは再度通知されない
- 複数バッジを同時に獲得可能

---

### 3. 統計機能

#### 3.1 ステータス表示

**メソッド**: `show_status()`, `get_status()`

**表示項目**:
- レベル
- 経験値（現在 / 次のレベル）
- レベルアップ進捗（%とプログレスバー）
- 合計ポモドーロ回数
- 現在のストリーク
- 最長ストリーク
- 獲得バッジ数

**プログレスバー実装**:
```python
next_level_xp = self.data["level"] * 500
current_level_xp = (self.data["level"] - 1) * 500
progress = ((self.data["xp"] - current_level_xp) / (next_level_xp - current_level_xp)) * 100

# 表示（20文字幅）
progress_chars = int(progress / 5)
bar = '█' * progress_chars + '░' * (20 - progress_chars)
print(f"進捗: [{bar}] {progress:.1f}%")
```

---

#### 3.2 期間統計

**メソッド**: `show_statistics(period: str)`, `get_statistics(period: str)`

**対応期間**:
- `"week"`: 過去7日間
- `"month"`: 過去30日間
- `"all"`: 全期間

**統計項目**:
- 完了セッション数
- 総作業時間（分・時間）
- 1日平均セッション数
- 現在のストリーク
- 最長ストリーク
- 日別完了数のグラフ

**期間計算**:
```python
today = datetime.now().date()
if period == "week":
    start_date = today - timedelta(days=7)
elif period == "month":
    start_date = today - timedelta(days=30)
else:
    start_date = datetime.min.date()
```

**日別集計**:
```python
daily_counts = {}
for session in period_sessions:
    date = session["date"]
    daily_counts[date] = daily_counts.get(date, 0) + 1
```

**グラフ表示**:
```python
max_count = max(daily_counts.values())
for date in sorted(daily_counts.keys())[-7:]:  # 最新7日分
    count = daily_counts[date]
    bar_length = int((count / max(max_count, 1)) * 30)
    bar = '▓' * bar_length
    print(f"  {date}: {bar} ({count}回)")
```

---

#### 3.3 バッジコレクション

**メソッド**: `show_badges()`, `display_badges()`

**表示形式**:
- バッジIDから表示名へのマッピング
- 獲得順（データファイル内の順序）に表示

**バッジ名マッピング**:
```python
badge_names = {
    "streak_3": "🔥 3日連続",
    "streak_7": "🔥🔥 7日連続",
    "streak_30": "🔥🔥🔥 30日連続",
    "streak_100": "🔥🔥🔥🔥 100日連続",
    "count_10": "⭐ 10回達成",
    "count_25": "⭐⭐ 25回達成",
    "count_50": "⭐⭐⭐ 50回達成",
    "count_100": "⭐⭐⭐⭐ 100回達成",
    "count_250": "⭐⭐⭐⭐⭐ 250回達成"
}
```

---

### 4. データ永続化

#### 4.1 データ構造

詳細は [data-models.md](./data-models.md) を参照。

#### 4.2 保存

**メソッド**: `save_data()`

**保存タイミング**: `add_pomodoro()` 実行後

**実装**:
```python
with open(self.data_file, 'w', encoding='utf-8') as f:
    json.dump(self.data, f, ensure_ascii=False, indent=2)
```

**設定**:
- `ensure_ascii=False`: 日本語などをそのまま保存
- `indent=2`: 人間が読みやすい形式

---

#### 4.3 読み込み

**メソッド**: `_load_data()`

**実行タイミング**: `GamificationManager` 初期化時

**エラーハンドリング**:
```python
if os.path.exists(self.data_file):
    try:
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return self._create_default_data()
return self._create_default_data()
```

**フォールバック**: すべてのエラーでデフォルトデータを返却

---

### 5. ユーザーインターフェース

#### 5.1 メニューシステム

**メソッド**: `show_menu()`

**実装パターン**: 無限ループ + ユーザー入力

```python
while True:
    self.clear_screen()
    # メニュー表示
    choice = input("\n選択してください: ")
    
    if choice == '1':
        self.start_pomodoro()
        input("\nEnterキーで続行...")
    # ...
    elif choice == '0':
        break
```

**画面遷移**:
- 各機能実行後、`input("\nEnterキーで続行...")` で待機
- Enterキー押下でメインメニューに戻る

---

#### 5.2 画面クリア

**メソッド**: `clear_screen()`

**実装**:
```python
os.system('clear' if os.name != 'nt' else 'cls')
```

**OS判定**:
- `os.name == 'nt'`: Windows
- それ以外: Unix系（Linux, macOS）

---

#### 5.3 表示フォーマット

**ヘッダー/区切り線**:
```python
print("=" * 50)
```

**絵文字の使用**:
- 🍅: ポモドーロタイマー
- ⏰: タイマー
- 🎉: 完了
- ✨: XP
- 📊: レベル/ステータス
- 🔥: ストリーク
- 🏆: バッジ
- ⭐: 回数達成
- 📈: 統計
- ☕: 休憩

---

## 機能の拡張性

### カスタマイズ可能なパラメータ

**PomodoroTimer**:
```python
def __init__(self, work_duration: int = 25, break_duration: int = 5):
```

**GamificationManager**:
```python
def __init__(self, data_file: str = "pomodoro_data.json"):
```

### 将来の拡張案

1. **設定ファイル**: 作業時間、休憩時間、XP係数などを外部設定化
2. **サウンド通知**: 完了時に音を鳴らす
3. **デスクトップ通知**: システム通知の統合
4. **複数タイマープリセット**: 短いポモドーロ、長いポモドーロなど
5. **カテゴリ別集計**: プロジェクトやタスクごとの統計
6. **エクスポート機能**: CSV、PDF形式での統計出力
7. **Webダッシュボード**: Flask/FastAPIでのWeb UI提供
8. **モバイルアプリ**: React NativeやFlutterでのモバイル対応

---

## パフォーマンス

### 実行時間

- タイマー更新: 1秒ごと（`time.sleep(1)`）
- データ保存: 数ミリ秒（JSONファイルサイズ依存）
- 統計計算: 数ミリ秒（セッション数に依存）

### メモリ使用量

- 非常に軽量（すべてのデータをメモリ上に保持）
- データサイズの目安:
  - 1年分のデータ（毎日5セッション）: 約200KB
  - 100個のバッジ: 約5KB

### スケーラビリティ

**現在の制限**:
- 単一ユーザー
- ローカルファイルストレージ
- 同時実行非対応

**スケールアップのために必要な変更**:
- データベース導入（SQLite, PostgreSQL）
- 複数ユーザー対応（認証機能）
- API化（REST/GraphQL）
- ファイルロック機構（並行アクセス対応）

---

## セキュリティとプライバシー

### 収集データ

- 完了日時
- 作業時間
- 計算されたXP、レベル、バッジ

### 収集しないデータ

- 個人情報（名前、メールアドレス等）
- 作業内容
- 位置情報
- デバイス情報

### データの保護

- ローカルストレージのみ
- 外部送信なし
- ファイルパーミッションに注意（推奨: 600）

---

## テスト

現在、ユニットテストは実装されていませんが、以下のテストケースが推奨されます：

### ユニットテストケース

**GamificationManager**:
- XP計算の正確性
- レベルアップロジック
- ストリーク更新ロジック
- バッジ解放条件
- データ保存/読み込み

**PomodoroTimer**:
- カウントダウンロジック（モック使用）
- 画面クリア処理
- メニュー選択処理

### 統合テストケース

- 完全なポモドーロフロー
- データ永続化の検証
- 複数セッションでのストリーク計算

### エンドツーエンドテストケース

- ユーザーシナリオベースのテスト
- 長期間使用のシミュレーション
- エラー回復の検証

---

## 既知の制限事項

1. **タイムゾーン**: システムのローカルタイムを使用（UTC非対応）
2. **時刻変更**: システム時刻の変更に弱い（ストリーク計算に影響）
3. **同時実行**: 複数プロセスでの同時実行は未サポート
4. **ファイルロック**: データファイルの排他制御なし
5. **バックアップ**: 自動バックアップ機能なし
6. **バージョン管理**: データスキーマのバージョン管理なし
7. **入力検証**: ユーザー入力の厳密なバリデーションなし
8. **国際化**: 日本語のみ（多言語未対応）

---

## 用語集

- **ポモドーロ**: 25分の作業セッション
- **セッション**: 1回のポモドーロ実行
- **XP**: 経験値（Experience Points）
- **ストリーク**: 連続実行日数
- **バッジ**: 達成条件を満たすと獲得できる称号
- **ゲーミフィケーション**: ゲーム要素を取り入れた仕組み
