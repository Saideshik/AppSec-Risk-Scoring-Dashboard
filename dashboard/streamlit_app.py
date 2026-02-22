import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text

DB = os.environ["DATABASE_URL"]

st.set_page_config(page_title="AppSec Risk Scoring Dashboard", layout="wide")
st.title("AppSec Risk Scoring Dashboard")

engine = create_engine(DB, pool_pre_ping=True)

@st.cache_data(ttl=30)
def load_latest_scores():
    q = '''
    WITH latest AS (
      SELECT DISTINCT ON (application_id)
        application_id, score, label, calculated_at,
        open_critical, open_high, open_medium, open_low, mttr_days
      FROM risk_scores
      ORDER BY application_id, calculated_at DESC
    )
    SELECT a.name, a.owner, a.internet_exposed, a.data_sensitivity,
           l.*
    FROM latest l
    JOIN applications a ON a.id = l.application_id
    ORDER BY l.score DESC;
    '''
    with engine.connect() as c:
        return pd.read_sql(text(q), c)

@st.cache_data(ttl=30)
def load_score_trend(app_id: int):
    q = '''
    SELECT calculated_at, score
    FROM risk_scores
    WHERE application_id = :app_id
    ORDER BY calculated_at ASC;
    '''
    with engine.connect() as c:
        return pd.read_sql(text(q), c, params={"app_id": app_id})

@st.cache_data(ttl=30)
def load_apps():
    with engine.connect() as c:
        return pd.read_sql(text("SELECT id, name FROM applications ORDER BY name"), c)

df = load_latest_scores()

if df.empty:
    st.warning("No data yet. Seed findings or POST to /findings, then call /metrics/recalc.")
    st.stop()

st.subheader("Executive View")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Apps Tracked", int(df["application_id"].nunique()))
col2.metric("High/Critical Apps", int((df["score"] >= 70).sum()))
col3.metric("Open Critical Findings (Total)", int(df["open_critical"].sum()))
col4.metric("Average Risk", int(round(df["score"].mean())))

show = df[["name", "owner", "score", "label", "open_critical", "open_high", "internet_exposed", "data_sensitivity", "mttr_days"]]
st.dataframe(show, use_container_width=True, hide_index=True)

st.subheader("Engineering Drilldown")
apps = load_apps()
name_to_id = dict(zip(apps["name"], apps["id"]))
selected = st.selectbox("Select an application", list(name_to_id.keys()))
app_id = int(name_to_id[selected])

trend = load_score_trend(app_id)
if not trend.empty:
    fig = px.line(trend, x="calculated_at", y="score", title=f"Risk Trend: {selected}")
    st.plotly_chart(fig, use_container_width=True)

q_find = '''
SELECT f.tool_source, f.tool_name, f.title, f.severity, f.cvss, f.exploit_available,
       f.internet_exposed, f.status, f.detected_at, f.fixed_at
FROM findings f
WHERE f.application_id = :app_id
ORDER BY
  CASE f.severity
    WHEN 'critical' THEN 1
    WHEN 'high' THEN 2
    WHEN 'medium' THEN 3
    WHEN 'low' THEN 4
    ELSE 5
  END,
  f.detected_at DESC;
'''
with engine.connect() as c:
    fdf = pd.read_sql(text(q_find), c, params={"app_id": app_id})
st.dataframe(fdf, use_container_width=True, hide_index=True)
