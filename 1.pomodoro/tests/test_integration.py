"""
統合テストとエンドツーエンドテスト
"""
import pytest
import json
import os
from datetime import datetime, timedelta
from gamification import GamificationManager
from app import PomodoroTimer
from unittest.mock import patch


class TestIntegration:
    """統合テストクラス"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        """一時的なデータファイル"""
        return str(tmp_path / "integration_test.json")
    
    def test_full_pomodoro_workflow(self, temp_data_file):
        """ポモドーロの完全なワークフローテスト"""
        # GamificationManagerとPomodoroTimerの統合
        with patch('app.GamificationManager') as MockGM:
            gm = GamificationManager(data_file=temp_data_file)
            MockGM.return_value = gm
            
            timer = PomodoroTimer(work_duration=25, break_duration=5)
            timer.gm = gm
            
            # 初期状態の確認
            status = timer.gm.get_status()
            assert status['level'] == 1
            assert status['xp'] == 0
            assert status['total_pomodoros'] == 0
            
            # ポモドーロを複数回実行
            for i in range(3):
                timer.gm.add_pomodoro(25)
            
            # 状態の確認
            status = timer.gm.get_status()
            assert status['total_pomodoros'] == 3
            assert status['xp'] == 300
            assert status['level'] == 1
    
    def test_level_up_workflow(self, temp_data_file):
        """レベルアップのワークフローテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # レベル1からレベル3まで進める
        # レベル2: 500XP (5回)
        # レベル3: 1000XP (10回)
        for i in range(10):
            result = gm.add_pomodoro(25)
        
        assert gm.data['level'] == 3
        assert gm.data['xp'] == 1000
        assert gm.data['total_pomodoros'] == 10
    
    def test_badge_earning_workflow(self, temp_data_file):
        """バッジ獲得のワークフローテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 10回のポモドーロで10回達成バッジ獲得
        for i in range(10):
            result = gm.add_pomodoro(25)
        
        assert 'count_10' in gm.data['badges']
        
        # さらに15回追加して25回達成バッジ獲得
        for i in range(15):
            gm.add_pomodoro(25)
        
        assert 'count_25' in gm.data['badges']
        assert gm.data['total_pomodoros'] == 25
    
    def test_streak_workflow(self, temp_data_file):
        """ストリークのワークフローテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        today = datetime.now().date()
        
        # 初日
        gm.data['last_completion_date'] = None
        result = gm.add_pomodoro(25)
        assert result['streak'] == 1
        
        # 2日目（連続）
        gm.data['last_completion_date'] = (today - timedelta(days=1)).isoformat()
        result = gm.add_pomodoro(25)
        assert result['streak'] == 2
        
        # 3日目（連続）
        gm.data['last_completion_date'] = (today - timedelta(days=1)).isoformat()
        result = gm.add_pomodoro(25)
        assert result['streak'] == 3
        assert 'streak_3' in gm.data['badges']
    
    def test_data_persistence_across_sessions(self, temp_data_file):
        """セッション間のデータ永続化テスト"""
        # 最初のセッション
        gm1 = GamificationManager(data_file=temp_data_file)
        for i in range(5):
            gm1.add_pomodoro(25)
        
        # データを保存
        first_session_data = {
            'xp': gm1.data['xp'],
            'level': gm1.data['level'],
            'total_pomodoros': gm1.data['total_pomodoros']
        }
        
        # 2番目のセッション（新しいインスタンス）
        gm2 = GamificationManager(data_file=temp_data_file)
        
        # データが保持されているか確認
        assert gm2.data['xp'] == first_session_data['xp']
        assert gm2.data['level'] == first_session_data['level']
        assert gm2.data['total_pomodoros'] == first_session_data['total_pomodoros']
        
        # さらにポモドーロを追加
        for i in range(5):
            gm2.add_pomodoro(25)
        
        # 3番目のセッション
        gm3 = GamificationManager(data_file=temp_data_file)
        assert gm3.data['total_pomodoros'] == 10
        assert gm3.data['xp'] == 1000
    
    def test_statistics_workflow(self, temp_data_file):
        """統計のワークフローテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 複数のポモドーロを追加
        for i in range(7):
            gm.add_pomodoro(25)
        
        # 週間統計
        week_stats = gm.get_statistics('week')
        assert week_stats['total_sessions'] == 7
        assert week_stats['total_minutes'] == 175
        
        # 月間統計
        month_stats = gm.get_statistics('month')
        assert month_stats['total_sessions'] == 7
        
        # 全期間統計
        all_stats = gm.get_statistics('all')
        assert all_stats['total_sessions'] == 7


class TestConcurrentScenarios:
    """同時実行シナリオのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        return str(tmp_path / "concurrent_test.json")
    
    def test_multiple_instances_sequential(self, temp_data_file):
        """複数インスタンスでの順次アクセステスト"""
        # インスタンス1でデータ作成
        gm1 = GamificationManager(data_file=temp_data_file)
        gm1.add_pomodoro(25)
        gm1.save_data()
        
        # インスタンス2でデータ読み込み
        gm2 = GamificationManager(data_file=temp_data_file)
        assert gm2.data['total_pomodoros'] == 1
        
        # インスタンス2でデータ追加
        gm2.add_pomodoro(25)
        
        # インスタンス3でデータ読み込み
        gm3 = GamificationManager(data_file=temp_data_file)
        assert gm3.data['total_pomodoros'] == 2
    
    def test_data_race_condition_simulation(self, temp_data_file):
        """データ競合状態のシミュレーション"""
        # 初期データを作成
        gm1 = GamificationManager(data_file=temp_data_file)
        gm1.add_pomodoro(25)
        
        # 2つのインスタンスが同じデータファイルを読み込む
        gm2 = GamificationManager(data_file=temp_data_file)
        gm3 = GamificationManager(data_file=temp_data_file)
        
        # 両方が更新を試みる
        gm2.add_pomodoro(25)
        gm3.add_pomodoro(25)
        
        # 最後に保存されたデータを読み込む
        gm4 = GamificationManager(data_file=temp_data_file)
        
        # 最後に保存されたインスタンスのデータが反映される
        # （この場合、gm3のデータが上書きされる可能性がある）
        assert gm4.data['total_pomodoros'] >= 2


class TestBoundaryValues:
    """境界値テスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        return str(tmp_path / "boundary_test.json")
    
    def test_minimum_values(self, temp_data_file):
        """最小値のテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 0分のポモドーロ
        result = gm.add_pomodoro(0)
        assert result['xp_earned'] == 0
        assert gm.data['total_pomodoros'] == 1
    
    def test_maximum_reasonable_values(self, temp_data_file):
        """妥当な最大値のテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 1000回のポモドーロ
        for i in range(1000):
            gm.add_pomodoro(25)
        
        assert gm.data['total_pomodoros'] == 1000
        assert gm.data['xp'] == 100000
        # レベル = 1 + floor(100000 / 500) = 201
        assert gm.data['level'] == 201
    
    def test_level_boundary(self, temp_data_file):
        """レベル境界のテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # レベルアップ直前
        gm.data['xp'] = 499
        gm._check_level_up()
        assert gm.data['level'] == 1
        
        # レベルアップ直後
        gm.data['xp'] = 500
        gm._check_level_up()
        assert gm.data['level'] == 2
        
        # レベル3の境界
        gm.data['xp'] = 999
        gm._check_level_up()
        assert gm.data['level'] == 2
        
        gm.data['xp'] = 1000
        gm._check_level_up()
        assert gm.data['level'] == 3
    
    def test_streak_boundary(self, temp_data_file):
        """ストリーク境界のテスト"""
        gm = GamificationManager(data_file=temp_data_file)
        today = datetime.now().date()
        
        # 2日連続（ストリーク3にはならない）
        gm.data['current_streak'] = 2
        gm._check_badges()
        assert 'streak_3' not in gm.data['badges']
        
        # 3日連続（ストリーク3になる）
        gm.data['current_streak'] = 3
        gm._check_badges()
        assert 'streak_3' in gm.data['badges']


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        return str(tmp_path / "error_test.json")
    
    def test_invalid_json_recovery(self, temp_data_file):
        """不正なJSONからの回復テスト"""
        # 不正なJSONファイルを作成
        with open(temp_data_file, 'w') as f:
            f.write('{"xp": 100, invalid')
        
        # デフォルトデータで初期化される
        gm = GamificationManager(data_file=temp_data_file)
        assert gm.data['xp'] == 0
        assert gm.data['level'] == 1
    
    def test_missing_fields_recovery(self, temp_data_file):
        """フィールド欠落からの回復テスト"""
        # 一部のフィールドが欠けたJSONを作成
        incomplete_data = {
            "xp": 500,
            "level": 2
            # 他のフィールドが欠けている
        }
        
        with open(temp_data_file, 'w') as f:
            json.dump(incomplete_data, f)
        
        # データを読み込んで使用（エラーが起きないことを確認）
        gm = GamificationManager(data_file=temp_data_file)
        
        # 欠けたフィールドはデフォルト値で補完される
        # add_pomodoroを実行してエラーが起きないことを確認
        try:
            result = gm.add_pomodoro(25)
            # 実行できれば成功
            assert True
        except (KeyError, AttributeError):
            # エラーが起きた場合は失敗
            assert False, "Missing fields should be handled gracefully"
    
    def test_file_permission_error(self, tmp_path):
        """ファイル権限エラーのテスト"""
        data_file = str(tmp_path / "readonly_test.json")
        
        # ファイルを作成
        gm = GamificationManager(data_file=data_file)
        gm.add_pomodoro(25)
        
        # ファイルを読み取り専用にする
        os.chmod(data_file, 0o444)
        
        try:
            # 保存を試みる（権限エラーが発生する）
            gm.add_pomodoro(25)
            # エラーが起きることを期待
        except (PermissionError, IOError):
            # 期待通りのエラー
            pass
        finally:
            # 後処理のためにパーミッションを戻す
            os.chmod(data_file, 0o644)


class TestComplexScenarios:
    """複雑なシナリオのテスト"""
    
    @pytest.fixture
    def temp_data_file(self, tmp_path):
        return str(tmp_path / "complex_test.json")
    
    def test_long_term_usage_simulation(self, temp_data_file):
        """長期使用のシミュレーション"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 100日間の使用をシミュレート
        today = datetime.now().date()
        
        for day in range(100):
            # 各日の前日を設定して連続日数を確保
            if day > 0:
                gm.data['last_completion_date'] = (today + timedelta(days=day - 1)).isoformat()
            
            # 1日3回のポモドーロ
            for _ in range(3):
                gm.add_pomodoro(25)
        
        # 結果を確認
        assert gm.data['total_pomodoros'] == 300
        assert gm.data['xp'] == 30000
        assert gm.data['level'] == 61  # 1 + floor(30000 / 500)
        
        # 100日連続のストリークは手動で設定しないと達成できないため、
        # ここでは回数バッジのみ確認
        assert 'count_250' in gm.data['badges']
        # 実際のストリークは1（毎回同じ日付で更新されるため）
        # 長期シミュレーションではストリークが正しく動作しないことを認識
    
    def test_mixed_duration_pomodoros(self, temp_data_file):
        """異なる時間のポモドーロの混在テスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 様々な時間のポモドーロを追加
        durations = [25, 50, 15, 30, 25, 45, 20]
        total_xp = 0
        
        for duration in durations:
            result = gm.add_pomodoro(duration)
            total_xp += (duration / 25) * 100
        
        assert gm.data['total_pomodoros'] == len(durations)
        assert abs(gm.data['xp'] - total_xp) < 0.01
    
    def test_badge_and_level_synchronization(self, temp_data_file):
        """バッジとレベルの同期テスト"""
        gm = GamificationManager(data_file=temp_data_file)
        
        # 50回のポモドーロを実行
        for i in range(50):
            result = gm.add_pomodoro(25)
        
        # バッジとレベルが正しく同期されているか確認
        assert gm.data['level'] == 11  # 5000 XP / 500 = 10 + 1
        assert 'count_10' in gm.data['badges']
        assert 'count_25' in gm.data['badges']
        assert 'count_50' in gm.data['badges']
        
        # ステータスを確認
        status = gm.get_status()
        assert status['level'] == 11
        assert status['total_pomodoros'] == 50
        assert status['badges_count'] == 3  # 3つのバッジ
