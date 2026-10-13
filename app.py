import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Google Dino Game trên Streamlit",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Trò chơi Khủng Long Chrome")
st.write("Sử dụng phím **Cách (Space)** hoặc phím **Mũi tên lên (Up Arrow)** để nhảy!")

dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Game</title>
    <style>
        body {
            margin: 0;
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }
        canvas {
            border: 1px solid #d3d3d3;
            background: #fff;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="600" height="200"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let dino = { x: 50, y: 140, width: 20, height: 30, vy: 0, gravity: 0.6, jump: -10, grounded: true };
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
    dino.y = 140;
    dino.vy = 0;
    dino.grounded = true;
    obstacles = [];
    score = 0;
    gameOver = false;
    frameCount = 0;
    loop();
}

function spawnObstacle() {
    let size = 20 + Math.random() * 15;
    obstacles.push({ x: canvas.width, y: 170 - size, width: 15, height: size, speed: 4 });
}

function update() {
    if (gameOver) return;
    frameCount++;
    score = Math.floor(frameCount / 10);

    dino.vy += dino.gravity;
    dino.y += dino.vy;

    if (dino.y > 140) {
        dino.y = 140;
        dino.vy = 0;
        dino.grounded = true;
    }

    if (frameCount % 100 === 0) {
        spawnObstacle();
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        obstacles[i].x -= obstacles[i].speed;

        if (
            dino.x < obstacles[i].x + obstacles[i].width &&
            dino.x + dino.width > obstacles[i].x &&
            dino.y < obstacles[i].y + obstacles[i].height &&
            dino.y + dino.height > obstacles[i].y
        ) {
            gameOver = true;
            if (score > highScore) highScore = score;
        }

        if (obstacles[i].x + obstacles[i].width < 0) {
            obstacles.splice(i, 1);
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#535353";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 170);
    ctx.lineTo(canvas.width, 170);
    ctx.stroke();

    ctx.fillStyle = "#535353";
    ctx.fillRect(dino.x, dino.y, dino.width, dino.height);

    ctx.fillStyle = "#e74c3c";
    for (let obs of obstacles) {
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
    }

    ctx.fillStyle = "#535353";
    ctx.font = "16px Arial";
    ctx.fillText("HI: " + highScore + "  |  SCO: " + score, canvas.width - 180, 30);

    if (gameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#fff";
        ctx.font = "24px Arial";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);
        
        ctx.font = "14px Arial";
        ctx.fillText("Nhấn R hoặc Click để chơi lại", canvas.width / 2, canvas.height / 2 + 20);
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

components.html(dino_html, height=250)
