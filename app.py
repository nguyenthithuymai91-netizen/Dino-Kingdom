import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long Siêu Dễ Thương (Bản Có Âm Thanh)")
st.write("💡 **Mẹo:** Hãy **click chuột trực tiếp vào trong ô trò chơi** phía dưới một lần, sau đó bấm phím **Cách (Space)** để khủng long nhảy và nghe âm thanh nhé!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cute Dino Game</title>
    <style>
        body { margin: 0; background-color: #f7f7f7; overflow: hidden; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        #game-container { position: relative; width: 800px; height: 300px; border: 4px solid #fff; border-radius: 10px; overflow: hidden; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); outline: none; }
        canvas { display: block; }
        #score-display, #game-over-display { position: absolute; font-weight: bold; }
        #score-display { top: 10px; right: 20px; font-size: 20px; z-index: 10; }
        #game-over-display { top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; display: none; background: rgba(0,0,0,0.75); color: #fff; padding: 25px; border-radius: 12px; border: 2px solid #fff; z-index: 20; }
        #game-over-display h1 { margin-top: 0; font-size: 36px; color: #ffeb3b; }
        .focus-hint { margin-top: 8px; font-size: 13px; color: #555; }
    </style>
</head>
<body>

<div id="game-container" tabindex="0">
    <div id="score-display">SCORE: 0</div>
    <div id="game-over-display">
        <h1>GAME OVER</h1>
        <p>Điểm số: <span id="final-score">0</span></p>
        <p>💡 Nhấn <b>Space</b> hoặc <b>R</b> để chơi lại!</p>
    </div>
    <canvas id="gameCanvas" width="800" height="300"></canvas>
</div>
<div class="focus-hint">👉 Click vào khung game bên trên nếu bấm phím không ăn!</div>

<script>
const container = document.getElementById("game-container");
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score-display");
const gameOverDisplay = document.getElementById("game-over-display");
const finalScoreDisplay = document.getElementById("final-score");

// --- TÍCH HỢP HỆ THỐNG ÂM THANH 8-BIT (Web Audio API) ---
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
            // Âm thanh nhảy vui tươi (tần số tăng dần)
            osc.type = 'square';
            osc.frequency.setValueAtTime(250, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(500, audioCtx.currentTime + 0.12);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.12);
        } else if (type === 'hit') {
            // Âm thanh va chạm/game over (tần số trầm rền)
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

// Tự động focus vào khung game khi trang vừa tải xong
window.onload = () => { container.focus(); };
window.onclick = () => { container.focus(); initAudio(); };

let gameState = 'playing';
let score = 0;
let highScore = 0;
let dino;
let obstacles = [];
let decorations = [];
let frameCount = 0;
let speed = 6;
const GROUND_Y = 250;

function isNight() {
    let cycle = Math.floor(score / 100);
    return cycle % 2 !== 0;
}

class Dino {
    constructor() {
        this.x = 80;
        this.y = GROUND_Y - 45;
        this.w = 40;
        this.h = 45;
        this.vy = 0;
        this.gravity = 0.8;
        this.jumpForce = -15;
        this.grounded = true;
    }

    jump() {
        if (this.grounded && gameState === 'playing') {
            this.vy = this.jumpForce;
            this.grounded = false;
            playSound('jump'); // Phát âm thanh khi nhảy
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
        ctx.roundRect(dx + 10, dy + 15, 28, 24, 10);
        ctx.fill();

        // Đầu
        ctx.beginPath();
        ctx.roundRect(dx + 18, dy - 5, 24, 22, 8);
        ctx.fill();

        // Má hồng
        ctx.fillStyle = "#ff80ab";
        ctx.beginPath();
        ctx.arc(dx + 34, dy + 8, 4, 0, Math.PI * 2);
        ctx.fill();

        // Mắt
        ctx.fillStyle = "#fff";
        ctx.beginPath();
        ctx.arc(dx + 30, dy + 3, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#111";
        ctx.beginPath();
        ctx.arc(dx + 31, dy + 3, 2, 0, Math.PI * 2);
        ctx.fill();

        // Đuôi
        ctx.fillStyle = isNight() ? "#a8e063" : "#68bb59";
        ctx.beginPath();
        ctx.moveTo(dx + 12, dy + 22);
        ctx.lineTo(dx, dy + 15);
        ctx.lineTo(dx + 10, dy + 32);
        ctx.fill();

        // Chân
        ctx.fillRect(dx + 14, dy + 38, 6, 7);
        ctx.fillRect(dx + 26, dy + 38, 6, 7);

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
            ctx.fillRect(this.x + 10, this.y, 10, this.h);
            ctx.fillRect(this.x + 2, this.y + 10, 8, 15);
            ctx.fillRect(this.x + 20, this.y + 5, 8, 18);
        } else if (this.type === 'bird') {
            ctx.fillStyle = isNight() ? "#ff7675" : "#e74c3c";
            ctx.beginPath(); ctx.arc(this.x + 15, this.y + 10, 10, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.arc(this.x + 12, this.y + 8, 5, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'cloud') {
            ctx.fillStyle = isNight() ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.85)";
            ctx.beginPath(); ctx.arc(this.x, this.y, 18, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 18, this.y - 5, 22, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 36, this.y, 18, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore();
    }

    collidesWith(obj) {
        if (this.type === 'cloud') return false;
        const hx = this.x + 4, hw = this.w - 8, hy = this.y + 4, hh = this.h - 8;
        return (obj.x < hx + hw && obj.x + obj.w > hx && obj.y < hy + hh && obj.y + obj.h > hy);
    }
}

function initGame() {
    dino = new Dino();
    obstacles = [];
    decorations = [];
    score = 0;
    speed = 6;
    
    for (let i = 0; i < 6; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 100 + 20, 50, 25, speed * 0.3, 'cloud'));
    }
    setTimeout(spawnObstacle, 2000);
}

function spawnObstacle() {
    if (gameState !== 'playing') return;
    let type = Math.random() < 0.6 ? 'cactus' : 'bird';
    let x = canvas.width + 50;
    if (type === 'cactus') {
        let h = Math.floor(Math.random() * 25) + 35;
        obstacles.push(new GameObject(x, GROUND_Y - h, 30, h, speed, 'cactus'));
    } else {
        let y = Math.floor(Math.random() * 70) + 130;
        obstacles.push(new GameObject(x, y, 30, 20, speed, 'bird'));
    }
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1400) + 1000);
}

function gameLoop() {
    let night = isNight();
    canvas.style.backgroundColor = night ? "#1e272c" : "#b9f2ff";
    ctx.fillStyle = night ? "#1e272c" : "#b9f2ff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    frameCount++;

    ctx.fillStyle = night ? "#f1c40f" : "#ffd700";
    ctx.beginPath(); ctx.arc(700, 60, 24, 0, Math.PI * 2); ctx.fill();

    if (Math.random() < 0.02) {
        decorations.push(new GameObject(canvas.width + 50, Math.random() * 100 + 20, 50, 25, speed * 0.3, 'cloud'));
    }
    for (let i = decorations.length - 1; i >= 0; i--) {
        decorations[i].update();
        decorations[i].draw();
        if (decorations[i].x < -60) decorations.splice(i, 1);
    }

    ctx.save();
    ctx.strokeStyle = night ? "#34495e" : "#2ecc71";
    ctx.lineWidth = 10;
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

    score = Math.floor(frameCount / 10);
    if (score > highScore) highScore = score;
    scoreDisplay.innerText = "SCORE: " + score + (night ? " 🌙 ĐÊM" : " ☀️ NGÀY");
    scoreDisplay.style.color = night ? "#f1c40f" : "#2c3e50";

    if (gameState === 'playing') {
        requestAnimationFrame(gameLoop);
    }
}

function gameOver() {
    gameState = 'over';
    playSound('hit'); // Phát âm thanh khi va chạm kết thúc game
    finalScoreDisplay.innerText = score;
    gameOverDisplay.style.display = 'block';
}

function resetGame() {
    gameOverDisplay.style.display = 'none';
    gameState = 'playing';
    initGame();
    gameLoop();
}

// Bắt sự kiện bàn phím trực tiếp trên container game
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

components.html(dino_html, height=380)
