📊 RWP Dashboard — Amazon (Dash)

An interactive Remote Work Productivity (RWP) dashboard built with Dash, Plotly, and dash-bootstrap-components to explore employee productivity, satisfaction, performance, and well-being.

✨ Highlights

Interactive Dash app with Bootstrap styling

Filters: Department & Year

KPI cards: Total Employees, Avg Satisfaction, Avg Email Response, Avg Project Completion Time

Charts: Work Hours & Productivity, Communication, Environmental Heatmap, Work Tools Usage, Engagement & Well-being

🗂️ Repository Structure
RWP-Dashboard-Amazon/
├─ Dashboard_Amazon_RWP.py               # Dash app (main entry point)
├─ BD_prepared_visualization_data.xlsx   # (Optional local copy) consolidated dataset
├─ Employee Productivity and Satisfaction HR Data.csv
├─ Employee Well-being Data.csv
├─ Employee’s Performance for HR Analytics.csv
├─ Productivity and Satisfaction Data.csv
├─ Remote Work Survey Data.csv
└─ BEMM461_Notebook-Main file.ipynb      # EDA / prototype (Dash + Plotly)


The app by default loads the main Excel from a raw GitHub URL (see FILE_PATH in the code). You can switch to the local .xlsx file if you prefer offline use (see “Data Path” below).

⚙️ Quickstart
1) Clone
git clone https://github.com/JeeDutta08/RWP-Dashboard-Amazon.git
cd RWP-Dashboard-Amazon

2) (Recommended) Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

3) Install dependencies

If you have requirements.txt, use it. Otherwise:

pip install dash dash-bootstrap-components pandas plotly openpyxl

4) Run the app
python Dashboard_Amazon_RWP.py


Open the URL shown in terminal (usually http://127.0.0.1:8050/).

🔗 Data Path (Important)

The app uses:

FILE_PATH = "https://raw.githubusercontent.com/Balajee-Dutta/Analytics-and-Viz-BEMM461-/main/BD_prepared_visualization_data.xlsx"


To use the local file instead, place BD_prepared_visualization_data.xlsx in the repo root and change:

FILE_PATH = "BD_prepared_visualization_data.xlsx"

📑 Expected Data Schema
Sheet: Employee_Productivity

Year (int/str)

Department (str)

Satisfaction_Score (numeric)

Project_Completion_Times (numeric)

Task_Duration (numeric)

Burnout_Indicator (numeric)

Sheet: Productivity_Satisfaction

Year (int/str)

Department (str)

Email_Response_Rate (numeric, %)

Internet_Stability (numeric)

Workspace_Setup (numeric)

Work_Tool_Hours (numeric)

Downtime (numeric)

If these columns or sheet names differ, you’ll see KeyError or empty charts. Align column names to match the above or adjust the code accordingly.

📊 What You’ll See

KPI Cards: Total Employees, Avg Satisfaction, Avg Email Response, Avg Project Completion Time

Work Hours & Productivity (Line): Task_Duration vs Project_Completion_Times

Communication (Bar): Email_Response_Rate by Department

Environmental Context (Heatmap): Internet_Stability & Workspace_Setup averages by Department

Work Tools Usage (Line): Work_Tool_Hours & Downtime

Engagement & Well-being (Scatter): Satisfaction_Score vs Burnout_Indicator colored by Department

🧱 Tech Stack

Dash (layout, callbacks)

dash-bootstrap-components (styling/layout, Bootstrap theme)

Plotly Express (charts)

Pandas (data handling)

openpyxl (read .xlsx)

🛠️ Troubleshooting

KeyError: <column> → Ensure your Excel sheets/columns match the schema above.

.xlsx read error → Install openpyxl (pip install openpyxl).

No charts / empty figures → Your filter selection may exclude all rows; clear filters or check data types.


🤝 Contributing

PRs welcome! For major changes, open an issue to discuss the proposal.

📜 License

MIT (or your preferred license). Add a LICENSE file and reference it here.
