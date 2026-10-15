import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long Siêu Dễ Thương (Có Lưu Kỷ Lục)")
st.write("💡 **Mẹo:** Hãy **click chuột trực tiếp vào trong ô trò chơi** phía dưới một lần, sau đó bấm phím **Cách (Space)** để khủng long nhảy!")

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
        <p>Điểm số hiện tại: <span id="final-score">0</span></p>
        <p>🏆 Kỷ lục cao nhất: <span id="high-score">0</span></p>
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
const highScoreDisplay = document.getElementById("high-score");

// --- TÍCH HỢP HỆ THỐNG ÂM THANH 8-BIT ---
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
let highScore = 0; // Biến lưu trữ kỷ lục cao nhất
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
        ctx.roundRect(dx + 10, dy + 15, 28, 24, 10);
