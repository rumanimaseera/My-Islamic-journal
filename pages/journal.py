# 🔄 Converted journal.py (Firebase) with updated calendar styling
import streamlit as st
import datetime
import calendar
import base64
from database import fetch_entries, fetch_entry_by_id
import pandas as pd
import altair as alt

# Background image setup
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

image_path = r"C:\Users\91887\Islamic_journal\photos\vintage2.jpg"
image_base64 = get_base64_of_image(image_path)

# PAGE CONFIG
st.set_page_config(page_title="Your Journal", layout="wide")
st.markdown(
    '<h1 style="text-align:center; font-size: 50px; color: #5a3820; font-family: Georgia, serif;">📖 Your Journal Entries</h1>',
    unsafe_allow_html=True
)

# AUTH CHECK
if "user" not in st.session_state:
    st.warning("⚠ Please log in to view your journal.")
    st.stop()

user_id = st.session_state["user"]

# MONTH & YEAR SELECTOR
today = datetime.date.today()
year_range = list(range(today.year, today.year - 5, -1))
month_names = list(calendar.month_name)[1:]
col_month, col_year = st.columns([2, 1])
selected_month = col_month.selectbox("📅 Select Month", month_names, index=today.month - 1)
selected_year = col_year.selectbox("🗓 Select Year", year_range)
month_num = list(calendar.month_name).index(selected_month)
start_date = datetime.date(selected_year, month_num, 1)
end_day = calendar.monthrange(selected_year, month_num)[1]
end_date = datetime.date(selected_year, month_num, end_day)

# FETCH ENTRIES
entries = []
for doc in fetch_entries(user_id, start_date, end_date):
    data = doc.to_dict()
    created = datetime.datetime.fromisoformat(data.get("created_at"))
    entries.append((doc.id, data.get("entry_text"), data.get("mood"), created))

# MOOD BAR CHART
def show_mood_bar(entries):
    if not entries:
        st.info("No journal entries found for this month.")
        return
    mood_counts = {}
    for entry in entries:
        mood_counts[entry[2]] = mood_counts.get(entry[2], 0) + 1
    mood_df = pd.DataFrame(list(mood_counts.items()), columns=["Mood", "Count"])
    base = alt.Chart(mood_df).encode(
        x=alt.X('Mood:N', sort='-y',
                axis=alt.Axis(labelFont="Georgia", labelFontSize=14, titleFontSize=16, titleFont="Georgia")),
        y=alt.Y('Count:Q',
                axis=alt.Axis(labelFont="Georgia", labelFontSize=14, titleFontSize=16, titleFont="Georgia")),
        tooltip=['Mood', 'Count']
    )
    bars = base.mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=50)
    text = base.mark_text(align='center', baseline='bottom', dy=-5, font='Georgia', fontSize=14).encode(text='Count:Q')
    chart = (bars + text).properties(
        width=600,
        height=400,
        title={"text": ["📊 Mood Distribution This Month"], "fontSize": 22, "font": "Georgia", "anchor": "middle"}
    )
    st.altair_chart(chart, use_container_width=True)

show_mood_bar(entries)

# CALENDAR DISPLAY with custom styling
def show_calendar(entries):
    st.subheader(f"🗓 Calendar - {selected_month} {selected_year}")
    num_days = calendar.monthrange(selected_year, month_num)[1]
    month_days = [datetime.date(selected_year, month_num, day) for day in range(1, num_days + 1)]
    entry_dates = {entry[3].date(): entry for entry in entries}
    html = (
        "<table><tr>"
        + "".join(f"<th>{wd}</th>" for wd in calendar.weekheader(3).split())
        + "</tr><tr>"
        + "<td></td>" * month_days[0].weekday()
    )
    for i, date in enumerate(month_days):
        if (i + month_days[0].weekday()) % 7 == 0 and i != 0:
            html += "</tr><tr>"
        if date in entry_dates:
            html += f"<td><a href='?entry_id={entry_dates[date][0]}'>📌<br>{date.day}</a></td>"
        else:
            html += f"<td>{date.day}</td>"
    html += "</tr></table>"
    st.markdown(html, unsafe_allow_html=True)

show_calendar(entries)

# DISPLAY ENTRY
def display_entry(entry_id):
    data = fetch_entry_by_id(entry_id)
    if data:
        created = datetime.datetime.fromisoformat(data.get("created_at"))
        st.subheader(f"📝 Journal Entry from {created.strftime('%d %b %Y')}")
        st.write(data.get("entry_text"))
        st.write(f"**Mood:** {data.get('mood')}")
        st.write(f"**Translation:** {data.get('translation')}")
        st.write(f"**Reference:** {data.get('reference')}")
        st.write(f"**Detected Mood from ML Model:** {data.get('mood_output')}")
    else:
        st.error("Entry not found or not authorized.")

entry_param = st.query_params.get("entry_id", [None])[0]
if entry_param:
    display_entry(entry_param)

# NAVIGATION BUTTONS
col1, col2 = st.columns([1,1])
if col1.button("➕ New Entry"):
    st.switch_page("app.py")
if col2.button("💬 Give Feedback"):
    st.switch_page("pages/feedback.py")

# ========================
# BACKGROUND IMAGE
# ========================
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

image_path = r"C:\Users\91887\VMJ_new\photos\vintage2.jpg"
image_base64 = get_base64_of_image(image_path)

if image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/webp;base64,{image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image could not be loaded.")

# ========================
# CUSTOM STYLING for Calendar and Buttons
# ========================
st.markdown("""
<style>
div.stButton > button {
    background-color: #5a3820;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 8px 20px;
    font-family: Georgia, serif;
    display: block;
    margin: 10px auto;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #a27555;
    color: #fff;
    cursor: pointer;
}
.stAlert {
    background-color: #eee0cb !important;
    border-left: 4px solid #795548;
    color: #3e2723 !important;
}
body {
    background-color: #f0e6d2;
}
.stButton>button {
    background-color: #5d4037;
    color: white;
    font-weight: bold;
}
div[data-baseweb="select"] > div {
    background-color: #8B4513 !important;  /* Brown dropdown */
    color: white !important;
}
div[data-baseweb="select"] > div > div {
    color: white !important;
}

/* Calendar CSS */
table {
    width: 100%;
    border-collapse: collapse;
    font-family: Georgia, serif;
    color: #3e2723;
}
th, td {
    border: 1px solid #3e2723;
    padding: 10px;
    text-align: center;
    background-color: #8B4513;  /* Brown background for cells */
}
th {
    background-color: #6A3F29;  /* Darker brown for headers */
    color: white;
}
td {
    background-color: #A56E41;  /* Lighter brown for the days */
}
td:hover {
    background-color: #5D2C1E;  /* Darken the box when hovered */
    cursor: pointer;
}
a {
    text-decoration: none;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
