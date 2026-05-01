import streamlit as st
import pydeck as pdk
import random
import time
from database import emergency_col


# -------- ONE TAP EMERGENCY --------
def trigger_emergency():

    st.subheader("🚨 One Tap Emergency")

    if st.button("🚑 CALL AMBULANCE", use_container_width=True):

        amb_id = f"AMB-{random.randint(100,999)}"

        emergency_col.insert_one({
            "user": st.session_state.user,
            "ambulance": amb_id,
            "status": "en route",
            "eta": random.randint(5,15)
        })

        st.success(f"Ambulance {amb_id} dispatched!")


# -------- GOOGLE MAP TRACKING --------
def live_tracking():

    st.subheader("📍 Live Ambulance Tracking")

    route = [
        [17.4948, 78.3996],
        [17.4900, 78.3950],
        [17.4850, 78.3850],
        [17.4700, 78.3900],
        [17.4530, 78.3910],
    ]

    placeholder = st.empty()

    if st.button("Start Tracking"):

        for point in route:

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=[{"position": point}],
                get_position="position",
                get_radius=200,
                get_color=[255, 0, 0]
            )

            view = pdk.ViewState(
                latitude=point[0],
                longitude=point[1],
                zoom=14
            )

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view,
                map_provider="google_maps",
                api_keys={"google_maps": st.secrets["google_maps_key"]}
            )

            with placeholder.container():
                st.pydeck_chart(deck)

            time.sleep(1)