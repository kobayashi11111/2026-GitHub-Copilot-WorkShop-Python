"""
PomodoroTimer クラスのテスト
"""
import pytest
from unittest.mock import MagicMock, patch, call
from app import PomodoroTimer


class TestPomodoroTimerInit:
    """初期化のテスト"""
    
    @pytest.fixture
    def timer(self):
        """PomodoroTimerのインスタンスを作成"""
        with patch('app.GamificationManager'):
            return PomodoroTimer()
    
    def test_default_initialization(self, timer):
        """デフォルトの初期化テスト"""
        assert timer.work_duration == 25
        assert timer.break_duration == 5
    
    def test_custom_initialization(self):
        """カスタム時間での初期化テスト"""
        with patch('app.GamificationManager'):
            timer = PomodoroTimer(work_duration=30, break_duration=10)
            assert timer.work_duration == 30
            assert timer.break_duration == 10
    
    def test_gamification_manager_initialized(self, timer):
        """GamificationManagerが初期化されるかテスト"""
        assert timer.gm is not None


class TestShowStatus:
    """ステータス表示機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager') as mock_gm:
            timer = PomodoroTimer()
            timer.gm = mock_gm.return_value
            return timer
    
    def test_show_status_calls_get_status(self, timer):
        """show_statusがget_statusを呼び出すかテスト"""
        mock_status = {
            'level': 5,
            'xp': 2000,
            'next_level_xp': 2500,
            'progress': 40.0,
            'total_pomodoros': 20,
            'current_streak': 7,
            'best_streak': 10,
            'badges_count': 5
        }
        timer.gm.get_status.return_value = mock_status
        
        with patch('builtins.print'):
            with patch.object(timer, 'clear_screen'):
                timer.show_status()
        
        timer.gm.get_status.assert_called_once()
    
    def test_show_status_displays_all_info(self, timer, capsys):
        """ステータスがすべて表示されるかテスト"""
        mock_status = {
            'level': 3,
            'xp': 1250.0,
            'next_level_xp': 1500,
            'progress': 50.0,
            'total_pomodoros': 12,
            'current_streak': 5,
            'best_streak': 7,
            'badges_count': 3
        }
        timer.gm.get_status.return_value = mock_status
        
        with patch.object(timer, 'clear_screen'):
            timer.show_status()
        
        captured = capsys.readouterr()
        output = captured.out
        
        # 主要な情報が表示されているか確認
        assert "レベル: 3" in output
        assert "経験値: 1250" in output
        assert "合計ポモドーロ: 12回" in output
        assert "現在のストリーク: 🔥 5日" in output
        assert "最長ストリーク: 🔥 7日" in output
        assert "獲得バッジ数: 3個" in output


class TestShowStatistics:
    """統計表示機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager') as mock_gm:
            timer = PomodoroTimer()
            timer.gm = mock_gm.return_value
            return timer
    
    def test_show_statistics_week(self, timer):
        """週間統計の表示テスト"""
        mock_stats = {
            'total_sessions': 15,
            'total_minutes': 375,
            'average_per_day': 2.14,
            'daily_counts': {'2024-01-01': 3, '2024-01-02': 5},
            'current_streak': 5,
            'best_streak': 8
        }
        timer.gm.get_statistics.return_value = mock_stats
        
        with patch('builtins.print'):
            with patch.object(timer, 'clear_screen'):
                timer.show_statistics("week")
        
        timer.gm.get_statistics.assert_called_once_with("week")
    
    def test_show_statistics_month(self, timer):
        """月間統計の表示テスト"""
        mock_stats = {
            'total_sessions': 50,
            'total_minutes': 1250,
            'average_per_day': 1.67,
            'daily_counts': {},
            'current_streak': 10,
            'best_streak': 15
        }
        timer.gm.get_statistics.return_value = mock_stats
        
        with patch('builtins.print'):
            with patch.object(timer, 'clear_screen'):
                timer.show_statistics("month")
        
        timer.gm.get_statistics.assert_called_once_with("month")
    
    def test_show_statistics_displays_info(self, timer, capsys):
        """統計情報が表示されるかテスト"""
        mock_stats = {
            'total_sessions': 20,
            'total_minutes': 500,
            'average_per_day': 2.86,
            'daily_counts': {'2024-01-01': 3},
            'current_streak': 7,
            'best_streak': 10
        }
        timer.gm.get_statistics.return_value = mock_stats
        
        with patch.object(timer, 'clear_screen'):
            timer.show_statistics("week")
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "完了セッション: 20回" in output
        assert "総作業時間: 500分" in output
        assert "1日平均: 2.9回" in output


class TestShowBadges:
    """バッジ表示機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager') as mock_gm:
            timer = PomodoroTimer()
            timer.gm = mock_gm.return_value
            return timer
    
    def test_show_badges_calls_display_badges(self, timer):
        """show_badgesがdisplay_badgesを呼び出すかテスト"""
        timer.gm.display_badges.return_value = "🔥 3日連続"
        
        with patch('builtins.print'):
            with patch.object(timer, 'clear_screen'):
                timer.show_badges()
        
        timer.gm.display_badges.assert_called_once()
    
    def test_show_badges_displays_result(self, timer, capsys):
        """バッジ情報が表示されるかテスト"""
        badge_text = "獲得バッジ:\n  🔥 3日連続\n  ⭐ 10回達成"
        timer.gm.display_badges.return_value = badge_text
        
        with patch.object(timer, 'clear_screen'):
            timer.show_badges()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "🏆 バッジコレクション" in output
        assert badge_text in output


class TestCountdown:
    """カウントダウン機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager'):
            return PomodoroTimer()
    
    def test_countdown_completion(self, timer):
        """カウントダウンが完了するかテスト"""
        with patch('time.sleep'):
            with patch('builtins.print'):
                result = timer.countdown(0, "テスト")
                assert result is True
    
    def test_countdown_interruption(self, timer):
        """カウントダウンが中断されるかテスト"""
        with patch('time.sleep', side_effect=KeyboardInterrupt):
            result = timer.countdown(1, "テスト")
            assert result is False
    
    def test_countdown_duration_calculation(self, timer):
        """カウントダウンの時間計算テスト"""
        with patch('time.sleep') as mock_sleep:
            with patch('builtins.print'):
                timer.countdown(1, "テスト")
                # 1分 = 60秒
                assert mock_sleep.call_count == 60


class TestStartPomodoro:
    """ポモドーロ開始機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager') as mock_gm:
            timer = PomodoroTimer()
            timer.gm = mock_gm.return_value
            return timer
    
    def test_start_pomodoro_success(self, timer):
        """ポモドーロが正常に完了するかテスト"""
        mock_result = {
            'xp_earned': 100,
            'total_xp': 100,
            'level': 1,
            'new_badges': [],
            'streak': 1
        }
        timer.gm.add_pomodoro.return_value = mock_result
        
        with patch.object(timer, 'clear_screen'):
            with patch.object(timer, 'countdown', return_value=True):
                with patch('builtins.input', return_value='n'):
                    with patch('builtins.print'):
                        result = timer.start_pomodoro()
        
        assert result is True
        timer.gm.add_pomodoro.assert_called_once_with(25)
    
    def test_start_pomodoro_interrupted(self, timer):
        """ポモドーロが中断されるかテスト"""
        with patch.object(timer, 'clear_screen'):
            with patch.object(timer, 'countdown', return_value=False):
                with patch('builtins.print'):
                    result = timer.start_pomodoro()
        
        assert result is False
        timer.gm.add_pomodoro.assert_not_called()
    
    def test_start_pomodoro_with_break(self, timer):
        """休憩時間を含むポモドーロのテスト"""
        mock_result = {
            'xp_earned': 100,
            'total_xp': 100,
            'level': 1,
            'new_badges': [],
            'streak': 1
        }
        timer.gm.add_pomodoro.return_value = mock_result
        
        with patch.object(timer, 'clear_screen'):
            with patch.object(timer, 'countdown', return_value=True) as mock_countdown:
                with patch('builtins.input', return_value='y'):
                    with patch('builtins.print'):
                        result = timer.start_pomodoro()
        
        # 作業時間と休憩時間の2回カウントダウンが呼ばれる
        assert mock_countdown.call_count == 2
    
    def test_start_pomodoro_displays_new_badges(self, timer, capsys):
        """新しいバッジが表示されるかテスト"""
        mock_result = {
            'xp_earned': 100,
            'total_xp': 500,
            'level': 2,
            'new_badges': ['🔥 3日連続達成！', 'レベル2到達！'],
            'streak': 3
        }
        timer.gm.add_pomodoro.return_value = mock_result
        
        with patch.object(timer, 'clear_screen'):
            with patch.object(timer, 'countdown', return_value=True):
                with patch('builtins.input', return_value='n'):
                    timer.start_pomodoro()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "新しいバッジを獲得しました" in output
        assert "🔥 3日連続達成！" in output
        assert "レベル2到達！" in output


class TestClearScreen:
    """画面クリア機能のテスト"""
    
    @pytest.fixture
    def timer(self):
        with patch('app.GamificationManager'):
            return PomodoroTimer()
    
    def test_clear_screen_unix(self, timer):
        """Unix系での画面クリアテスト"""
        with patch('os.system') as mock_system:
            with patch('os.name', 'posix'):
                timer.clear_screen()
                mock_system.assert_called_once_with('clear')
    
    def test_clear_screen_windows(self, timer):
        """Windowsでの画面クリアテスト"""
        with patch('os.system') as mock_system:
            with patch('os.name', 'nt'):
                timer.clear_screen()
                mock_system.assert_called_once_with('cls')


class TestEdgeCases:
    """エッジケースのテスト"""
    
    def test_zero_work_duration(self):
        """作業時間が0分の場合のテスト"""
        with patch('app.GamificationManager'):
            timer = PomodoroTimer(work_duration=0, break_duration=5)
            assert timer.work_duration == 0
    
    def test_zero_break_duration(self):
        """休憩時間が0分の場合のテスト"""
        with patch('app.GamificationManager'):
            timer = PomodoroTimer(work_duration=25, break_duration=0)
            assert timer.break_duration == 0
    
    def test_large_duration(self):
        """非常に長い時間の場合のテスト"""
        with patch('app.GamificationManager'):
            timer = PomodoroTimer(work_duration=1000, break_duration=100)
            assert timer.work_duration == 1000
            assert timer.break_duration == 100
