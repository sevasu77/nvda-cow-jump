import streamlit as st
import yfinance as yf

# --- 1. UIの完全固定化 ---
st.set_page_config(page_title="NVDA Cow Jump", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header, footer { display: none !important; }
    .main .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2.  ---
@st.cache_data(ttl=3600)
def get_nvda_coeff():
    try:
        nvda = yf.Ticker("NVDA")
        change = ((nvda.history(period="2d")['Close'].pct_change()) * 100).iloc[-1]
        # 物理定数
        return {"k": round(0.4 * (1 - (change / 15)), 4), "p": round(-12 * (1 + (change / 40)), 4), "raw": round(change, 2)}
    except:
        return {"k": 0.38, "p": -11.5, "raw": 1.02}

m_data = get_nvda_coeff()

# --- 3. ゲームエンジン ---
game_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        body {{ margin: 0; background: #000428; color: white; font-family: monospace; overflow: hidden; }}
        #stage {{ position: relative; width: 400px; height: 600px; background: #000428; margin: auto; border: 4px solid #fff; overflow: hidden; }}
        #unit {{ position: absolute; width: 50px; height: 50px; font-size: 40px; z-index: 10; }}
        
        .p-node {{ position: absolute; height: 10px; background: #00ffcc; border-radius: 5px; width: 100px; }}
        #ui {{ position: absolute; top: 10px; left: 10px; font-size: 11px; z-index: 100; background: rgba(0,0,0,0.8); padding: 5px; }}
    </style>
</head>
<body>
<div id="stage">
    <div id="ui">MARKET_REF: {m_data['raw']}%<br>ALT: <span id="a">0</span></div>
    <div id="unit">🐄</div>
    <div id="n0" class="p-node"></div><div id="n1" class="p-node"></div>
    <div id="n2" class="p-node"></div><div id="n3" class="p-node"></div>
    <div id="n4" class="p-node"></div><div id="n5" class="p-node"></div>
</div>

<script>
    const _K = {m_data['k']}, _P = {m_data['p']};
    let _y = 300, _vy = 0, _x = 175, _alt = 0;
    let _s = [550, 440, 330, 220, 110, 0]; // 垂直オフセット
    let _lx = [100, 200, 50, 250, 150, 80]; // 水平固定値
    let _keys = {{}};

    // if(y > p.y...) 
    function _check(_cy, _cx) {{
        let hit = false;
        _s.forEach((v, i) => {{
            const dx = _cx - _lx[i];
            
            if (_vy > 0 && Math.abs(_cy + 45 - v) < 8 && dx > -30 && dx < 80) hit = true;
        }});
        return hit;
    }}

    function _proc() {{
        _vy += _K; _y += _vy;
        if(_keys['ArrowLeft']) _x -= 6; if(_keys['ArrowRight']) _x += 6;
        
        if(_check(_y, _x)) _vy = _P;

        if(_y < 250) {{
            let d = 250 - _y; _y = 250; _alt += d/10;
            _s = _s.map(v => (v + d > 600) ? 0 : v + d);
        }}

        const u = document.getElementById('unit');
        u.style.top = _y + 'px'; u.style.left = _x + 'px';
        _s.forEach((v, i) => {{
            const n = document.getElementById('n' + i);
            n.style.top = v + 'px'; n.style.left = _lx[i] + 'px';
        }});
        document.getElementById('a').innerText = Math.floor(_alt);
        
        if(_y > 600) location.reload();
        requestAnimationFrame(_proc);
    }}

    window.onkeydown = e => _keys[e.key] = true;
    window.onkeyup = e => _keys[e.key] = false;
    _proc();
</script>
</body>
</html>
"""

st.components.v1.html(game_code, height=650)
