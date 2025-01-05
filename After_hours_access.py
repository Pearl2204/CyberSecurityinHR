import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app title
st.title("After-Hours Access Detection")

# Upload CSV file
uploaded_file = st.file_uploader("Upload Login Data (CSV)", type="csv")

if uploaded_file:
    # Load data
    login_data = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
    st.write("### Uploaded Data", login_data.head())

    # Define working hours and weekends
    WORK_HOURS_START = 9  # 9 AM
    WORK_HOURS_END = 18   # 6 PM
    WEEKENDS = [5, 6]     # Saturday=5, Sunday=6

    # Add columns for analysis
    login_data['Hour'] = login_data['Timestamp'].dt.hour
    login_data['DayOfWeek'] = login_data['Timestamp'].dt.dayofweek  # Monday=0, Sunday=6

    # Filter logins outside working hours
    after_hours_logins = login_data[(login_data['Hour'] < WORK_HOURS_START) | 
                                    (login_data['Hour'] > WORK_HOURS_END) |
                                    (login_data['DayOfWeek'].isin(WEEKENDS))]

    # Display flagged logins
    st.write("### Flagged After-Hours Logins", after_hours_logins)

    # Save the flagged data for download
    flagged_csv = after_hours_logins.to_csv(index=False).encode('utf-8')
    st.download_button("Download Flagged Logins CSV", data=flagged_csv, file_name="after_hours_logins.csv")

    # Visualization: After-Hours Logins by Day of the Week
    st.write("### Visualization: After-Hours Logins by Day of the Week")
    after_hours_counts = after_hours_logins['DayOfWeek'].value_counts()
    fig, ax = plt.subplots()
    after_hours_counts.sort_index().plot(kind='bar', ax=ax)
    ax.set_title("After-Hours Logins by Day of the Week")
    ax.set_xlabel("Day of the Week (0=Monday, 6=Sunday)")
    ax.set_ylabel("Number of Logins")
    st.pyplot(fig)
else:
    st.write("Please upload a CSV file to proceed.")
