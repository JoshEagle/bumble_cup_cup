# import streamlit as st
# import pandas as pd

# st.title("Bumble Cup Cup 2024")

# data = pd.DataFrame(columns=['event','team','result'])

# event_list = ['Hungry Humans', 'Beer Pong', 'Speed Stacking']

# event = st.selectbox("Event?", event_list)
# team = st.selectbox("Team?", ('team1','team2'))
# result = st.selectbox("Result?", ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'))

# df_row = [event,team,result]

# with st.expander("Developer Use"):
#     event_list
#     event
#     team
    


# dat

import streamlit as st
import pandas as pd

# List of teams and number of events
teams = ['Team A', 'Team B', 'Team C', 'Team D', 'Team E', 'Team F', 'Team G', 'Team H']
num_events = 8

# Points assigned to each position (1st to 8th place)
points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}

# Columns for the standings table
columns = ['Team'] + [f'Event {i+1} Points' for i in range(num_events)] + ['Total Points']

# Initialize standings table
def initialize_standings():
    # Create a DataFrame where each team starts with 0 points for each event
    data = {col: [0] * len(teams) for col in columns}
    data['Team'] = teams
    return pd.DataFrame(data)

# Function to update standings based on event rankings
def update_standings(standings, event_num, event_ranking):
    # Reset the points for the selected event (event_num)
    for i, team in enumerate(teams):
        position = event_ranking.index(i + 1) + 1  # 1-based index: rank corresponds to position
        points_awarded = points[position]
        standings.loc[standings['Team'] == team, f'Event {event_num} Points'] = points_awarded
    
    # Recalculate Total Points by summing the points for each event column (Event 1, Event 2, ..., Event 8)
    standings['Total Points'] = standings.iloc[:, 1:num_events+1].sum(axis=1)
    return standings

# Streamlit UI
st.title('Live Event Standings Tracker')

# Initialize standings if not already in session state
if 'standings' not in st.session_state:
    st.session_state.standings = initialize_standings()

# Dropdown to select which event is being submitted
event_num = st.selectbox('Select Event', range(1, num_events + 1))

# Input for event rankings (1st to 8th place) for the selected event
st.subheader(f'Enter Rankings for Event {event_num}')

event_ranking = []
for i in range(8):
    rank = st.selectbox(f'Rank for {teams[i]}', range(1, 9), key=f'event_{event_num}_team_{i}')
    event_ranking.append(rank)

# Button to submit event results
if st.button(f'Submit Event {event_num} Results'):
    # Update standings based on event rankings
    st.session_state.standings = update_standings(st.session_state.standings, event_num, event_ranking)
    st.success(f'Event {event_num} results updated successfully!')

# Display live standings
st.subheader('Live Standings')

# Sort standings by total points (descending order)
standings_sorted = st.session_state.standings.sort_values(by='Total Points', ascending=False).reset_index(drop=True)

# Display the standings table
st.dataframe(standings_sorted)


