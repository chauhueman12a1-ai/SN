// Danh sách 10 bức ảnh trong thư mục assets/
const photoPaths = [
    "assets/photo1.jpg",
    "assets/photo2.jpg",
    "assets/photo3.jpg",
    "assets/photo4.jpg",
    "assets/photo5.jpg",
    "assets/photo6.jpg",
    "assets/photo7.jpg",
    "assets/photo8.jpg",
    "assets/photo9.jpg",
    "assets/photo10.jpg"
];

// Nạp 10 ảnh vào album ở lá thư cuối
const photoGrid = document.getElementById('photo-grid');
photoPaths.forEach((src, index) => {
    const img = document.createElement('img');
    img.src = src;
    img.alt = `Ảnh kỷ niệm ${index + 1}`;
    photoGrid.appendChild(img);
});

// Điều khiển nhạc MP3
const bgMusic = document.getElementById('bg-music');
const musicBtn = document.getElementById('music-toggle');
let isPlaying = false;

function toggleMusic() {
    if (isPlaying) {
        bgMusic.pause();
        musicBtn.innerText = "🔇 Đã tắt nhạc";
        isPlaying = false;
    } else {
        bgMusic.play();
        musicBtn.innerText = "🔊 Đang phát nhạc";
        isPlaying = true;
    }
}

// --- 1. CANVAS VŨ TRỤ SAO + PHÁO HOA + TRÁI TIM HẠT 3D ---
const canvas = document.getElementById('mainCanvas');
const ctx = canvas.getContext('2d');
let W = canvas.width = window.innerWidth;
let H = canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
});

const stars = Array.from({ length: 140 }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    r: Math.random() * 1.6 + 0.3,
    alpha: Math.random(),
    speed: Math.random() * 0.02 + 0.005
}));

let fireworks = [];
let particles = [];
let fireworkActive = true;

class Firework {
    constructor() {
        this.x = Math.random() * W;
        this.y = H;
        this.targetY = Math.random() * (H * 0.45) + 50;
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
        for (let i = 0; i < 65; i++) {
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

// --- TRÁI TIM HẠT HỒNG 3D ---
let heart3DActive = false;
const heartParticles = [];
const totalHeartDots = 1600;

for (let i = 0; i < totalHeartDots; i++) {
    const t = Math.random() * Math.PI * 2;
    const r = Math.pow(Math.random(), 0.45);
    const hx = 16 * Math.pow(Math.sin(t), 3) * r;
    const hy = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * r;
    const hz = (Math.random() - 0.5) * 10 * (1 - r * 0.4);

    heartParticles.push({
        hx, hy, hz,
        size: Math.random() * 2.2 + 1.1,
        color: Math.random() > 0.3 ? '#ff5e8e' : '#ff9ebb'
    });
}

let heartBeatPhase = 0;
let heartRotY = 0;

function draw3DHeart() {
    heartBeatPhase += 0.07;
    heartRotY += 0.015;
    const beatScale = 1 + Math.sin(heartBeatPhase) * 0.05;
    const baseScale = Math.min(W, H) * 0.014 * beatScale;

    const cosY = Math.cos(heartRotY);
    const sinY = Math.sin(heartRotY);

    for (let i = 0; i < heartParticles.length; i++) {
        const p = heartParticles[i];
        const rx = p.hx * cosY - p.hz * sinY;
        const rz = p.hx * sinY + p.hz * cosY;

        const fov = 350;
        const perspective = fov / (fov + rz * 10);
        const screenX = W / 2 + rx * baseScale * perspective;
        const screenY = H / 2 + (p.hy - 1.5) * baseScale * perspective;

        ctx.beginPath();
        ctx.arc(screenX, screenY, p.size * perspective, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
    }
}

function mainLoop() {
    ctx.fillStyle = 'rgba(5, 2, 8, 0.28)';
    ctx.fillRect(0, 0, W, H);

    stars.forEach(s => {
        s.alpha += s.speed;
        const a = 0.3 + Math.abs(Math.sin(s.alpha)) * 0.7;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${a})`;
        ctx.fill();
    });

    if (fireworkActive && Math.random() < 0.14) {
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

    if (heart3DActive) {
        draw3DHeart();
    }

    requestAnimationFrame(mainLoop);
}
mainLoop();

// --- 2. VÒNG QUAY 10 ẢNH + CHỮ CHÚC QUANH TRÁI TIM 3D ---
const orbitStage = document.getElementById('orbit-stage');
const orbitRing = document.getElementById('orbit-ring');
let orbitAnimId = null;
let orbitAngle = 0;

const orbitCaptions = [
    "Tuổi mới luôn xinh đẹp ✨",
    "Sinh nhật thật vui nha Nhi 🎂",
    "Cười tươi mỗi ngày nha 😆",
    "Tiền đầy túi, tình đầy tim 💖",
    "Mãi đỉnh bồ tèo ơi 🥳"
];

function startHeartOrbitScene() {
    heart3DActive = true;
    orbitStage.style.display = 'block';
    orbitRing.innerHTML = '';

    const orbitElements = [];

    photoPaths.forEach((src, i) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'orbit-item';
        const img = document.createElement('img');
        img.src = src;
        img.className = 'orbit-photo';
        wrapper.appendChild(img);
        orbitRing.appendChild(wrapper);

        orbitElements.push({
            el: wrapper,
            angleOffset: (i / photoPaths.length) * Math.PI * 2,
            yOffset: (i % 2 === 0 ? -1 : 1) * (40 + (i % 3) * 35),
            radiusX: Math.min(W * 0.36, 360),
            radiusZ: 240
        });
    });

    orbitCaptions.forEach((text, i) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'orbit-item orbit-label';
        wrapper.innerText = text;
        orbitRing.appendChild(wrapper);

        orbitElements.push({
            el: wrapper,
            angleOffset: (i / orbitCaptions.length) * Math.PI * 2 + 0.3,
            yOffset: (i - 2) * 75,
            radiusX: Math.min(W * 0.42, 420),
            radiusZ: 280
        });
    });

    function animateOrbit() {
        orbitAngle += 0.012;
        orbitElements.forEach(item => {
            const theta = orbitAngle + item.angleOffset;
            const x = Math.sin(theta) * item.radiusX;
            const z = Math.cos(theta) * item.radiusZ;

            const scale = (z + 450) / 650;
            const opacity = z < -120 ? 0.35 : 1;
            const zIndex = Math.round(z + 300);

            item.el.style.transform = `translate(-50%, -50%) translate3d(${x}px, ${item.yOffset}px, 0) scale(${scale})`;
            item.el.style.opacity = opacity;
            item.el.style.zIndex = zIndex;
        });

        orbitAnimId = requestAnimationFrame(animateOrbit);
    }
    animateOrbit();
}

function stopHeartOrbitScene() {
    heart3DActive = false;
    orbitStage.style.display = 'none';
    if (orbitAnimId) cancelAnimationFrame(orbitAnimId);
}

// --- 3. MƯA CHỮ KHÔNG GIAN 3D DÀY ĐẶC + TRÁI TIM NHỎ ---
const wishesList = [
    "Chúc mừng sinh nhật bé Nhi 🎂",
    "Tuổi mới luôn xinh đẹp 💖",
    "Dẫu có nắng hay mưa mãi rạng rỡ ✨",
    "Hay ăn chóng lớn nha bồ tèo 😂",
    "Tiền vào như nước 💰",
    "Vạn sự như ý 🌟",
    "May mắn ngập tràn 🍀",
    "Mãi keo nhé Nhi ơi 🥳",
    "Hạnh phúc vô biên 💕",
    "Happy Birthday Nhi 🎀",
    "Cười thật tươi mỗi ngày nha 😄",
    "Mọi điều ước đều thành hiện thực 🌠"
];

let wish3DInterval;
const space3D = document.getElementById('space-3d');

function spawnSingle3DItem(initialDelay = 0) {
    const isHeart = Math.random() < 0.38;
    const el = document.createElement('div');

    if (isHeart) {
        el.className = 'heart-3d';
        el.innerText = '❤';
    } else {
        el.className = 'wish-3d';
        el.innerText = wishesList[Math.floor(Math.random() * wishesList.length)];
    }

    const zDepth = Math.floor(Math.random() * 850) - 600;
    const isVeryFar = zDepth < -320;
    const isFar = zDepth >= -320 && zDepth < -80;

    el.style.left = Math.random() * 92 - 4 + 'vw';

    if (isHeart) {
        el.style.fontSize = isVeryFar ? '0.9rem' : (isFar ? '1.4rem' : '2.1rem');
    } else {
        el.style.fontSize = isVeryFar ? '0.85rem' : (isFar ? '1.15rem' : '1.6rem');
    }

    el.style.filter = isVeryFar ? 'blur(2px)' : (isFar ? 'blur(0.8px)' : 'none');
    el.style.setProperty('--z-depth', `${zDepth}px`);
    el.style.setProperty('--max-opacity', isVeryFar ? '0.45' : (isFar ? '0.75' : '1'));
    el.style.setProperty('--rx', `${Math.random() * 24 - 12}deg`);
    el.style.setProperty('--ry', `${Math.random() * 34 - 17}deg`);
    el.style.setProperty('--drift-x', `${Math.random() * 90 - 45}px`);

    const duration = isVeryFar
        ? (Math.random() * 1.5 + 4.2)
        : (isFar ? (Math.random() * 1.2 + 3.2) : (Math.random() * 1 + 2.4));

    el.style.animationDuration = `${duration}s`;
    el.style.animationDelay = `${initialDelay}s`;

    space3D.appendChild(el);
    setTimeout(() => el.remove(), (duration + initialDelay) * 1000);
}

function start3DWishes() {
    for (let i = 0; i < 35; i++) {
        spawnSingle3DItem(Math.random() * 1.5);
    }

    wish3DInterval = setInterval(() => {
        spawnSingle3DItem(0);
        spawnSingle3DItem(0);
    }, 75);
}

function stop3DWishes() {
    clearInterval(wish3DInterval);
}

// --- 4. ĐIỀU KHIỂN KỊCH BẢN THEO ĐÚNG TRÌNH TỰ ---
let candleLit = true;

function startCelebration() {
    document.getElementById('start-screen').style.display = 'none';
    musicBtn.style.display = 'block';
    bgMusic.play().then(() => {
        isPlaying = true;
    }).catch(err => console.log(err));

    // Bước 1: Pháo hoa mở màn 3 giây
    fireworkActive = true;

    setTimeout(() => {
        // Bước 2: Đếm ngược 3 - 2 - 1
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

                // Bước 3: Phát video em bé chào đời
                playBabyVideoStage();
            }
        }, 1000);
    }, 3000);
}

function playBabyVideoStage() {
    const videoScene = document.getElementById('baby-video-scene');
    const babyVideo = document.getElementById('baby-video');
    videoScene.style.display = 'flex';

    let movedToNext = false;
    function finishBabyVideo() {
        if (movedToNext) return;
        movedToNext = true;
        babyVideo.pause();
        videoScene.style.display = 'none';
        startHeartAndRainSequence();
    }

    babyVideo.currentTime = 0;
    babyVideo.play().catch(() => {
        setTimeout(finishBabyVideo, 3000);
    });

    babyVideo.onended = finishBabyVideo;
    setTimeout(finishBabyVideo, 14500);
}

function startHeartAndRainSequence() {
    // Bước 4: Trái tim hạt 3D + 10 bức ảnh quay quanh (7 giây)
    startHeartOrbitScene();

    setTimeout(() => {
        stopHeartOrbitScene();

        // Bước 5: Mưa chữ 3D dày đặc + trái tim nhỏ rơi trong 5 giây
        start3DWishes();

        setTimeout(() => {
            stop3DWishes();

            // Hiện chữ "Chúc mừng sinh nhật bồ tèo... mặt cười haha"
            const boTeoEl = document.getElementById('bo-teo-msg');
            boTeoEl.style.display = 'block';

            // Sau 2.5 giây -> Chữ nhòe đi
            setTimeout(() => {
                boTeoEl.classList.add('blur-out');

                // Sau 1.8 giây -> Hiện bánh kem 3 tầng (ngọn nến CHƯA tắt)
                setTimeout(() => {
                    boTeoEl.style.display = 'none';
                    const cakeScene = document.getElementById('cake-scene');
                    cakeScene.style.display = 'flex';
                    candleLit = true;
                }, 1800);
            }, 2500);
        }, 5000);
    }, 7000);
}

// Bước 6: Bấm vào bánh kem -> Thổi tắt nến & Mở lá thư
function blowCandleAndOpenLetter() {
    if (candleLit) {
        document.getElementById('flame').classList.add('out');
        document.getElementById('smoke').classList.add('rise');
        document.getElementById('cake-hint').innerText = '🎉 Chúc điều ước của Nhi thành hiện thực! Đang mở thư...';
        candleLit = false;

        setTimeout(() => {
            document.getElementById('letter-modal').style.display = 'flex';
            document.getElementById('cake-hint').innerText = '👉 Bấm vào bánh để đọc lại thư nhé!';
            fireworkActive = true;
        }, 1200);
    } else {
        document.getElementById('letter-modal').style.display = 'flex';
        fireworkActive = true;
    }
}

function closeLetter() {
    document.getElementById('letter-modal').style.display = 'none';
    fireworkActive = true;
}