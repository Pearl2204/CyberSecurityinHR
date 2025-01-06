import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Interactive HR Cybersecurity Risk Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload Data File (CSV)", type=["csv"])

if uploaded_file:
    # Allow user to select the type of data uploaded
    data_type = st.radio(
        "Select the data type:",
        ("Login Data", "File Access Data", "Communication Data")
    )

    if data_type == "Login Data":
        # Load login data
        login_data = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
        st.write("### Uploaded Login Data", login_data.head())

        # After-Hours Access Detection
        st.subheader("1. After-Hours Access Detection")
        WORK_HOURS_START = 9  # 9 AM
        WORK_HOURS_END = 18   # 6 PM
        WEEKENDS = [5, 6]     # Saturday=5, Sunday=6

        # Add columns for analysis
        login_data['Hour'] = login_data['Timestamp'].dt.hour
        login_data['DayOfWeek'] = login_data['Timestamp'].dt.dayofweek  # Monday=0, Sunday=6

        # Filter logins outside working hours
        flagged_logins = login_data[
            (login_data['Hour'] < WORK_HOURS_START) |
            (login_data['Hour'] > WORK_HOURS_END) |
            (login_data['DayOfWeek'].isin(WEEKENDS))
        ]

        if not flagged_logins.empty:
            flagged_counts = flagged_logins["UserID"].value_counts().reset_index()
            flagged_counts.columns = ["UserID", "Flagged Logins"]
            #st.write("### Flagged Users and Counts", flagged_counts.head(7))  # Show top 7 rows
            st.write("Scroll for more details ⬇")
            st.dataframe(flagged_counts, height=200)  # Enable scrolling

            # Visualization: After-Hours Logins
            fig, ax = plt.subplots()
            day_counts = flagged_logins["DayOfWeek"].value_counts().sort_index()
            day_counts.plot(kind="bar", ax=ax, color="orange")
            ax.set_title("After-Hours Logins by Day of the Week")
            ax.set_xlabel("Day of the Week (0=Monday, 6=Sunday)")
            ax.set_ylabel("Number of Logins")

            # Add numbers on top of bars
            for i, bar in enumerate(ax.patches):
                value = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    value + 0.5,
                    f"{int(value)}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

            st.pyplot(fig)
        else:
            st.write("No after-hours logins detected.")

    elif data_type == "File Access Data":
        # Load file access data
        file_access_data = pd.read_csv(uploaded_file, parse_dates=["AccessTime"])
        st.write("### Uploaded File Access Data", file_access_data.head())

        # Quiet Quitting Detection (Flagging Users Exceeding Threshold)
        st.subheader("2. Quiet Quitting Detection")
        THRESHOLD = 100  # Example threshold (in MB)
        cumulative_downloads = file_access_data.groupby("UserID")["FileSize(MB)"].sum().reset_index()
        flagged_users = cumulative_downloads[cumulative_downloads["FileSize(MB)"] > THRESHOLD]

        if not flagged_users.empty:
           # st.write("### Flagged Users (Above Threshold)", flagged_users.head(7))  # Show top 7 rows
            st.write("Scroll for more details ⬇")
            st.dataframe(flagged_users, height=200)  # Enable scrolling

            # Visualization: Cumulative Downloads for Flagged Users
            fig, ax = plt.subplots()
            flagged_users.plot(kind="bar", x="UserID", y="FileSize(MB)", ax=ax, color="red", legend=False)
            ax.set_title("Cumulative Downloads by Flagged Users")
            ax.set_ylabel("File Size (MB)")

            # Add numbers on top of bars
            for i, bar in enumerate(ax.patches):
                value = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    value + 1,
                    f"{value:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

            st.pyplot(fig)
        else:
            st.write("No users exceeded the download threshold.")

    elif data_type == "Communication Data":
        # Load communication data
        communication_data = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
        st.write("### Uploaded Communication Data", communication_data.head())

        # Internal Social Engineering Detection (Flagged Users and Counts)
        st.subheader("3. Internal Social Engineering Detection")
        suspicious_phrases = ["urgent", "send immediately", "approve quickly", "client list"]
        communication_data["Flagged"] = communication_data["Content"].apply(
            lambda x: any(phrase in x.lower() for phrase in suspicious_phrases)
        )
        flagged_messages = communication_data[communication_data["Flagged"]]

        if not flagged_messages.empty:
            flagged_counts = flagged_messages["Sender"].value_counts().reset_index()
            flagged_counts.columns = ["Sender", "Flagged Messages"]
            #st.write("### Flagged Senders and Counts", flagged_counts.head(7))  # Show top 7 rows
            st.write("Scroll for more details ⬇")
            st.dataframe(flagged_counts, height=200)  # Enable scrolling

            # Visualization: Number of Suspicious Messages per Sender
            fig, ax = plt.subplots()
            flagged_counts.plot(kind="bar", x="Sender", y="Flagged Messages", ax=ax, color="red")
            ax.set_title("Suspicious Messages by Sender")
            ax.set_xlabel("Sender")
            ax.set_ylabel("Number of Messages")

            # Add numbers on top of bars
            for i, bar in enumerate(ax.patches):
                value = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    value + 0.5,
                    f"{int(value)}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

            st.pyplot(fig)

            # Show detailed flagged messages (optional)
            st.write("### Detailed Flagged Messages", flagged_messages[["Sender", "Content"]])
        else:
            st.write("No suspicious messages detected.")
else:
    st.write("Please upload a data file to proceed.")
