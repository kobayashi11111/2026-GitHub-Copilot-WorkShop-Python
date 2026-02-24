"""
GamificationManager クラスの包括的なテスト
"""
import json
import os
import pytest
from datetime import datetime, timedelta
from gamification import GamificationManager


class TestGamificationManagerBasics:
    """基本機能のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        """一時的なデータファイルを作成"""
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        """GamificationManagerのインスタンスを作成"""
        return GamificationManager(data_file=temp_data_file)
    
    def test_initialization(self, gm):
        """初期化が正しく行われるかテスト"""
        assert gm.data["xp"] == 0
        assert gm.data["level"] == 1
        assert gm.data["total_pomodoros"] == 0
        assert gm.data["current_streak"] == 0
        assert gm.data["best_streak"] == 0
        assert len(gm.data["badges"]) == 0
        assert len(gm.data["sessions"]) == 0
    
    def test_create_default_data(self, gm):
        """デフォルトデータ構造が正しく作成されるかテスト"""
        default_data = gm._create_default_data()
        assert "xp" in default_data
        assert "level" in default_data
        assert "total_pomodoros" in default_data
        assert "completed_dates" in default_data
        assert "badges" in default_data
        assert "sessions" in default_data
        assert "current_streak" in default_data
        assert "best_streak" in default_data
        assert "last_completion_date" in default_data
    
    def test_save_and_load_data(self, temp_data_file):
        """データの保存と読み込みが正しく動作するかテスト"""
        # データを作成して保存
        gm1 = GamificationManager(data_file=temp_data_file)
        gm1.data["xp"] = 500
        gm1.data["level"] = 2
        gm1.save_data()
        
        # 新しいインスタンスでデータを読み込み
        gm2 = GamificationManager(data_file=temp_data_file)
        assert gm2.data["xp"] == 500
        assert gm2.data["level"] == 2


class TestPomodoroCompletion:
    """ポモドーロ完了機能のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_add_pomodoro_basic(self, gm):
        """基本的なポモドーロ追加のテスト"""
        result = gm.add_pomodoro(25)
        
        assert result["xp_earned"] == 100
        assert result["total_xp"] == 100
        assert result["level"] == 1
        assert gm.data["total_pomodoros"] == 1
        assert len(gm.data["sessions"]) == 1
    
    def test_add_pomodoro_custom_duration(self, gm):
        """カスタム時間でのポモドーロ追加テスト"""
        result = gm.add_pomodoro(50)
        
        # 50分 = 25分の2倍 = 200XP
        assert result["xp_earned"] == 200
        assert result["total_xp"] == 200
    
    def test_add_pomodoro_session_recording(self, gm):
        """セッション記録が正しく行われるかテスト"""
        gm.add_pomodoro(25)
        
        session = gm.data["sessions"][0]
        assert session["duration"] == 25
        assert session["xp_earned"] == 100
        assert "date" in session
        assert "datetime" in session
    
    def test_add_multiple_pomodoros(self, gm):
        """複数のポモドーロを追加するテスト"""
        for i in range(5):
            gm.add_pomodoro(25)
        
        assert gm.data["total_pomodoros"] == 5
        assert gm.data["xp"] == 500
        assert len(gm.data["sessions"]) == 5


class TestLevelUpSystem:
    """レベルアップシステムのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_level_up_at_500xp(self, gm):
        """500XPでレベル2になることをテスト"""
        # 500XP = 5回のポモドーロ
        for i in range(5):
            gm.add_pomodoro(25)
        
        assert gm.data["level"] == 2
        assert gm.data["xp"] == 500
    
    def test_level_up_at_1000xp(self, gm):
        """1000XPでレベル3になることをテスト"""
        # 1000XP = 10回のポモドーロ
        for i in range(10):
            gm.add_pomodoro(25)
        
        assert gm.data["level"] == 3
        assert gm.data["xp"] == 1000
    
    def test_level_up_notification(self, gm):
        """レベルアップ時に通知が返されるかテスト"""
        # レベルアップ直前まで進める
        gm.data["xp"] = 450
        gm.data["level"] = 1
        
        # レベルアップするポモドーロを追加
        result = gm.add_pomodoro(25)
        
        # レベルアップ通知があるか確認
        assert any("レベル2" in badge for badge in result["new_badges"])
    
    def test_check_level_up_formula(self, gm):
        """レベル計算式が正しいかテスト"""
        test_cases = [
            (0, 1),
            (499, 1),
            (500, 2),
            (999, 2),
            (1000, 3),
            (1499, 3),
            (1500, 4),
        ]
        
        for xp, expected_level in test_cases:
            gm.data["xp"] = xp
            gm._check_level_up()
            assert gm.data["level"] == expected_level, f"XP {xp} should be level {expected_level}"


class TestStreakSystem:
    """ストリークシステムのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_first_streak(self, gm):
        """初回のストリークテスト"""
        gm.add_pomodoro(25)
        assert gm.data["current_streak"] == 1
        assert gm.data["best_streak"] == 1
    
    def test_same_day_multiple_pomodoros(self, gm):
        """同じ日に複数のポモドーロを完了してもストリークは1のまま"""
        gm.add_pomodoro(25)
        assert gm.data["current_streak"] == 1
        
        gm.add_pomodoro(25)
        assert gm.data["current_streak"] == 1
        
        gm.add_pomodoro(25)
        assert gm.data["current_streak"] == 1
    
    def test_consecutive_days_streak(self, gm):
        """連続した日のストリークテスト"""
        today = datetime.now().date()
        
        # 初日
        gm.data["last_completion_date"] = None
        gm._update_streak()
        assert gm.data["current_streak"] == 1
        
        # 2日目（連続）
        gm.data["last_completion_date"] = (today - timedelta(days=1)).isoformat()
        gm._update_streak()
        assert gm.data["current_streak"] == 2
        
        # 3日目（連続）
        gm.data["last_completion_date"] = (today - timedelta(days=1)).isoformat()
        gm._update_streak()
        assert gm.data["current_streak"] == 3
    
    def test_broken_streak(self, gm):
        """ストリークが途切れるテスト"""
        today = datetime.now().date()
        
        # ストリーク3まで進める
        gm.data["current_streak"] = 3
        gm.data["best_streak"] = 3
        
        # 3日前を最終完了日として設定（2日空いている）
        gm.data["last_completion_date"] = (today - timedelta(days=3)).isoformat()
        gm._update_streak()
        
        # ストリークが1にリセットされる
        assert gm.data["current_streak"] == 1
        # ベストストリークは保持される
        assert gm.data["best_streak"] == 3
    
    def test_best_streak_update(self, gm):
        """ベストストリークが更新されるかテスト"""
        today = datetime.now().date()
        
        gm.data["current_streak"] = 5
        gm.data["best_streak"] = 3
        gm.data["last_completion_date"] = (today - timedelta(days=1)).isoformat()
        
        gm._update_streak()
        
        # ベストストリークが更新される
        assert gm.data["best_streak"] == 6


class TestBadgeSystem:
    """バッジシステムのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_streak_badge_3_days(self, gm):
        """3日連続バッジの獲得テスト"""
        today = datetime.now().date()
        
        # 3日連続のストリークを設定
        gm.data["current_streak"] = 3
        gm.data["last_completion_date"] = (today - timedelta(days=1)).isoformat()
        
        result = gm.add_pomodoro(25)
        
        # 3日連続バッジが獲得される
        assert "streak_3" in gm.data["badges"]
    
    def test_streak_badge_7_days(self, gm):
        """7日連続バッジの獲得テスト"""
        gm.data["current_streak"] = 7
        
        new_badges = gm._check_badges()
        
        # 3日と7日のバッジが両方獲得される
        assert "streak_3" in gm.data["badges"]
        assert "streak_7" in gm.data["badges"]
    
    def test_count_badge_10(self, gm):
        """10回達成バッジのテスト"""
        # 10回のポモドーロを完了
        for i in range(10):
            gm.add_pomodoro(25)
        
        assert "count_10" in gm.data["badges"]
    
    def test_count_badge_25(self, gm):
        """25回達成バッジのテスト"""
        gm.data["total_pomodoros"] = 25
        gm._check_badges()
        
        # 10回と25回のバッジが両方獲得される
        assert "count_10" in gm.data["badges"]
        assert "count_25" in gm.data["badges"]
    
    def test_badge_not_duplicated(self, gm):
        """同じバッジが重複して獲得されないことをテスト"""
        gm.data["total_pomodoros"] = 10
        
        # 1回目のチェック
        gm._check_badges()
        badges_count_1 = len(gm.data["badges"])
        
        # 2回目のチェック
        gm._check_badges()
        badges_count_2 = len(gm.data["badges"])
        
        # バッジ数が増えていない
        assert badges_count_1 == badges_count_2
    
    def test_all_count_badges(self, gm):
        """すべての回数バッジのテスト"""
        test_cases = [
            (10, "count_10"),
            (25, "count_25"),
            (50, "count_50"),
            (100, "count_100"),
            (250, "count_250"),
        ]
        
        for count, badge_id in test_cases:
            gm.data["total_pomodoros"] = count
            gm.data["badges"] = []  # リセット
            gm._check_badges()
            assert badge_id in gm.data["badges"], f"Badge {badge_id} should be earned at {count} pomodoros"


class TestStatistics:
    """統計機能のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_statistics_week(self, gm):
        """週間統計のテスト"""
        # 週間統計を取得
        stats = gm.get_statistics("week")
        
        assert stats["period"] == "week"
        assert stats["total_sessions"] == 0
        assert stats["total_minutes"] == 0
        assert "average_per_day" in stats
        assert "daily_counts" in stats
        assert "current_streak" in stats
        assert "best_streak" in stats
    
    def test_statistics_month(self, gm):
        """月間統計のテスト"""
        stats = gm.get_statistics("month")
        
        assert stats["period"] == "month"
        assert "total_sessions" in stats
        assert "total_minutes" in stats
    
    def test_statistics_all(self, gm):
        """全期間統計のテスト"""
        stats = gm.get_statistics("all")
        
        assert stats["period"] == "all"
    
    def test_statistics_with_data(self, gm):
        """データがある場合の統計テスト"""
        # 複数のポモドーロを追加
        for i in range(5):
            gm.add_pomodoro(25)
        
        stats = gm.get_statistics("week")
        
        assert stats["total_sessions"] == 5
        assert stats["total_minutes"] == 125  # 25分 × 5回
        assert stats["average_per_day"] > 0
    
    def test_statistics_daily_counts(self, gm):
        """日別カウントの統計テスト"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 今日3回のポモドーロを完了
        for i in range(3):
            gm.add_pomodoro(25)
        
        stats = gm.get_statistics("week")
        
        assert today in stats["daily_counts"]
        assert stats["daily_counts"][today] == 3
    
    def test_statistics_average_calculation(self, gm):
        """平均計算のテスト"""
        # 5回のポモドーロを追加
        for i in range(5):
            gm.add_pomodoro(25)
        
        stats = gm.get_statistics("week")
        
        # 週間（7日）での平均
        expected_average = 5 / 7
        assert abs(stats["average_per_day"] - expected_average) < 0.01


class TestStatus:
    """ステータス機能のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_get_status_basic(self, gm):
        """基本的なステータス取得のテスト"""
        status = gm.get_status()
        
        assert status["level"] == 1
        assert status["xp"] == 0
        assert status["next_level_xp"] == 500
        assert status["progress"] == 0
        assert status["total_pomodoros"] == 0
        assert status["current_streak"] == 0
        assert status["best_streak"] == 0
        assert status["badges_count"] == 0
    
    def test_get_status_with_progress(self, gm):
        """進捗があるステータステスト"""
        # 250XP（レベル1の50%）
        gm.data["xp"] = 250
        gm.data["level"] = 1
        
        status = gm.get_status()
        
        assert status["level"] == 1
        assert status["xp"] == 250
        assert status["progress"] == 50.0
    
    def test_get_status_level_2(self, gm):
        """レベル2のステータステスト"""
        gm.data["xp"] = 750
        gm.data["level"] = 2
        
        status = gm.get_status()
        
        assert status["level"] == 2
        assert status["next_level_xp"] == 1000
        # 750 - 500 = 250, (250 / (1000 - 500)) * 100 = 50%
        assert status["progress"] == 50.0


class TestBadgeDisplay:
    """バッジ表示のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_display_badges_empty(self, gm):
        """バッジがない場合の表示テスト"""
        result = gm.display_badges()
        assert "まだバッジを獲得していません" in result
    
    def test_display_badges_with_badges(self, gm):
        """バッジがある場合の表示テスト"""
        gm.data["badges"] = ["streak_3", "count_10"]
        result = gm.display_badges()
        
        assert "獲得バッジ:" in result
        assert "🔥" in result or "⭐" in result


class TestEdgeCases:
    """エッジケースのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    def test_corrupted_json_file(self, temp_data_file):
        """破損したJSONファイルの処理テスト"""
        # 破損したJSONファイルを作成
        with open(temp_data_file, 'w') as f:
            f.write("{invalid json content")
        
        # デフォルトデータで初期化されるはず
        gm = GamificationManager(data_file=temp_data_file)
        assert gm.data["xp"] == 0
        assert gm.data["level"] == 1
    
    def test_empty_json_file(self, temp_data_file):
        """空のJSONファイルの処理テスト"""
        # 空のファイルを作成
        with open(temp_data_file, 'w') as f:
            f.write("")
        
        gm = GamificationManager(data_file=temp_data_file)
        assert gm.data["xp"] == 0
        assert gm.data["level"] == 1
    
    def test_zero_duration_pomodoro(self, temp_data_file):
        """0分のポモドーロのテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        result = gm.add_pomodoro(0)
        
        assert result["xp_earned"] == 0
        assert gm.data["total_pomodoros"] == 1
    
    def test_negative_duration_pomodoro(self, temp_data_file):
        """負の時間のポモドーロのテスト
        
        Note: これは既知の制限事項です。現在の実装では負の時間が許可されており、
        負のXPが計算されます。本来は入力検証で防ぐべきですが、
        このテストは現在の挙動を記録するためのものです。
        """
        gm = GamificationManager(data_file=temp_data_file)
        result = gm.add_pomodoro(-25)
        
        # 現在の挙動: 負のXPが計算される
        assert result["xp_earned"] == -100
        assert gm.data["total_pomodoros"] == 1
        
        # TODO: 将来的には、gamification.pyのadd_pomodoroメソッドで
        # 入力検証を追加して負の時間を拒否するべき
    
    def test_very_large_duration(self, temp_data_file):
        """非常に長い時間のポモドーロのテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        result = gm.add_pomodoro(10000)
        
        # 10000分 = 40000XP
        assert result["xp_earned"] == 40000
        # レベル81になるはず（40000 / 500 = 80 + 1）
        assert gm.data["level"] == 81
    
    def test_concurrent_data_access(self, temp_data_file):
        """複数インスタンスでのデータアクセステスト"""
        gm1 = GamificationManager(data_file=temp_data_file)
        gm1.add_pomodoro(25)
        gm1.save_data()
        
        # 別のインスタンスでデータを読み込み
        gm2 = GamificationManager(data_file=temp_data_file)
        assert gm2.data["total_pomodoros"] == 1
        assert gm2.data["xp"] == 100
    
    def test_data_persistence_after_multiple_operations(self, temp_data_file):
        """複数操作後のデータ永続化テスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 複数の操作を実行
        for i in range(10):
            gm.add_pomodoro(25)
        
        # 新しいインスタンスでデータを確認
        gm2 = GamificationManager(data_file=temp_data_file)
        assert gm2.data["total_pomodoros"] == 10
        assert gm2.data["xp"] == 1000
        assert gm2.data["level"] == 3


class TestDataIntegrity:
    """データ整合性のテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        data_file = tmp_path / "test_pomodoro_data.json"
        return str(data_file)
    
    @pytest.fixture
    def gm(self, temp_data_file):
        return GamificationManager(data_file=temp_data_file)
    
    def test_session_count_matches_total_pomodoros(self, gm):
        """セッション数と合計ポモドーロ数が一致するかテスト"""
        for i in range(7):
            gm.add_pomodoro(25)
        
        assert len(gm.data["sessions"]) == gm.data["total_pomodoros"]
    
    def test_xp_calculation_consistency(self, gm):
        """XP計算の一貫性テスト"""
        # 各セッションのXPを手動で計算
        expected_xp = 0
        for i in range(5):
            duration = 25
            gm.add_pomodoro(duration)
            expected_xp += (duration / 25) * 100
        
        assert gm.data["xp"] == expected_xp
    
    def test_completed_dates_unique(self, gm):
        """完了日付が重複しないことをテスト"""
        # 同じ日に複数回実行
        for i in range(5):
            gm.add_pomodoro(25)
        
        # 完了日付リストはユニーク
        assert len(gm.data["completed_dates"]) == 1
    
    def test_badges_unique(self, gm):
        """バッジが重複しないことをテスト"""
        # 複数回同じ条件をクリア
        for i in range(3):
            gm.data["total_pomodoros"] = 10
            gm._check_badges()
        
        # バッジは重複しない
        badge_ids = gm.data["badges"]
        assert len(badge_ids) == len(set(badge_ids))
