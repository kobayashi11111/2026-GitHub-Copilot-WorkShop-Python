"""
VisualFeedback クラスのテスト
"""
import pytest
from visual_feedback import VisualFeedback


class TestVisualFeedbackInit:
    """初期化のテスト"""
    
    def test_default_initialization(self):
        """デフォルトの初期化テスト"""
        vf = VisualFeedback()
        assert vf.width == 60
        assert vf.particle_positions == []
    
    def test_custom_width_initialization(self):
        """カスタム幅での初期化テスト"""
        vf = VisualFeedback(width=80)
        assert vf.width == 80


class TestColorSelection:
    """色選択のテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_color_for_high_progress(self, vf):
        """高進捗時の色（青）"""
        color = vf.get_color_for_progress(80)
        assert color == vf.COLORS['blue']
    
    def test_color_for_medium_high_progress(self, vf):
        """中高進捗時の色（シアン）"""
        color = vf.get_color_for_progress(55)
        assert color == vf.COLORS['cyan']
    
    def test_color_for_medium_progress(self, vf):
        """中進捗時の色（黄）"""
        color = vf.get_color_for_progress(40)
        assert color == vf.COLORS['yellow']
    
    def test_color_for_low_progress(self, vf):
        """低進捗時の色（オレンジ）"""
        color = vf.get_color_for_progress(25)
        assert color == vf.COLORS['orange']
    
    def test_color_for_very_low_progress(self, vf):
        """非常に低い進捗時の色（赤）"""
        color = vf.get_color_for_progress(10)
        assert color == vf.COLORS['red']
    
    def test_color_transitions(self, vf):
        """色の遷移を確認"""
        # 100% -> 青
        assert vf.get_color_for_progress(100) == vf.COLORS['blue']
        # 67% -> 青
        assert vf.get_color_for_progress(67) == vf.COLORS['blue']
        # 66% -> シアン
        assert vf.get_color_for_progress(66) == vf.COLORS['cyan']
        # 50% -> シアン
        assert vf.get_color_for_progress(50) == vf.COLORS['cyan']
        # 34% -> 黄
        assert vf.get_color_for_progress(34) == vf.COLORS['yellow']
        # 33.9% -> オレンジ（境界値）
        assert vf.get_color_for_progress(33.9) == vf.COLORS['orange']
        # 20% -> オレンジ
        assert vf.get_color_for_progress(20) == vf.COLORS['orange']
        # 19% -> 赤
        assert vf.get_color_for_progress(19) == vf.COLORS['red']
        # 0% -> 赤
        assert vf.get_color_for_progress(0) == vf.COLORS['red']


class TestCircularProgress:
    """円形プログレスバーのテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_circular_progress_returns_string(self, vf):
        """円形プログレスバーが文字列を返すか"""
        result = vf.create_circular_progress(50)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_circular_progress_contains_circles(self, vf):
        """円形プログレスバーに円文字が含まれるか"""
        result = vf.create_circular_progress(50)
        # ANSIコードを除去してチェック
        assert '●' in result or '○' in result or '◉' in result
    
    def test_circular_progress_with_different_radii(self, vf):
        """異なる半径で円形プログレスバーを作成"""
        result_small = vf.create_circular_progress(50, radius=5)
        result_large = vf.create_circular_progress(50, radius=15)
        # 大きい半径の方が文字数が多い
        assert len(result_large) > len(result_small)
    
    def test_circular_progress_full(self, vf):
        """100%進捗の円形プログレスバー"""
        result = vf.create_circular_progress(100)
        assert isinstance(result, str)
        # 完全に塗りつぶされているはず
        assert '●' in result
    
    def test_circular_progress_empty(self, vf):
        """0%進捗の円形プログレスバー"""
        result = vf.create_circular_progress(0)
        assert isinstance(result, str)
        # 空の円が多いはず
        assert '○' in result


class TestLinearProgressBar:
    """線形プログレスバーのテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_linear_progress_bar_full(self, vf):
        """100%進捗のバー"""
        result = vf.create_linear_progress_bar(100, width=20)
        # ANSIコードを除去
        clean_result = result.replace(vf.COLORS['blue'], '').replace(vf.COLORS['reset'], '')
        assert '█' in clean_result
        assert clean_result.count('█') == 20
    
    def test_linear_progress_bar_half(self, vf):
        """50%進捗のバー"""
        result = vf.create_linear_progress_bar(50, width=20)
        clean_result = result.replace(vf.COLORS['cyan'], '').replace(vf.COLORS['reset'], '')
        assert '█' in clean_result
        assert '░' in clean_result
        # 約半分が塗りつぶされている
        assert clean_result.count('█') == 10
    
    def test_linear_progress_bar_empty(self, vf):
        """0%進捗のバー"""
        result = vf.create_linear_progress_bar(0, width=20)
        clean_result = result.replace(vf.COLORS['red'], '').replace(vf.COLORS['reset'], '')
        assert '░' in clean_result
        assert clean_result.count('░') == 20
    
    def test_linear_progress_bar_uses_default_width(self, vf):
        """デフォルト幅を使用"""
        result = vf.create_linear_progress_bar(50)
        assert isinstance(result, str)
        # デフォルト幅は60
        assert len(result.replace(vf.COLORS['cyan'], '').replace(vf.COLORS['reset'], '')) == 60


class TestWaveEffect:
    """波紋エフェクトのテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_wave_effect_returns_string(self, vf):
        """波紋エフェクトが文字列を返すか"""
        result = vf.create_wave_effect(0)
        assert isinstance(result, str)
    
    def test_wave_effect_contains_wave_chars(self, vf):
        """波紋エフェクトに波文字が含まれるか"""
        result = vf.create_wave_effect(0)
        # ANSIコードを除去
        clean_result = result.replace(vf.COLORS['cyan'], '').replace(vf.COLORS['reset'], '')
        wave_chars = ['~', '≈', '∼', '⋍']
        assert any(char in clean_result for char in wave_chars)
    
    def test_wave_effect_animation(self, vf):
        """波紋エフェクトがアニメーションするか"""
        result1 = vf.create_wave_effect(0, width=30)
        result2 = vf.create_wave_effect(10, width=30)
        # フレームが違うと結果も違うはず
        assert result1 != result2


class TestParticles:
    """パーティクルエフェクトのテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_particles_returns_string(self, vf):
        """パーティクルが文字列を返すか"""
        result = vf.create_particles(0)
        assert isinstance(result, str)
    
    def test_particles_multiline(self, vf):
        """パーティクルが複数行か"""
        result = vf.create_particles(0)
        lines = result.split('\n')
        assert len(lines) == 4  # 4行表示
    
    def test_particles_initialized(self, vf):
        """パーティクルが初期化されるか"""
        vf.create_particles(0, num_particles=10)
        assert len(vf.particle_positions) == 10
    
    def test_particles_have_properties(self, vf):
        """パーティクルが必要なプロパティを持つか"""
        vf.create_particles(0, num_particles=5)
        for particle in vf.particle_positions:
            assert 'x' in particle
            assert 'y' in particle
            assert 'char' in particle
            assert 'speed' in particle
    
    def test_particles_move(self, vf):
        """パーティクルが移動するか"""
        vf.create_particles(0, num_particles=5)
        initial_positions = [p['x'] for p in vf.particle_positions]
        vf.create_particles(1, num_particles=5)
        # 少なくとも一部のパーティクルが移動しているはず
        new_positions = [p['x'] for p in vf.particle_positions]
        # 移動しているかチェック（完全一致でない）
        assert initial_positions != new_positions or any(p['speed'] > 0 for p in vf.particle_positions)


class TestTimeDisplay:
    """時間表示のテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_time_display_format(self, vf):
        """時間表示のフォーマット"""
        result = vf.format_time_display(25, 30, 80, "作業時間")
        assert isinstance(result, str)
        assert "25:30" in result
        assert "作業時間" in result
    
    def test_time_display_with_colors(self, vf):
        """時間表示に色が含まれるか"""
        result = vf.format_time_display(10, 0, 50, "休憩時間")
        assert vf.COLORS['reset'] in result
        # 何らかの色コードが含まれているはず
        assert '\033[' in result
    
    def test_time_display_zero_padding(self, vf):
        """時間表示のゼロパディング"""
        result = vf.format_time_display(5, 3, 70)
        assert "05:03" in result


class TestCompleteDisplay:
    """完全な表示のテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_complete_display_returns_string(self, vf):
        """完全な表示が文字列を返すか"""
        result = vf.create_complete_display(300, 1500, "作業時間", 0, True)
        assert isinstance(result, str)
    
    def test_complete_display_with_particles(self, vf):
        """パーティクル付きの完全な表示"""
        result = vf.create_complete_display(600, 1500, "作業時間", 0, True)
        assert isinstance(result, str)
        # 複数行あるはず
        assert '\n' in result
    
    def test_complete_display_without_particles(self, vf):
        """パーティクルなしの完全な表示"""
        result = vf.create_complete_display(300, 300, "休憩時間", 0, False)
        assert isinstance(result, str)
    
    def test_complete_display_progress_calculation(self, vf):
        """進捗計算が正しいか"""
        # 半分の時間
        result = vf.create_complete_display(750, 1500, "作業時間", 0, True)
        assert "50.0%" in result
    
    def test_complete_display_contains_all_elements(self, vf):
        """すべての要素が含まれるか"""
        result = vf.create_complete_display(900, 1500, "作業時間", 5, True)
        # 時間表示
        assert "15:00" in result
        # 進捗
        assert "進捗" in result
        assert "%" in result
        # ラベル
        assert "作業時間" in result


class TestEdgeCases:
    """エッジケースのテスト"""
    
    @pytest.fixture
    def vf(self):
        return VisualFeedback()
    
    def test_progress_over_100(self, vf):
        """100%を超える進捗"""
        color = vf.get_color_for_progress(150)
        assert color == vf.COLORS['blue']
    
    def test_progress_negative(self, vf):
        """負の進捗"""
        color = vf.get_color_for_progress(-10)
        assert color == vf.COLORS['red']
    
    def test_zero_remaining_time(self, vf):
        """残り時間0"""
        result = vf.create_complete_display(0, 1500, "完了", 0, False)
        assert "00:00" in result
    
    def test_small_width(self, vf):
        """小さい幅での表示"""
        vf_small = VisualFeedback(width=10)
        result = vf_small.create_linear_progress_bar(50, width=10)
        assert isinstance(result, str)
