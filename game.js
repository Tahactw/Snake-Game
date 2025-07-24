const canvas = document.getElementById('gameCanvas');
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
startGame();