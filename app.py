import streamlit as st
import streamlit.components.v1 as components
import random

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Khủng Long Dino Vương Quốc",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Vương Quốc Khủng Long")
st.write("Dùng **Space** hoặc **Mũi tên lên** để nhảy. Tránh cây, chim và bông hoa!")

# --- PHẦN MÃ HTML, CSS VÀ JAVASCRIPT ---
dino_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Game</title>
    <style>
        body { margin: 0; background-color: #9cd4e3; overflow: hidden; font-family: sans-serif; }
        #game-container { position: relative; width: 800px; height: 300px; margin: 20px auto; border: 4px solid #fff; border-radius: 10px; overflow: hidden; background-color: #c9eaf2; }
        canvas { display: block; background: #c9eaf2; }
        #score, #game-over-screen { position: absolute; color: #fff; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); font-weight: bold; }
        #score { top: 10px; right: 20px; font-size: 20px; }
        #game-over-screen { top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; display: none;
