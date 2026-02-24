"""
ポモドーロタイマーの視覚的フィードバック機能
円形プログレスバー、色のグラデーション、背景エフェクトを提供
"""
import math
import time
import random


class VisualFeedback:
    """視覚的フィードバックを管理するクラス"""
    
    # ANSIカラーコード
    COLORS = {
        'blue': '\033[94m',      # 青（開始時：100%-67%）
        'cyan': '\033[96m',      # シアン（66%-50%）
        'yellow': '\033[93m',    # 黄（49%-34%）
        'orange': '\033[38;5;208m',  # オレンジ（33%-20%）
        'red': '\033[91m',       # 赤（19%-0%）
        'reset': '\033[0m',      # リセット
        'bold': '\033[1m',       # ボールド
        'dim': '\033[2m'         # 薄暗い
    }
    
    # 円形プログレスバー用の文字
    CIRCLE_CHARS = ['○', '◔', '◑', '◕', '●']
    BLOCK_CHARS = ['░', '▒', '▓', '█']
    
    def __init__(self, width: int = 60):
        """
        初期化
        
        Args:
            width: 表示幅（デフォルト: 60）
        """
        self.width = width
        self.particle_positions = []
    
    def get_color_for_progress(self, progress_percent: float) -> str:
        """
        進捗に応じた色を取得
        
        Args:
            progress_percent: 進捗率（0-100）
        
        Returns:
            ANSIカラーコード
        """
        if progress_percent >= 67:
            return self.COLORS['blue']
        elif progress_percent >= 50:
            return self.COLORS['cyan']
        elif progress_percent >= 34:
            return self.COLORS['yellow']
        elif progress_percent >= 20:
            return self.COLORS['orange']
        else:
            return self.COLORS['red']
    
    def create_circular_progress(self, progress_percent: float, radius: int = 10) -> str:
        """
        円形プログレスバーを作成
        
        Args:
            progress_percent: 進捗率（0-100）
            radius: 円の半径
        
        Returns:
            円形プログレスバーの文字列表現
        """
        color = self.get_color_for_progress(progress_percent)
        reset = self.COLORS['reset']
        
        # 円を描画
        lines = []
        for y in range(-radius, radius + 1):
            line = []
            for x in range(-radius * 2, radius * 2 + 1, 2):
                # 円の方程式: x^2 + y^2 <= r^2
                distance = math.sqrt((x/2)**2 + y**2)
                
                if distance <= radius:
                    # 角度を計算（上から時計回り）
                    angle = (math.atan2(y, x/2) + math.pi/2) % (2 * math.pi)
                    angle_percent = (angle / (2 * math.pi)) * 100
                    
                    # 進捗に応じて塗りつぶし
                    if angle_percent <= progress_percent or progress_percent >= 99:
                        # 距離に応じて文字を変更
                        if distance <= radius * 0.3:
                            line.append('●')
                        elif distance <= radius * 0.6:
                            line.append('◉')
                        else:
                            line.append('●')
                    else:
                        line.append('○')
                else:
                    line.append(' ')
            
            lines.append(color + ''.join(line) + reset)
        
        return '\n'.join(lines)
    
    def create_linear_progress_bar(self, progress_percent: float, width: int = None) -> str:
        """
        線形プログレスバーを作成（円形の補助として）
        
        Args:
            progress_percent: 進捗率（0-100）
            width: バーの幅
        
        Returns:
            プログレスバーの文字列
        """
        if width is None:
            width = self.width
        
        color = self.get_color_for_progress(progress_percent)
        reset = self.COLORS['reset']
        
        filled = int(width * progress_percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        
        return f"{color}{bar}{reset}"
    
    def create_wave_effect(self, frame: int, width: int = None) -> str:
        """
        波紋エフェクトを作成
        
        Args:
            frame: アニメーションフレーム番号
            width: エフェクトの幅
        
        Returns:
            波紋エフェクトの文字列
        """
        if width is None:
            width = self.width
        
        wave_chars = ['~', '≈', '∼', '⋍']
        result = []
        
        for i in range(width):
            # サイン波を使って波を作成
            wave_value = math.sin((i + frame) * 0.3) * 2
            char_index = int((wave_value + 2) / 4 * len(wave_chars))
            char_index = min(max(char_index, 0), len(wave_chars) - 1)
            result.append(wave_chars[char_index])
        
        color = self.COLORS['cyan']
        reset = self.COLORS['reset']
        return f"{color}{''.join(result)}{reset}"
    
    def create_particles(self, frame: int, num_particles: int = 20) -> str:
        """
        パーティクルエフェクトを作成
        
        Args:
            frame: アニメーションフレーム番号
            num_particles: パーティクルの数
        
        Returns:
            パーティクルエフェクトの文字列（複数行）
        """
        # パーティクルの初期化または更新
        if not self.particle_positions or frame % 10 == 0:
            self.particle_positions = [
                {
                    'x': random.randint(0, self.width - 1),
                    'y': random.randint(0, 3),
                    'char': random.choice(['*', '·', '✦', '✧', '◦']),
                    'speed': random.uniform(0.5, 2.0)
                }
                for _ in range(num_particles)
            ]
        
        # パーティクルを移動
        for particle in self.particle_positions:
            particle['x'] = (particle['x'] + int(particle['speed'])) % self.width
        
        # 描画
        lines = [list(' ' * self.width) for _ in range(4)]
        for particle in self.particle_positions:
            x, y = particle['x'], particle['y']
            if 0 <= x < self.width and 0 <= y < 4:
                lines[y][x] = particle['char']
        
        color = self.COLORS['dim']
        reset = self.COLORS['reset']
        return '\n'.join([color + ''.join(line) + reset for line in lines])
    
    def format_time_display(self, minutes: int, seconds: int, 
                           progress_percent: float, label: str = "作業時間") -> str:
        """
        時間表示を整形（色付き、大きなフォント風）
        
        Args:
            minutes: 分
            seconds: 秒
            progress_percent: 進捗率
            label: ラベル
        
        Returns:
            整形された時間表示
        """
        color = self.get_color_for_progress(progress_percent)
        bold = self.COLORS['bold']
        reset = self.COLORS['reset']
        
        # 大きな数字風の表示
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        display = f"{bold}{color}"
        display += f"\n  ╔══════════════════════════╗\n"
        display += f"  ║   {label:^18}   ║\n"
        display += f"  ║                          ║\n"
        display += f"  ║      {time_str:^14}      ║\n"
        display += f"  ║                          ║\n"
        display += f"  ╚══════════════════════════╝\n"
        display += reset
        
        return display
    
    def create_complete_display(self, remaining_seconds: int, total_seconds: int,
                               label: str = "作業時間", frame: int = 0,
                               show_particles: bool = True) -> str:
        """
        完全な視覚的フィードバック表示を作成
        
        Args:
            remaining_seconds: 残り秒数
            total_seconds: 合計秒数
            label: ラベル
            frame: アニメーションフレーム
            show_particles: パーティクルを表示するか
        
        Returns:
            完全な表示文字列
        """
        # 進捗を計算（残り時間が多いほど進捗が大きい）
        progress_percent = (remaining_seconds / total_seconds) * 100
        mins, secs = divmod(remaining_seconds, 60)
        
        # 各要素を組み立て
        display_parts = []
        
        # パーティクル（上部）
        if show_particles:
            display_parts.append(self.create_particles(frame))
            display_parts.append("")
        
        # 時間表示
        display_parts.append(self.format_time_display(mins, secs, progress_percent, label))
        
        # 円形プログレスバー
        display_parts.append(self.create_circular_progress(progress_percent, radius=8))
        display_parts.append("")
        
        # 線形プログレスバー
        progress_bar = self.create_linear_progress_bar(progress_percent, 40)
        display_parts.append(f"  進捗: [{progress_bar}] {progress_percent:.1f}%")
        display_parts.append("")
        
        # 波紋エフェクト（下部）
        if show_particles:
            display_parts.append(self.create_wave_effect(frame, 50))
        
        return '\n'.join(display_parts)


def demo():
    """デモンストレーション"""
    vf = VisualFeedback()
    
    total = 60  # 60秒のデモ
    
    print("\n視覚的フィードバックのデモ（60秒）\n")
    print("=" * 60)
    
    try:
        for i in range(total, 0, -1):
            # 画面クリア（簡易版）
            print("\033[2J\033[H", end='')
            
            # 完全な表示を作成
            display = vf.create_complete_display(i, total, "デモ", total - i, True)
            print(display)
            
            time.sleep(1)
        
        print("\n\nデモ完了！")
    
    except KeyboardInterrupt:
        print("\n\nデモを中断しました")


if __name__ == "__main__":
    demo()
