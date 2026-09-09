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

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {
        background: #0f1117;
        color: #f1f5f9 !important;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 30px;
        padding-bottom: 50px;
    }

    /* ตัวหนังสือทั่วไป */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span,
    .stText,
    label,
    p {
        color: #f1f5f9 !important;
    }

    /* Caption */
    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #9ca3af !important;
    }

    /* =====================================================
       ซ่อน Streamlit UI
    ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .big-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 5px;
    }

    .small-title {
        text-align: center;
        color: #aeb7c5 !important;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .notice-box {
        text-align: center;

        color: #e5e7eb !important;

        background: #191c25;

        border: 1px solid #303644;

        border-radius: 30px;

        padding: 10px 20px;

        margin: 0 auto 30px auto;

        max-width: 750px;

        font-size: 13px;
    }


    /* =====================================================
       SECTION TITLE
    ===================================================== */

    .section-title {
        font-size: 21px;
        font-weight: 750;

        color: #ffffff !important;

        margin-top: 28px;
        margin-bottom: 12px;
    }


    /* =====================================================
       METRIC CARD
    ===================================================== */

    div[data-testid="stMetric"] {

        background: #181b24 !important;

        border: 1px solid #2b303c !important;

        border-radius: 18px;

        padding: 18px;

        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    div[data-testid="stMetricLabel"] {
        color: #aeb7c5 !important;
    }

    div[data-testid="stMetricLabel"] * {
        color: #aeb7c5 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    div[data-testid="stMetricValue"] * {
        color: #ffffff !important;
    }


    /* =====================================================
       CONTAINER CARD
    ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background: #181b24 !important;

        border: 1px solid #2b303c !important;

        border-radius: 18px !important;

        padding: 5px;
    }


    /* =====================================================
       TEXT INPUT
    ===================================================== */

    div[data-baseweb="input"] {

        background: #181b24 !important;

        border: 1px solid #343a48 !important;

        border-radius: 12px !important;
    }

    div[data-baseweb="input"] input {

        color: #ffffff !important;

        background: transparent !important;

        caret-color: #ffffff !important;
    }

    div[data-baseweb="input"] input::placeholder {

        color: #7f8998 !important;

        opacity: 1 !important;
    }


    /* =====================================================
       ALERT / INFO / WARNING / SUCCESS
    ===================================================== */

    [data-testid="stAlert"] {

        color: #ffffff !important;

        border-radius: 12px;
    }

    [data-testid="stAlert"] p {

        color: #ffffff !important;
    }

    [data-testid="stAlert"] span {

        color: #ffffff !important;
    }


    /* =====================================================
       PROGRESS BAR
    ===================================================== */

    div[data-testid="stProgress"] {

        margin-top: 8px;
        margin-bottom: 5px;
    }

    div[data-testid="stProgress"] > div {

        background-color: #292e39 !important;

        border-radius: 20px;
    }

    div[data-testid="stProgress"] > div > div {

        background-color: #ff4b4b !important;

        border-radius: 20px;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .footer-text {

        text-align: center;

        color: #737c8c !important;

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
    '<div class="big-title">'
    '🎮 ดูสถานะคิวเชิญเพื่อน Cookie Run'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="small-title">'
    'ระบบตรวจสอบสถานะคิวออนไลน์'
    '</div>',
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
# LOAD DATA
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

            # มี ⏳ = กำลังทำ
            if "⏳" in val:
                has_waiting = True

            # มี ✅ หรือ TRUE = สำเร็จ
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

        # ถ้ามี ⏳ = กำลังทำ
        if row["has_waiting"]:
            return "กำลังทำ"

        # ครบ 3 ช่อง = สำเร็จ
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
# MAIN
# =========================================================

try:

    df, col_link = load_data()

    # ลิงก์สำหรับแสดง
    df["masked_link"] = df[col_link].apply(mask_url)

    # แยกคิว
    in_progress_df = df[
        df["status"] == "กำลังทำ"
    ]

    waiting_df = df[
        df["status"] == "รอคิว"
    ]


    # =====================================================
    # ภาพรวมคิว
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📊 ภาพรวมคิว'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "⚡ กำลังทำ",
            len(in_progress_df)
        )

    with col2:

        st.metric(
            "⌛ รอคิว",
            len(waiting_df)
        )


    # =====================================================
    # คิวที่กำลังทำ
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '⚡ คิวที่กำลังทำอยู่ขณะนี้'
        '</div>',
        unsafe_allow_html=True
    )

    if not in_progress_df.empty:

        for idx, row in in_progress_df.iterrows():

            ticks = int(row["tick_count"])

            # จำนวนที่ทำไป
            done_count = min(
                ticks * 10,
                29
            )

            # เปอร์เซ็นต์
            progress_pct = min(
                int((done_count / 29) * 100),
                100
            )

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(
                        f"🔗 **ลิงก์:** "
                        f"`{row['masked_link']}`"
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
                        f"**{done_count} / 29**"
                    )

    else:

        st.info(
            "💡 ขณะนี้ยังไม่มีคิวที่กำลังทำอยู่"
        )


    # =====================================================
    # คิวที่รอถัดไป
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '⌛ คิวที่รอถัดไป'
        '</div>',
        unsafe_allow_html=True
    )

    next_queues = waiting_df.head(5)

    if not next_queues.empty:

        for idx, row in next_queues.iterrows():

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    st.markdown(
                        f"🔗 **ลิงก์:** "
                        f"`{row['masked_link']}`"
                    )

                with right:

                    st.warning(
                        "🕒 รอทำคิวถัดไป"
                    )

    else:

        st.info(
            "🎉 ไม่มีคิวรอทำในระบบ"
        )

    # =====================================================
# คิวที่ทำสำเร็จล่าสุด
# =====================================================

st.markdown(
    '<div class="section-title">'
    '✅ คิวที่ทำสำเร็จเรียบร้อยแล้ว ล่าสุด'
    '</div>',
    unsafe_allow_html=True
)

# ดึงเฉพาะคิวที่สำเร็จ
completed_df = df[
    df["status"] == "สำเร็จ"
]

if not completed_df.empty:

    # แสดง 10 คิวล่าสุด
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
                    f"✅ **ลิงก์:** "
                    f"`{row['masked_link']}`"
                )

            with right:

                st.success("29/29")

else:

    st.info(
        "ยังไม่มีคิวที่ทำสำเร็จ"
    )
    

    # =====================================================
    # ค้นหาคิวของตัวเอง
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

                # =========================================
                # สำเร็จ
                # =========================================

                if row["status"] == "สำเร็จ":

                    st.write(
                        "📊 สถานะ: "
                        "**✅ ทำสำเร็จเรียบร้อยแล้ว (29/29)**"
                    )

                    st.progress(1.0)


                # =========================================
                # กำลังทำ
                # =========================================

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


                # =========================================
                # รอคิว
                # =========================================

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
