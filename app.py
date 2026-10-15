import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long (Có Thêm Chim & Cúi Người)")
st.write("💡 **Mẹo:** Nhấn **Cách (Space)** hoặc **Mũi tên lên** để nhảy qua xương rồng, và nhấn **Mũi tên xuống** để cúi người né chim bay!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Dino Game with Duck & Bird</title>
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
                this.h = 50; // Trở về chiều cao cũ
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

            // Đầu cúi thấp
            ctx.beginPath();
            ctx.roundRect(dx + 30, dy - 2, 20, 16, 5);
            ctx.fill();

            // Má hồng
            ctx.fillStyle = "#ff80ab";
            ctx.beginPath();
            ctx.arc(dx + 42, dy + 4, 3, 0, Math.PI * 2);
            ctx.fill();

            // Mắt
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
        this.type = type; // 'cactus', 'bird', 'cloud'
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
            // --- VẼ CHIM BAY CAO (CẦN CÚI ĐỂ NÉ) ---
            ctx.fillStyle = isN ? "#ff7675" : "#e74c3c";
            ctx.beginPath(); 
            ctx.ellipse(this.x + 15, this.y + 10, 14, 8, 0, 0, Math.PI * 2); 
            ctx.fill();
            // Cánh chim
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(this.x + 12, this.y + 6, 4, 0, Math.PI * 2);
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
    d
