📊 Automated Return Dashboard
A real-time Streamlit web application designed to track, filter, and visualize product return data directly from a Google Sheets backend. This tool helps inventory managers identify pending items and monitor return statuses without manual spreadsheet filtering.

✨ Features
Live Google Sheets Sync: Fetches data via CSV export, acting as a lightweight, cloud-based database.

Automatic Data Cleaning: * Fuzzy matching for columns (handles typos like "resspective godown").

Robust date parsing and error handling for missing values.

Pending Item Focus: Automatically filters out any items already moved to the godown, keeping the view focused on actionable tasks.

Key Performance Metrics: Instant count of statuses including Closed, Re-inspection, Waiting on Customer, Unit with Brand, and Reference ID issues.

Interactive Sidebar: Filter "Closed" items by custom date ranges to track performance over specific periods.

Manual Refresh: Includes a one-click button to clear the 60-second cache and pull the absolute latest data.
