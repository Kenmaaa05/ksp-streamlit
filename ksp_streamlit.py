import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Setup ---
st.set_page_config(page_title="Kerbnik-1 Mission Analysis", layout="wide")
st.title("🚀 Kerbnik-1 Mission Telemetry Analysis")
st.markdown("A replica of Sputnik-1 in Kerbal Space Program.")

# --- Load Data ---
df = pd.read_csv("https://raw.githubusercontent.com/Kenmaaa05/ksp-streamlit/main/kerbnik_1_telemetry.csv")
df.columns = df.columns.str.strip()

# --- Calculations ---
total_time = df["Time"].iloc[-1] - df["Time"].iloc[0]

battery_start = df["Battery (%)"].iloc[0]
battery_min = df["Battery (%)"].min()
battery_end_time = df.loc[df["Battery (%)"].idxmin(), "Time"]
battery_drain_rate = (battery_start - battery_min) / total_time

peak_velocity = df["Orbital Velocity (m/s)"].max()
velocity_time = df.loc[df["Orbital Velocity (m/s)"].idxmax(), "Time"]

max_altitude = df["Altitude (m)"].max()
altitude_time = df.loc[df["Altitude (m)"].idxmax(), "Time"]

apoapsis_range = df["Apoapsis (m)"].max() - df["Apoapsis (m)"].min()
periapsis_range = df["Periapsis (m)"].max() - df["Periapsis (m)"].min()
apoapsis_std = df["Apoapsis (m)"].std()
periapsis_std = df["Periapsis (m)"].std()

max_inside_temp = df["Inside Temp (K)"].max()
max_outside_temp = df["Outside Temp (K)"].max()

temp_drop_inside = df["Inside Temp (K)"].iloc[0] - df["Inside Temp (K)"].iloc[-1]
temp_drop_outside = df["Outside Temp (K)"].iloc[0] - df["Outside Temp (K)"].iloc[-1]
rate_inside = temp_drop_inside / total_time
rate_outside = temp_drop_outside / total_time

inclination_start = df["Inclination (deg)"].iloc[0]
inclination_end = df["Inclination (deg)"].iloc[-1]
inclination_change = inclination_end - inclination_start
inclination_std = df["Inclination (deg)"].std()

# --- Metrics ---
st.subheader("📊 Mission Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Battery Start (%)", f"{battery_start}")
col2.metric("Battery End (%)", f"{battery_min}")
col3.metric("Battery Death Time (s)", f"{battery_end_time}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Battery Drain Rate", f"{battery_drain_rate:.4f} %/s")
col5.metric("Max Velocity", f"{peak_velocity} m/s", f"at {velocity_time}s")
col6.metric("Max Altitude", f"{max_altitude} m", f"at {altitude_time}s")

col7, col8, col9 = st.columns(3)
col7.metric("Apoapsis Std Dev", f"{apoapsis_std:,.0f} m")
col8.metric("Periapsis Std Dev", f"{periapsis_std:,.0f} m")
col9.metric("Inclination Drift", f"{inclination_change:.2f}°", f"±{inclination_std:.2f}°")

# --- Temperature ---
st.subheader("Temperature")
st.markdown(f"""
- Max inside temp: **{max_inside_temp} K**  
- Max outside temp: **{max_outside_temp} K**  
- Inside dropped **{temp_drop_inside:.1f} K** over {total_time}s (~{rate_inside:.4f} K/s)  
- Outside dropped **{temp_drop_outside:.1f} K** over {total_time}s (~{rate_outside:.4f} K/s)
""")

# --- Verdict ---
st.subheader("Final Verdict")
if peak_velocity < 3000 and battery_min < battery_start:
    st.error("❌ Orbit not achieved before battery died.")
elif apoapsis_std > 100000:
    st.warning("⚠️ Orbit likely unstable due to apoapsis variance.")
else:
    st.success("✅ Orbit likely achieved.")

# --- Visualization ---
st.subheader("📈 Telemetry Over Time (All Metrics)")
def plot_all_metrics(df):
    fig, axs = plt.subplots(3, 3, figsize=(20, 15))

    axs[0][0].plot(df["Time"], df["Battery (%)"], color='green')
    axs[0][0].set_title("Battery Level over Time")
    axs[0][0].set_xlabel("Time (s)")
    axs[0][0].set_ylabel("Battery (%)")
    axs[0][0].grid(True)

    axs[0][1].plot(df['Time'], df['Altitude (m)'], color='blue')
    axs[0][1].set_title('Altitude over Time')
    axs[0][1].set_ylabel('Altitude (m)')
    axs[0][1].set_xlabel('Time (s)')
    axs[0][1].grid(True)

    axs[0][2].plot(df["Time"], df["Inclination (deg)"], color='red')
    axs[0][2].set_title("Inclination over Time")
    axs[0][2].set_xlabel("Time (s)")
    axs[0][2].set_ylabel("Inclination (deg)")
    axs[0][2].grid(True)

    axs[1][0].plot(df["Time"], df["Inside Temp (K)"], color='magenta')
    axs[1][0].set_title("Inside Temp over Time")
    axs[1][0].set_xlabel("Time (s)")
    axs[1][0].set_ylabel("Inside Temp (K)")
    axs[1][0].grid(True)

    axs[1][1].plot(df["Time"], df["Outside Temp (K)"], color='black')
    axs[1][1].set_title("Outside Temp over Time")
    axs[1][1].set_xlabel("Time (s)")
    axs[1][1].set_ylabel("Outside Temp (K)")
    axs[1][1].grid(True)

    axs[1][2].plot(df["Time"], df["Orbital Velocity (m/s)"], color='purple')
    axs[1][2].set_title("Orbital Velocity over Time")
    axs[1][2].set_xlabel("Time (s)")
    axs[1][2].set_ylabel("Velocity (m/s)")
    axs[1][2].grid(True)

    axs[2][0].plot(df["Time"], df["Apoapsis (m)"], color='pink')
    axs[2][0].set_title("Apoapsis over Time")
    axs[2][0].set_xlabel("Time (s)")
    axs[2][0].set_ylabel("Apoapsis (m)")
    axs[2][0].grid(True)

    axs[2][1].plot(df["Time"], df["Periapsis (m)"], color='orange')
    axs[2][1].set_title("Periapsis over Time")
    axs[2][1].set_xlabel("Time (s)")
    axs[2][1].set_ylabel("Periapsis (m)")
    axs[2][1].grid(True)

    axs[2][2].axis("off")

    plt.tight_layout()
    return fig

fig = plot_all_metrics(df)
# st.subheader("📈 Telemetry Metrics by Tab")


tabs = st.tabs([
    "Battery", "Altitude", "Inclination", "Inside Temp",
    "Outside Temp", "Velocity", "Apoapsis", "Periapsis"
])
metrics = [
    "Battery (%)", "Altitude (m)", "Inclination (deg)", "Inside Temp (K)",
    "Outside Temp (K)", "Orbital Velocity (m/s)", "Apoapsis (m)", "Periapsis (m)"
]

for tab, metric in zip(tabs, metrics):
    with tab:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Time"], df[metric])
        ax.set_title(f"{metric} over Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(metric)
        ax.grid(True)
        st.pyplot(fig)


# --- Optional: Raw Data ---
with st.expander("📄 View Raw Data"):
    st.dataframe(df)
