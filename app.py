import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Khủng Long Vương Quốc",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long")
st.write("Sử dụng phím **Cách (Space)** hoặc **Mũi tên lên** để nhảy qua chướng ngại vật!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Game</title>
    <style>
        body { margin: 0; background-color: #9cd4e3; overflow: hidden; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { border: 4px solid #fff; border-radius: 10px; background: #c9eaf2; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="800" height="300"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const GROUND_Y = 250;
let dino = { x: 80, y: GROUND_Y - 40, w: 30, h: 40, vy: 0, gravity: 0.8, jump: -15, grounded: true };
let obstacles = [];
let score = 0;
let highScore = 0;
let gameOver = false;
let frameCount = 0;

document.addEventListener("keydown", function(e) {
    if ((e.code === "Space" || e.code === "ArrowUp") && dino.grounded) {
        dino.vy = dino.jump;
        dino.grounded = false;
        e.preventDefault();
    }
    if (e.code === "KeyR" && gameOver) {
        resetGame();
    }
});

canvas.addEventListener("click", function() {
    if (dino.grounded) {
        dino.vy = dino.jump;
        dino.grounded = false;
    }
    if (gameOver) {
        resetGame();
    }
});

function resetGame() {
    dino.y = GROUND_Y - 40;
    dino.vy = 0;
    dino.grounded = true;
    obstacles = [];
    score = 0;
    gameOver = false;
    frameCount = 0;
    loop();
}

function spawnObstacle() {
    let type = Math.random() < 0.5 ? 'tree' : 'bird';
    let h = type === 'tree' ? 40 : 25;
    let y = type === 'tree' ? GROUND_Y - h : GROUND_Y - 70;
    obstacles.push({ x: canvas.width, y: y, w: 25, h: h, type: type, speed: 5 });
}

function update() {
    if (gameOver) return;
    frameCount++;
    score = Math.floor(frameCount / 10);

    dino.vy += dino.gravity;
    dino.y += dino.vy;

    if (dino.y + dino.h > GROUND_Y) {
        dino.y = GROUND_Y - dino.h;
        dino.vy = 0;
        dino.grounded = true;
    }

    if (frameCount % 90 === 0) {
        spawnObstacle();
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].x -= obstacles[i].speed;

        // Va chạm
        if (
            dino.x < obstacles[i].x + obstacles[i].w &&
            dino.x + dino.w > obstacles[i].x &&
            dino.y < obstacles[i].y + obstacles[i].h &&
            dino.y + dino.h > obstacles[i].y
        ) {
            gameOver = true;
            if (score > highScore) highScore = score;
        }

        if (obstacles[i].x + obstacles[i].w < 0) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Vẽ mặt trời
    ctx.fillStyle = "#ffeb3b";
    ctx.beginPath(); ctx.arc(700, 60, 25, 0, Math.PI * 2); ctx.fill();

    // Vẽ mây
    ctx.fillStyle = "rgba(255,255,255,0.8)";
    ctx.beginPath(); ctx.arc(200, 70, 20, 0, Math.PI * 2); ctx.arc(225, 65, 25, 0, Math.PI * 2); ctx.arc(250, 70, 20, 0, Math.PI * 2); ctx.fill();

    // Vẽ mặt đất & cỏ
    ctx.strokeStyle = "#4caf50"; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(0, GROUND_Y); ctx.lineTo(canvas.width, GROUND_Y); ctx.stroke();

    // Vẽ Khủng long
    ctx.fillStyle = "#689f38";
    ctx.fillRect(dino.x, dino.y, dino.w, dino.h);
    // Đầu khủng long
    ctx.fillStyle = "#558b2f";
    ctx.fillRect(dino.x + 15, dino.y - 12, 22, 20);
    // Mắt
    ctx.fillStyle = "#fff";
    ctx.fillRect(dino.x + 28, dino.y - 8, 4, 4);

    // Vẽ chướng ngại vật (Cây hoặc Chim)
    for (let obs of obstacles) {
        if (obs.type === 'tree') {
            ctx.fillStyle = "#2e7d32"; // Cây xanh
            ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
        } else {
            ctx.fillStyle = "#d32f2f"; // Chim đỏ
            ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
        }
    }

    // Hiển thị điểm số
    ctx.fillStyle = "#333";
    ctx.font = "18px sans-serif";
    ctx.fillText("SCORE: " + score + "  |  HI: " + highScore, 550, 30);

    if (gameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#fff";
        ctx.font = "30px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);
        
        ctx.font = "15px sans-serif";
        ctx.fillText("Nhấn phím R hoặc Click để chơi lại", canvas.width / 2, canvas.height / 2 + 25);
        ctx.textAlign = "left";
    }
}

function loop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(loop);
    } else {
        draw();
    }
}

loop();
</script>

</body>
</html>
"""

components.html(dino_html, height=350)
