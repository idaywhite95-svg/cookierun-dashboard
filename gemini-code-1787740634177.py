import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Cookie Run Queue Tracker",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MODERN CSS
# =========================================================
st.markdown("""
<style>

    /* ================================
       GLOBAL
    ================================= */
    .stApp {
        background: #0f1117;
        color: #f5f7fa;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ซ่อนเมนู Streamlit */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ================================
       HEADER
    ================================= */
    .hero {
        background:
            linear-gradient(
                135deg,
                rgba(255,75,75,0.20),
                rgba(120,80,255,0.15)
            );

        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;

        padding: 30px 25px;
        margin-bottom: 25px;

        text-align: center;

        box-shadow:
            0 15px 40px rgba(0,0,0,0.25);
    }

    .hero-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        margin-top: 8px;
        font-size: 15px;
        color: #aeb4c0;
    }

    .notice {
        display: inline-block;

        margin-top: 16px;
        padding: 8px 16px;

        border-radius: 999px;

        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);

        color: #d7dbe2;
        font-size: 13px;
    }

    /* ================================
       STAT CARDS
    ================================= */
    .stat-card {
        background: #171a23;

        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;

        padding: 20px;

        min-height: 110px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.18);
    }

    .stat-title {
        color: #8f96a3;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .stat-number {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
    }

    .stat-desc {
        color: #737b89;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ================================
       SECTION TITLE
    ================================= */
    .section-title {
        font-size: 21px;
        font-weight: 750;

        margin-top: 32px;
        margin-bottom: 15px;

        color: #ffffff;
    }

    /* ================================
       QUEUE CARD
    ================================= */
    .queue-card {
        background: #171a23;

        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;

        padding: 18px 20px;
        margin-bottom: 12px;

        box-shadow:
            0 7px 20px rgba(0,0,0,0.16);

        transition: all 0.2s ease;
    }

    .queue-card:hover {
        border-color: rgba(255,255,255,0.16);

        transform: translateY(-1px);
    }

    .queue-link {
        color: #dce1e8;
        font-family: monospace;
        font-size: 14px;
    }

    .status-running {
        display: inline-block;

        padding: 5px 11px;

        border-radius: 999px;

        background: rgba(255,193,7,0.12);
        color: #ffc107;

        font-size: 12px;
        font-weight: 700;
    }

    .status-waiting {
        display: inline-block;

        padding: 5px 11px;

        border-radius: 999px;

        background: rgba(120,130,150,0.12);
        color: #aeb5c1;

        font-size: 12px;
        font-weight: 700;
    }

    .status-success {
        display: inline-block;

        padding: 5px 11px;

        border-radius: 999px;

        background: rgba(46,204,113,0.12);
        color: #4ade80;

        font-size: 12px;
        font-weight: 700;
    }

    /* ================================
       SEARCH BOX
    ================================= */
    .search-title {
        font-size: 21px;
        font-weight: 750;

        color: #ffffff;

        margin-top: 35px;
        margin-bottom: 8px;
    }

    .search-desc {
        color: #858c99;
        font-size: 13px;
        margin-bottom: 10px;
    }

    /* ================================
       SUCCESS LIST
    ================================= */
    .completed-card {
        background: #151a18;

        border: 1px solid rgba(74,222,128,0.10);
        border-radius: 15px;

        padding: 14px 18px;
        margin-bottom: 9px;
    }

    .completed-link {
        color: #d5ddd7;
        font-family: monospace;
        font-size: 13px;
    }

    /* ================================
       INFO
    ================================= */
    .empty-box {
        background: #151821;

        border: 1px dashed rgba(255,255,255,0.10);

        border-radius: 16px;

        padding: 25px;

        text-align: center;

        color: #737b89;

        margin-bottom: 10px;
    }

    /* ================================
       FOOTER
    ================================= */
    .footer {
        text-align: center;

        color: #5f6672;

        font-size: 12px;

        margin-top: 30px;
        padding-top: 20px;

        border-top: 1px solid rgba(255,255,255,0.06);
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">

    <div class="hero-icon">🎮</div>

    <div class="hero-title">
        ดูสถานะคิวเชิญเพื่อน Cookie Run
    </div>

    <div class="hero-subtitle">
        ระบบตรวจสอบสถานะคิวแบบออนไลน์
    </div>

    <div class="notice">
        🖐️ เป็นงานกดมือ 100% 
        &nbsp; • &nbsp;
        เว็บไซต์นี้มีไว้สำหรับอัพเดตสถานะคิวของท่านเท่านั้น!!
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
# LOAD DATA
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

    status_result = df.apply(
        analyze_status,
        axis=1
    )

    df["tick_count"] = status_result["tick_count"]
    df["has_waiting"] = status_result["has_waiting"]

    def get_status(row):

        if row["has_waiting"]:
            return "กำลังทำ"

        elif row["tick_count"] >= 3:
            return "สำเร็จ"

        else:
            return "รอคิว"

    df["status"] = df.apply(
        get_status,
        axis=1
    )

    return df, col_link


# =========================================================
# MASK URL
# =========================================================
def mask_url(url):

    url_str = str(url).strip()

    if len(url_str) >= 2:
        return url_str[:-2] + "**"

    return url_str


# =========================================================
# MAIN
# =========================================================
try:

    df, col_link = load_data()

    df["masked_link"] = df[col_link].apply(mask_url)

    # แยกสถานะ
    in_progress_df = df[
        df["status"] == "กำลังทำ"
    ]

    waiting_df = df[
        df["status"] == "รอคิว"
    ]

    completed_df = df[
        df["status"] == "สำเร็จ"
    ]


    # =====================================================
    # STATISTICS
    # =====================================================
    st.markdown(
        '<div class="section-title">📊 ภาพรวมคิว</div>',
        unsafe_allow_html=True
    )

    stat1, stat2, stat3 = st.columns(3)

    with stat1:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-title">
                ⚡ กำลังทำ
            </div>

            <div class="stat-number">
                {len(in_progress_df)}
            </div>

            <div class="stat-desc">
                คิวที่กำลังดำเนินการ
            </div>

        </div>
        """, unsafe_allow_html=True)


    with stat2:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-title">
                ⌛ รอคิว
            </div>

            <div class="stat-number">
                {len(waiting_df)}
            </div>

            <div class="stat-desc">
                คิวที่รอดำเนินการ
            </div>

        </div>
        """, unsafe_allow_html=True)


    with stat3:

        st.markdown(f"""
        <div class="stat-card">

            <div class="stat-title">
                ✅ สำเร็จแล้ว
            </div>

            <div class="stat-number">
                {len(completed_df)}
            </div>

            <div class="stat-desc">
                จำนวนคิวที่ทำสำเร็จ
            </div>

        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # RUNNING QUEUES
    # =====================================================
    st.markdown(
        '<div class="section-title">⚡ คิวที่กำลังทำอยู่ขณะนี้</div>',
        unsafe_allow_html=True
    )

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            done_count = min(
                ticks * 10,
                29
            )

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            st.markdown(f"""
            <div class="queue-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:12px;
                ">

                    <div>
                        🔗
                        <span class="queue-link">
                            {row['masked_link']}
                        </span>
                    </div>

                    <div class="status-running">
                        ⏳ กำลังทำ
                    </div>

                </div>

                <div style="
                    background:#252a35;
                    height:8px;
                    border-radius:10px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{progress_pct}%;
                        height:100%;
                        background:linear-gradient(
                            90deg,
                            #ff4b4b,
                            #ff8a4b
                        );
                        border-radius:10px;
                    "></div>

                </div>

                <div style="
                    margin-top:9px;
                    color:#8f96a3;
                    font-size:12px;
                ">
                    ความคืบหน้า {done_count} / 29
                </div>

            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="empty-box">
            💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่
        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # WAITING QUEUES
    # =====================================================
    st.markdown(
        '<div class="section-title">⌛ คิวที่รอถัดไป</div>',
        unsafe_allow_html=True
    )

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for idx, row in next_queues.iterrows():

            st.markdown(f"""
            <div class="queue-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>
                        🔗
                        <span class="queue-link">
                            {row['masked_link']}
                        </span>
                    </div>

                    <div class="status-waiting">
                        🕒 รอทำคิวถัดไป
                    </div>

                </div>

            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="empty-box">
            🎉 ไม่มีคิวรอทำในระบบ
        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # COMPLETED
    # =====================================================
    st.markdown(
        '<div class="section-title">✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด</div>',
        unsafe_allow_html=True
    )

    if not completed_df.empty:

        latest_completed = (
            completed_df
            .tail(10)
            .iloc[::-1]
        )

        for idx, row in latest_completed.iterrows():

            st.markdown(f"""
            <div class="completed-card">

                <span style="margin-right:8px;">
                    ✅
                </span>

                <span class="completed-link">
                    {row['masked_link']}
                </span>

                <span style="
                    float:right;
                    color:#4ade80;
                    font-size:12px;
                    font-weight:600;
                ">
                    29/29
                </span>

            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="empty-box">
            ยังไม่มีคิวที่ทำสำเร็จ
        </div>
        """, unsafe_allow_html=True)


    # =====================================================
    # SEARCH
    # =====================================================
    st.markdown(
        '<div class="search-title">🔍 ตรวจสอบสถานะคิวของคุณ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="search-desc">'
        'วางลิงก์ของคุณด้านล่างเพื่อดูสถานะคิว'
        '</div>',
        unsafe_allow_html=True
    )

    search_input = st.text_input(
        "",
        placeholder="🔗 วางลิงก์ Cookie Run ของคุณที่นี่...",
        label_visibility="collapsed"
    )


    if search_input:

        search_text = search_input.strip()

        search_result = df[
            df[col_link]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False,
                regex=False
            )
        ]

        if not search_result.empty:

            for _, row in search_result.iterrows():

                ticks = int(row["tick_count"])

                st.markdown(
                    '<div style="margin-top:20px;"></div>',
                    unsafe_allow_html=True
                )

                # =========================================
                # SUCCESS
                # =========================================
                if row["status"] == "สำเร็จ":

                    st.success(
                        "🎉 พบข้อมูลคิวของคุณ!"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        "📊 สถานะ: **✅ "
                        "ทำสำเร็จเรียบร้อยแล้ว (29/29)**"
                    )

                    st.progress(100)


                # =========================================
                # RUNNING
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

                    st.info(
                        "🎉 พบข้อมูลคิวของคุณ!"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        f"📊 สถานะ: **⏳ "
                        f"กำลังดำเนินการ "
                        f"({done_count}/29)**"
                    )

                    st.progress(progress_pct)


                # =========================================
                # WAITING
                # =========================================
                else:

                    st.warning(
                        "🎉 พบข้อมูลคิวของคุณ!"
                    )

                    st.write(
                        f"🔗 ลิงก์: `{row['masked_link']}`"
                    )

                    st.write(
                        "📊 สถานะ: **🕒 "
                        "รอทำคิวถัดไป (0/29)**"
                    )

                    st.progress(0)


        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )


    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown("""
    <div class="footer">

        🔄 ระบบอัปเดตข้อมูลจาก Google Sheets ทุก 5 วินาที
        <br>
        Cookie Run Queue Tracker

    </div>
    """, unsafe_allow_html=True)


except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )
```
