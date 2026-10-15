import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long (Đã sửa lỗi hiển thị)")
st.write("💡 **Mẹo:** Click chuột vào khung game bên dưới một lần, sau đó bấm phím **Cách (Space)** để khủng long nhảy!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cute Dino Game Fixed</title>
    <style>
        body { margin: 0; background-color: #f7f7f7; overflow: hidden; font-family: 'Courier New', Courier, monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
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
let speed = 7;
const GROUND_Y = 330;

function isNight() {
    let cycle = Math.floor(score / 100);
    return cycle % 2 !== 0;
}

class Dino {
    constructor() {
        this.x = 90;
        this.y = GROUND_Y - 55;
        this.w = 50;
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
        
        // Thân khủng long
        ctx.fillRect(dx + 10, dy + 18, 32, 28);

        // Đầu khủng long
        ctx.fillRect(dx + 22, dy - 4, 28, 24);

        // Mắt khủng long
        ctx.fillStyle = "#111";
        ctx.fillRect(dx + 40, dy + 2, 5, 5);

        // Đuôi khủng long
        ctx.fillStyle = isNight() ? "#a8e063" : "#68bb59";
        ctx.beginPath();
        ctx.moveTo(dx + 10, dy + 22);
        ctx.lineTo(dx, dy + 12);
        ctx.lineTo(dx + 10, dy + 32);
        ctx.fill();

        // Chân khủng long
        ctx.fillRect(dx + 14, dy + 46, 8, 9);
        ctx.fillRect(dx + 30, dy + 46, 8, 9);

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
            ctx.fillRect(this.x, this.y + 5, 25, 12);
        } else if (this.type === 'cloud') {
            ctx.fillStyle = isNight() ? "rgba(255,255,255,0.25)" : "rgba(255,255,255,0.85)";
            ctx.fillRect(this.x, this.y, 50, 20);
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
