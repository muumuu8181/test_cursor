#!/bin/bash

# 動画冗長部分削除ツール - インストールスクリプト

echo "🎬 動画冗長部分削除ツール インストール開始"

# Pythonバージョン確認
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python3がインストールされていません"
    exit 1
fi

# pipの確認
python3 -m pip --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ pipがインストールされていません"
    exit 1
fi

# システムパッケージのインストール（Ubuntu/Debian）
echo "📦 システムパッケージをインストール中..."
if command -v apt-get > /dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg libsndfile1 libsndfile1-dev
elif command -v yum > /dev/null 2>&1; then
    sudo yum install -y ffmpeg libsndfile libsndfile-devel
elif command -v brew > /dev/null 2>&1; then
    # macOS
    brew install ffmpeg libsndfile
else
    echo "⚠️  システムパッケージマネージャーが見つかりません"
    echo "   手動でffmpegとlibsndfileをインストールしてください"
fi

# 仮想環境の作成
echo "🐍 仮想環境を作成中..."
python3 -m venv venv

# 仮想環境のアクティベート
echo "🔧 仮想環境をアクティベート..."
source venv/bin/activate

# pip のアップグレード
echo "📦 pipをアップグレード中..."
pip install --upgrade pip

# 依存関係のインストール
echo "📦 依存関係をインストール中..."
pip install -r requirements.txt

# 実行権限の付与
echo "🔒 実行権限を付与中..."
chmod +x video_editor.py
chmod +x gui_video_editor.py
chmod +x batch_process.py

echo "✅ インストール完了！"
echo ""
echo "=== 使用方法 ==="
echo "1. 仮想環境をアクティベート:"
echo "   source venv/bin/activate"
echo ""
echo "2. コマンドライン版:"
echo "   python video_editor.py your_video.mp4"
echo ""
echo "3. GUI版:"
echo "   python gui_video_editor.py"
echo ""
echo "4. 一括処理:"
echo "   python batch_process.py *.mp4 -o output_directory"
echo ""
echo "5. ヘルプ:"
echo "   python video_editor.py --help"