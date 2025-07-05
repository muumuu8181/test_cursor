# Twitter Auto Poster - クイックスタート

## 1. セットアップ

### 自動セットアップ
```bash
python setup.py
```

### 手動セットアップ
```bash
# 1. 依存関係をインストール
pip install -r requirements.txt

# 2. 設定ファイルを作成
cp .env.example .env

# 3. .envファイルを編集してTwitter APIキーを設定
# 4. 投稿フォルダを作成
mkdir posts
```

## 2. 基本的な使い方

### 新しい投稿を作成
```bash
python main.py --create-example 2024-12-30_14-30
```

### 今後の投稿を確認
```bash
python main.py --upcoming
```

### システムテスト
```bash
python main.py --test
```

### 自動投稿を開始
```bash
python main.py --start
```

## 3. フォルダ構造の例

```
posts/
├── 2024-12-29_09-00/       # 12月29日 09:00
│   ├── message.txt         # 投稿メッセージ
│   └── image.jpg          # 投稿画像
├── 2024-12-30_14-30/       # 12月30日 14:30
│   ├── message.txt
│   └── photo.png
└── 20241231_1200/          # 12月31日 12:00
    ├── message.txt
    └── picture.gif
```

## 4. 対応する日付フォーマット

- `YYYY-MM-DD_HH-MM` → 2024-12-29_14-30
- `YYYY-MM-DD` → 2024-12-29 (09:00がデフォルト)
- `YYYYMMDD_HHMM` → 20241229_1430
- `YYYYMMDD` → 20241229 (09:00がデフォルト)

## 5. バックグラウンド実行

### screenを使用
```bash
screen -S twitter-poster
python main.py --start
# Ctrl+A, Dで切り離し
```

### systemdサービスとして実行
```bash
./install-service.sh
```

## 6. 設定項目

`.env`ファイルで以下を設定：

- `TWITTER_API_KEY` - Twitter API キー
- `TWITTER_API_SECRET` - Twitter API シークレット
- `TWITTER_ACCESS_TOKEN` - アクセストークン
- `TWITTER_ACCESS_TOKEN_SECRET` - アクセストークンシークレット
- `CHECK_INTERVAL_MINUTES` - チェック間隔（デフォルト: 5分）
- `DEFAULT_TIMEZONE` - タイムゾーン（デフォルト: Asia/Tokyo）

## 7. トラブルシューティング

### ログの確認
```bash
tail -f posting.log
```

### API認証エラー
- Twitter Developer Portalで適切な権限が設定されているか確認
- API v2のRead and Write権限が必要

### 画像アップロードエラー
- 画像サイズが5MB以下であることを確認
- 対応形式: jpg, jpeg, png, gif, webp