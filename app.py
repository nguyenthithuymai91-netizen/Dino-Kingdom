import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long (Màn Hình Phóng To)")
st.write("💡 **Mẹo:** Click chuột vào khung game bên dưới một lần, sau đó bấm phím **Cách (Space)** để nhảy!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cute Dino Game Large</title>
    <style>
        body { margin: 0; background-color: #f7f7f7; overflow: hidden; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        /* Tăng kích thước khung game rộng hơn (1050x400) */
        #game-container { position: relative; width: 1050px; height: 400px; border: 4px solid #fff; border-radius: 12px; overflow: hidden; box-shadow: 0px 6px 20px rgba(0,0,0,0.25); outline: none; }
        canvas { display: block; }
        #score-display, #game-over-display { position: absolute; font-weight: bold; }
        #score-display { top: 15px; right: 25px; font-size: 24px; z-index: 10; }
        #game-over-display { top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; display: none; background: rgba(0,0,0,0.8); color: #fff; padding: 30px; border-radius: 15px; border: 2px solid #fff; z-index: 20; }
        #game-over-display h1 { margin-top: 0; font-size: 42px; color: #ffeb3b; }
        #game-over-display p { font-size: 18px; margin: 10px 0; }
        .focus-hint { margin-top: 10px; font-size: 14px; color: #555; }
    </style>
</head>
<body>

<div id="game-container" tabindex="0">
    <div id="score-display">SCORE: 0</div>
    <div id="game-over-display">
        <h1>GAME OVER</h1>
        <p>Điểm số hiện tại: <span id="final-score">0</span></p>
        <p>🏆 Kỷ lục cao nhất: <span id="high-score">0</span></p>
        <p>💡 Nhấn <b>Space</b> hoặc <b>R</b> để chơi lại!</p>
    </div>
    <!-- Phóng to độ phân giải canvas tương ứng -->
    <canvas id="gameCanvas" width="1050" height="400"></canvas>
</div>
<div class="focus-hint">👉 Click vào khung game bên trên nếu bấm phím không ăn!</div>

<script>
const container = document.getElementById("game-container");
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score-display");
const gameOverDisplay = document.getElementById("game-over-display");
const finalScoreDisplay = document.getElementById("final-score");
const highScoreDisplay = document.getElementById("high-score");

// --- ÂM THANH 8-BIT ---
let audioCtx = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

function playSound(type) {
    try {
        initAudio();
        if (!audioCtx) return;

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'jump') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(250, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(500, audioCtx.currentTime + 0.12);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.12);
        } else if (type === 'hit') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(180, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.35);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.35);
        }
    } catch (e) {
        console.log("Audio play error: ", e);
    }
}

window.onload = () => { container.focus(); };
window.onclick = () => { container.focus(); initAudio(); };

let gameState = 'playing';
let score = 0;
let highScore = 0;
let dino;
let obstacles = [];
let decorations = [];
let frameCount = 0;
let speed = 7; // Tăng nhẹ tốc độ cho màn hình lớn
const GROUND_Y = 330; // Mặt đất dời xuống thấp hơn để cân đối với chiều cao 400px

function isNight() {
    let cycle = Math.floor(score / 100);
    return cycle % 2 !== 0;
}

class Dino {
    constructor() {
        this.x = 90;
        this.y = GROUND_Y - 55;
        this.w = 50;  // Phóng to kích thước khủng long
        this.h = 55;
        this.vy = 0;
        this.gravity = 0.85;
        this.jumpForce = -16.5;
        this.grounded = true;
    }

    jump() {
        if (this.grounded && gameState === 'playing') {
            this.vy = this.jumpForce;
            this.grounded = false;
            playSound('jump');
        }
    }

    update() {
        this.vy += this.gravity;
        this.y += this.vy;
        if (this.y + this.h > GROUND_Y) {
            this.y = GROUND_Y - this.h;
            this.vy = 0;
            this.grounded = true;
        }
    }

    draw() {
        ctx.save();
        const dx = this.x;
        const dy = this.y;
        
        ctx.fillStyle = isNight() ? "#a8e063" : "#68bb59";
        
        // Thân
        ctx.beginPath();
        ctx.roundRect(dx + 12, dy + 18, 35, 30, 12);
        ctx.fill();

        // Đầu
        ctx.beginPath();
        ctx.roundRect(dx + 22, dy - 6, 30, 26, 10);
        ctx.fill();

        // Má hồng
        ctx.fillStyle = "#ff80ab";
        ctx.beginPath();
        ctx.arc(dx + 42, dy + 9, 5, 0, Math.PI * 2);
        ctx.fill();

        // Mắt
        ctx.fillStyle = "#fff";
        ctx.beginPath();
        ctx.arc(dx + 38, dy + 3, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#111";
        ctx.beginPath();
        ctx.arc(dx + 39, dy + 3, 2.5, 0, Math.PI * 2);
        ctx.fill();

        // Đuôi
        ctx.fillStyle = isNight() ? "#a8e063" : "#68bb59";
        ctx.beginPath();
        ctx.moveTo(dx + 15, dy + 28);
        ctx.lineTo(dx, dy + 18);
        ctx.lineTo(dx + 12, dy + 40);
        ctx.fill();

        // Chân
        ctx.fillRect(dx + 18, dy + 48, 7, 8);
        ctx.fillRect(dx + 32, dy + 48, 7, 8);

        ctx.restore();
    }
}

class GameObject {
    constructor(x, y, w, h, speed, type) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.speed = speed;
        this.type = type;
    }

    update() {
        this.x -= this.speed;
    }

    draw() {
        ctx.save();
        if (this.type === 'cactus') {
            ctx.fillStyle = isNight() ? "#48c9b0" : "#2e7d32";
            ctx.fillRect(this.x + 12, this.y, 12, this.h);
            ctx.fillRect(this.x + 3, this.y + 12, 9, 18);
            ctx.fillRect(this.x + 24, this.y + 6, 9, 22);
        } else if (this.type === 'bird') {
            ctx.fillStyle = isNight() ? "#ff7675" : "#e74c3c";
            ctx.beginPath(); ctx.arc(this.x + 18, this.y + 12, 12, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.arc(this.x + 14, this.y + 9, 6, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'cloud') {
            ctx.fillStyle = isNight() ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.85)";
            ctx.beginPath(); ctx.arc(this.x, this.y, 22, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 22, this.y - 6, 28, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 44, this.y, 22, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore();
    }

    collidesWith(obj) {
        if (this.type === 'cloud') return false;
        const hx = this.x + 5, hw = this.w - 10, hy = this.y + 5, hh = this.h - 10;
        return (obj.x < hx + hw && obj.x + obj.w > hx && obj.y < hy + hh && obj.y + obj.h > hy);
    }
}

function initGame() {
    dino = new Dino();
    obstacles = [];
    decorations = [];
    score = 0;
    frameCount = 0;
    speed = 7;
    
    for (let i = 0; i < 6; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 120 + 30, 60, 30, speed * 0.3, 'cloud'));
    }
    setTimeout(spawnObstacle, 2000);
}

function spawnObstacle() {
    if (gameState !== 'playing') return;
    let type = Math.random() < 0.6 ? 'cactus' : 'bird';
    let x = canvas.width + 50;
    if (type === 'cactus') {
        let h = Math.floor(Math.random() * 30) + 45;
        obstacles.push(new GameObject(x, GROUND_Y - h, 36, h, speed, 'cactus'));
    } else {
        let y = Math.floor(Math.random() * 90) + 160;
        obstacles.push(new GameObject(x, y, 36, 24, speed, 'bird'));
    }
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1400) + 1000);
}

function gameLoop() {
    let night = isNight();
    canvas.style.backgroundColor = night ? "#1e272c" : "#b9f2ff";
    ctx.fillStyle = night ? "#1e272c" : "#b9f2ff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'playing') {
        frameCount++;
        score = Math.floor(frameCount / 10);
    }

    // Mặt trời / Mặt trăng phóng to
    ctx.fillStyle = night ? "#f1c40f" : "#ffd700";
    ctx.beginPath(); ctx.arc(920, 75, 30, 0, Math.PI * 2); ctx.fill();

    if (Math.random() < 0.02) {
        decorations.push(new GameObject(canvas.width + 50, Math.random() * 120 + 30, 60, 30, speed * 0.3, 'cloud'));
    }
    for (let i = decorations.length - 1; i >= 0; i--) {
        decorations[i].update();
        decorations[i].draw();
        if (decorations[i].x < -80) decorations.splice(i, 1);
    }

    // Đường mặt đất
    ctx.save();
    ctx.strokeStyle = night ? "#34495e" : "#2ecc71";
    ctx.lineWidth = 12;
    ctx.beginPath(); ctx.moveTo(0, GROUND_Y); ctx.lineTo(canvas.width, GROUND_Y); ctx.stroke();
    ctx.restore();

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.update();
        obs.draw();
        if (obs.collidesWith(dino)) {
            gameOver();
        }
        if (obs.x < -obs.w) obstacles.splice(i, 1);
    }

    dino.update();
    dino.draw();

    scoreDisplay.innerText = "SCORE: " + score + (night ? " 🌙 ĐÊM" : " ☀️ NGÀY");
    scoreDisplay.style.color = night ? "#f1c40f" : "#2c3e50";

    if (gameState === 'playing') {
        requestAnimationFrame(gameLoop);
    }
}

function gameOver() {
    gameState = 'over';
    playSound('hit');
    
    if (score > highScore) {
        highScore = score;
    }

    finalScoreDisplay.innerText = score;
    highScoreDisplay.innerText = highScore;
    gameOverDisplay.style.display = 'block';
}

function resetGame() {
    gameOverDisplay.style.display = 'none';
    gameState = 'playing';
    initGame();
    gameLoop();
}

container.addEventListener("keydown", function(e) {
    if (e.code === "Space" || e.code === "ArrowUp") {
        if (gameState === 'over') {
            resetGame();
        } else {
            dino.jump();
        }
        e.preventDefault();
    }
    if (gameState === 'over' && e.code === "KeyR") {
        resetGame();
        e.preventDefault();
    }
});

canvas.addEventListener("click", () => {
    container.focus();
    initAudio();
    if (gameState === 'over') {
        resetGame();
    } else {
        dino.jump();
    }
});

initGame();
gameLoop();
</script>
</body>
</html>
"""

# Điều chỉnh chiều cao hiển thị của Streamlit component phù hợp với khung game mới (480px)
components.html(dino_html, height=480)
