const express = require('express');
const bodyParser = require('body-parser');
const { Client, middleware } = require('@line/bot-sdk');
const dotenv = require('dotenv');
const axios = require('axios');

// 環境変数の読み込み
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// LINE Bot SDK設定
const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET
};

const client = new Client(config);

// ミドルウェア設定
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// ヘルスチェック用エンドポイント
app.get('/', (req, res) => {
  res.send('LINE Bot 自動チャット対応システムが稼働中です！');
});

// LINE Webhook エンドポイント
app.post('/webhook', middleware(config), async (req, res) => {
  try {
    const events = req.body.events;
    
    // 各イベントを処理
    const promises = events.map(event => handleEvent(event));
    await Promise.all(promises);
    
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook処理エラー:', error);
    res.status(500).send('Internal Server Error');
  }
});

// イベントハンドラー
async function handleEvent(event) {
  console.log('受信イベント:', event);
  
  // メッセージイベントの場合
  if (event.type === 'message' && event.message.type === 'text') {
    const userMessage = event.message.text;
    const userId = event.source.userId;
    
    console.log(`ユーザー ${userId} からのメッセージ: ${userMessage}`);
    
    // 自動応答メッセージを生成
    const responseMessage = await generateResponse(userMessage);
    
    // 返信メッセージを送信
    await client.replyMessage(event.replyToken, {
      type: 'text',
      text: responseMessage
    });
  }
  
  // フォローイベントの場合
  else if (event.type === 'follow') {
    const welcomeMessage = '友達登録ありがとうございます！🎉\n自動チャットボットです。何でもお気軽にお話しください。';
    
    await client.replyMessage(event.replyToken, {
      type: 'text',
      text: welcomeMessage
    });
  }
}

// 自動応答メッセージ生成
async function generateResponse(userMessage) {
  // 基本的なキーワードベースの応答
  const lowerMessage = userMessage.toLowerCase();
  
  // 挨拶パターン
  if (lowerMessage.includes('こんにちは') || lowerMessage.includes('おはよう') || lowerMessage.includes('こんばんは')) {
    return 'こんにちは！お元気ですか？😊 何かお手伝いできることがあれば、お気軽にお聞かせください。';
  }
  
  // 質問パターン
  if (lowerMessage.includes('何') || lowerMessage.includes('どう') || lowerMessage.includes('？') || lowerMessage.includes('?')) {
    return 'とても興味深いご質問ですね！🤔 もう少し詳しく教えていただけますか？';
  }
  
  // 感謝パターン
  if (lowerMessage.includes('ありがとう') || lowerMessage.includes('感謝')) {
    return 'どういたしまして！😊 お役に立てて嬉しいです。他にもお手伝いできることがあれば、いつでもお声かけください。';
  }
  
  // 時間関連
  if (lowerMessage.includes('時間') || lowerMessage.includes('いつ')) {
    const now = new Date();
    const timeString = now.toLocaleString('ja-JP', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
    return `現在の時間は ${timeString} です⏰`;
  }
  
  // 天気関連
  if (lowerMessage.includes('天気') || lowerMessage.includes('weather')) {
    return '申し訳ございませんが、現在の天気情報は取得できません。🌤️ 天気予報は気象庁のサイトなどでご確認ください。';
  }
  
  // ヘルプ
  if (lowerMessage.includes('ヘルプ') || lowerMessage.includes('help')) {
    return `こんなことができます：
    
📝 基本的な会話
🕐 現在時刻の確認
💬 質問への応答
❓ その他お気軽にお話しください！
    
「時間」「天気」「ありがとう」などのキーワードに反応します。`;
  }
  
  // OpenAI APIを使用した応答（オプション）
  if (process.env.OPENAI_API_KEY) {
    try {
      const aiResponse = await generateAIResponse(userMessage);
      return aiResponse;
    } catch (error) {
      console.error('OpenAI API エラー:', error);
    }
  }
  
  // デフォルト応答
  const defaultResponses = [
    'なるほど！興味深いですね。もう少し詳しく教えていただけますか？',
    'そうですね！それについてもう少しお聞かせください。',
    'とても面白いお話ですね！😊 他にも何かお聞きしたいことがあれば、お気軽にどうぞ。',
    'ありがとうございます！そのことについて、もう少し詳しく知りたいです。',
    '素晴らしいですね！他にも何かお話しすることがあれば、ぜひお聞かせください。'
  ];
  
  return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
}

// OpenAI APIを使用した応答生成（オプション）
async function generateAIResponse(userMessage) {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'あなたは親切で丁寧な日本語アシスタントです。ユーザーの質問に対して、簡潔で分かりやすい回答を提供してください。'
          },
          {
            role: 'user',
            content: userMessage
          }
        ],
        max_tokens: 150,
        temperature: 0.7
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('OpenAI API エラー:', error);
    throw error;
  }
}

// エラーハンドリング
app.use((error, req, res, next) => {
  console.error('アプリケーションエラー:', error);
  res.status(500).send('Internal Server Error');
});

// サーバー起動
app.listen(PORT, () => {
  console.log(`🚀 LINE Bot サーバーが起動しました！`);
  console.log(`📍 ポート: ${PORT}`);
  console.log(`🔗 Webhook URL: http://localhost:${PORT}/webhook`);
  console.log(`💡 ヘルスチェック: http://localhost:${PORT}/`);
});

module.exports = app;