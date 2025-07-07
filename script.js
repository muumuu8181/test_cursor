// アプリケーション状態管理
class QuizApp {
    constructor() {
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.currentSession = {
            questions: [],
            answers: [],
            score: 0,
            startTime: null,
            endTime: null
        };
        this.records = JSON.parse(localStorage.getItem('quizRecords') || '[]');
        this.init();
    }

    init() {
        this.loadDefaultQuestions();
        this.bindEvents();
        this.updateStats();
        this.showScreen('homeScreen');
    }

    // デフォルト問題を読み込み
    loadDefaultQuestions() {
        this.questions = [
            {
                question: "日本の首都はどこですか？",
                choices: ["大阪", "東京", "京都", "名古屋"],
                correct: 1
            },
            {
                question: "1 + 1 = ?",
                choices: ["1", "2", "3", "4"],
                correct: 1
            },
            {
                question: "地球で最も大きな海は？",
                choices: ["大西洋", "太平洋", "インド洋", "北極海"],
                correct: 1
            },
            {
                question: "日本の国鳥は？",
                choices: ["つる", "きじ", "からす", "すずめ"],
                correct: 1
            },
            {
                question: "オリンピックは何年に一度開催されますか？",
                choices: ["2年", "3年", "4年", "5年"],
                correct: 2
            },
            {
                question: "日本で一番高い山は？",
                choices: ["富士山", "北岳", "穂高岳", "槍ヶ岳"],
                correct: 0
            },
            {
                question: "1年は何日ですか？",
                choices: ["364日", "365日", "366日", "367日"],
                correct: 1
            },
            {
                question: "日本の通貨単位は？",
                choices: ["円", "ドル", "ウォン", "元"],
                correct: 0
            },
            {
                question: "太陽系で最も大きな惑星は？",
                choices: ["土星", "木星", "天王星", "海王星"],
                correct: 1
            },
            {
                question: "日本の国花は？",
                choices: ["桜", "菊", "梅", "椿"],
                correct: 0
            }
        ];
    }

    // イベントリスナーを設定
    bindEvents() {
        // ナビゲーションボタン
        document.getElementById('homeBtn').addEventListener('click', () => this.showScreen('homeScreen'));
        document.getElementById('recordsBtn').addEventListener('click', () => this.showScreen('recordsScreen'));
        document.getElementById('settingsBtn').addEventListener('click', () => this.showScreen('settingsScreen'));

        // クイズ開始
        document.getElementById('startQuizBtn').addEventListener('click', () => this.startQuiz());

        // 選択肢ボタン
        document.querySelectorAll('.choice-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectAnswer(e));
        });

        // 次の問題ボタン
        document.getElementById('nextBtn').addEventListener('click', () => this.nextQuestion());

        // 結果画面のボタン
        document.getElementById('retryBtn').addEventListener('click', () => this.startQuiz());
        document.getElementById('backHomeBtn').addEventListener('click', () => this.showScreen('homeScreen'));

        // 記録クリア
        document.getElementById('clearRecordsBtn').addEventListener('click', () => this.clearRecords());

        // ファイル読み込み
        document.getElementById('fileInput').addEventListener('change', (e) => this.loadQuestionFile(e));

        // サンプルファイルダウンロード
        document.getElementById('downloadSampleBtn').addEventListener('click', () => this.downloadSample());
    }

    // 画面切り替え
    showScreen(screenId) {
        // 全画面を非表示
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });

        // 指定画面を表示
        document.getElementById(screenId).classList.add('active');

        // ナビゲーションボタンの状態更新
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        if (screenId === 'homeScreen') {
            document.getElementById('homeBtn').classList.add('active');
            this.updateStats();
        } else if (screenId === 'recordsScreen') {
            document.getElementById('recordsBtn').classList.add('active');
            this.displayRecords();
        } else if (screenId === 'settingsScreen') {
            document.getElementById('settingsBtn').classList.add('active');
        }
    }

    // 統計情報更新
    updateStats() {
        const totalQuestions = this.records.reduce((sum, record) => sum + record.questions.length, 0);
        const correctAnswers = this.records.reduce((sum, record) => sum + record.score, 0);
        const accuracyRate = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;

        document.getElementById('totalQuestions').textContent = totalQuestions;
        document.getElementById('accuracyRate').textContent = accuracyRate + '%';
        document.getElementById('totalSessions').textContent = this.records.length;
    }

    // クイズ開始
    startQuiz() {
        if (this.questions.length === 0) {
            alert('問題が読み込まれていません。設定画面で問題ファイルを読み込んでください。');
            return;
        }

        // 問題をランダムに5問選択
        const shuffledQuestions = [...this.questions].sort(() => Math.random() - 0.5);
        this.currentSession = {
            questions: shuffledQuestions.slice(0, Math.min(5, shuffledQuestions.length)),
            answers: [],
            score: 0,
            startTime: new Date()
        };

        this.currentQuestionIndex = 0;
        this.showScreen('quizScreen');
        this.displayQuestion();
    }

    // 問題表示
    displayQuestion() {
        const question = this.currentSession.questions[this.currentQuestionIndex];
        const progress = ((this.currentQuestionIndex + 1) / this.currentSession.questions.length) * 100;

        document.getElementById('questionText').textContent = question.question;
        document.getElementById('questionCounter').textContent = 
            `${this.currentQuestionIndex + 1}/${this.currentSession.questions.length}`;
        document.getElementById('progressFill').style.width = progress + '%';

        // 選択肢を表示
        const choiceBtns = document.querySelectorAll('.choice-btn');
        choiceBtns.forEach((btn, index) => {
            btn.querySelector('.choice-text').textContent = question.choices[index];
            btn.classList.remove('selected', 'correct', 'incorrect');
            btn.disabled = false;
        });

        document.getElementById('nextBtn').style.display = 'none';
    }

    // 回答選択
    selectAnswer(event) {
        const selectedBtn = event.currentTarget;
        const selectedChoice = parseInt(selectedBtn.dataset.choice);
        const question = this.currentSession.questions[this.currentQuestionIndex];

        // 既に選択済みの場合は何もしない
        if (selectedBtn.classList.contains('selected')) return;

        // 回答を記録
        this.currentSession.answers.push({
            questionIndex: this.currentQuestionIndex,
            selectedChoice: selectedChoice,
            correctChoice: question.correct,
            isCorrect: selectedChoice === question.correct
        });

        // 正答の場合はスコアを加算
        if (selectedChoice === question.correct) {
            this.currentSession.score++;
        }

        // 全てのボタンを無効化
        document.querySelectorAll('.choice-btn').forEach(btn => {
            btn.disabled = true;
        });

        // 選択されたボタンをハイライト
        selectedBtn.classList.add('selected');

        // 正解/不正解の表示
        setTimeout(() => {
            document.querySelectorAll('.choice-btn').forEach((btn, index) => {
                if (index === question.correct) {
                    btn.classList.add('correct');
                } else if (index === selectedChoice && selectedChoice !== question.correct) {
                    btn.classList.add('incorrect');
                }
            });

            // 次の問題ボタンを表示
            document.getElementById('nextBtn').style.display = 'block';
        }, 500);
    }

    // 次の問題
    nextQuestion() {
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex < this.currentSession.questions.length) {
            this.displayQuestion();
        } else {
            this.showResults();
        }
    }

    // 結果表示
    showResults() {
        this.currentSession.endTime = new Date();
        
        // 記録を保存
        this.records.push({
            date: this.currentSession.startTime.toISOString(),
            questions: this.currentSession.questions.length,
            score: this.currentSession.score,
            answers: this.currentSession.answers,
            duration: this.currentSession.endTime - this.currentSession.startTime
        });

        localStorage.setItem('quizRecords', JSON.stringify(this.records));

        // 結果画面を表示
        const score = this.currentSession.score;
        const total = this.currentSession.questions.length;
        const percentage = Math.round((score / total) * 100);

        document.getElementById('scoreText').textContent = `${total}問中${score}問正解`;
        document.getElementById('scorePercentage').textContent = percentage + '%';

        // 詳細結果を表示
        const detailsContainer = document.getElementById('resultDetails');
        detailsContainer.innerHTML = '';

        this.currentSession.answers.forEach((answer, index) => {
            const question = this.currentSession.questions[answer.questionIndex];
            const detailDiv = document.createElement('div');
            detailDiv.className = 'result-detail-item';
            detailDiv.innerHTML = `
                <div style="margin-bottom: 10px;">
                    <strong>問題${index + 1}:</strong> ${question.question}
                </div>
                <div style="margin-bottom: 5px;">
                    <span style="color: ${answer.isCorrect ? '#4caf50' : '#f44336'};">
                        ${answer.isCorrect ? '正解' : '不正解'}
                    </span>
                </div>
                <div style="font-size: 0.9rem; color: #666;">
                    あなたの答え: ${question.choices[answer.selectedChoice]}<br>
                    正解: ${question.choices[answer.correctChoice]}
                </div>
                <hr style="margin: 15px 0; border: none; border-top: 1px solid #eee;">
            `;
            detailsContainer.appendChild(detailDiv);
        });

        this.showScreen('resultScreen');
    }

    // 記録表示
    displayRecords() {
        const recordsList = document.getElementById('recordsList');
        recordsList.innerHTML = '';

        if (this.records.length === 0) {
            recordsList.innerHTML = '<p style="text-align: center; color: #666;">記録がありません</p>';
            return;
        }

        // 記録を新しい順に並べ替え
        const sortedRecords = [...this.records].sort((a, b) => new Date(b.date) - new Date(a.date));

        sortedRecords.forEach(record => {
            const recordDiv = document.createElement('div');
            recordDiv.className = 'record-item';
            
            const date = new Date(record.date);
            const percentage = Math.round((record.score / record.questions) * 100);
            
            recordDiv.innerHTML = `
                <div class="record-date">${date.toLocaleDateString('ja-JP')} ${date.toLocaleTimeString('ja-JP')}</div>
                <div class="record-score">${record.questions}問中${record.score}問正解 (${percentage}%)</div>
            `;
            
            recordsList.appendChild(recordDiv);
        });
    }

    // 記録クリア
    clearRecords() {
        if (confirm('すべての記録を削除しますか？この操作は取り消せません。')) {
            this.records = [];
            localStorage.removeItem('quizRecords');
            this.displayRecords();
            this.updateStats();
        }
    }

    // 問題ファイル読み込み
    loadQuestionFile(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                this.parseQuestionFile(e.target.result);
                alert(`${this.questions.length}問の問題を読み込みました！`);
            } catch (error) {
                alert('ファイルの形式が正しくありません。設定画面の形式例を確認してください。');
                console.error('Error parsing question file:', error);
            }
        };
        reader.readAsText(file, 'UTF-8');
    }

    // 問題ファイル解析
    parseQuestionFile(content) {
        const lines = content.trim().split('\n').filter(line => line.trim() !== '');
        const questions = [];

        for (let i = 0; i < lines.length; i += 6) {
            if (i + 5 >= lines.length) break;

            const question = {
                question: lines[i].trim(),
                choices: [
                    lines[i + 1].trim(),
                    lines[i + 2].trim(),
                    lines[i + 3].trim(),
                    lines[i + 4].trim()
                ],
                correct: parseInt(lines[i + 5].trim()) - 1 // 1-4 を 0-3 に変換
            };

            if (question.correct < 0 || question.correct > 3) {
                throw new Error(`Invalid correct answer index: ${question.correct + 1}`);
            }

            questions.push(question);
        }

        if (questions.length === 0) {
            throw new Error('No valid questions found');
        }

        this.questions = questions;
    }

    // サンプルファイルダウンロード
    downloadSample() {
        const sampleContent = `富士山の高さは何メートルですか？
3776m
3677m
3767m
3867m
1

日本の首都はどこですか？
大阪
東京
京都
名古屋
2

1 + 1 = ?
1
2
3
4
2

地球で最も大きな海は？
大西洋
太平洋
インド洋
北極海
2

オリンピックは何年に一度開催されますか？
2年
3年
4年
5年
3`;

        const blob = new Blob([sampleContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sample_questions.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// アプリケーション開始
document.addEventListener('DOMContentLoaded', () => {
    new QuizApp();
});