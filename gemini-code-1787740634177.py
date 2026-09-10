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
# MODERN CSS — ปรับเฉพาะหน้าตา
# =========================================================
st.markdown("""
<style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #f8fafc 100%
        );
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ==============================
       HEADER
    ============================== */

    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;

        background: linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6,
            #ec4899
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 35px;
    }

    /* ==============================
       SECTION TITLE
    ============================== */

    h2, h3 {
        color: #1e293b !important;
        font-weight: 750 !important;
        letter-spacing: -0.3px;
    }

    /* ==============================
       CARD
    ============================== */

    .modern-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(226,232,240,0.9);
        border-radius: 18px;
        padding: 22px 24px;
        margin: 12px 0;
        box-shadow:
            0 8px 25px rgba(15,23,42,0.06),
            0 2px 6px rgba(15,23,42,0.04);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow:
            0 14px 35px rgba(15,23,42,0.10),
            0 4px 10px rgba(15,23,42,0.05);
    }

    /* ==============================
       LINK
    ============================== */

    .queue-link {
        color: #334155;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .queue-link code {
        background: #f1f5f9;
        color: #475569;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
    }

    /* ==============================
       STATUS BADGES
    ============================== */

    .status-progress {
        display: inline-block;
        background: linear-gradient(
            135deg,
            #fff7ed,
            #ffedd5
        );
        color: #c2410c;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
        border: 1px solid #fed7aa;
    }

    .status-waiting {
        display: inline-block;
        background: linear-gradient(
            135deg,
            #eff6ff,
            #dbeafe
        );
        color: #2563eb;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
        border: 1px solid #bfdbfe;
    }

    .status-success {
        display: inline-block;
        background: linear-gradient(
            135deg,
            #ecfdf5,
            #d1fae5
        );
        color: #047857;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
        border: 1px solid #a7f3d0;
    }

    /* ==============================
       SEARCH BOX
    ============================== */

    div[data-baseweb="input"] {
        border-radius: 12px !important;
    }

    div[data-baseweb="input"] > div {
        background: rgba(255,255,255,0.95) !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        min-height: 48px;
        box-shadow: 0 3px 12px rgba(15,23,42,0.04);
    }

    div[data-baseweb="input"] > div:focus-within {
        border: 1px solid #6366f1 !important;
        box-shadow:
            0 0 0 3px rgba(99,102,241,0.12) !important;
    }

    /* ==============================
       PROGRESS BAR
    ============================== */

    div[data-testid="stProgress"] {
        margin-top: 12px;
        margin-bottom: 5px;
    }

    div[data-testid="stProgress"] > div {
        height: 10px !important;
        border-radius: 999px !important;
        background-color: #e2e8f0 !important;
    }

    div[data-testid="stProgress"] > div > div {
        border-radius: 999px !important;
        background: linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6,
            #ec4899
        ) !important;
    }

    /* ==============================
       STREAMLIT ALERTS
    ============================== */

    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid rgba(226,232,240,0.8) !important;
        box-shadow: 0 5px 18px rgba(15,23,42,0.04);
    }

    /* ==============================
       DIVIDER
    ============================== */

    hr {
        border: none !important;
        border-top: 1px solid #e2e8f0 !important;
        margin: 30px 0 !important;
    }

    /* ==============================
       FOOTER
    ============================== */

    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 25px;
        padding-top: 15px;
    }

    /* ==============================
       MOBILE
    ============================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .main-title {
            font-size: 1.8rem;
        }

        .sub-title {
            font-size: 0.9rem;
        }

        .modern-card {
            padding: 17px;
            border-radius: 15px;
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
    "เป็นงานกดมือ 100% เว็บไซต์นี้มีไว้สำหรับอัพเดตสถานะคิวของท่าน เท่านั้น!!"
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

    col_link = df.columns[0]

    status_cols = df.columns[1:]

    def analyze_status(row):

        tick_count = 0
        has_waiting = False

        for col in status_cols:

            val = str(row[col]).strip().upper()

            if "⏳" in val:
                has_waiting = True

            if "✅" in val or val == "TRUE":
                tick_count += 1

        return pd.Series({
            "tick_count": tick_count,
            "has_waiting": has_waiting
        })

    status_result = df.apply(analyze_status, axis=1)

    df["tick_count"] = status_result["tick_count"]
    df["has_waiting"] = status_result["has_waiting"]

    def get_status(row):

        if row["has_waiting"]:
            return "กำลังทำ"

        elif row["tick_count"] >= 3:
            return "สำเร็จ"

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

    df["masked_link"] = df[col_link].apply(mask_url)

    in_progress_df = df[df["status"] == "กำลังทำ"]

    waiting_df = df[df["status"] == "รอคิว"]

    completed_df = df[df["status"] == "สำเร็จ"]

    # =====================================================
    # 1. คิวที่กำลังทำอยู่
    # =====================================================

    st.subheader("⚡ คิวที่กำลังทำอยู่ขณะนี้")

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            done_count = min(ticks * 10, 29)

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            with st.container():

                st.markdown(
                    "<div class='modern-card'>",
                    unsafe_allow_html=True
                )

                col_a, col_b = st.columns([2.4, 1])

                with col_a:

                    st.markdown(
                        f"""
                        <div class='queue-link'>
                        🔗 ลิงก์: <code>{row['masked_link']}</code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.progress(progress_pct)

                with col_b:

                    st.markdown(
                        f"""
                        <div style="
                            display:flex;
                            justify-content:flex-end;
                            align-items:center;
                            height:100%;
                            padding-top:10px;
                        ">
                            <span class='status-progress'>
                                ⏳ กำลังทำ &nbsp; ({done_count} / 29)
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

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

            st.markdown(
                f"""
                <div class='modern-card'>
                    <div class='queue-link'>
                        🔹 <strong>รอทำคิวถัดไป</strong>
                        <br><br>
                        <code>{row['masked_link']}</code>
                        <span class='status-waiting'
                        style='float:right;'>
                            🕒 รอคิว (0/29)
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
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

    latest_completed = completed_df.tail(10).iloc[::-1]

    for idx, row in latest_completed.iterrows():

        st.markdown(
            f"""
            <div class="modern-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:15px;
                    flex-wrap:wrap;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                        min-width:0;
                    ">

                        <span style="
                            color:#047857;
                            font-weight:700;
                            font-size:0.95rem;
                            white-space:nowrap;
                        ">
                            ✅ สำเร็จ
                        </span>

                        <code style="
                            background:#f1f5f9;
                            color:#475569;
                            padding:6px 10px;
                            border-radius:8px;
                            font-size:0.85rem;
                            word-break:break-all;
                        ">
                            {row['masked_link']}
                        </code>

                    </div>

                    <span class="status-success">
                        29 / 29
                    </span>

                </div>

                <div style="
                    color:#64748b;
                    font-size:0.9rem;
                    margin-top:15px;
                ">
                    ทำสำเร็จเรียบร้อยแล้ว
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.caption(
        "ยังไม่มีคิวที่ทำสำเร็จ"
    )
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

                    st.markdown(
                        "<div class='modern-card'>",
                        unsafe_allow_html=True
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

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

                    st.markdown(
                        "<div class='modern-card'>",
                        unsafe_allow_html=True
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

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

                    st.markdown(
                        "<div class='modern-card'>",
                        unsafe_allow_html=True
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **{status_text}**"
                    )

                    st.progress(progress_pct)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )

    st.markdown("---")

    # =====================================================
    # อัปเดตอัตโนมัติ
    # =====================================================

    st.markdown(
        """
        <div class='footer-text'>
            🔄 ระบบอัปเดตข้อมูลจาก Google Sheets ทุก 5 วินาที
        </div>
        """,
        unsafe_allow_html=True
    )


except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )

