import streamlit as st
import streamlit.components.v1 as components

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Vương Quốc Khủng Long",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long")
st.write("Dùng **Phím Cách (Space)** hoặc **Mũi tên lên** để nhảy. Nhấn **'R'** để chơi lại!")

# --- PHẦN MÃ HTML, CSS VÀ JAVASCRIPT ---
dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Game</title>
    <style>
        body { margin: 0; background-color: #f7f7f7; overflow: hidden; font-family: 'Courier New', Courier, monospace; }
        #game-container { position: relative; width: 800px; height: 300px; margin: 20px auto; border: 4px solid #fff; border-radius: 10px; overflow: hidden; background-color: #c9eaf2; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
        canvas { display: block; }
        #score-display, #game-over-display { position: absolute; color: #535353; font-weight: bold; }
        #score-display { top: 10px; right: 20px; font-size: 20px; }
        #game-over-display { top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; display: none; background: rgba(0,0,0,0.6); color: #fff; padding: 20px; border-radius: 10px; border: 2px solid #fff; }
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
// --- CẤU HÌNH & BIẾN GAME ---
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score-display");
const gameOverDisplay = document.getElementById("game-over-display");
const finalScoreDisplay = document.getElementById("final-score");

// Trạng thái game
let gameState = 'playing'; // 'playing', 'over'
let score = 0;
let highScore = 0;
let dino;
let obstacles = [];
let decorationParams = []; // Đám mây, mặt trời, hoa
let frameCount = 0;
let speed = 6;
const GROUND_Y = 250;

// Các hằng số vẽ Khủng long
const DINO_WIDTH = 44
