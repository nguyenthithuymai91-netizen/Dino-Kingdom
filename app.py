import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long - Ngày & Đêm",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long (Đổi Ngày/Đêm mỗi 100 điểm)")
st.write("Dùng **Space** hoặc **Mũi tên lên** để nhảy. Cứ **100 điểm** trời sẽ chuyển từ Ngày sang Đêm và ngược lại!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Game</title>
    <style>
        body { margin: 0; background-color: #f7f7f7; overflow: hidden; font-family: 'Courier New', Courier, monospace; }
        #game-container { position: relative; width: 800px; height: 300px; margin: 20px auto; border: 4px solid #fff; border-radius: 10px; overflow: hidden; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
        canvas { display: block; }
        #score-display, #game-over-display { position: absolute; font-weight: bold; }
        #score-display { top: 10px; right: 20px; font-size: 20px; }
        #game-over-display { top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; display: none; background: rgba(0,0,0,0.7); color: #fff; padding: 20px; border-radius: 10px; border: 2px solid #fff; }
        #game-over-display h1 { margin-top: 0; font-size: 40px; }
    </style>
</head>
<body>

<div id="game-container">
    <div id="score-display">SCORE: 0</div>
    <div id="game-over-display">
        <h1>GAME OVER</h1>
        <p>Score: <span id="final-score">0</span></p>
        <p>(Nhấn 'R' để chơi lại)</p>
    </div>
    <canvas id="gameCanvas" width="800" height="300"></canvas>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score-display");
const gameOverDisplay = document.getElementById("game-over-display");
const finalScoreDisplay = document.getElementById("final-score");

let gameState = 'playing';
let score = 0;
let highScore = 0;
let dino;
let obstacles = [];
let decorations = [];
let frameCount = 0;
let speed = 6;
const GROUND_Y = 250;

// Kiểm tra xem có đang ở ban đêm không (cứ 100 điểm đổi 1 lần)
function isNight() {
    let cycle = Math.floor(score / 100);
    return cycle % 2 !== 0; // Số lẻ là Đêm, Số chẵn là Ngày
}

class Dino {
    constructor() {
        this.x = 80;
        this.y = GROUND_Y - 47;
        this.w = 44;
        this.h = 47;
        this.vy = 0;
        this.gravity = 0.8;
        this.jump = -15;
        this.grounded = true;
    }

    jump() {
        if (this.grounded && gameState === 'playing') {
            this.vy = this.jump;
            this.grounded = false;
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
        ctx.fillStyle = isNight() ? "#fff" : "#535353"; // Đổi màu khủng long theo ngày/đêm
        const dx = this.x;
        const dy = this.y;

        // Thân & Chân
        ctx.fillRect(dx + 16, dy + 2, 26, 26);
        ctx.fillRect(dx + 2, dy + 18, 16, 16);
        ctx.fillRect(dx + 16, dy + 28, 8, 16);
        ctx.fillRect(dx + 30, dy + 28, 8, 16);
        
        // Đầu & Cổ
        ctx.fillRect(dx + 20, dy - 14, 24, 16);
        ctx.fillRect(dx + 26, dy - 20, 12, 6);
        
        // Mắt
        ctx.fillStyle = isNight() ? "#000" : "#fff";
        ctx.fillRect(dx + 28, dy - 10, 4, 4);
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
        this.type = type; // 'cactus', 'bird', 'cloud', 'star'
    }

    update() {
        this.x -= this.speed;
    }

    draw() {
        ctx.save();
        if (this.type === 'cactus') {
            // Xương rồng
            ctx.fillStyle = isNight() ? "#a3e4d7" : "#2e7d32";
            ctx.fillRect(this.x + this.w / 2 - 4, this.y, 8, this.h);
            ctx.fillRect(this.x + this.w / 2 - 12, this.y + 8, 8, this.h / 2);
            ctx.fillRect(this.x + this.w / 2 + 4, this.y + 12, 8, this.h / 3);
        } else if (this.type === 'bird') {
            // Chim bay
            ctx.fillStyle = isNight() ? "#f1948a" : "#d32f2f";
            ctx.fillRect(this.x, this.y, 30, 15);
            ctx.fillRect(this.x + 8, this.y - 10, 14, 10);
            ctx.fillRect(this.x + 22, this.y + 3, 6, 9);
        } else if (this.type === 'cloud') {
            // Đám mây
            ctx.fillStyle = isNight() ? "rgba(255,255,255,0.3)" : "rgba(255,255,255,0.8)";
            ctx.beginPath(); ctx.arc(this.x, this.y, 20, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 20, this.y, 25, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 40, this.y, 20, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'star') {
            // Ngôi sao ban đêm
            ctx.fillStyle = "#fff";
            ctx.fillRect(this.x, this.y, 3, 3);
        }
        ctx.restore();
    }

    collidesWith(obj) {
        if (this.type === 'cloud' || this.type === 'star') return false;
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
    
    // Tạo mây & sao ban đầu
    for (let i = 0; i < 10; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 120, 60, 30, speed * 0.3, 'cloud'));
    }
    setTimeout(spawnObstacle, 2000);
}

function spawnObstacle() {
    if (gameState !== 'playing') return;
    let type = Math.random() < 0.6 ? 'cactus' : 'bird';
    let x = canvas.width + 50;
    if (type === 'cactus') {
        let h = Math.floor(Math.random() * 30) + 40;
        obstacles.push(new GameObject(x, GROUND_Y - h, 30, h, speed, 'cactus'));
    } else {
        let y = Math.floor(Math.random() * 80) + 120;
        obstacles.push(new GameObject(x, y, 30, 20, speed, 'bird'));
    }
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1500) + 1000);
}

function gameLoop() {
    // Đổi màu nền theo Ngày / Đêm
    let night = isNight();
    canvas.style.backgroundColor = night ? "#111b27" : "#c9eaf2";
    ctx.fillStyle = night ? "#111b27" : "#c9eaf2";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    frameCount++;

    // Vẽ Mặt trời (Ngày) hoặc Mặt trăng + Sao (Đêm)
    if (night) {
        // Vẽ mặt trăng
        ctx.fillStyle = "#f4d03f";
        ctx.beginPath(); ctx.arc(700, 60, 25, 0, Math.PI * 2); ctx.fill();
    } else {
        // Vẽ mặt trời
        ctx.fillStyle = "#ffeb3b";
        ctx.beginPath(); ctx.arc(700, 60, 25, 0, Math.PI * 2); ctx.fill();
    }

    // Cập nhật và vẽ mây/trang trí
    if (Math.random() < 0.02) {
        decorations.push(new GameObject(canvas.width + 50, Math.random() * 120, 60, 30, speed * 0.3, 'cloud'));
    }
    for (let i = decorations.length - 1; i >= 0; i--) {
        decorations[i].update();
        decorations[i].draw();
        if (decorations[i].x < -60) decorations.splice(i, 1);
    }

    // Vẽ mặt đất
    ctx.save();
    ctx.strokeStyle = night ? "#566573" : "#4caf50";
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(0, GROUND_Y); ctx.lineTo(canvas.width, GROUND_Y); ctx.stroke();
    ctx.restore();

    // Cập nhật và vẽ chướng ngại vật (Xương rồng, Chim)
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.update();
        obs.draw();
        if (obs.collidesWith(dino)) {
            gameOver();
        }
        if (obs.x < -obs.w) obstacles.splice(i, 1);
    }

    // Cập nhật và vẽ Khủng long
    dino.update();
    dino.draw();

    // Tính điểm
    score = Math.floor(frameCount / 10);
    if (score > highScore) highScore = score;
    scoreDisplay.innerText = "SCORE: " + score + (night ? " 🌙 (ĐÊM)" : " ☀️ (NGÀY)");
    scoreDisplay.style.color = night ? "#f4d03f" : "#333";

    if (gameState === 'playing') {
        requestAnimationFrame(gameLoop);
    }
}

function gameOver() {
    gameState = 'over';
    finalScoreDisplay.innerText = score;
    gameOverDisplay.style.display = 'block';
}

function resetGame() {
    gameOverDisplay.style.display = 'none';
    gameState = 'playing';
    initGame();
    gameLoop();
}

window.addEventListener("keydown", function(e) {
    if (e.code === "Space" || e.code === "ArrowUp") {
        dino.jump();
        e.preventDefault();
    }
    if (gameState === 'over' && e.code === 'KeyR') {
        resetGame();
    }
});
canvas.addEventListener("click", () => {
    dino.jump();
    if (gameState === 'over') resetGame();
});

initGame();
gameLoop();
</script>
</body>
</html>
"""

components.html(dino_html, height=350)
