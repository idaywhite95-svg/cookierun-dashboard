import streamlit as st
import pandas as pd

# =========================================================
# ตั้งค่าหน้าเว็บ
# =========================================================
st.set_page_config(
    page_title="Cookie Run Queue Tracker",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS - Modern Dark Dashboard
# =========================================================
st.markdown("""
<style>

    /* พื้นหลัง */
    .stApp {
        background: #0f1117;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 30px;
        padding-bottom: 50px;
    }

    /* ซ่อนเมนูด้านบน */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* หัวข้อ */
    .big-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
    }

    .small-title {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .notice-box {
        text-align: center;
        color: #d1d5db;
        background: #191c25;
        border: 1px solid #2a2f3b;
        border-radius: 30px;
        padding: 10px 20px;
        margin: 0 auto 30px auto;
        max-width: 750px;
        font-size: 13px;
    }

    /* Section */
    .section-title {
        font-size: 21px;
        font-weight: 750;
        color: white;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Card */
    div[data-testid="stMetric"] {
        background: #181b24;
        border: 1px solid #292e3a;
        border-radius: 18px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9ca3af;
    }

    div[data-testid="stMetricValue"] {
        color: white;
    }

    /* Container */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #171a22;
        border: 1px solid #292e3a;
        border-radius: 18px;
    }

    /* Input */
    div[data-baseweb="input"] {
        background: #181b24;
        border: 1px solid #303643;
        border-radius: 12px;
    }

    div[data-baseweb="input"] input {
        color: white;
    }

    /* Progress */
    div[data-testid="stProgress"] > div > div {
        border-radius: 20px;
    }

    /* Caption */
    .footer-text {
        text-align: center;
        color: #626a78;
        font-size: 12px;
        margin-top: 35px;
        padding-top: 20px;
        border-top: 1px solid #252a34;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="big-title">🎮 ดูสถานะคิวเชิญเพื่อน Cookie Run</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="small-title">ระบบตรวจสอบสถานะคิวออนไลน์</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="notice-box">'
    '🖐️ เป็นงานกดมือ 100% &nbsp; • &nbsp; '
    'เว็บไซต์นี้มีไว้สำหรับอัพเดตสถานะคิวของท่านเท่านั้น!!'
    '</div>',
    unsafe_allow_html=True
)


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
# โหลดข้อมูล
# =========================================================
@st.cache_data(ttl=5)
def load_data():

    df = pd.read_csv(GSHEET_URL)

    # คอลัมน์แรก = ลิงก์
    col_link = df.columns[0]

    # คอลัมน์ที่เหลือ = สถานะ
    status_cols = df.columns[1:]

    def analyze_status(row):

        tick_count = 0
        has_waiting = False

        for col in status_cols:

            val = str(row[col]).strip().upper()

            # ถ้ามี ⏳ = กำลังทำ
            if "⏳" in val:
                has_waiting = True

            # ถ้ามี ✅ หรือ TRUE = สำเร็จ
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

    # กำหนดสถานะ
    def get_status(row):

        # มี ⏳ = กำลังทำ
        if row["has_waiting"]:
            return "กำลังทำ"

        # ครบ 3 = สำเร็จ
        elif row["tick_count"] >= 3:
            return "สำเร็จ"

        # ที่เหลือ = รอคิว
        else:
            return "รอคิว"

    df["status"] = df.apply(
        get_status,
        axis=1
    )

    return df, col_link


# =========================================================
# ปิดท้ายลิงก์ 2 ตัว
# =========================================================
def mask_url(url):

    url_str = str(url).strip()

    if len(url_str) >= 2:
        return url_str[:-2] + "**"

    return url_str


# =========================================================
# เริ่มระบบ
# =========================================================
try:

    df, col_link = load_data()

    # สร้างลิงก์สำหรับแสดงผล
    df["masked_link"] = df[col_link].apply(mask_url)

    # แยกคิว
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
    # ภาพรวม
    # =====================================================
    st.markdown(
        '<div class="section-title">📊 ภาพรวมคิว</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⚡ กำลังทำ",
            len(in_progress_df),
            help="จำนวนคิวที่กำลังดำเนินการ"
        )

    with col2:
        st.metric(
            "⌛ รอคิว",
            len(waiting_df),
            help="จำนวนคิวที่รอดำเนินการ"
        )

    with col3:
        st.metric(
            "✅ สำเร็จแล้ว",
            len(completed_df),
            help="จำนวนคิวที่ทำสำเร็จ"
        )


    # =====================================================
    # คิวกำลังทำ
    # =====================================================
    st.markdown(
        '<div class="section-title">⚡ คิวที่กำลังทำอยู่ขณะนี้</div>',
        unsafe_allow_html=True
    )

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            # 3 ขั้นตอน
            done_count = min(ticks * 10, 29)

            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(
                        f"🔗 **ลิงก์:** `{row['masked_link']}`"
                    )

                    st.progress(
                        progress_pct / 100
                    )

                    st.caption(
                        f"ความคืบหน้า {done_count} / 29"
                    )

                with right:

                    st.warning(
                        f"⏳ กำลังทำ\n\n"
                        f"**{done_count}/29**"
                    )

    else:

        st.info(
            "💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่"
        )


    # =====================================================
    # คิวรอ
    # =====================================================
    st.markdown(
        '<div class="section-title">⌛ คิวที่รอถัดไป</div>',
        unsafe_allow_html=True
    )

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for idx, row in next_queues.iterrows():

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(
                        f"🔗 `{row['masked_link']}`"
                    )

                with right:

                    st.caption(
                        "🕒 รอทำคิวถัดไป"
                    )

    else:

        st.info(
            "🎉 ไม่มีคิวรอทำในระบบ"
        )


    # =====================================================
    # สำเร็จล่าสุด
    # =====================================================
    st.markdown(
        '<div class="section-title">'
        '✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด'
        '</div>',
        unsafe_allow_html=True
    )

    if not completed_df.empty:

        # เอา 10 รายการล่าสุด
        latest_completed = (
            completed_df
            .tail(10)
            .iloc[::-1]
        )

        for idx, row in latest_completed.iterrows():

            with st.container(border=True):

                left, right = st.columns([4, 1])

                with left:

                    st.markdown(
                        f"✅ `{row['masked_link']}`"
                    )

                with right:

                    st.caption(
                        "29/29"
                    )

    else:

        st.info(
            "ยังไม่มีคิวที่ทำสำเร็จ"
        )


    # =====================================================
    # ค้นหาคิว
    # =====================================================
    st.markdown(
        '<div class="section-title">'
        '🔍 ตรวจสอบสถานะคิวของคุณ'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "วางลิงก์ของคุณด้านล่างเพื่อดูสถานะคิว"
    )

    search_input = st.text_input(
        "ลิงก์คิว",
        placeholder="🔗 วางลิงก์ Cookie Run ของคุณที่นี่...",
        label_visibility="collapsed"
    )


    # =====================================================
    # ผลการค้นหา
    # =====================================================
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

                st.markdown("---")

                st.success(
                    "🎉 พบข้อมูลคิวของคุณ!"
                )

                st.write(
                    f"🔗 ลิงก์: `{row['masked_link']}`"
                )

                # -------------------------------
                # สำเร็จ
                # -------------------------------
                if row["status"] == "สำเร็จ":

                    st.write(
                        "📊 สถานะ: "
                        "**✅ ทำสำเร็จเรียบร้อยแล้ว (29/29)**"
                    )

                    st.progress(1.0)


                # -------------------------------
                # กำลังทำ
                # -------------------------------
                elif row["status"] == "กำลังทำ":

                    done_count = min(
                        ticks * 10,
                        29
                    )

                    progress_pct = min(
                        done_count / 29,
                        1.0
                    )

                    st.write(
                        f"📊 สถานะ: "
                        f"**⏳ กำลังดำเนินการ "
                        f"({done_count}/29)**"
                    )

                    st.progress(
                        progress_pct
                    )


                # -------------------------------
                # รอคิว
                # -------------------------------
                else:

                    st.write(
                        "📊 สถานะ: "
                        "**🕒 รอทำคิวถัดไป (0/29)**"
                    )

                    st.progress(0.0)


        else:

            st.error(
                "❌ ไม่พบลิงก์นี้ในระบบ "
                "กรุณาตรวจสอบลิงก์ใหม่อีกครั้ง"
            )


    # =====================================================
    # FOOTER
    # =====================================================
    st.markdown(
        '<div class="footer-text">'
        '🔄 ระบบอัปเดตข้อมูลจาก Google Sheets ทุก 5 วินาที'
        '<br>'
        'Cookie Run Queue Tracker'
        '</div>',
        unsafe_allow_html=True
    )


except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheets: {e}"
    )
