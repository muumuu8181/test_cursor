# Twitter Auto Poster

日本語での自動投稿システムです。指定した時間に画像付きのツイートを自動投稿します。

## 🚀 機能

- **自動投稿**: 指定した時間に自動でツイートを投稿
- **画像対応**: 画像付きのツイートを投稿
- **フォルダ管理**: フォルダ名で投稿日時を指定
- **柔軟な設定**: 投稿間隔や時間帯を調整可能
- **複数形式対応**: 日付フォーマットを複数サポート

## 📋 必要要件

- Python 3.7以上
- Twitter Developer Account
- Twitter API v2 アクセス権限

## 🛠️ セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. Twitter API設定

1. [Twitter Developer Platform](https://developer.twitter.com/)でアプリケーションを作成
2. API Key、API Secret、Access Token、Access Token Secretを取得
3. `.env`ファイルを作成:

```bash
cp .env.example .env
```

4. `.env`ファイルを編集してAPIキーを設定

### 3. 投稿フォルダの準備

投稿コンテンツを格納するフォルダを作成します：

```bash
mkdir posts
```

## 📁 フォルダ構造

投稿は以下の構造で管理されます：

```
posts/
├── 2024-01-15_09-00/          # 2024年1月15日 09:00に投稿
│   ├── message.txt            # 投稿メッセージ
│   └── image.jpg             # 投稿画像
├── 2024-01-16_14-30/          # 2024年1月16日 14:30に投稿
│   ├── message.txt
│   └── image.png
└── 20240117_1200/             # 2024年1月17日 12:00に投稿
    ├── message.txt
    └── image.gif
```

### サポートされる日付フォーマット

- `YYYY-MM-DD_HH-MM` (例: 2024-01-15_14-30)
- `YYYY-MM-DD` (例: 2024-01-15) - 09:00がデフォルト
- `YYYYMMDD_HHMM` (例: 20240115_1430)
- `YYYYMMDD` (例: 20240115) - 09:00がデフォルト

## 🚀 使い方

### 基本的な使用方法

1. **投稿フォルダの作成**:
```bash
python main.py --create-example 2024-01-15_14-30
```

2. **画像とメッセージの追加**:
   - 作成されたフォルダに画像ファイルを追加
   - `message.txt`を編集してメッセージを入力

3. **システムテスト**:
```bash
python main.py --test
```

4. **今後の投稿を確認**:
```bash
python main.py --upcoming
```

5. **スケジューラーを開始**:
```bash
python main.py --start
```

### コマンドライン引数

- `--start`: スケジューラーを開始
- `--test`: システムの動作確認
- `--once`: 一度だけ投稿チェックを実行
- `--upcoming`: 今後の投稿予定を表示
- `--create-example <フォルダ名>`: サンプル投稿フォルダを作成

## ⚙️ 設定

`.env`ファイルで以下の設定を変更できます：

```env
# Twitter API設定
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here

# 投稿設定
POSTS_FOLDER=posts                # 投稿フォルダのパス
DEFAULT_TIMEZONE=Asia/Tokyo       # タイムゾーン

# スケジュール設定
CHECK_INTERVAL_MINUTES=5          # チェック間隔（分）
MAX_IMAGE_SIZE_MB=5               # 最大画像サイズ（MB）

# ログ設定
LOG_LEVEL=INFO                    # ログレベル
LOG_FILE=posting.log              # ログファイル
```

## 🔧 高度な使用方法

### バックグラウンドで実行

```bash
# スクリーンセッションで実行
screen -S twitter-poster
python main.py --start

# セッションから抜ける（Ctrl+A, D）
# セッションに戻る
screen -r twitter-poster
```

### cronで定期実行

```bash
# crontabを編集
crontab -e

# 5分ごとにチェック
*/5 * * * * cd /path/to/your/project && python main.py --once
```

## 📝 投稿メッセージの例

`message.txt`の例：

```
おはようございます！今日も一日頑張りましょう！ 🌟

#朝活 #モチベーション #今日の目標
```

## 🔍 トラブルシューティング

### よくある問題

1. **Twitter API認証エラー**
   - API キーが正しく設定されているか確認
   - アクセス権限がv2対応しているか確認

2. **画像がアップロードできない**
   - 画像サイズが5MB以下か確認
   - 対応形式（jpg, png, gif, webp）か確認

3. **時間通りに投稿されない**
   - システムが起動しているか確認
   - ログファイルでエラーを確認

### ログの確認

```bash
tail -f posting.log
```

## 🆘 サポート

問題が発生した場合は、以下の情報を確認してください：

1. ログファイル（`posting.log`）
2. システムテストの結果（`python main.py --test`）
3. Python バージョン（`python --version`）

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

バグ報告や機能改善の提案は、GitHubのIssuesまでお願いします。