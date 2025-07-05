# 動画冗長部分削除ツール - セットアップガイド

## 🚀 クイックスタート

### 1. 自動インストール（推奨）
```bash
./install.sh
```

### 2. 仮想環境をアクティベート
```bash
source venv/bin/activate
```

### 3. 動画を処理
```bash
# 基本的な使用法
python video_editor.py your_video.mp4

# GUI版を使用
python gui_video_editor.py

# 複数ファイルを一括処理
python batch_process.py *.mp4 -o output
```

## 📝 よく使われるコマンド

### 講義動画の処理
```bash
python video_editor.py lecture.mp4 -t -35 -d 1.0 -a
```

### 会議録画の処理
```bash
python video_editor.py meeting.mp4 -t -45 -d 0.3 -f 0.2
```

### 分析結果の可視化
```bash
python video_editor.py video.mp4 -v
```

## 🎯 デモの実行

実際の動画ファイルなしでツールの機能を確認:
```bash
python quick_demo.py
```

## 🔧 パラメータ調整

| パラメータ | 説明 | 推奨値 |
|-----------|------|--------|
| `-t` | 無音判定閾値（dB） | -40（標準）、-35（厳しい）、-45（緩い） |
| `-d` | 最小無音時間（秒） | 0.5（標準）、1.0（長い無音のみ）、0.3（短い無音も） |
| `-f` | フェード時間（秒） | 0.1（標準）、0.2（長い）、0.05（短い） |
| `-a` | 積極的モード | なし（標準）、あり（より多く削除） |

## 🐛 トラブルシューティング

### FFmpegエラー
```bash
sudo apt-get install ffmpeg
```

### 依存関係エラー
```bash
pip install -r requirements.txt
```

### メモリ不足
```bash
# 並列処理数を減らす
python batch_process.py *.mp4 -w 1
```

## 📞 サポート

- 詳細なマニュアル: `README.md`
- 使用例: `example_usage.py`
- デモ: `quick_demo.py`