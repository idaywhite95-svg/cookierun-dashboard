```python
import streamlit as st
import pandas as pd

# =========================================================
# ตั้งค่าหน้าตาเว็บ Dashboard
# =========================================================
st.set_page_config(
    page_title="Cookie Run Queue Tracker",
    page_icon="🎮",
    layout="wide"
)

# =========================================================
# MODERN GAMING DASHBOARD CSS
# ปรับเฉพาะหน้าตา ไม่เปลี่ยนระบบการทำงานเดิม
# =========================================================
st.markdown("""
<style>

/* =========================
   GLOBAL THEME
========================= */

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(255, 75, 75, 0.10),
            transparent 32%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(70, 120, 255, 0.09),
            transparent 30%
        ),
        #0b1020;
    color: #edf2ff;
}

[data-testid="stHeader"] {
    background: rgba(11, 16, 32, 0.80);
}

[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* =========================
   MAIN TITLE
========================= */

.main-title {
    text-align: center;
    font-size: clamp(1.7rem, 4vw, 2.65rem);
    font-weight: 850;
    letter-spacing: -1px;
    line-height: 1.4;
    margin: 10px 0 12px 0;
    color: #ffffff;
    text-shadow: 0 0 30px rgba(255, 75, 75, 0.22);
}

.sub-title {
    text-align: center;
    color: #aab5d0;
    font-size: 0.98rem;
    line-height: 1.8;
    margin: 0 auto 35px auto;
    max-width: 760px;
}

/* =========================
   SECTION HEADINGS
========================= */

h2, h3 {
    color: #f3f6ff !important;
    font-weight: 750 !important;
    letter-spacing: -0.3px;
}

h3 {
    font-size: 1.22rem !important;
    margin-top: 1.3rem !important;
    margin-bottom: 1rem !important;
}

[data-testid="stMarkdownContainer"] h3 {
    padding-left: 12px;
    border-left: 4px solid #ff626d;
}

/* =========================
   TEXT
========================= */

p, label, .stCaption, [data-testid="stCaptionContainer"] {
    color: #b9c4dc;
}

strong, b {
    color: #f6f8ff;
}

code {
    color: #8fe8ff !important;
    background: #172239 !important;
    border: 1px solid #293954;
    border-radius: 7px;
    padding: 4px 7px !important;
    overflow-wrap: anywhere;
    white-space: pre-wrap !important;
}

/* =========================
   DIVIDERS
========================= */

hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #34415f,
        transparent
    );
    margin: 25px 0;
}

/* =========================
   ALERT BOXES
========================= */

[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid #2c3a55;
    background: #151e31;
    color: #edf2ff;
    padding: 13px 16px;
}

[data-testid="stAlert"] p {
    color: #e7edfb !important;
}

[data-testid="stAlert"][data-alert-type="success"] {
    background: rgba(26, 145, 95, 0.12);
    border-color: rgba(58, 210, 145, 0.35);
}

[data-testid="stAlert"][data-alert-type="info"] {
    background: rgba(63, 124, 255, 0.12);
    border-color: rgba(92, 145, 255, 0.35);
}

[data-testid="stAlert"][data-alert-type="warning"] {
    background: rgba(255, 175, 55, 0.10);
    border-color: rgba(255, 185, 75, 0.35);
}

[data-testid="stAlert"][data-alert-type="error"] {
    background: rgba(255, 75, 90, 0.10);
    border-color: rgba(255, 90, 105, 0.35);
}

/* =========================
   PROGRESS BAR
========================= */

[data-testid="stProgressBar"] {
    margin-top: 10px;
    margin-bottom: 10px;
}

[data-testid="stProgressBar"] > div {
    background: #222d45;
    border-radius: 100px;
    overflow: hidden;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #ff596b,
        #ff9b67
    );
    border-radius: 100px;
}

/* =========================
   SEARCH INPUT
========================= */

[data-testid="stTextInput"] label {
    color: #e6ecfa !important;
    font-weight: 650;
    margin-bottom: 8px;
}

[data-testid="stTextInput"] input {
    background: #111a2c !important;
    color: #f5f7ff !important;
    border: 1px solid #34415e !important;
    border-radius: 12px !important;
    min-height: 48px;
    transition: border-color 0.2s, box-shadow 0.2s;
}

[data-testid="stTextInput"] input:focus {
    border-color: #ff6572 !important;
    box-shadow: 0 0 0 2px rgba(255, 101, 114, 0.15) !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #71809f !important;
}

/* =========================
   COLUMNS / QUEUE ITEMS
========================= */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(19, 28, 47, 0.68);
    border: 1px solid #283650;
    border-radius: 16px;
    padding: 15px 17px;
}

[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

/* =========================
   DATAFRAME / TABLE IF USED
========================= */

[data-testid="stDataFrame"] {
    border: 1px solid #293650;
    border-radius: 12px;
    overflow: hidden;
}

/* =========================
   FOOTER / CAPTIONS
========================= */

[data-testid="stCaptionContainer"] {
    color: #8190ae !important;
    font-size: 0.84rem;
}

/* =========================
   LINKS
========================= */

a {
    color: #75dfff !important;
}

/* =========================
   MOBILE RESPONSIVE
========================= */

@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 1.65rem;
        letter-spacing: -0.5px;
    }

    .sub-title {
        font-size: 0.88rem;
        margin-bottom: 25px;
    }

    h3 {
        font-size: 1.08rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 12px;
    }
}

/* =========================
   REDUCE ANIMATION
========================= */

@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
        animation: none !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# หัวเว็บ
# =========================================================
st.markdown(
    "<div class='main-title'>🎮 ดูสถานะคิวเชิญเพื่อน Cookie Run</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>"
    "เป็นงานกดมือ 100% เว็บไซต์นี้มีไว้สำหรับอัปเดตสถานะคิวของท่านเท่านั้น"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# Google Sheets
# =========================================================
SPREADSHEET_ID = "1vZi4vkxw3hmUjteYVXYLDlhzLgrtLJySny_JiGaLtWc"
SHEET_NAME = "Sheet1"

GSHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
)


# =========================================================
# โหลดข้อมูล
# =========================================================
@st.cache_data(ttl=5)
def load_data():

    df = pd.read_csv(GSHEET_URL)

    # คอลัมน์แรก = ลิงก์
    col_link = df.columns[0]

    # คอลัมน์สถานะทั้งหมด
    status_cols = df.columns[1:]

    # -----------------------------------------------------
    # ตรวจสอบสถานะของแต่ละแถว
    # -----------------------------------------------------
    def analyze_status(row):

        tick_count = 0
        has_waiting = False

        for col in status_cols:

            val = str(row[col]).strip().upper()

            # มี ⏳ = กำลังทำ
            if "⏳" in val:
                has_waiting = True

            # รองรับเครื่องหมายสำเร็จ
            if "✅" in val or val == "TRUE":
                tick_count += 1

        return pd.Series({
            "tick_count": tick_count,
            "has_waiting": has_waiting
        })

    status_result = df.apply(analyze_status, axis=1)

    df["tick_count"] = status_result["tick_count"]
    df["has_waiting"] = status_result["has_waiting"]

    # -----------------------------------------------------
    # กำหนดสถานะ
    # -----------------------------------------------------
    def get_status(row):

        # ถ้ามี ⏳ อย่างน้อย 1 ช่อง = กำลังทำ
        if row["has_waiting"]:
            return "กำลังทำ"

        # ครบ 3 ช่อง = สำเร็จ
        elif row["tick_count"] >= 3:
            return "สำเร็จ"

        # นอกนั้น = รอคิว
        else:
            return "รอคิว"

    df["status"] = df.apply(get_status, axis=1)

    return df, col_link


# =========================================================
# ปิดบังลิงก์
# =========================================================
def mask_url(url):

    url_str = str(url).strip()

    if len(url_str) >= 4:
        return url_str[:-4] + "**"

    return url_str


# =========================================================
# เริ่มระบบ
# =========================================================
try:

    df, col_link = load_data()

    # สร้างลิงก์แบบปิดท้าย
    df["masked_link"] = df[col_link].apply(mask_url)

    # =====================================================
    # แยกประเภทคิว
    # =====================================================

    # กำลังทำ
    in_progress_df = df[df["status"] == "กำลังทำ"]

    # รอคิว
    waiting_df = df[df["status"] == "รอคิว"]

    # สำเร็จ
    completed_df = df[df["status"] == "สำเร็จ"]

    # =====================================================
    # 1. คิวที่กำลังทำอยู่
    # =====================================================
    st.subheader("⚡ คิวที่กำลังทำอยู่ขณะนี้")

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            # คำนวณความคืบหน้า
            done_count = min(ticks * 10, 29)

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            with st.container():

                col_a, col_b = st.columns([2, 1])

                with col_a:

                    st.markdown(
                        f"🔗 **ลิงก์:** `{row['masked_link']}`"
                    )

                    st.progress(progress_pct)

                with col_b:

                    st.info(
                        f"⏳ **กำลังทำ** "
                        f"({done_count} / 29)"
                    )

                st.divider()

    else:

        st.info(
            "💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่"
        )

    # =====================================================
    # 2. คิวที่รอถัดไป
    # =====================================================
    st.subheader("⌛ คิวที่รอถัดไป")

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for idx, row in next_queues.iterrows():

            st.warning(
                f"🔹 **รอทำคิวถัดไป:** "
                f"`{row['masked_link']}` "
                f"— 🕒 สถานะ: **รอคิว (0/29)**"
            )

    else:

        st.caption(
            "ไม่มีคิวรอทำในระบบ"
        )

    st.markdown("---")

    # =====================================================
    # 3. คิวที่ทำสำเร็จล่าสุด
    # =====================================================
    st.subheader("✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด")

    if not completed_df.empty:

        # เอา 10 คิวล่าสุด
        latest_completed = completed_df.tail(10).iloc[::-1]

        for idx, row in latest_completed.iterrows():

            st.success(
                f"✅ `{row['masked_link']}` "
                f"— **ทำสำเร็จเรียบร้อยแล้ว (29/29)**"
            )

    else:

        st.caption(
            "ยังไม่มีคิวที่ทำสำเร็จ"
        )

    st.markdown("---")

    # =====================================================
    # 4. ค้นหาคิวของตัวเอง
    # =====================================================
    st.subheader("🔍 ตรวจสอบสถานะคิวของคุณ")

    search_input = st.text_input(
        "วางลิงก์ของคุณที่นี่เพื่อค้นหาสถานะ:",
        placeholder="เช่น https://cookierunglobal.onelink.me/..."
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

            for _, row in search_result.iterrows():

                ticks = int(row["tick_count"])

                # =========================================
                # สำเร็จ
                # =========================================
                if row["status"] == "สำเร็จ":

                    status_text = (
                        "✅ ทำสำเร็จเรียบร้อยแล้ว (29/29)"
                    )

                    progress_pct = 100

                    st.success(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                # =========================================
                # กำลังทำ
                # =========================================
                elif row["status"] == "กำลังทำ":

                    done_count = min(
                        ticks * 10,
                        29
                    )

                    progress_pct = min(
                        int((done_count / 29) * 100),
                        100
                    )

                    status_text = (
                        f"⏳ กำลังดำเนินการ "
                        f"({done_count}/29)"
                    )

                    st.info(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                # =========================================
                # รอคิว
                # =========================================
                else:

                    status_text = (
                        "🕒 รอทำคิวถัดไป (0/29)"
                    )

                    progress_pct = 0

                    st.warning(
                        "🎉 **พบข้อมูลคิวของคุณ!**"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )

    st.markdown("---")

    # =====================================================
    # อัปเดตอัตโนมัติ
    # =====================================================
    st.caption(
        "🔄 ระบบอัปเดตข้อมูลจาก Google Sheets ทุก 5 วินาที"
    )


except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )
```
