"""
ゲーミフィケーション要素を持つポモドーロタイマーアプリ
"""
import time
import os
import sys
from datetime import datetime
from gamification import GamificationManager
from visual_feedback import VisualFeedback


class PomodoroTimer:
    """ポモドーロタイマーのメインクラス"""
    
    def __init__(self, work_duration: int = 25, break_duration: int = 5, 
                 use_visual_feedback: bool = True):
        self.work_duration = work_duration  # 作業時間（分）
        self.break_duration = break_duration  # 休憩時間（分）
        self.gm = GamificationManager()
        self.use_visual_feedback = use_visual_feedback
        self.vf = VisualFeedback() if use_visual_feedback else None
    
    def clear_screen(self):
        """画面をクリア"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def countdown(self, minutes: int, label: str) -> bool:
        """
        カウントダウンタイマー
        Returns: True if completed, False if interrupted
        """
        total_seconds = minutes * 60
        
        try:
            if self.use_visual_feedback and self.vf:
                # 視覚的フィードバック付きカウントダウン
                for remaining in range(total_seconds, 0, -1):
                    # 画面をクリアして再描画
                    print("\033[2J\033[H", end='')
                    
                    # フレーム番号を計算
                    frame = total_seconds - remaining
                    
                    # 完全な視覚的表示を作成
                    display = self.vf.create_complete_display(
                        remaining, total_seconds, label, frame, 
                        show_particles=(label == "⏰ 作業時間")
                    )
                    print(display)
                    
                    time.sleep(1)
            else:
                # シンプルなカウントダウン
                for remaining in range(total_seconds, 0, -1):
                    mins, secs = divmod(remaining, 60)
                    timer = f'{mins:02d}:{secs:02d}'
                    print(f'\r{label}: {timer}', end='', flush=True)
                    time.sleep(1)
            
            print(f'\r{label}: 完了！' + ' ' * 20)
            return True
        except KeyboardInterrupt:
            print(f'\n\n{label}が中断されました')
            return False
    
    def start_pomodoro(self) -> bool:
        """ポモドーロセッションを開始"""
        self.clear_screen()
        print("=" * 50)
        print("🍅 ポモドーロタイマー開始！")
        print("=" * 50)
        print(f"作業時間: {self.work_duration}分")
        print("Ctrl+C で中断\n")
        
        # 作業時間
        if not self.countdown(self.work_duration, "⏰ 作業時間"):
            return False
        
        # 作業完了時の処理
        result = self.gm.add_pomodoro(self.work_duration)
        
        print("\n" + "=" * 50)
        print("🎉 ポモドーロ完了！")
        print("=" * 50)
        print(f"✨ 獲得XP: +{result['xp_earned']:.0f} (合計: {result['total_xp']:.0f})")
        print(f"📊 レベル: {result['level']}")
        print(f"🔥 現在のストリーク: {result['streak']}日")
        
        if result['new_badges']:
            print("\n🎊 新しいバッジを獲得しました！")
            for badge in result['new_badges']:
                print(f"   {badge}")
        
        print("\n" + "=" * 50)
        
        # 休憩時間
        response = input(f"\n{self.break_duration}分の休憩を取りますか？ (y/n): ")
        if response.lower() == 'y':
            print("\n休憩時間開始...")
            self.countdown(self.break_duration, "☕ 休憩時間")
            print("\n休憩終了！次のポモドーロを始めましょう！")
        
        return True
    
    def show_status(self):
        """現在のステータスを表示"""
        self.clear_screen()
        status = self.gm.get_status()
        
        print("=" * 50)
        print("📊 ステータス")
        print("=" * 50)
        print(f"レベル: {status['level']}")
        print(f"経験値: {status['xp']:.0f} / {status['next_level_xp']}")
        
        # プログレスバー
        progress = int(status['progress'] / 5)
        bar = '█' * progress + '░' * (20 - progress)
        print(f"進捗: [{bar}] {status['progress']:.1f}%")
        
        print(f"\n合計ポモドーロ: {status['total_pomodoros']}回")
        print(f"現在のストリーク: 🔥 {status['current_streak']}日")
        print(f"最長ストリーク: 🔥 {status['best_streak']}日")
        print(f"獲得バッジ数: {status['badges_count']}個")
        print("=" * 50)
    
    def show_statistics(self, period: str = "week"):
        """統計情報を表示"""
        self.clear_screen()
        stats = self.gm.get_statistics(period)
        
        period_name = {"week": "週間", "month": "月間", "all": "全期間"}
        
        print("=" * 50)
        print(f"📈 {period_name.get(period, period)}統計")
        print("=" * 50)
        print(f"完了セッション: {stats['total_sessions']}回")
        print(f"総作業時間: {stats['total_minutes']}分 ({stats['total_minutes']/60:.1f}時間)")
        print(f"1日平均: {stats['average_per_day']:.1f}回")
        print(f"現在のストリーク: {stats['current_streak']}日")
        print(f"最長ストリーク: {stats['best_streak']}日")
        
        # 日別グラフ（シンプルなテキストベース）
        if stats['daily_counts']:
            print("\n日別完了数:")
            max_count = max(stats['daily_counts'].values())
            for date in sorted(stats['daily_counts'].keys())[-7:]:  # 最新7日分
                count = stats['daily_counts'][date]
                bar_length = int((count / max(max_count, 1)) * 30)
                bar = '▓' * bar_length
                print(f"  {date}: {bar} ({count}回)")
        
        print("=" * 50)
    
    def show_badges(self):
        """バッジ一覧を表示"""
        self.clear_screen()
        print("=" * 50)
        print("🏆 バッジコレクション")
        print("=" * 50)
        print(self.gm.display_badges())
        print("=" * 50)
    
    def show_menu(self):
        """メインメニューを表示"""
        while True:
            self.clear_screen()
            print("=" * 50)
            print("🍅 ポモドーロタイマー with ゲーミフィケーション")
            print("=" * 50)
            print("1. ポモドーロ開始")
            print("2. ステータス表示")
            print("3. 週間統計")
            print("4. 月間統計")
            print("5. バッジ一覧")
            print("6. 視覚的フィードバック切替")
            print("0. 終了")
            print("=" * 50)
            if self.use_visual_feedback:
                print("✨ 視覚的フィードバック: ON")
            else:
                print("📝 視覚的フィードバック: OFF")
            print("=" * 50)
            
            choice = input("\n選択してください: ")
            
            if choice == '1':
                self.start_pomodoro()
                input("\nEnterキーで続行...")
            elif choice == '2':
                self.show_status()
                input("\nEnterキーで続行...")
            elif choice == '3':
                self.show_statistics("week")
                input("\nEnterキーで続行...")
            elif choice == '4':
                self.show_statistics("month")
                input("\nEnterキーで続行...")
            elif choice == '5':
                self.show_badges()
                input("\nEnterキーで続行...")
            elif choice == '6':
                self.use_visual_feedback = not self.use_visual_feedback
                if self.use_visual_feedback and self.vf is None:
                    self.vf = VisualFeedback()
                status = "ON" if self.use_visual_feedback else "OFF"
                print(f"\n視覚的フィードバックを{status}にしました")
                time.sleep(1)
            elif choice == '0':
                print("\nありがとうございました！")
                break
            else:
                print("\n無効な選択です")
                time.sleep(1)


def main():
    """メイン関数"""
    timer = PomodoroTimer()
    timer.show_menu()


if __name__ == "__main__":
    main()
