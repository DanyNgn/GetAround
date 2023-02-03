import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

### Config
st.set_page_config(
    page_title="GetAround",
    page_icon="🚗 ",
    layout="wide"
  )

  ###  Set a title and presentation
st.title("GetAround 🚗 ")

st.markdown("""
    Rental car delay analysis
""")

st.markdown("""
    The dataset we used for this analysis :
""")

  ### Load data
DATA_URL = ('get_around_delay_analysis_copy.xlsx')

@st.cache 
def load_data():
    data = pd.read_excel(DATA_URL)
    return data

data = load_data()
st.write(data.head(10))

### Transform data

df_delay = data[['rental_id', 'car_id', 'checkin_type', 'state',
       'delay_at_checkout_in_minutes', 'previous_ended_rental_id',
       'time_delta_with_previous_rental_in_minutes']]

df_delay['is_delay'] = df_delay.delay_at_checkout_in_minutes.apply(lambda x : "Yes" if x>=0 else "no")

### Plot 1, show the delay
fig = px.pie(df_delay, 'is_delay', title="Percentage of delay")
st.plotly_chart(fig, use_container_width=True)

### Plot 2, show the state
fig2 = px.pie(df_delay, 'state', title="Percentage of state, ended or canceled")
st.plotly_chart(fig2, use_container_width=True)

### Plot 3, show the way to check in, by mobile or connect
fig3 = px.pie(df_delay, 'checkin_type', title="Percentage of checking by mobile or connect")
st.plotly_chart(fig3, use_container_width=True)

### Plot 4, show delay at checkout in minutes
fig4 = px.histogram(df_delay[df_delay['delay_at_checkout_in_minutes']>0],
                    x ='delay_at_checkout_in_minutes',
                    range_x = [0,720],
                    nbins=7200,
                    title = 'delay at checkout in minutes')
st.plotly_chart(fig4, use_container_width=True)

### Plot 5, show the delay by checkin type
fig5 = px.histogram(df_delay, x = 'checkin_type',
                    color = 'is_delay',
                    text_auto = '.0f',
                    barmode = 'group',
                    title = 'delay by checkin type')
st.plotly_chart(fig5, use_container_width=True)

### Plot final, estimated time for a car to become available
specs = np.repeat({'type':'domain'}, 5).tolist()
fig = make_subplots(rows=1, cols=5, specs=[specs])
for hours_cut in range(0,5):
    dataset_before = len( df_delay[df_delay['delay_at_checkout_in_minutes'] < (hours_cut*60)] )
    dataset_after = len( df_delay[df_delay['delay_at_checkout_in_minutes'] >= (hours_cut*60)] )
    fig.add_trace(go.Pie(labels=['Ready', 'Unvailable'], 
                         values=[dataset_before, dataset_after], 
                         name=f"{hours_cut} hour(s) between ck_in & check out"),
                         1, (hours_cut+1) 
                        )
fig.update_layout(
    title = 'Cars available between check in and check out after a delay of ...',
    annotations=[dict(text='Without', x=0.06, y=1.09, font_size=20, showarrow=False),
                 dict(text='After 1 hour', x=0.26, y=1.09, font_size=20, showarrow=False),
                 dict(text='After 2 hours', x=0.50, y=1.09, font_size=20, showarrow=False),
                 dict(text='After 3 hours', x=0.74, y=1.09, font_size=20, showarrow=False),
                 dict(text='After 4 hours', x=0.95, y=1.09, font_size=20, showarrow=False),
                ])
st.plotly_chart(fig, use_container_width=True)

### Conclusion
st.markdown("""
    To conclude, we can see that most of the delays, the checkins are done by mobile and that the vehicles are often available only 2 hours after the check out.
""")




