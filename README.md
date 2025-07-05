# LINE Bot 自動チャット対応システム

LINEにメッセージが来たら自動でチャット対応する仕組みです。

## 🚀 機能

- ✅ LINE Botによる自動メッセージ応答
- ✅ キーワードベースの応答システム
- ✅ 挨拶、質問、感謝などの基本的な会話パターン
- ✅ 現在時刻の確認
- ✅ 友達登録時の自動ウェルカムメッセージ
- ✅ OpenAI API連携（オプション）
- ✅ Webhook対応

## 📋 必要な準備

### 1. LINE Developers アカウントの作成

1. [LINE Developers](https://developers.line.biz/ja/) にアクセス
2. LINE アカウントでログイン
3. 新しいプロバイダーを作成
4. 「Messaging API」チャンネルを作成

### 2. LINE Bot の設定

1. LINE Developersコンソールで作成したチャンネルを開く
2. 「Channel access token」を発行
3. 「Channel secret」を確認
4. Webhook URL を設定: `https://your-domain.com/webhook`
5. 「Use webhook」を有効にする

## 🛠️ セットアップ

### 1. 依存関係のインストール

```bash
npm install
```

### 2. 環境変数の設定

`.env.example` を `.env` にコピーして編集:

```bash
cp .env.example .env
```

`.env` ファイルを編集:

```env
# LINE Bot API設定
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# サーバー設定
PORT=3000
NODE_ENV=development

# OpenAI API設定（オプション）
OPENAI_API_KEY=your_openai_api_key_here

# 自動応答設定
DEFAULT_RESPONSE_MESSAGE=こんにちは！自動応答システムです。
```

### 3. サーバーの起動

開発環境:
```bash
npm run dev
```

本番環境:
```bash
npm start
```

## 🌐 本番環境へのデプロイ

### Herokuへのデプロイ

1. Herokuアカウントの作成
2. Heroku CLIのインストール
3. アプリケーションの作成:

```bash
heroku create your-line-bot-app
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
heroku config:set LINE_CHANNEL_SECRET=your_secret
heroku config:set OPENAI_API_KEY=your_openai_key
git push heroku main
```

### ngrok を使用したローカルテスト

開発時にローカル環境でテストする場合:

```bash
# ngrok のインストール
npm install -g ngrok

# サーバーを起動
npm run dev

# 別のターミナルで ngrok を起動
ngrok http 3000
```

ngrokが生成したHTTPS URLを LINE Developers の Webhook URL に設定してください。

## 📝 使用方法

### 基本的な対話

LINE Botと以下のような対話が可能です：

- **挨拶**: 「こんにちは」「おはよう」「こんばんは」
- **質問**: 「何？」「どう？」「？」
- **感謝**: 「ありがとう」「感謝」
- **時間**: 「時間」「いつ」
- **天気**: 「天気」「weather」
- **ヘルプ**: 「ヘルプ」「help」

### カスタム応答の追加

`server.js` の `generateResponse` 関数を編集して、新しい応答パターンを追加できます：

```javascript
// 新しいパターンの追加例
if (lowerMessage.includes('営業時間')) {
  return '営業時間は平日9:00-18:00です。土日祝日は休業となります。';
}
```

## 🔧 カスタマイズ

### 応答メッセージの変更

`generateResponse` 関数内の応答メッセージを編集することで、Bot の応答をカスタマイズできます。

### OpenAI API の活用

OpenAI API キーを設定することで、より高度な自動応答が可能になります。GPT-3.5 turbo を使用して、より自然な対話を実現できます。

## 📊 ログとモニタリング

- サーバーログはコンソールに出力されます
- 受信したメッセージとイベントがログに記録されます
- エラーハンドリングによりサーバーの安定性を確保

## 🛡️ セキュリティ

- LINE Webhook署名検証を使用
- 環境変数による機密情報の管理
- エラーハンドリングによる適切なエラーレスポンス

## 📱 対応機能

- ✅ テキストメッセージの自動応答
- ✅ 友達登録時の自動ウェルカムメッセージ
- ✅ 複数ユーザーへの同時対応
- ✅ キーワードベースの応答
- ✅ OpenAI API連携（オプション）

## 🚨 トラブルシューティング

### よくある問題

1. **Webhook エラー**: LINE Developers の Webhook URL が正しく設定されているか確認
2. **Token エラー**: 環境変数が正しく設定されているか確認
3. **応答しない**: サーバーが起動しているか、ログを確認

### ログの確認

```bash
# サーバーログの確認
npm run dev

# Herokuログの確認
heroku logs --tail
```

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. LINE Developers Console の設定
2. 環境変数の設定
3. サーバーのログ
4. Webhook URL の有効性

## 🎯 今後の拡張予定

- 📊 ユーザー行動分析
- 🎯 パーソナライズされた応答
- 📱 リッチメッセージ対応
- 🔔 プッシュ通知機能
- 💾 データベース連携

---

**注意**: 本番環境では必ず HTTPS を使用し、適切なセキュリティ対策を講じてください。