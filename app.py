import streamlit as st

# Hyper Cow Jump - Official Demo Version
# This code is a functional prototype for the full version available on itch.io.
hyper_cow_jump_official = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Hyper Cow Jump - Official Demo</title>
    <style>
        body { 
            margin: 0; background: #000428; color: white; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100vh; overflow: hidden;
        }
        #game-container {
            position: relative; width: 400px; height: 600px;
            background: linear-gradient(to top, #004e92, #000428);
            border: 4px solid #fff; border-radius: 10px; overflow: hidden;
            box-shadow: 0 0 20px rgba(255,255,255,0.2);
        }
        #cow {
            position: absolute; font-size: 50px; z-index: 10;
            transform-origin: center bottom;
        }
        .platform {
            position: absolute; height: 15px; background: #00ffcc;
            border-radius: 5px; box-shadow: 0 0 10px #00ffcc;
            transform-origin: center;
        }
        .burger { position: absolute; font-size: 30px; }
        #ui {
            position: absolute; top: 10px; left: 10px; z-index: 100;
            font-size: 16px; width: 90%; letter-spacing: 1px;
        }
        #hunger-bar-container {
            width: 100%; height: 8px; background: #333; border-radius: 4px; margin-top: 5px;
        }
        #hunger-bar { width: 100%; height: 100%; background: #ff4b2b; border-radius: 4px; }
        #altitude { color: gold; font-weight: bold; }
        #game-over {
            position: absolute; inset: 0; background: rgba(0,0,0,0.9);
            display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 1000;
            text-align: center; padding: 20px;
        }
        button { 
            padding: 12px 24px; font-size: 18px; cursor: pointer; background: gold; 
            border: none; border-radius: 5px; margin-top: 15px; font-weight: bold;
        }
        .itch-link { 
            color: #ff4b2b; font-weight: bold; text-decoration: none; 
            margin-top: 20px; font-size: 14px; border: 1px solid #ff4b2b;
            padding: 8px 16px; border-radius: 20px; transition: 0.3s;
        }
        .itch-link:hover { background: #ff4b2b; color: white; }
    </style>
</head>
<body>

<div id="game-container">
    <div id="ui">
        ALTITUDE: <span id="altitude">0</span> m<br>
        ENERGY:
        <div id="hunger-bar-container"><div id="hunger-bar"></div></div>
    </div>

    <div id="cow">🐄</div>

    <div id="game-over">
        <h2 id="fail-reason">Game Over</h2>
        <p>Record: <span id="final-alt">0</span>m</p>
        <p id="promo-msg" style="display:none; color: #00ffcc; font-size: 14px;">
            Thank you for playing the Demo!<br>
            The full version with enhanced graphics and sound is available on itch.io.
        </p>
        <button onclick="location.reload()">Try Again</button>
        <a href="https://sevasu77.itch.io/" target="_blank" class="itch-link">Play Full Version on itch.io</a>
    </div>
</div>

<script>
    const container = document.getElementById('game-container');
    const cowEl = document.getElementById('cow');
    const hungerBar = document.getElementById('hunger-bar');
    const altDisp = document.getElementById('altitude');

    let cow = { x: 180, y: 300, vx: 0, vy: 0, w: 50, h: 50 };
    let platforms = [];
    let altitude = 0;
    let hunger = 100;
    let keys = {};
    let gameActive = true;

    function init() {
        for(let i=0; i<6; i++) {
            spawnPlatform(500 - (i * 120));
        }
        requestAnimationFrame(loop);
    }

    function spawnPlatform(y) {
        platforms.push({
            x: Math.random() * 250 + 20,
            y: y,
            w: 100,
            angle: 0,
            targetY: y,
            offset: Math.random() * 100,
            isBurger: Math.random() > 0.8
        });
    }

    function loop() {
        if(!gameActive) return;

        // Demo Limitation: Altitude limit
        if (altitude > 1000) { 
            endGame("Demo Limit Reached", true); 
            return;
        }

        cow.vy += 0.4;
        if(keys['a'] || keys['arrowleft']) cow.vx -= 0.8;
        if(keys['d'] || keys['arrowright']) cow.vx += 0.8;
        cow.vx *= 0.9;
        cow.x += cow.vx;
        cow.y += cow.vy;

        hunger -= 0.05 + (altitude / 10000);
        hungerBar.style.width = Math.max(0, hunger) + '%';
        if(hunger <= 0) endGame("Energy Depleted");

        platforms.forEach(p => {
            p.y = p.targetY + Math.sin((Date.now() + p.offset) / 500) * 30;
            if(cow.vy > 0 && 
               cow.x + cow.w > p.x && cow.x < p.x + p.w &&
               cow.y + cow.h > p.y && cow.y + cow.h < p.y + 20) {
                let center = p.x + p.w / 2;
                p.angle = ((cow.x + cow.w/2) - center) * 0.4;
                if(cow.y + cow.h <= p.y + 10 + Math.abs(p.angle/2)) {
                    cow.y = p.y - cow.h + Math.abs(p.angle/2);
                    cow.vy = -12;
                    if(p.isBurger) { hunger = Math.min(100, hunger + 30); p.isBurger = false; }
                }
            }
        });

        if(cow.y < 300) {
            let diff = 300 - cow.y;
            cow.y = 300;
            altitude += Math.floor(diff);
            altDisp.innerText = Math.floor(altitude/10);
            platforms.forEach(p => {
                p.targetY += diff;
                if(p.targetY > 600) {
                    platforms.splice(platforms.indexOf(p), 1);
                    spawnPlatform(-50);
                }
            });
        }

        cowEl.style.left = cow.x + 'px';
        cowEl.style.top = cow.y + 'px';
        cowEl.style.transform = `rotate(${cow.vx * 2}deg)`;

        renderPlatforms();

        if(cow.y > 600) endGame("Fell Off");
        requestAnimationFrame(loop);
    }

    function renderPlatforms() {
        const platformEls = container.querySelectorAll('.platform, .burger');
        platformEls.forEach(el => el.remove());
        platforms.forEach(p => {
            const el = document.createElement('div');
            el.className = 'platform';
            el.style.left = p.x + 'px'; el.style.top = p.y + 'px';
            el.style.width = p.w + 'px'; el.style.transform = `rotate(${p.angle}deg)`;
            container.appendChild(el);
            if(p.isBurger) {
                const b = document.createElement('div');
                b.className = 'burger'; b.innerText = '🍔';
                b.style.left = (p.x + 30) + 'px'; b.style.top = (p.y - 40) + 'px';
                container.appendChild(b);
            }
        });
    }

    function endGame(reason, isPromo = false) {
        gameActive = false;
        document.getElementById('game-over').style.display = 'flex';
        document.getElementById('fail-reason').innerText = reason;
        document.getElementById('final-alt').innerText = Math.floor(altitude/10);
        if(isPromo) {
            document.getElementById('promo-msg').style.display = 'block';
        }
    }

    window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
    window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);
    init();
</script>
</body>
</html>
"""

st.components.v1.html(hyper_cow_jump_official, height=650)
