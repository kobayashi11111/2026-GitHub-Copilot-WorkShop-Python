"""
ゲーミフィケーション要素を管理するモジュール
経験値、レベル、バッジ、ストリーク、統計などを扱う
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Set


class GamificationManager:
    """ゲーミフィケーション要素を管理するクラス"""
    
    def __init__(self, data_file: str = "pomodoro_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """データファイルから情報を読み込む"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError, OSError):
                return self._create_default_data()
        return self._create_default_data()
    
    def _create_default_data(self) -> Dict:
        """デフォルトのデータ構造を作成"""
        return {
            "xp": 0,
            "level": 1,
            "total_pomodoros": 0,
            "completed_dates": [],  # 完了した日付のリスト
            "badges": [],  # 獲得したバッジのリスト
            "sessions": [],  # セッション履歴
            "current_streak": 0,
            "best_streak": 0,
            "last_completion_date": None
        }
    
    def save_data(self):
        """データをファイルに保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_pomodoro(self, duration_minutes: int = 25):
        """
        ポモドーロ完了時の処理
        - XPを付与
        - レベルアップチェック
        - ストリーク更新
        - バッジチェック
        """
        # XP付与（25分で100XP）
        xp_earned = (duration_minutes / 25) * 100
        self.data["xp"] += xp_earned
        
        # ポモドーロ数増加
        self.data["total_pomodoros"] += 1
        
        # セッション記録
        today = datetime.now().strftime("%Y-%m-%d")
        session = {
            "date": today,
            "datetime": datetime.now().isoformat(),
            "duration": duration_minutes,
            "xp_earned": xp_earned
        }
        self.data["sessions"].append(session)
        
        # 完了日付を記録
        if today not in self.data["completed_dates"]:
            self.data["completed_dates"].append(today)
        
        # ストリーク更新
        self._update_streak()
        
        # レベルアップチェック
        new_badges = []
        old_level = self.data["level"]
        self._check_level_up()
        if self.data["level"] > old_level:
            new_badges.append(f"レベル{self.data['level']}到達！")
        
        # バッジチェック
        new_badges.extend(self._check_badges())
        
        self.save_data()
        
        return {
            "xp_earned": xp_earned,
            "total_xp": self.data["xp"],
            "level": self.data["level"],
            "new_badges": new_badges,
            "streak": self.data["current_streak"]
        }
    
    def _check_level_up(self):
        """レベルアップのチェックと処理"""
        # レベル計算式: level = 1 + floor(xp / 500)
        new_level = 1 + int(self.data["xp"] / 500)
        if new_level > self.data["level"]:
            self.data["level"] = new_level
    
    def _update_streak(self):
        """ストリーク（連続日数）の更新"""
        today = datetime.now().date()
        last_date = self.data.get("last_completion_date")
        
        if last_date:
            last_date = datetime.fromisoformat(last_date).date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # 同じ日
                pass
            elif days_diff == 1:
                # 連続している
                self.data["current_streak"] += 1
            else:
                # 連続が途切れた
                self.data["current_streak"] = 1
        else:
            # 初回
            self.data["current_streak"] = 1
        
        # ベストストリーク更新
        if self.data["current_streak"] > self.data["best_streak"]:
            self.data["best_streak"] = self.data["current_streak"]
        
        self.data["last_completion_date"] = today.isoformat()
    
    def _check_badges(self) -> List[str]:
        """新しいバッジをチェック"""
        new_badges = []
        
        # ストリークバッジ
        streak_badges = {
            3: "🔥 3日連続達成！",
            7: "🔥🔥 1週間連続達成！",
            30: "🔥🔥🔥 30日連続達成！",
            100: "🔥🔥🔥🔥 100日連続達成！"
        }
        
        for days, badge in streak_badges.items():
            badge_id = f"streak_{days}"
            if self.data["current_streak"] >= days and badge_id not in self.data["badges"]:
                self.data["badges"].append(badge_id)
                new_badges.append(badge)
        
        # 回数達成バッジ
        count_badges = {
            10: "⭐ 10回達成！",
            25: "⭐⭐ 25回達成！",
            50: "⭐⭐⭐ 50回達成！",
            100: "⭐⭐⭐⭐ 100回達成！",
            250: "⭐⭐⭐⭐⭐ 250回達成！"
        }
        
        for count, badge in count_badges.items():
            badge_id = f"count_{count}"
            if self.data["total_pomodoros"] >= count and badge_id not in self.data["badges"]:
                self.data["badges"].append(badge_id)
                new_badges.append(badge)
        
        return new_badges
    
    def get_statistics(self, period: str = "week") -> Dict:
        """統計情報を取得"""
        today = datetime.now().date()
        
        if period == "week":
            start_date = today - timedelta(days=7)
        elif period == "month":
            start_date = today - timedelta(days=30)
        else:
            start_date = datetime.min.date()
        
        # 期間内のセッションを抽出
        period_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["datetime"]).date() >= start_date
        ]
        
        total_sessions = len(period_sessions)
        total_minutes = sum(s["duration"] for s in period_sessions)
        
        # 日別のポモドーロ数
        daily_counts = {}
        for session in period_sessions:
            date = session["date"]
            daily_counts[date] = daily_counts.get(date, 0) + 1
        
        # 経過日数を計算（最低1日）
        days_elapsed = max(1, (today - start_date).days)
        if days_elapsed == 0:
            days_elapsed = 1
        
        return {
            "period": period,
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
            "average_per_day": total_sessions / days_elapsed,
            "daily_counts": daily_counts,
            "current_streak": self.data["current_streak"],
            "best_streak": self.data["best_streak"]
        }
    
    def get_status(self) -> Dict:
        """現在の状態を取得"""
        next_level_xp = self.data["level"] * 500
        current_level_xp = (self.data["level"] - 1) * 500
        progress = ((self.data["xp"] - current_level_xp) / (next_level_xp - current_level_xp)) * 100
        
        return {
            "level": self.data["level"],
            "xp": self.data["xp"],
            "next_level_xp": next_level_xp,
            "progress": progress,
            "total_pomodoros": self.data["total_pomodoros"],
            "current_streak": self.data["current_streak"],
            "best_streak": self.data["best_streak"],
            "badges_count": len(self.data["badges"])
        }
    
    def display_badges(self) -> str:
        """獲得したバッジを表示用文字列として返す"""
        if not self.data["badges"]:
            return "まだバッジを獲得していません"
        
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
        
        result = "獲得バッジ:\n"
        for badge_id in self.data["badges"]:
            badge_name = badge_names.get(badge_id, badge_id)
            result += f"  {badge_name}\n"
        
        return result
