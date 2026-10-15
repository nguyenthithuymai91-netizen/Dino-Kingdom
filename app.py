import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long Siêu Dễ Thương")
st.write("💡 **Mẹo:** Click chuột vào khung game bên dưới một lần, sau đó bấm phím **Cách (Space)** hoặc mũi tên lên để nhảy!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cute Dino Game</title>
    <style>
        body { 
            margin: 0; 
            background-color: #f7f7f7; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            font-family: 'Courier New', Courier, monospace; 
        }
        #gameCanvas {
            border: 4px solid #333;
            border-radius: 12px;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
            background: #b9f2ff;
            outline: none;
            display: block;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="1050" height="420" tabindex="1"></canvas>

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
    } catch (e) {
        console.log("Audio play error: ", e);
    }
}

let gameState = 'playing';
let score = 0;
let highScore = 0;
let frameCount = 0;
let speed = 7;
const GROUND_Y = 340;

let dino = {
    x: 90,
    y: GROUND_Y - 55,
    w: 50,
    h: 55,
    vy: 0,
    gravity: 0.85,
    jumpForce: -16.5,
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
        ctx.save();
        const dx = this.x;
        const dy = this.y;
        let isN = isNight();
        
        ctx.fillStyle = isN ? "#a8e063" : "#68bb59";
        
        // Thân khủng long tròn trịa dễ thương
        ctx.beginPath();
        ctx.roundRect(dx + 12, dy + 18, 34, 30, 10);
        ctx.fill();

        // Đầu khủng long
        ctx.beginPath();
        ctx.roundRect(dx + 22, dy - 4, 28, 24, 8);
        ctx.fill();

        // Má hồng dễ thương
        ctx.fillStyle = "#ff80ab";
        ctx.beginPath();
        ctx.arc(dx + 40, dy + 8, 4.5, 0, Math.PI * 2);
        ctx.fill();

        // Mắt khủng long
        ctx.fillStyle = "#fff";
        ctx.beginPath();
        ctx.arc(dx + 36, dy + 3, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#111";
        ctx.beginPath();
        ctx.arc(dx + 37, dy + 3, 2, 0, Math.PI * 2);
        ctx.fill();

        // Đuôi
        ctx.fillStyle = isN ? "#a8e063" : "#68bb59";
        ctx.beginPath();
        ctx.moveTo(dx + 15, dy + 24);
        ctx.lineTo(dx, dy + 14);
        ctx.lineTo(dx + 12, dy + 36);
        ctx.fill();

        // Chân
        ctx.fillRect(dx + 18, dy + 48, 7, 8);
        ctx.fillRect(dx + 32, dy + 48, 7, 8);

        ctx.restore();
    }
};

let obstacles = [];
let decorations = [];

function isNight() {
    let cycle = Math.floor(score / 100);
    return cycle % 2 !== 0;
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
        let isN = isNight();
        if (this.type === 'cactus') {
            ctx.fillStyle = isN ? "#48c9b0" : "#2e7d32";
            ctx.fillRect(this.x + 12, this.y, 12, this.h);
            ctx.fillRect(this.x + 3, this.y + 12, 9, 18);
            ctx.fillRect(this.x + 24, this.y + 6, 9, 22);
        } else if (this.type === 'bird') {
            ctx.fillStyle = isN ? "#ff7675" : "#e74c3c";
            ctx.beginPath(); ctx.arc(this.x + 15, this.y + 10, 12, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#fff";
            ctx.beginPath(); ctx.arc(this.x + 11, this.y + 8, 5, 0, Math.PI * 2); ctx.fill();
        } else if (this.type === 'cloud') {
            // Vẽ lại đám mây bồng bềnh xinh xắn
            ctx.fillStyle = isN ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.85)";
            ctx.beginPath(); ctx.arc(this.x, this.y, 18, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 18, this.y - 6, 22, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(this.x + 36, this.y, 18, 0, Math.PI * 2); ctx.fill();
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
    dino.y = GROUND_Y - dino.h;
    dino.vy = 0;
    dino.grounded = true;
    obstacles = [];
    decorations = [];
    score = 0;
    frameCount = 0;
    speed = 7;
    
    for (let i = 0; i < 5; i++) {
        decorations.push(new GameObject(Math.random() * canvas.width, Math.random() * 120 + 30, 50, 25, speed * 0.3, 'cloud'));
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
        let y = Math.floor(Math.random() * 90) + 170;
        obstacles.push(new GameObject(x, y, 36, 24, speed, 'bird'));
    }
    setTimeout(spawnObstacle, Math.floor(Math.random() * 1400) + 1000);
}

function gameLoop() {
    let night = isNight();
    canvas.style.backgroundColor = night ? "#1e272c" : "#b9f2ff";
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'playing') {
        frameCount++;
        score = Math.floor(frameCount / 10);
    }

    // Mặt trời / Mặt trăng
    ctx.fillStyle = night ? "#f1c40f" : "#ffd700";
    ctx.beginPath(); ctx.arc(920, 75, 30, 0, Math.PI * 2); ctx.fill();

    // Mây bồng bềnh
    if (Math.random() < 0.02) {
        decorations.push(new GameObject(canvas.width + 50, Math.random() * 120 + 30, 50, 25, speed * 0.3, 'cloud'));
    }
    for (let i = decorations.length - 1; i >= 0; i--) {
        decorations[i].update();
        decorations[i].draw();
        if (decorations[i].x < -80) decorations.splice(i, 1);
    }

    // Mặt đất
    ctx.strokeStyle = night ? "#34495e" : "#2ecc71";
    ctx.lineWidth = 12;
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

    // Khủng long dễ thương
    dino.update();
    dino.draw();

    // Điểm số và Kỷ lục
    ctx.fillStyle = night ? "#f1c40f" : "#2c3e50";
    ctx.font = "bold 22px 'Courier New', monospace";
    ctx.textAlign = "right";
    ctx.fillText("HI: " + highScore + "  |  SCORE: " + score + (night ? " 🌙 ĐÊM" : " ☀️ NGÀY"), canvas.width - 30, 45);

    // Màn hình Game Over
    if (gameState === 'over') {
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#ffeb3b";
        ctx.font = "bold 42px 'Courier New', monospace";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 40);

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px 'Courier New', monospace";
        ctx.fillText("Điểm số hiện tại: " + score, canvas.width / 2, canvas.height / 2 + 5);
        ctx.fillText("🏆 Kỷ lục cao nhất: " + highScore, canvas.width / 2, canvas.height / 2 + 40);
        ctx.fillText("💡 Nhấn SPACE hoặc Click để chơi lại!", canvas.width / 2, canvas.height / 2 + 85);
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

components.html(dino_html, height=480)
