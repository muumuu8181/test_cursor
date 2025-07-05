# 動画冗長部分削除ツール (Video Redundancy Remover)

🎬 動画内の冗長な間（無音部分・沈黙部分）を自動で検出・削除して、より短く見やすい動画に変換するツールです。

## 🌟 主な機能

- **自動無音検出**: 音声レベルを分析して無音・低音量区間を自動検出
- **冗長部分削除**: 検出された区間を自動的に削除
- **複数モード対応**: 通常モードと積極的モードを選択可能
- **GUI版**: 直感的な操作が可能なグラフィカルインターフェース
- **一括処理**: 複数のファイルを同時に処理
- **可視化機能**: 音声分析結果をグラフで表示
- **スムーズなトランジション**: フェードイン/アウト効果付き

## 📋 必要なシステム要件

- Python 3.7以上
- FFmpeg
- libsndfile

## 🚀 インストール

### 自動インストール（推奨）

```bash
chmod +x install.sh
./install.sh
```

### 手動インストール

1. 必要なシステムパッケージをインストール:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg libsndfile1 libsndfile1-dev
   
   # CentOS/RHEL
   sudo yum install ffmpeg libsndfile libsndfile-devel
   
   # macOS
   brew install ffmpeg libsndfile
   ```

2. 仮想環境を作成:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 使用方法

### 1. コマンドライン版

基本的な使用法:
```bash
python video_editor.py input_video.mp4
```

詳細なオプション:
```bash
python video_editor.py input_video.mp4 \
    -o output_video.mp4 \
    -t -35 \
    -d 0.8 \
    -f 0.2 \
    -a \
    -v
```

#### パラメータ説明:
- `-o, --output`: 出力ファイル名
- `-t, --threshold`: 無音判定閾値（dB）、デフォルト: -40
- `-d, --duration`: 削除対象とする最小無音時間（秒）、デフォルト: 0.5
- `-f, --fade`: フェードイン/アウト時間（秒）、デフォルト: 0.1
- `-a, --aggressive`: より積極的な削除を行う
- `-v, --visualize`: 音声分析結果を可視化

### 2. GUI版

```bash
python gui_video_editor.py
```

GUI版では以下の操作が可能:
- ファイル選択（ドラッグ＆ドロップ対応）
- パラメータ調整（スライダーで直感的に設定）
- リアルタイムログ表示
- 処理進捗表示

### 3. 一括処理

複数のファイルを同時に処理:
```bash
python batch_process.py *.mp4 -o output_directory
```

グロブパターンを使用:
```bash
python batch_process.py "videos/*.mp4" "recordings/*.avi" -o processed_videos
```

## 🔧 設定パラメータの調整

### 無音判定閾値（Silence Threshold）
- **範囲**: -60dB ～ -20dB
- **デフォルト**: -40dB
- **低い値**: より厳密な無音検出（より多くの区間を削除）
- **高い値**: より緩い無音検出（より少ない区間を削除）

### 最小無音時間（Minimum Silence Duration）
- **範囲**: 0.1秒 ～ 2.0秒
- **デフォルト**: 0.5秒
- **短い値**: 短い無音も削除（より積極的）
- **長い値**: 長い無音のみ削除（より保守的）

### フェード時間（Fade Duration）
- **範囲**: 0.0秒 ～ 1.0秒
- **デフォルト**: 0.1秒
- **効果**: カット間のスムーズなトランジション

### 積極的モード（Aggressive Mode）
- **通常モード**: 無音区間のみを削除
- **積極的モード**: 無音区間＋低音量区間も削除

## 📊 可視化機能

音声分析結果をグラフで表示:
```bash
python video_editor.py input_video.mp4 -v
```

生成されるグラフ:
- 音声レベル（dB）の時系列データ
- 無音判定閾値の表示
- 削除対象区間のハイライト

## 🔍 使用例

### 例1: 講義動画の処理
```bash
python video_editor.py lecture.mp4 -t -35 -d 1.0 -a
```
- 講義の間の長い沈黙を削除
- やや積極的な設定で処理時間を短縮

### 例2: 会議録画の処理
```bash
python video_editor.py meeting.mp4 -t -45 -d 0.3 -f 0.2
```
- 会議中の短い沈黙も削除
- 自然なトランジションを維持

### 例3: 大量のファイルを一括処理
```bash
python batch_process.py "recordings/*.mp4" -o condensed -w 4
```
- 4つのファイルを並行処理
- 処理時間を大幅に短縮

## 🎨 カスタマイズ

### 独自の検出アルゴリズム
`VideoRedundancyRemover`クラスを継承して独自の検出ロジックを実装できます:

```python
class CustomVideoProcessor(VideoRedundancyRemover):
    def detect_redundant_segments(self, times, rms_db):
        # 独自の検出ロジック
        pass
```

### 新しい出力フォーマット
MoviePyが対応する任意の形式で出力可能:
```python
final_video.write_videofile(output_path, codec='libx265', audio_codec='aac')
```

## 🐛 トラブルシューティング

### よくある問題と解決法

1. **FFmpegエラー**
   ```
   解決法: FFmpegが正しくインストールされているか確認
   sudo apt-get install ffmpeg
   ```

2. **メモリ不足**
   ```
   解決法: より小さなファイルに分割して処理
   python batch_process.py large_video.mp4 -w 1
   ```

3. **音声が検出されない**
   ```
   解決法: 閾値を調整
   python video_editor.py input.mp4 -t -50
   ```

4. **処理が遅い**
   ```
   解決法: 並列処理数を増やす
   python batch_process.py *.mp4 -w 8
   ```

## 📈 パフォーマンス

### 処理時間の目安
- **10分の動画**: 約2-3分
- **1時間の動画**: 約10-15分
- **一括処理**: 並列数に応じて短縮

### メモリ使用量
- **音声分析**: 約100MB（1時間動画）
- **動画処理**: 約500MB（1時間動画）

## 🤝 貢献方法

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📝 ライセンス

MITライセンス - 詳細は`LICENSE`ファイルを参照

## 🙏 謝辞

- [MoviePy](https://github.com/Zulko/moviepy) - 動画処理ライブラリ
- [librosa](https://github.com/librosa/librosa) - 音声分析ライブラリ
- [FFmpeg](https://ffmpeg.org/) - マルチメディアフレームワーク

## 📮 サポート

問題や質問がある場合は、[Issues](https://github.com/your-repo/issues)で報告してください。

---

**🎬 動画編集を効率化し、より魅力的なコンテンツを作成しましょう！**