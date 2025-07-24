import os
import json

def create_snake_game():
    """Generate a complete Snake game for GitHub Pages"""
    
    # Create directory structure
    base_dir = "snake-game"
    os.makedirs(base_dir, exist_ok=True)
    
    # HTML content
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retro Snake Game</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
</head>
<body>
    <div class="game-container">
        <h1 class="game-title">SNAKE</h1>
        
        <div class="game-info">
            <div class="score-container">
                <span>SCORE: </span>
                <span id="score">0</span>
            </div>
            <div class="high-score-container">
                <span>HIGH: </span>
                <span id="highScore">0</span>
            </div>
        </div>
        
        <div class="difficulty-container">
            <button class="difficulty-btn active" data-speed="150">EASY</button>
            <button class="difficulty-btn" data-speed="100">NORMAL</button>
            <button class="difficulty-btn" data-speed="50">HARD</button>
        </div>
        
        <canvas id="gameCanvas"></canvas>
        
        <div id="gameOver" class="game-over hidden">
            <h2>GAME OVER!</h2>
            <p>Final Score: <span id="finalScore">0</span></p>
            <button id="restartBtn" class="restart-btn">PLAY AGAIN</button>
        </div>
        
        <div class="controls-info">
            <p>USE ARROW KEYS TO MOVE</p>
            <p>PRESS SPACE TO PAUSE</p>
        </div>
        
        <button id="soundToggle" class="sound-toggle">🔊</button>
    </div>
    
    <script src="game.js"></script>
</body>
</html>'''
    
    # CSS content
    css_content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: #0a0a0a;
    color: #33ff33;
    font-family: 'Press Start 2P', cursive;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    image-rendering: pixelated;
    image-rendering: -moz-crisp-edges;
    image-rendering: crisp-edges;
}

.game-container {
    text-align: center;
    padding: 20px;
    background-color: #1a1a1a;
    border: 4px solid #33ff33;
    box-shadow: 0 0 20px rgba(51, 255, 51, 0.5);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 20px rgba(51, 255, 51, 0.3); }
    to { box-shadow: 0 0 30px rgba(51, 255, 51, 0.6); }
}

.game-title {
    font-size: 48px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 0px #1a8f1a;
    animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.game-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    font-size: 14px;
}

.score-container, .high-score-container {
    background-color: #0a0a0a;
    padding: 10px;
    border: 2px solid #33ff33;
}

.difficulty-container {
    margin-bottom: 20px;
}

.difficulty-btn {
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
    padding: 10px 20px;
    margin: 0 5px;
    background-color: #1a1a1a;
    color: #33ff33;
    border: 2px solid #33ff33;
    cursor: pointer;
    transition: all 0.3s;
}

.difficulty-btn:hover {
    background-color: #33ff33;
    color: #0a0a0a;
    transform: scale(1.1);
}

.difficulty-btn.active {
    background-color: #33ff33;
    color: #0a0a0a;
}

#gameCanvas {
    border: 4px solid #33ff33;
    background-color: #0a0a0a;
    display: block;
    margin: 0 auto;
    image-rendering: pixelated;
}

.game-over {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #1a1a1a;
    border: 4px solid #ff3333;
    padding: 30px;
    text-align: center;
    animation: shake 0.5s;
}

.game-over.hidden {
    display: none;
}

@keyframes shake {
    0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
    25% { transform: translate(-52%, -50%) rotate(-1deg); }
    75% { transform: translate(-48%, -50%) rotate(1deg); }
}

.game-over h2 {
    color: #ff3333;
    margin-bottom: 20px;
    font-size: 24px;
}

.restart-btn {
    font-family: 'Press Start 2P', cursive;
    font-size: 14px;
    padding: 15px 30px;
    background-color: #33ff33;
    color: #0a0a0a;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
}

.restart-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 0 10px rgba(51, 255, 51, 0.8);
}

.controls-info {
    margin-top: 20px;
    font-size: 10px;
    line-height: 1.8;
    opacity: 0.7;
}

.sound-toggle {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    background: none;
    border: none;
    cursor: pointer;
    transition: transform 0.2s;
}

.sound-toggle:hover {
    transform: scale(1.2);
}

.sound-toggle.muted {
    opacity: 0.5;
}'''
    
    # JavaScript content
    js_content = '''const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('highScore');
const gameOverElement = document.getElementById('gameOver');
const finalScoreElement = document.getElementById('finalScore');
const restartBtn = document.getElementById('restartBtn');
const soundToggle = document.getElementById('soundToggle');
const difficultyBtns = document.querySelectorAll('.difficulty-btn');

// Game settings
const GRID_SIZE = 20;
const CELL_SIZE = 20;
canvas.width = GRID_SIZE * CELL_SIZE;
canvas.height = GRID_SIZE * CELL_SIZE;

// Game state
let snake = [{x: 10, y: 10}];
let direction = {x: 1, y: 0};
let food = generateFood();
let score = 0;
let highScore = localStorage.getItem('snakeHighScore') || 0;
let gameRunning = false;
let gamePaused = false;
let gameSpeed = 150;
let soundEnabled = true;

highScoreElement.textContent = highScore;

// Sound system using Web Audio API
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

function playSound(frequency, duration, type = 'square') {
    if (!soundEnabled) return;
    
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration);
}

function playEatSound() {
    playSound(523.25, 0.1); // C5
    setTimeout(() => playSound(659.25, 0.1), 50); // E5
    setTimeout(() => playSound(783.99, 0.1), 100); // G5
}

function playGameOverSound() {
    playSound(293.66, 0.2); // D4
    setTimeout(() => playSound(261.63, 0.2), 100); // C4
    setTimeout(() => playSound(196.00, 0.3), 200); // G3
}

function playMoveSound() {
    playSound(150, 0.05, 'sine');
}

// Game functions
function generateFood() {
    let newFood;
    do {
        newFood = {
            x: Math.floor(Math.random() * GRID_SIZE),
            y: Math.floor(Math.random() * GRID_SIZE)
        };
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
}

function drawPixel(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2);
}

function drawSnake() {
    snake.forEach((segment, index) => {
        if (index === 0) {
            // Head - brighter green
            drawPixel(segment.x, segment.y, '#44ff44');
            
            // Draw eyes based on direction
            ctx.fillStyle = '#ffffff';
            let eyeSize = 3;
            if (direction.x === 1) { // Right
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + 4, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
            } else if (direction.x === -1) { // Left
                ctx.fillRect(segment.x * CELL_SIZE + 4, segment.y * CELL_SIZE + 4, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 4, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
            } else if (direction.y === -1) { // Up
                ctx.fillRect(segment.x * CELL_SIZE + 4, segment.y * CELL_SIZE + 4, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + 4, eyeSize, eyeSize);
            } else { // Down
                ctx.fillRect(segment.x * CELL_SIZE + 4, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
            }
        } else {
            // Body - darker green gradient
            let greenValue = Math.max(180 - index * 5, 100);
            drawPixel(segment.x, segment.y, `rgb(51, ${greenValue}, 51)`);
        }
    });
}

function drawFood() {
    // Animate food
    const pulse = Math.sin(Date.now() * 0.005) * 0.2 + 0.8;
    ctx.fillStyle = `rgba(255, 51, 51, ${pulse})`;
    
    const foodX = food.x * CELL_SIZE;
    const foodY = food.y * CELL_SIZE;
    const size = CELL_SIZE - 2;
    
    // Draw food as a pixel apple
    ctx.fillRect(foodX + 4, foodY + 2, size - 8, size - 6);
    ctx.fillRect(foodX + 2, foodY + 4, size - 4, size - 10);
    
    // Stem
    ctx.fillStyle = '#654321';
    ctx.fillRect(foodX + size/2 - 1, foodY, 2, 4);
}

function update() {
    if (!gameRunning || gamePaused) return;
    
    const head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};
    
    // Check wall collision
    if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
        gameOver();
        return;
    }
    
    // Check self collision
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver();
        return;
    }
    
    snake.unshift(head);
    
    // Check food collision
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreElement.textContent = score;
        food = generateFood();
        playEatSound();
        
        // Speed boost animation
        gameSpeed = Math.max(gameSpeed - 2, 30);
    } else {
        snake.pop();
        if (Math.random() < 0.1) playMoveSound();
    }
}

function draw() {
    // Clear canvas with fade effect
    ctx.fillStyle = 'rgba(10, 10, 10, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid pattern
    ctx.strokeStyle = 'rgba(51, 255, 51, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= GRID_SIZE; i++) {
        ctx.beginPath();
        ctx.moveTo(i * CELL_SIZE, 0);
        ctx.lineTo(i * CELL_SIZE, canvas.height);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(0, i * CELL_SIZE);
        ctx.lineTo(canvas.width, i * CELL_SIZE);
        ctx.stroke();
    }
    
    drawFood();
    drawSnake();
}

function gameLoop() {
    update();
    draw();
    
    if (gameRunning && !gamePaused) {
        setTimeout(gameLoop, gameSpeed);
    }
}

function startGame() {
    snake = [{x: 10, y: 10}];
    direction = {x: 1, y: 0};
    food = generateFood();
    score = 0;
    scoreElement.textContent = score;
    gameRunning = true;
    gamePaused = false;
    gameOverElement.classList.add('hidden');
    gameLoop();
}

function gameOver() {
    gameRunning = false;
    finalScoreElement.textContent = score;
    gameOverElement.classList.remove('hidden');
    playGameOverSound();
    
    if (score > highScore) {
        highScore = score;
        highScoreElement.textContent = highScore;
        localStorage.setItem('snakeHighScore', highScore);
    }
}

// Event listeners
document.addEventListener('keydown', (e) => {
    if (!gameRunning && e.key !== ' ') return;
    
    switch(e.key) {
        case 'ArrowUp':
            if (direction.y === 0) {
                direction = {x: 0, y: -1};
            }
            break;
        case 'ArrowDown':
            if (direction.y === 0) {
                direction = {x: 0, y: 1};
            }
            break;
        case 'ArrowLeft':
            if (direction.x === 0) {
                direction = {x: -1, y: 0};
            }
            break;
        case 'ArrowRight':
            if (direction.x === 0) {
                direction = {x: 1, y: 0};
            }
            break;
        case ' ':
            if (gameRunning) {
                gamePaused = !gamePaused;
                if (!gamePaused) gameLoop();
            }
            break;
    }
});

restartBtn.addEventListener('click', startGame);

soundToggle.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    soundToggle.textContent = soundEnabled ? '🔊' : '🔇';
    soundToggle.classList.toggle('muted');
});

difficultyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        difficultyBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        gameSpeed = parseInt(btn.dataset.speed);
    });
});

// Start game
startGame();'''
    
    # README content
    readme_content = '''# Retro Snake Game 🐍

A classic Snake game with a retro pixel-art aesthetic, built with pure HTML, CSS, and JavaScript.

## Features

- 🎮 Classic Snake gameplay
- 📊 Score tracking with persistent high score
- 🎚️ Three difficulty levels (Easy, Normal, Hard)
- 🔊 Retro sound effects (toggle on/off)
- 🎨 Pixel art style with glowing effects
- ⏸️ Pause functionality (SPACE key)
- 📱 Responsive design

## How to Play

1. Use arrow keys to control the snake
2. Eat the red food to grow and increase your score
3. Avoid hitting walls or yourself
4. Press SPACE to pause/unpause
5. Try different difficulty levels for more challenge!

## GitHub Pages Deployment

1. Push this repository to GitHub
2. Go to Settings > Pages
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Save and wait a few minutes
6. Your game will be available at: `https://[your-username].github.io/[repository-name]/`

## Technologies Used

- HTML5 Canvas for game rendering
- CSS3 for retro styling and animations
- Vanilla JavaScript for game logic
- Web Audio API for sound effects
- Local Storage for high score persistence

Enjoy the game! 🎮'''
    
    # Write files
    with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    with open(os.path.join(base_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    with open(os.path.join(base_dir, 'game.js'), 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    with open(os.path.join(base_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Snake game created successfully in '{base_dir}' directory!")
    print("\nFiles created:")
    print("  - index.html")
    print("  - style.css")
    print("  - game.js")
    print("  - README.md")
    print("\n📁 Directory structure:")
    print(f"  {base_dir}/")
    print(f"  ├── index.html")
    print(f"  ├── style.css")
    print(f"  ├── game.js")
    print(f"  └── README.md")
    print("\n🚀 To deploy:")
    print("  1. Navigate to the directory: cd snake-game")
    print("  2. Initialize git: git init")
    print("  3. Add files: git add .")
    print("  4. Commit: git commit -m 'Initial commit'")
    print("  5. Add your GitHub repository as origin")
    print("  6. Push to GitHub: git push -u origin main")
    print("  7. Enable GitHub Pages in repository settings")
    print("\n🎮 To test locally:")
    print("  Open index.html in your web browser")

if __name__ == "__main__":
    create_snake_game()