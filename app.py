import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long Siêu Dễ Thương")
st.write("💡 **Mẹo:** Click chuột vào màn hình game bên dưới, sau đó bấm phím **Cách (Space)** để khủng long nhảy!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Dino Game Ultra Safe</title>
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
    x: 80,
    y: GROUND_Y - 50,
    w: 45,
    h: 50,
    vy: 0,
    gravity: 0.8,
    jumpForce: -15,
    grounded: true,
    jump: function() {
        if (this.grounded && gameState === 'playing') {
            this.vy = this.jumpForce;
            this.grounded = false;
            playSound('jump');
        }
    },
    update: function() {
        this.vy += this.gravity;
        this.y += this.vy;
        if (this.y + this.h > GROUND_Y) {
            this.y = GROUND_Y - this.h;
            this.vy = 0;
            this.grounded = true;
        }
    },
    draw: function() {
        // --- VẼ KHỦNG LONG BẰNG HÌNH KHỐI CƠ BẢN (CHẮC CHẮN HIỆN) ---
        let isN = (Math.floor(score / 100) % 2 !== 0);
        
        // Thân khủng long
        ctx.fillStyle = isN ? "#a8e063" : "#68bb59";
        ctx.fillRect(this.x + 10, this.y + 15, 30, 25);

        // Đầu khủng long
        ctx.fillRect(this.x + 22, this.y - 5, 24, 22);

        // Má hồng dễ thương
        ctx.fillStyle = "#ff80ab";
        ctx.fillRect(this.x + 38, this.y + 6, 5, 5);

        // Mắt khủng long
        ctx.fillStyle = "#111";
        ctx.fillRect(this.x + 34, this.y + 2, 4, 4);

        // Chân khủng long
        ctx.fillStyle = isN ? "#a8e063" : "#68bb59";
        ctx.fillRect(this.x + 14, this.y + 40, 8, 10);
        ctx.fillRect(this.x + 28, this.y + 40, 8, 10);
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
        let isN = (Math.floor(score / 100) % 2 !== 0);
        if (this.type === 'cactus') {
            ctx.fillStyle = isN ? "#48c9b0" : "#2e7d32";
            ctx.fillRect(this.x + 10, this.y, 10, this.h);
            ctx.fillRect(this.x + 2, this.y + 10, 8, 16);
            ctx.fillRect(this.x + 20, this.y + 5, 8, 20);
        } else if (this.type === 'bird') {
            ctx.fillStyle = isN ? "#ff7675" : "#e74c3c";
            ctx.fillRect(this.x, this.y + 5, 25, 12);
        } else if (this.type === 'cloud') {
            ctx.fillStyle = isN ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.9)";
            ctx.fillRect(this.x, this.y, 45, 18);
        }
    }
    collidesWith(obj) {
        if (this.type === 'cloud') return false;
        const hx = this.x + 4, hw = this.w - 8, hy = this.y + 4, hh = this.h - 8;
        return (obj.x < hx + hw && obj.x + obj.w > hx && obj.y < hy + hh && obj.y + obj.h > hy);
    }
}

function initGame() {
    dino.y = GROUND_Y - dino.h;
    dino.vy = 0;
    dino.grounded = true;
    obstacles = [];
    decorations = [];
    score = 0;
    frameCount = 0;
    speed = 6;
    
    for (let i = 0; i < 4; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 100 + 20, 45, 18, speed * 0.3, 'cloud'));
    }
    setTimeout(spawnObstacle, 2000);
}

function spawnObstacle() {
    if (gameState !== 'playing') return;
    let type = Math.random() < 0.6 ? 'cactus' : 'bird';
    let x = canvas.width + 50;
    if (type === 'cactus') {
        let h = Math.floor(Math.random() * 25) + 40;
        obstacles.push(new GameObject(x, GROUND_Y - h, 30, h, speed, 'cactus'));
    } else {
        let y = Math.floor(Math.random() * 80) + 150;
        obstacles.push(new GameObject(x, y, 30, 20, speed, 'bird'));
    }
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1400) + 1000);
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

    // Hiển thị Điểm (HI ở trên, SCORE ở dưới góc phải)
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
    if (e.code === "Space" || e.code === "ArrowUp") {
        if (gameState === 'over') {
            resetGame();
        } else {
            dino.jump();
        }
        e.preventDefault();
    }
});

canvas.addEventListener("click", () => {
    canvas.focus();
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

components.html(dino_html, height=450)
