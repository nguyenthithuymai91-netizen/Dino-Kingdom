import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long (Đã tối ưu hóa xuất hiện Chim)")
st.write("💡 **Mẹo:** Nhấn **Cách (Space)** hoặc **Mũi tên lên** để nhảy qua xương rồng, và giữ **Mũi tên xuống** để cúi người né chim!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Dino Game with Birds</title>
    <style>
        body {
            margin: 0;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: monospace;
        }
        canvas {
            border: 4px solid #333;
            border-radius: 12px;
            background: #b9f2ff;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
            outline: none;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="900" height="400" tabindex="1"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

window.onload = () => { canvas.focus(); };
window.onclick = () => { canvas.focus(); initAudio(); };

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
    } catch (e) {}
}

let gameState = 'playing';
let score = 0;
let highScore = 0;
let frameCount = 0;
let speed = 6;
const GROUND_Y = 320;

let dino = {
    x: 130,
    y: GROUND_Y - 50,
    w: 45,
    h: 50,
    vy: 0,
    gravity: 0.8,
    jumpForce: -15,
    grounded: true,
    isDuck: false,
    
    jump: function() {
        if (this.grounded && gameState === 'playing' && !this.isDuck) {
            this.vy = this.jumpForce;
            this.grounded = false;
            playSound('jump');
        }
    },
    
    duck: function(status) {
        if (this.grounded) {
            this.isDuck = status;
            if (status) {
                this.h = 30; // Thu nhỏ chiều cao khi cúi
                this.y = GROUND_Y - 30;
            } else {
                this.h = 50; 
                this.y = GROUND_Y - 50;
            }
        }
    },

    update: function() {
        this.vy += this.gravity;
        this.y += this.vy;
        if (this.y + this.h > GROUND_Y) {
            this.y = GROUND_Y - this.h;
            this.vy = 0;
            this.grounded = true;
            if (this.isDuck) {
                this.h = 30;
                this.y = GROUND_Y - 30;
            }
        }
    },

    draw: function() {
        ctx.save();
        const dx = this.x;
        const dy = this.y;
        let isN = (Math.floor(score / 100) % 2 !== 0);

        ctx.fillStyle = isN ? "#a8e063" : "#68bb59";

        if (this.isDuck) {
            // --- HÌNH DÁNG KHI CÚI XUỐNG ---
            ctx.beginPath();
            ctx.roundRect(dx + 5, dy + 5, 42, 22, 6);
            ctx.fill();

            ctx.beginPath();
            ctx.roundRect(dx + 30, dy - 2, 20, 16, 5);
            ctx.fill();

            ctx.fillStyle = "#ff80ab";
            ctx.beginPath();
            ctx.arc(dx + 42, dy + 4, 3, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#111";
            ctx.fillRect(dx + 38, dy + 2, 3, 3);
        } else {
            // --- HÌNH DÁNG BÌNH THƯỜNG ---
            ctx.beginPath();
            ctx.roundRect(dx + 10, dy + 15, 30, 26, 8);
            ctx.fill();

            ctx.beginPath();
            ctx.roundRect(dx + 20, dy - 4, 25, 22, 6);
            ctx.fill();

            ctx.fillStyle = "#ff80ab";
            ctx.beginPath();
            ctx.arc(dx + 36, dy + 7, 4, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(dx + 32, dy + 3, 4.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#111";
            ctx.beginPath();
            ctx.arc(dx + 33, dy + 3, 2, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = isN ? "#a8e063" : "#68bb59";
            ctx.beginPath();
            ctx.moveTo(dx + 12, dy + 20);
            ctx.lineTo(dx, dy + 10);
            ctx.lineTo(dx + 10, dy + 30);
            ctx.fill();

            ctx.fillRect(dx + 14, dy + 41, 7, 9);
            ctx.fillRect(dx + 28, dy + 41, 7, 9);
        }

        ctx.restore();
    }
};

let obstacles = [];
let decorations = [];

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
        let isN = (Math.floor(score / 100) % 2 !== 0);
        if (this.type === 'cactus') {
            ctx.fillStyle = isN ? "#48c9b0" : "#2e7d32";
            ctx.fillRect(this.x + 10, this.y, 10, this.h);
            ctx.fillRect(this.x + 2, this.y + 10, 8, 16);
            ctx.fillRect(this.x + 20, this.y + 5, 8, 20);
        } else if (this.type === 'bird') {
            // --- VẼ CHIM BAY MÀU ĐỎ/HỒNG NỔI BẬT ---
            ctx.fillStyle = isN ? "#ff7675" : "#e74c3c";
            ctx.beginPath(); 
            ctx.ellipse(this.x + 18, this.y + 12, 16, 9, 0, 0, Math.PI * 2); 
            ctx.fill();
            // Cánh chim
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(this.x + 14, this.y + 8, 5, 0, Math.PI * 2);
            ctx.fill();
        } else if (this.type === 'cloud') {
            ctx.fillStyle = isN ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.9)";
            ctx.beginPath(); ctx.arc(this.x, this.y, 15, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 15, this.y - 6, 18, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 32, this.y, 15, 0, Math.PI * 2); ctx.fill();
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
    dino.x = 130;
    dino.h = 50;
    dino.y = GROUND_Y - dino.h;
    dino.vy = 0;
    dino.grounded = true;
    dino.isDuck = false;
    obstacles = [];
    decorations = [];
    score = 0;
    frameCount = 0;
    speed = 6;
    
    for (let i = 0; i < 4; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 100 + 20, 45, 18, speed * 0.3, 'cloud'));
    }
    // Rút ngắn thời gian để chim xuất hiện nhanh hơn ngay khi bắt đầu
    setTimeout(spawnObstacle, 1200);
}

function spawnObstacle() {
    if (gameState !== 'playing') return;
    
    // Tăng tỉ lệ xuất hiện chim lên 50%
    let type = Math.random() < 0.5 ? 'cactus' : 'bird';
    let x = canvas.width + 50;
    
    if (type === 'cactus') {
        let h = Math.floor(Math.random() * 25) + 40;
        obstacles.push(new GameObject(x, GROUND_Y - h, 30, h, speed, 'cactus'));
    } else {
        // Đặt vị trí chim bay ở tầm cao vừa phải để khủng long cúi đầu né
        let birdHeights = [GROUND_Y - 70, GROUND_Y - 95]; 
        let y = birdHeights[Math.floor(Math.random() * birdHeights.length)];
        obstacles.push(new GameObject(x, y, 40, 24, speed, 'bird'));
    }
    // Thời gian chờ sinh chướng ngại vật tiếp theo ngắn hơn
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1000) + 900);
}

function gameLoop() {
    let isN = (Math.floor(score / 100) % 2 !== 0);
    canvas.style.backgroundColor = isN ? "#1e272c" : "#b9f2ff";
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'playing') {
        frameCount++;
        score = Math.floor(frameCount / 10);
    }

    // Mặt trời / Mặt trăng
    ctx.fillStyle = isN ? "#f1c40f" : "#ffd700";
    ctx.beginPath(); ctx.arc(800, 60, 25, 0, Math.PI * 2); ctx.fill();

    // Mây
    if (Math.random() < 0.02) {
        decorations.push(new GameObject(canvas.width + 50, Math.random() * 100 + 20, 45, 18, speed * 0.3, 'cloud'));
    }
    for (let i = decorations.length - 1; i >= 0; i--) {
        decorations[i].update();
        decorations[i].draw();
        if (decorations[i].x < -60) decorations.splice(i, 1);
    }

    // Mặt đất
    ctx.strokeStyle = isN ? "#34495e" : "#2ecc71";
    ctx.lineWidth = 10;
    ctx.beginPath(); ctx.moveTo(0, GROUND_Y); ctx.lineTo(canvas.width, GROUND_Y); ctx.stroke();

    // Chướng ngại vật
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.update();
        obs.draw();
        if (obs.collidesWith(dino)) {
            gameOver();
        }
        if (obs.x < -obs.w) obstacles.splice(i, 1);
    }

    // Khủng long
    dino.update();
    dino.draw();

    // Điểm số
    ctx.fillStyle = isN ? "#f1c40f" : "#2c3e50";
    ctx.font = "bold 18px monospace";
    ctx.textAlign = "right";
    ctx.fillText("🏆 HI: " + highScore, canvas.width - 25, 30);
    ctx.fillText("🎯 SCORE: " + score + (isN ? " 🌙" : " ☀️"), canvas.width - 25, 55);

    // Màn hình Game Over
    if (gameState === 'over') {
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ffeb3b";
        ctx.font = "bold 38px monospace";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 35);

        ctx.fillStyle = "#ffffff";
        ctx.font = "18px monospace";
        ctx.fillText("Điểm số hiện tại: " + score, canvas.width / 2, canvas.height / 2 + 5);
        ctx.fillText("🏆 Kỷ lục cao nhất: " + highScore, canvas.width / 2, canvas.height / 2 + 35);
        ctx.fillText("💡 Nhấn SPACE để chơi lại!", canvas.width / 2, canvas.height / 2 + 75);
    }

    requestAnimationFrame(gameLoop);
}

function gameOver() {
    gameState = 'over';
    playSound('hit');
    if (score > highScore) {
        highScore = score;
    }
}

function resetGame() {
    gameState = 'playing';
    initGame();
}

window.addEventListener("keydown", function(e) {
    if (e.code === "Space"
