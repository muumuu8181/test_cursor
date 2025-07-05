// Hue Swap Game Logic
class HueSwapGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = 8;
        this.cellSize = 40;
        
        // ゲーム状態
        this.currentLevel = 1;
        this.score = 0;
        this.selectedColor = null;
        this.currentLayer = 'foreground';
        
        // レイヤー（前景・背景）
        this.foregroundLayer = [];
        this.backgroundLayer = [];
        
        // 色パレット
        this.colorPalette = {
            'red': { r: 255, g: 0, b: 0 },
            'green': { r: 0, g: 255, b: 0 },
            'blue': { r: 0, g: 0, b: 255 },
            'yellow': { r: 255, g: 255, b: 0 },
            'magenta': { r: 255, g: 0, b: 255 },
            'cyan': { r: 0, g: 255, b: 255 }
        };
        
        // レベル定義
        this.levels = [
            { target: { r: 255, g: 255, b: 0 }, name: "Yellow" },        // 黄色
            { target: { r: 255, g: 0, b: 255 }, name: "Magenta" },      // マゼンタ
            { target: { r: 0, g: 255, b: 255 }, name: "Cyan" },         // シアン
            { target: { r: 255, g: 128, b: 0 }, name: "Orange" },       // オレンジ
            { target: { r: 128, g: 255, b: 128 }, name: "Light Green" }, // 薄緑
            { target: { r: 128, g: 128, b: 255 }, name: "Light Blue" },  // 薄青
            { target: { r: 192, g: 192, b: 192 }, name: "Gray" },       // グレー
            { target: { r: 255, g: 192, b: 203 }, name: "Pink" },       // ピンク
        ];
        
        this.targetColor = this.levels[0].target;
        
        this.initializeGame();
        this.setupEventListeners();
    }
    
    initializeGame() {
        // レイヤー初期化
        this.foregroundLayer = Array(this.gridSize).fill(null).map(() => Array(this.gridSize).fill(null));
        this.backgroundLayer = Array(this.gridSize).fill(null).map(() => Array(this.gridSize).fill(null));
        
        // UI更新
        this.updateUI();
        this.render();
    }
    
    setupEventListeners() {
        // カラーパレットのクリック
        document.querySelectorAll('.palette-piece').forEach(piece => {
            piece.addEventListener('click', (e) => {
                this.selectColor(e.target.dataset.color);
            });
        });
        
        // レイヤー切り替え
        document.querySelectorAll('.layer-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchLayer(e.target.dataset.layer);
            });
        });
        
        // キャンバスのクリック/タッチ
        this.canvas.addEventListener('click', (e) => {
            this.handleCanvasClick(e);
        });
        
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.handleCanvasClick(e.touches[0]);
        });
        
        // ボタンイベント
        document.getElementById('swap-layers-button').addEventListener('click', () => {
            this.swapLayers();
        });
        
        document.getElementById('clear-layer-button').addEventListener('click', () => {
            this.clearCurrentLayer();
        });
        
        document.getElementById('reset-button').addEventListener('click', () => {
            this.resetGame();
        });
        
        document.getElementById('next-level-button').addEventListener('click', () => {
            this.nextLevel();
        });
    }
    
    selectColor(colorName) {
        this.selectedColor = colorName;
        
        // UI更新
        document.querySelectorAll('.palette-piece').forEach(piece => {
            piece.classList.remove('selected');
        });
        document.querySelector(`[data-color="${colorName}"]`).classList.add('selected');
    }
    
    switchLayer(layer) {
        this.currentLayer = layer;
        
        // UI更新
        document.querySelectorAll('.layer-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-layer="${layer}"]`).classList.add('active');
        
        this.render();
    }
    
    handleCanvasClick(event) {
        if (!this.selectedColor) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const gridX = Math.floor(x / this.cellSize);
        const gridY = Math.floor(y / this.cellSize);
        
        if (gridX >= 0 && gridX < this.gridSize && gridY >= 0 && gridY < this.gridSize) {
            this.placePiece(gridX, gridY, this.selectedColor);
        }
    }
    
    placePiece(x, y, color) {
        const layer = this.currentLayer === 'foreground' ? this.foregroundLayer : this.backgroundLayer;
        layer[y][x] = color;
        
        this.render();
        this.updateCurrentColor();
        this.checkWinCondition();
    }
    
    swapLayers() {
        [this.foregroundLayer, this.backgroundLayer] = [this.backgroundLayer, this.foregroundLayer];
        this.render();
        this.updateCurrentColor();
    }
    
    clearCurrentLayer() {
        const layer = this.currentLayer === 'foreground' ? this.foregroundLayer : this.backgroundLayer;
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                layer[y][x] = null;
            }
        }
        
        this.render();
        this.updateCurrentColor();
    }
    
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // グリッド描画
        this.drawGrid();
        
        // 背景レイヤー描画
        this.drawLayer(this.backgroundLayer, 0.6);
        
        // 前景レイヤー描画
        this.drawLayer(this.foregroundLayer, 1.0);
        
        // 現在選択中のレイヤーをハイライト
        this.highlightCurrentLayer();
    }
    
    drawGrid() {
        this.ctx.strokeStyle = '#ddd';
        this.ctx.lineWidth = 1;
        
        for (let x = 0; x <= this.gridSize; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * this.cellSize, 0);
            this.ctx.lineTo(x * this.cellSize, this.gridSize * this.cellSize);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.gridSize; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * this.cellSize);
            this.ctx.lineTo(this.gridSize * this.cellSize, y * this.cellSize);
            this.ctx.stroke();
        }
    }
    
    drawLayer(layer, opacity) {
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const color = layer[y][x];
                if (color) {
                    const colorData = this.colorPalette[color];
                    this.ctx.fillStyle = `rgba(${colorData.r}, ${colorData.g}, ${colorData.b}, ${opacity})`;
                    this.ctx.fillRect(x * this.cellSize + 1, y * this.cellSize + 1, this.cellSize - 2, this.cellSize - 2);
                }
            }
        }
    }
    
    highlightCurrentLayer() {
        this.ctx.strokeStyle = this.currentLayer === 'foreground' ? '#007bff' : '#28a745';
        this.ctx.lineWidth = 3;
        this.ctx.strokeRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    updateCurrentColor() {
        const mixedColor = this.calculateMixedColor();
        
        // 現在の色を表示
        const currentColorElement = document.getElementById('current-color');
        currentColorElement.style.backgroundColor = `rgb(${mixedColor.r}, ${mixedColor.g}, ${mixedColor.b})`;
        
        const currentRgbElement = document.getElementById('current-rgb');
        currentRgbElement.textContent = `RGB(${mixedColor.r}, ${mixedColor.g}, ${mixedColor.b})`;
    }
    
    calculateMixedColor() {
        let totalR = 0, totalG = 0, totalB = 0;
        let count = 0;
        
        // 前景と背景の色を混合
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const foregroundColor = this.foregroundLayer[y][x];
                const backgroundColor = this.backgroundLayer[y][x];
                
                if (foregroundColor || backgroundColor) {
                    let r = 0, g = 0, b = 0;
                    
                    if (backgroundColor) {
                        const bgColor = this.colorPalette[backgroundColor];
                        r += bgColor.r * 0.5;
                        g += bgColor.g * 0.5;
                        b += bgColor.b * 0.5;
                    }
                    
                    if (foregroundColor) {
                        const fgColor = this.colorPalette[foregroundColor];
                        r += fgColor.r * 0.5;
                        g += fgColor.g * 0.5;
                        b += fgColor.b * 0.5;
                    }
                    
                    totalR += r;
                    totalG += g;
                    totalB += b;
                    count++;
                }
            }
        }
        
        if (count === 0) {
            return { r: 0, g: 0, b: 0 };
        }
        
        return {
            r: Math.round(totalR / count),
            g: Math.round(totalG / count),
            b: Math.round(totalB / count)
        };
    }
    
    checkWinCondition() {
        const currentColor = this.calculateMixedColor();
        const target = this.targetColor;
        
        // 色の差を計算（許容範囲：各色成分で±20）
        const tolerance = 20;
        const rDiff = Math.abs(currentColor.r - target.r);
        const gDiff = Math.abs(currentColor.g - target.g);
        const bDiff = Math.abs(currentColor.b - target.b);
        
        if (rDiff <= tolerance && gDiff <= tolerance && bDiff <= tolerance) {
            this.showSuccessModal();
        }
    }
    
    showSuccessModal() {
        this.score += 100 * this.currentLevel;
        this.updateUI();
        document.getElementById('success-modal').classList.remove('hidden');
    }
    
    nextLevel() {
        this.currentLevel++;
        if (this.currentLevel > this.levels.length) {
            this.currentLevel = 1; // ループ
        }
        
        this.targetColor = this.levels[this.currentLevel - 1].target;
        this.initializeGame();
        document.getElementById('success-modal').classList.add('hidden');
    }
    
    resetGame() {
        this.currentLevel = 1;
        this.score = 0;
        this.targetColor = this.levels[0].target;
        this.initializeGame();
        document.getElementById('success-modal').classList.add('hidden');
    }
    
    updateUI() {
        document.getElementById('level-number').textContent = this.currentLevel;
        document.getElementById('score').textContent = this.score;
        
        // 目標色を表示
        const targetColorElement = document.getElementById('target-color');
        targetColorElement.style.backgroundColor = `rgb(${this.targetColor.r}, ${this.targetColor.g}, ${this.targetColor.b})`;
        
        const targetRgbElement = document.getElementById('target-rgb');
        targetRgbElement.textContent = `RGB(${this.targetColor.r}, ${this.targetColor.g}, ${this.targetColor.b})`;
    }
}

// ゲーム開始
document.addEventListener('DOMContentLoaded', () => {
    new HueSwapGame();
});