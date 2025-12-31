import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config for Mobile
st.set_page_config(page_title="CFB/Madden Film Room", layout="wide")

st.title("🏈 Scheme Lab: Film Review")

# 1. Mock Data (This would be replaced by your OCR script output)
data = {
    'Formation': ['Gun Bunch', 'Gun Bunch', 'Trip Left', 'I-Form Pro', 'Gun Bunch'],
    'Play Name': ['Verticals', 'HB Base', 'Crossers', 'Stretch', 'Verticals'],
    'Down': [1, 2, 3, 1, 3],
    'Distance': [10, 6, 4, 10, 8],
    'Yards Gained': [12, 2, 5, -1, 15],
    'Twitch_Link': ['https://twitch.tv/videos/123?t=0h10m05s', 'https://twitch.tv/videos/123?t=0h12m10s', 
                    'https://twitch.tv/videos/123?t=0h15m30s', 'https://twitch.tv/videos/123?t=0h18m45s', 
                    'https://twitch.tv/videos/123?t=0h22m00s']
}
df = pd.DataFrame(data)

# 2. Success Logic Formula
def check_success(row):
    if row['Down'] == 1: return row['Yards Gained'] >= (row['Distance'] * 0.5)
    if row['Down'] == 2: return row['Yards Gained'] >= (row['Distance'] * 0.7)
    return row['Yards Gained'] >= row['Distance']

df['Success'] = df.apply(check_success, axis=1)

# 3. Mobile-Friendly Metrics
col1, col2 = st.columns(2)
success_rate = (df['Success'].sum() / len(df)) * 100
col1.metric("Overall Success Rate", f"{success_rate:.1f}%")
col2.metric("Avg Yards/Play", f"{df['Yards Gained'].mean():.1f}")

# 4. Scheme Analysis (Charts)
st.subheader("Scheme Efficiency by Formation")
fig = px.bar(df.groupby('Formation')['Success'].mean().reset_index(), 
             x='Formation', y='Success', color='Formation',
             labels={'Success': 'Success %'}, height=300)
st.plotly_chart(fig, use_container_width=True)

# 5. The "Film Table"
st.subheader("Play-by-Play Review")
# Filter by formation on mobile
selected_form = st.selectbox("Filter by Formation", options=['All'] + list(df['Formation'].unique()))
filtered_df = df if selected_form == 'All' else df[df['Formation'] == selected_form]

# Displaying the data
for index, row in filtered_df.iterrows():
    with st.expander(f"{row['Formation']} - {row['Play Name']} ({'✅' if row['Success'] else '❌'})"):
        st.write(f"**Situation:** {row['Down']} & {row['Distance']}")
        st.write(f"**Gain:** {row['Yards Gained']} yards")
        st.link_button("Watch Clip", row['Twitch_Link'])

