from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chúc Mừng Sinh Nhật Bé Nhi! 🎂</title>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: radial-gradient(circle at center, #1a0b2e 0%, #090312 100%);
            color: #fff;
            font-family: 'Quicksand', sans-serif;
            overflow: hidden;
            height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            user-select: none;
        }
        canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
        }
        .stage {
            position: relative;
            z-index: 10;
            text-align: center;
            width: 100%;
            padding: 20px;
        }

        /* Đếm ngược 3 2 1 */
        #countdown {
            font-size: 9rem;
            font-weight: 700;
            color: #ffde59;
            text-shadow: 0 0 30px #ff4d94, 0 0 60px #ff4d94;
            display: none;
            animation: popScale 0.8s ease-in-out infinite;
        }
        @keyframes popScale {
            0% { transform: scale(0.5); opacity: 0; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }

        /* Em bé sơ sinh chào đời */
        #baby-scene {
            display: none;
            flex-direction: column;
            align-items: center;
            animation: bounceIn 1s ease forwards;
        }
        .baby-icon {
            font-size: 8rem;
            filter: drop-shadow(0 0 25px rgba(255, 222, 89, 0.8));
            animation: babyWiggle 1.2s infinite ease-in-out;
        }
        .baby-text {
            font-size: 1.8rem;
            color: #ffb3d9;
            margin-top: 15px;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        }
        @keyframes babyWiggle {
            0%, 100% { transform: rotate(-8deg) scale(1); }
            50% { transform: rotate(8deg) scale(1.1); }
        }
        @keyframes bounceIn {
            0% { transform: scale(0); opacity: 0; }
            70% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }

        /* Câu chúc rơi từ trên trời */
        .falling-wish {
            position: fixed;
            top: -60px;
            z-index: 5;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 182, 193, 0.4);
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
            white-space: nowrap;
            box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
            animation: fallDown linear forwards;
        }
        @keyframes fallDown {
            0% { transform: translateY(0) rotate(-5deg); opacity: 0; }
            15% { opacity: 1; }
            85% { opacity: 1; }
            100% { transform: translateY(110vh) rotate(5deg); opacity: 0; }
        }

        /* Chữ Chúc mừng sinh nhật bồ tèo */
        #bo-teo-msg {
            display: none;
            font-size: 3.2rem;
            font-weight: 700;
            color: #ffde59;
            text-shadow: 0 0 20px #ff2a85, 0 0 40px #ff2a85;
            line-height: 1.4;
            transition: filter 2s ease, opacity 2s ease, transform 2s ease;
        }
        .blur-out {
            filter: blur(25px);
            opacity: 0;
            transform: scale(1.3);
        }

        /* Bánh sinh nhật & Ngọn nến */
        #cake-scene {
            display: none;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            animation: fadeIn 1.5s ease forwards;
        }
        .cake-wrapper {
            position: relative;
            width: 220px;
            height: 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            transition: transform 0.3s ease;
        }
        .cake-wrapper:hover {
            transform: scale(1.06);
        }
        /* Ngọn lửa lấp lánh */
        .flame {
            width: 22px;
            height: 36px;
            background: radial-gradient(ellipse at bottom, #fff 0%, #ffde59 40%, #ff6a00 85%, transparent 100%);
            border-radius: 50% 50% 35% 35%;
            box-shadow: 0 0 20px #ffde59, 0 0 40px #ff6a00, 0 0 60px #ff2a85;
            animation: flicker 0.25s infinite alternate;
            margin-bottom: -2px;
            z-index: 3;
            transition: opacity 0.4s ease, transform 0.4s ease;
        }
        .flame.out {
            opacity: 0;
            transform: scale(0.1) translateY(-10px);
        }
        /* Khói sau khi thổi tắt */
        .smoke {
            position: absolute;
            top: 15px;
            font-size: 1.8rem;
            opacity: 0;
            pointer-events: none;
        }
        .smoke.rise {
            animation: smokeRise 2s ease-out forwards;
        }
        @keyframes smokeRise {
            0% { opacity: 0.9; transform: translateY(0) scale(0.8); }
            100% { opacity: 0; transform: translateY(-60px) scale(1.6); }
        }
        @keyframes flicker {
            0% { transform: scale(1) rotate(-3deg); opacity: 0.9; }
            100% { transform: scale(1.12) rotate(3deg); opacity: 1; }
        }
        /* Cây nến */
        .candle {
            width: 16px;
            height: 50px;
            background: repeating-linear-gradient(45deg, #fff, #fff 6px, #ff4d94 6px, #ff4d94 12px);
            border-radius: 4px 4px 0 0;
            z-index: 2;
        }
        /* Tầng bánh trên */
        .cake-top {
            width: 140px;
            height: 55px;
            background: linear-gradient(to bottom, #ff99cc, #ff66b3);
            border-radius: 15px 15px 5px 5px;
            position: relative;
            box-shadow: inset 0 -5px 10px rgba(0,0,0,0.15);
        }
        .cake-top::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 18px;
            background: #fff5f8;
            border-radius: 15px 15px 20px 20px;
        }
        /* Tầng bánh dưới */
        .cake-bottom {
            width: 200px;
            height: 70px;
            background: linear-gradient(to bottom, #ff4d94, #d61a6c);
            border-radius: 15px 15px 10px 10px;
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .cake-bottom::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 20px;
            background: #ffe6f0;
            border-radius: 15px 15px 25px 25px;
        }
        .plate {
            width: 240px;
            height: 14px;
            background: #e0e0e0;
            border-radius: 50%;
            margin-top: -4px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.6);
        }
        #cake-hint {
            margin-top: 25px;
            font-size: 1.3rem;
            color: #ffde59;
            font-weight: 700;
            animation: pulseText 1.2s infinite;
        }
        @keyframes pulseText {
            0%, 100% { opacity: 0.7; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Lá thư lời chúc */
        #letter-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(6px);
            z-index: 50;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .letter-paper {
            background: linear-gradient(135deg, #fff9f0 0%, #ffeef5 100%);
            color: #3a1c2e;
            max-width: 520px;
            width: 100%;
            padding: 35px 30px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(255, 77, 148, 0.45);
            border: 3px solid #ff85b3;
            position: relative;
            text-align: left;
            animation: openLetter 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes openLetter {
            0% { transform: scale(0.3) rotate(-10deg); opacity: 0; }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        .letter-paper h2 {
            font-family: 'Dancing Script', cursive;
            font-size: 2.5rem;
            color: #d61a6c;
            margin-bottom: 15px;
            text-align: center;
        }
        .letter-paper p {
            font-size: 1.12rem;
            line-height: 1.7;
            margin-bottom: 14px;
            color: #4a2538;
        }
        .letter-sign {
            text-align: right;
            font-family: 'Dancing Script', cursive;
            font-size: 1.7rem;
            color: #d61a6c;
            margin-top: 20px;
        }
        .close-btn {
            display: block;
            margin: 20px auto 0;
            padding: 10px 26px;
            background: linear-gradient(45deg, #ff4d94, #ff758c);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 77, 148, 0.4);
        }
        .close-btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <canvas id="fireworksCanvas"></canvas>

    <div class="stage">
        <!-- Giai đoạn 2: Đếm ngược -->
        <div id="countdown">3</div>

        <!-- Giai đoạn 3: Em bé sơ sinh chào đời -->
        <div id="baby-scene">
            <div class="baby-icon">👶✨</div>
            <div class="baby-text">Oa oa oa... Bé Nhi chính thức hạ cánh xuống Trái Đất! 🚀</div>
        </div>

        <!-- Giai đoạn 4: Chữ chúc mừng sinh nhật bồ tèo -->
        <div id="bo-teo-msg">
            Chúc mừng sinh nhật bồ tèo Nhi! 😆😂🤣
        </div>

        <!-- Giai đoạn 5: Bánh sinh nhật -->
        <div id="cake-scene" onclick="openLetter()">
            <div class="cake-wrapper">
                <div class="smoke" id="smoke">💨</div>
                <div class="flame" id="flame"></div>
                <div class="candle"></div>
                <div class="cake-top"></div>
                <div class="cake-bottom"></div>
                <div class="plate"></div>
            </div>
            <div id="cake-hint">✨ Ước một điều thật đẹp đi nào... ✨</div>
        </div>
    </div>

    <!-- Giai đoạn 6: Lá thư lời chúc -->
    <div id="letter-modal">
        <div class="letter-paper">
            <h2>Gửi bé Nhi siêu cấp đáng yêu! 💌</h2>
            <p>Chúc mừng sinh nhật bồ tèo nhé! Thêm một tuổi mới, chúc Nhi lúc nào cũng tươi tắn, cười nhiều như được mùa, tiền đầy túi, tình đầy tim và mọi deadline đều tự động né xa.</p>
            <p>Cảm ơn vì đã xuất hiện trên thế giới này để mang lại thật nhiều tiếng cười và năng lượng tích cực. Chúc mọi điều ước lúc nãy thổi nến của cậu đều thành hiện thực 100%!</p>
            <p>Tuổi mới bùng nổ, rực rỡ và hạnh phúc hết nấc nha! 🥳🎂💖</p>
            <div class="letter-sign">Mãi keo nhé bồ tèo! ✨</div>
            <button class="close-btn" onclick="closeLetter()">Đóng thư & Ngắm pháo hoa 🎆</button>
        </div>
    </div>

    <script>
        // --- 1. HIỆU ỨNG PHÁO HOA CANVAS ---
        const canvas = document.getElementById('fireworksCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        let fireworks = [];
        let particles = [];
        let fireworkActive = true;

        class Firework {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = canvas.height;
                this.targetY = Math.random() * (canvas.height * 0.45) + 50;
                this.speed = Math.random() * 4 + 6;
                this.angle = -Math.PI / 2 + (Math.random() - 0.5) * 0.2;
                this.vx = Math.cos(this.angle) * this.speed;
                this.vy = Math.sin(this.angle) * this.speed;
                this.hue = Math.floor(Math.random() * 360);
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.y <= this.targetY) {
                    this.explode();
                    return false;
                }
                return true;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
                ctx.fillStyle = `hsl(${this.hue}, 100%, 65%)`;
                ctx.fill();
            }
            explode() {
                const count = 65;
                for (let i = 0; i < count; i++) {
                    particles.push(new Particle(this.x, this.y, this.hue));
                }
            }
        }

        class Particle {
            constructor(x, y, hue) {
                this.x = x;
                this.y = y;
                this.hue = hue + (Math.random() * 30 - 15);
                const angle = Math.random() * Math.PI * 2;
                const speed = Math.random() * 6 + 1;
                this.vx = Math.cos(angle) * speed;
                this.vy = Math.sin(angle) * speed;
                this.gravity = 0.08;
                this.friction = 0.96;
                this.alpha = 1;
                this.decay = Math.random() * 0.015 + 0.012;
            }
            update() {
                this.vx *= this.friction;
                this.vy *= this.friction;
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= this.decay;
                return this.alpha > 0;
            }
            draw() {
                ctx.save();
                ctx.globalAlpha = this.alpha;
                ctx.beginPath();
                ctx.arc(this.x, this.y, 2.5, 0, Math.PI * 2);
                ctx.fillStyle = `hsl(${this.hue}, 100%, 65%)`;
                ctx.fill();
                ctx.restore();
            }
        }

        function animateFireworks() {
            ctx.fillStyle = 'rgba(9, 3, 18, 0.22)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (fireworkActive && Math.random() < 0.12) {
                fireworks.push(new Firework());
            }

            fireworks = fireworks.filter(fw => {
                fw.draw();
                return fw.update();
            });

            particles = particles.filter(p => {
                p.draw();
                return p.update();
            });

            requestAnimationFrame(animateFireworks);
        }
        animateFireworks();

        // --- 2. CÁC CÂU CHÚC RƠI TỪ TRÊN TRỜI ---
        const wishesList = [
            "🎂 Hay ăn chóng lớn nha Nhi!",
            "💖 Xinh đẹp rạng ngời!",
            "💰 Tiền vào như nước!",
            "😂 Cười tươi mỗi ngày!",
            "🌟 Vạn sự như ý!",
            "🍀 May mắn ngập tràn!",
            "🎉 Tuổi mới bùng nổ!",
            "🥳 Mãi đỉnh bồ tèo ơi!",
            "✨ Hạnh phúc vô biên!"
        ];

        let wishInterval;
        function startFallingWishes() {
            wishInterval = setInterval(() => {
                const wish = document.createElement('div');
                wish.className = 'falling-wish';
                wish.innerText = wishesList[Math.floor(Math.random() * wishesList.length)];
                wish.style.left = Math.random() * 75 + 5 + 'vw';
                const duration = Math.random() * 2 + 3; // 3s - 5s
                wish.style.animationDuration = duration + 's';
                document.body.appendChild(wish);

                setTimeout(() => {
                    wish.remove();
                }, duration * 1000);
            }, 350);
        }

        function stopFallingWishes() {
            clearInterval(wishInterval);
        }

        // --- 3. ĐIỀU KHIỂN KỊCH BẢN THEO THỜI GIAN ---
        let candleBlownOut = false;

        // Bắt đầu: Pháo hoa bắn 3 giây đầu tiên
        setTimeout(() => {
            // Chuyển sang đếm ngược 3 - 2 - 1
            fireworkActive = false;
            const countdownEl = document.getElementById('countdown');
            countdownEl.style.display = 'block';
            let count = 3;
            countdownEl.innerText = count;

            const countTimer = setInterval(() => {
                count--;
                if (count > 0) {
                    countdownEl.innerText = count;
                } else {
                    clearInterval(countTimer);
                    countdownEl.style.display = 'none';

                    // Hiện em bé sơ sinh chào đời + mưa câu chúc rơi trong 5 giây
                    const babyScene = document.getElementById('baby-scene');
                    babyScene.style.display = 'flex';
                    startFallingWishes();

                    // Sau 5 giây -> Hiện chữ "Chúc mừng sinh nhật bồ tèo... mặt cười haha"
                    setTimeout(() => {
                        babyScene.style.display = 'none';
                        stopFallingWishes();

                        const boTeoEl = document.getElementById('bo-teo-msg');
                        boTeoEl.style.display = 'block';

                        // Sau 2.5 giây -> Chữ nhòe đi
                        setTimeout(() => {
                            boTeoEl.classList.add('blur-out');

                            // Sau 1.8 giây nhòe xong -> Hiện bánh sinh nhật với ngọn nến lấp lánh
                            setTimeout(() => {
                                boTeoEl.style.display = 'none';
                                const cakeScene = document.getElementById('cake-scene');
                                cakeScene.style.display = 'flex';

                                // Ngọn nến lấp lánh 3 giây rồi tự thổi tắt
                                setTimeout(() => {
                                    document.getElementById('flame').classList.add('out');
                                    document.getElementById('smoke').classList.add('rise');
                                    document.getElementById('cake-hint').innerText = '👉 Bấm vào chiếc bánh để mở lá thư nhé!';
                                    candleBlownOut = true;
                                }, 3000);

                            }, 1800);
                        }, 2500);
                    }, 5000);
                }
            }, 1000);
        }, 3000);

        // --- 4. MỞ & ĐÓNG LÁ THƯ ---
        function openLetter() {
            if (!candleBlownOut) {
                // Nếu bấm sớm khi nến chưa tắt thì nhắc nhẹ
                document.getElementById('cake-hint').innerText = '⏳ Chờ nến tắt đã nào bồ tèo...';
                return;
            }
            document.getElementById('letter-modal').style.display = 'flex';
            fireworkActive = true; // Bật lại pháo hoa chúc mừng
        }

        function closeLetter() {
            document.getElementById('letter-modal').style.display = 'none';
            fireworkActive = true;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def birthday_nhi():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True, port=5000)