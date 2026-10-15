import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Cookie Run Queue Tracker",
    page_icon="🎮",
    layout="wide"
)

# =========================================================
# NEON GAMING THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #080b16;
    --panel: #11162a;
    --panel2: #171d35;
    --border: #292e52;
    --purple: #a970ff;
    --blue: #55d9ff;
    --pink: #ff63c3;
    --green: #4be3ad;
    --yellow: #ffc76b;
    --text: #f2f4ff;
    --muted: #9ca8c9;
}

html, body, [class*="css"] {
    font-family: 'Prompt', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, #29134b 0%, transparent 34%),
        radial-gradient(ellipse at 95% 12%, #102b50 0%, transparent 32%),
        linear-gradient(145deg, #080b16, #0b1020 55%, #090d19);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(8, 11, 22, 0.7);
}

[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1220px;
    padding: 2rem 2rem 3rem;
}

/* ---------- HERO ---------- */

.hero {
    position: relative;
    overflow: hidden;
    padding: 32px 26px;
    margin-bottom: 25px;
    border: 1px solid rgba(169, 112, 255, 0.38);
    border-radius: 24px;
    background:
        linear-gradient(120deg,
            rgba(104, 55, 190, 0.22),
            rgba(35, 101, 170, 0.13) 55%,
            rgba(255, 99, 195, 0.08));
    box-shadow:
        0 0 35px rgba(111, 72, 220, 0.10),
        inset 0 0 30px rgba(110, 100, 255, 0.035);
    text-align: center;
}

.hero::before {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    top: -165px;
    right: -70px;
    background: rgba(85, 217, 255, 0.10);
    filter: blur(10px);
}

.hero-tag {
    display: inline-block;
    padding: 6px 13px;
    border: 1px solid rgba(85, 217, 255, 0.35);
    border-radius: 999px;
    color: var(--blue);
    background: rgba(85, 217, 255, 0.07);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(1.65rem, 4vw, 2.65rem);
    font-weight: 800;
    line-height: 1.4;
    margin: 0;
    text-shadow: 0 0 25px rgba(169, 112, 255, 0.35);
}

.hero-title span {
    color: var(--blue);
}

.hero-subtitle {
    color: #b8c4e5;
    font-size: 0.95rem;
    margin-top: 10px;
    line-height: 1.8;
}

.hero-note {
    display: inline-block;
    margin-top: 15px;
    color: #d8c6ff;
    font-size: 0.82rem;
    background: rgba(169, 112, 255, 0.09);
    border: 1px solid rgba(169, 112, 255, 0.2);
    padding: 7px 12px;
    border-radius: 10px;
}

/* ---------- SECTION HEADINGS ---------- */

h1, h2, h3 {
    color: var(--text) !important;
    font-family: 'Prompt', sans-serif !important;
}

h3 {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-top: 1.25rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stMarkdownContainer"] h3 {
    border-left: 3px solid var(--purple);
    padding-left: 12px;
}

/* ---------- STAT CARDS ---------- */

.stat-card {
    position: relative;
    overflow: hidden;
    min-height: 138px;
    padding: 19px;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, #171d35, #101528);
    transition: transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: var(--glow);
    box-shadow: 0 0 24px var(--shadow);
}

.stat-card::after {
    content: "";
    position: absolute;
    width: 90px;
    height: 90px;
    right: -30px;
    bottom: -45px;
    border-radius: 50%;
    background: var(--shadow);
    filter: blur(24px);
}

.stat-label {
    color: #aeb9d8;
    font-size: 0.88rem;
    font-weight: 500;
}

.stat-value {
    color: var(--glow);
    font-size: 2.1rem;
    line-height: 1.45;
    font-weight: 800;
    text-shadow: 0 0 18px var(--shadow);
}

.stat-caption {
    color: #8997bb;
    font-size: 0.77rem;
}

.stat-icon {
    font-size: 1.45rem;
    margin-bottom: 8px;
}

/* ---------- QUEUE CARDS ---------- */

.queue-card {
    background: linear-gradient(135deg, #151b31, #101526);
    border: 1px solid #293353;
    border-radius: 16px;
    padding: 17px 19px;
    margin: 9px 0 13px 0;
    transition: transform 0.22s ease,
                border-color 0.22s ease,
                box-shadow 0.22s ease;
}

.queue-card:hover {
    transform: translateY(-3px);
    border-color: #7460c6;
    box-shadow: 0 0 22px rgba(145, 99, 255, 0.14);
}

.queue-link-label {
    color: #aab6d6;
    font-size: 0.8rem;
    margin-bottom: 5px;
}

.queue-link {
    color: var(--blue);
    font-weight: 600;
    overflow-wrap: anywhere;
}

.queue-meta {
    color: #c6cfea;
    font-size: 0.9rem;
    margin-top: 8px;
}

.status-pill {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 7px;
}

.pill-progress {
    color: #d7c1ff;
    background: rgba(169, 112, 255, 0.13);
    border: 1px solid rgba(169, 112, 255, 0.32);
}

.pill-waiting {
    color: #ffda95;
    background: rgba(255, 199, 107, 0.10);
    border: 1px solid rgba(255, 199, 107, 0.27);
}

.pill-success {
    color: #83f5cb;
    background: rgba(75, 227, 173, 0.10);
    border: 1px solid rgba(75, 227, 173, 0.27);
}

.queue-number {
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 700;
}

/* ---------- PROGRESS BAR ---------- */

[data-testid="stProgressBar"] {
    margin: 10px 0 5px;
}

[data-testid="stProgressBar"] > div {
    height: 10px;
    background: #252b47;
    border-radius: 100px;
    overflow: hidden;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #4f8cff,
        #55d9ff,
        #c17aff
    );
    background-size: 250% 100%;
    animation: neon-flow 3s linear infinite;
    border-radius: 100px;
}

@keyframes neon-flow {
    0% { background-position: 0% 50%; }
    100% { background-position: 250% 50%; }
}

/* ---------- INPUT ---------- */

[data-testid="stTextInput"] label {
    color: #dfe6ff !important;
    font-weight: 600;
    margin-bottom: 8px;
}

[data-testid="stTextInput"] input {
    background: #11172b !important;
    color: #ffffff !important;
    border: 1px solid #343d62 !important;
    border-radius: 13px !important;
    min-height: 49px;
    transition: all 0.2s ease;
}

[data-testid="stTextInput"] input:focus {
    border-color: #a970ff !important;
    box-shadow: 0 0 0 2px rgba(169, 112, 255, 0.16),
                0 0 20px rgba(169, 112, 255, 0.10) !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #7886a9 !important;
}

/* ---------- ALERTS ---------- */

[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid #303a5a;
    background: #141a2e;
}

[data-testid="stAlert"] p {
    color: #edf2ff !important;
}

[data-testid="stAlert"] svg {
    color: #a8b9ff;
}

/* ---------- CODE / LINKS ---------- */

code {
    color: #74e3ff !important;
    background: #101b30 !important;
    border: 1px solid #293e5d;
    border-radius: 7px;
    padding: 4px 7px !important;
    white-space: pre-wrap !important;
    overflow-wrap: anywhere;
}

a {
    color: var(--blue) !important;
}

/* ---------- DIVIDERS / CAPTIONS ---------- */

hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #343c62,
        transparent
    );
    margin: 27px 0;
}

[data-testid="stCaptionContainer"] {
    color: #8f9cbd !important;
}

/* ---------- MOBILE ---------- */

@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] .main .block-container {
        padding: 1rem 0.8rem 2rem;
    }

    .hero {
        padding: 25px 15px;
        border-radius: 18px;
    }

    .hero-title {
        font-size: 1.65rem;
    }

    .hero-subtitle {
        font-size: 0.84rem;
    }

    .stat-card {
        min-height: 115px;
        padding: 13px;
        border-radius: 14px;
    }

    .stat-value {
        font-size: 1.7rem;
    }

    .stat-label {
        font-size: 0.78rem;
    }

    .queue-card {
        padding: 14px;
    }

    h3 {
        font-size: 1.05rem !important;
    }
}

/* ลดการเคลื่อนไหวตามการตั้งค่าของอุปกรณ์ */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ COOKIE RUN • QUEUE CENTER ✦</div>
    <div class="hero-title">🎮 COOKIE RUN <span>Classic</span></div>
    <div class="hero-subtitle">
        ระบบตรวจสอบสถานะคิวเชิญเพื่อนของคุณ<br>
        ติดตามสถานะได้ง่าย สะดวก และรวดเร็ว<br>
        ** เว็บไซต์นี้มีไว้แค่ดูสถานะคิวเท่านั้น
    </div>
    <div class="hero-note">🛡️ ระบบกดมือ 100% ปลอดภัยแน่นอน • </div>
    <br>
    <div class="hero-note"> ติดต่อสอบถาม Facebook :
    <a href="https://www.facebook.com/sakkarin.38"
       target="_blank" rel="noopener noreferrer"
       style="color:#55d9ff; font-weight:700; text-decoration:none;">
        Sakkarin papai
    </a>
</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# GOOGLE SHEETS
# =========================================================
SPREADSHEET_ID = "1vZi4vkxw3hmUjteYVXYLDlhzLgrtLJySny_JiGaLtWc"
SHEET_NAME = "Sheet1"

GSHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
)


# =========================================================
# LOAD DATA - คงตรรกะเดิม
# =========================================================
@st.cache_data(ttl=5)
def load_data():

    df = pd.read_csv(GSHEET_URL)

    # คอลัมน์แรก = ลิงก์
    col_link = df.columns[0]

    # คอลัมน์สถานะทั้งหมด
    status_cols = df.columns[1:]

    def analyze_status(row):

        tick_count = 0
        has_waiting = False
        has_progress = False

        for col in status_cols:

            val = str(row[col]).strip().upper()

            # ⏳ = กำลังดำเนินการ
            if "⏳" in val:
                has_waiting = True

            # ✅ = มีความคืบหน้า; นับจำนวนช่องที่ทำเครื่องหมายแล้ว
            if "✅" in val or val == "TRUE":
                tick_count += 1
                has_progress = True

        return pd.Series({
            "tick_count": tick_count,
            "has_waiting": has_waiting,
            "has_progress": has_progress
        })

    status_result = df.apply(analyze_status, axis=1)

    df["tick_count"] = status_result["tick_count"]
    df["has_waiting"] = status_result["has_waiting"]
    df["has_progress"] = status_result["has_progress"]

    def get_status(row):

        # ครบ 3 ช่อง ✅ ให้เป็นสำเร็จ แม้มีเครื่องหมายอื่นในแถว
        if row["tick_count"] >= 3:
            return "สำเร็จ"

        # มี ✅ อย่างน้อย 1 ช่อง หรือมี ⏳ ให้เป็นกำลังดำเนินการ
        elif row["has_progress"] or row["has_waiting"]:
            return "กำลังทำ"

        else:
            return "รอคิว"

    df["status"] = df.apply(get_status, axis=1)

    return df, col_link


# =========================================================
# MASK URL - คงฟังก์ชันเดิม
# =========================================================
def mask_url(url):

    url_str = str(url).strip()

    if len(url_str) >= 4:
        return url_str[:-4] + "**"

    return url_str


# =========================================================
# UI HELPERS
# =========================================================
def show_queue_card(link, status, detail, progress=None, icon="🔗"):

    st.markdown(f"""
    <div class="queue-card">
        <div class="queue-link-label">{icon} ลิงก์คิว</div>
        <div class="queue-link">{link}</div>
        <div class="queue-meta">{status} · {detail}</div>
    </div>
    """, unsafe_allow_html=True)

    if progress is not None:
        st.progress(max(0, min(int(progress), 100)))


def show_stat_card(icon, label, value, caption, color, shadow):
    st.markdown(f"""
    <div class="stat-card"
         style="--glow:{color}; --shadow:{shadow};">
        <div class="stat-icon">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-caption">{caption}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MAIN DASHBOARD
# =========================================================
try:

    df, col_link = load_data()

    df["masked_link"] = df[col_link].apply(mask_url)

    # แยกประเภทคิว
    in_progress_df = df[df["status"] == "กำลังทำ"]
    waiting_df = df[df["status"] == "รอคิว"]
    completed_df = df[df["status"] == "สำเร็จ"]

    # =====================================================
    # SUMMARY CARDS
    # แสดงเฉพาะกำลังดำเนินการและรอคิว
    # =====================================================
    st.markdown("### ✨ ภาพรวมสถานะคิว")

    stat1, stat2 = st.columns(2)

    with stat1:
        show_stat_card(
            "⚡", "กำลังดำเนินการ",
            len(in_progress_df), "คิวที่กำลังทำ",
            "#b78aff", "rgba(169,112,255,0.25)"
        )

    with stat2:
        show_stat_card(
            "⌛", "รอคิว",
            len(waiting_df), "คิวที่รอดำเนินการ",
            "#ffd078", "rgba(255,199,107,0.22)"
        )

    st.markdown("---")

    # =====================================================
    # 1. IN PROGRESS
    # =====================================================
    st.subheader("⚡ คิวที่กำลังทำอยู่ขณะนี้")

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            # คงสูตรความคืบหน้าเดิม
            done_count = min(ticks * 10, 29)

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            col_a, col_b = st.columns([2, 1])

            with col_a:
                show_queue_card(
                    row["masked_link"],
                    "กำลังดำเนินการ",
                    f"ความคืบหน้า {done_count}/29",
                    progress_pct,
                    "🔗"
                )

            with col_b:
                st.markdown(
                    f"""
                    <div class="queue-card">
                        <div class="status-pill pill-progress">
                            ● กำลังทำ
                        </div>
                        <div class="queue-number">
                            {done_count} / 29 รายการ
                        </div>
                        <div class="queue-meta">
                            ความคืบหน้า {progress_pct}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่")

    # =====================================================
    # 2. WAITING QUEUES
    # =====================================================
    st.subheader("⌛ คิวที่รอถัดไป")

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for position, (idx, row) in enumerate(
            next_queues.iterrows(), start=1
        ):

            st.markdown(f"""
            <div class="queue-card">
                <div class="status-pill pill-waiting">
                    ⏳ ลำดับคิว {position}
                </div>
                <div class="queue-link-label">🔗 ลิงก์คิว</div>
                <div class="queue-link">{row['masked_link']}</div>
                <div class="queue-meta">
                    🕒 รอทำคิวถัดไป · 0/29 รายการ
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.caption("✨ ไม่มีคิวรอทำในระบบ")

    st.markdown("---")

    # =====================================================
    # 3. LATEST COMPLETED - 10 QUEUES
    # =====================================================
    st.subheader("✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด")

    if not completed_df.empty:

        latest_completed = completed_df.tail(10).iloc[::-1]

        for idx, row in latest_completed.iterrows():

            st.markdown(f"""
            <div class="queue-card"
                 style="border-color:rgba(75,227,173,0.24);">
                <div class="status-pill pill-success">
                    ✓ สำเร็จแล้ว
                </div>
                <div class="queue-link">{row['masked_link']}</div>
                <div class="queue-meta">
                    🎉 ทำสำเร็จเรียบร้อยแล้ว · 29/29
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.caption("ยังไม่มีคิวที่ทำสำเร็จ")

    st.markdown("---")

    # =====================================================
    # 4. SEARCH QUEUE
    # =====================================================
    st.subheader("🔍 ตรวจสอบสถานะคิวของคุณ")

    st.markdown("""
    <div class="queue-meta" style="margin-bottom:12px;">
        วางลิงก์เชิญเพื่อนของคุณในช่องด้านล่าง
        เพื่อค้นหาสถานะจากข้อมูลในระบบ
    </div>
    """, unsafe_allow_html=True)

    search_input = st.text_input(
        "ลิงก์เชิญเพื่อน",
        placeholder="เช่น https://cookierunglobal.onelink.me/...",
        key="queue_search"
    )

    if search_input:

        search_text = search_input.strip()

        search_result = df[
            df[col_link]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        if not search_result.empty:

            st.success("🎉 พบข้อมูลคิวของคุณ!")

            for _, row in search_result.iterrows():

                ticks = int(row["tick_count"])

                if row["status"] == "สำเร็จ":

                    status_text = "✅ ทำสำเร็จเรียบร้อยแล้ว (29/29)"
                    progress_pct = 100
                    status_class = "pill-success"

                elif row["status"] == "กำลังทำ":

                    done_count = min(ticks * 10, 29)

                    progress_pct = min(
                        int((done_count / 29) * 100),
                        100
                    )

                    status_text = (
                        f"⏳ กำลังดำเนินการ ({done_count}/29)"
                    )
                    status_class = "pill-progress"

                else:

                    status_text = "🕒 รอทำคิวถัดไป (0/29)"
                    progress_pct = 0
                    status_class = "pill-waiting"

                st.markdown(f"""
                <div class="queue-card">
                    <div class="status-pill {status_class}">
                        ผลการค้นหาคิว
                    </div>
                    <div class="queue-link-label">🔗 ลิงก์ของคุณ</div>
                    <div class="queue-link">{row['masked_link']}</div>
                    <div class="queue-meta">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(progress_pct)

        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )

    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown("---")

    st.markdown("""
    <div style="
        text-align:center;
        padding:15px 5px;
        color:#8996b8;
        font-size:0.82rem;
        line-height:1.9;
    ">
        <div style="color:#b8a0ff;font-weight:600;">
            🎮 COOKIE RUN QUEUE TRACKER
        </div>
        🔄 ระบบอัปเดตข้อมูล ทุก 5 วินาที หรือหากข้อมูลไม่อัปเดต โปรดกดรีเฟรช ใหม่อีกครั้ง
    </div>
    """, unsafe_allow_html=True)

except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )
