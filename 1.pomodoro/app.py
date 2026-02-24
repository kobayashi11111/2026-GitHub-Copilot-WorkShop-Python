"""
Pomodoro Timer Web Application
Flask application factory pattern
"""
import os
from flask import Flask, render_template


def create_app(config=None):
    """
    アプリケーションファクトリ
    テスト時に設定を差し替え可能にするため、ファクトリパターンを採用
    """
    app = Flask(__name__)
    
    # デフォルト設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pomodoro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # テスト用の設定を上書き
    if config:
        app.config.update(config)
    
    # ルート定義
    @app.route('/')
    def index():
        """メインページ"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """ヘルスチェック用エンドポイント"""
        return {'status': 'ok'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
