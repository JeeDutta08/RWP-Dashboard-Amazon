# ====================== IMPORTING LIBRARIES ======================
import dash  # Core Dash library for building web applications
from dash import dcc, html, Input, Output  # Dash components and callback decorators
import dash_bootstrap_components as dbc  # Bootstrap components for styling and layout
import pandas as pd  
import plotly.express as px  # Plotly for interactive charts

# ====================== DATA LOADING ======================
FILE_PATH = r"C:\Users\Jeedu\OneDrive\Desktop\Analytics and Visualisation Data set\BD_prepared_visualization_data.xlsx"  # Path to the Excel file

employee_productivity = pd.read_excel(FILE_PATH, sheet_name='Employee_Productivity')  # Reads data from the "Employee_Productivity" sheet
productivity_satisfaction = pd.read_excel(FILE_PATH, sheet_name='Productivity_Satisfaction')  # Reads data from the "Productivity_Satisfaction" sheet

DEPARTMENTS = sorted(productivity_satisfaction['Department'].dropna().unique())  # Gets sorted unique departments

# ====================== NEW CODE: ADDING YEAR FILTER ======================
# Assuming both dataframes have a 'Year' column. If only one has it, adjust accordingly.
YEARS = sorted(employee_productivity['Year'].dropna().unique())  # Gets sorted unique years
# ========================================================================

COLOR_PALETTE = px.colors.qualitative.Plotly  # Plotly's color palette
DEPARTMENT_COLORS = {dept: COLOR_PALETTE[i % len(COLOR_PALETTE)] for i, dept in enumerate(DEPARTMENTS)}  # Assigns colors to departments

# ====================== APP INITIALIZATION ======================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Initializes the Dash app with Bootstrap theme

# ====================== REUSABLE COMPONENT FUNCTIONS ======================

def create_metric_card(title, value_id):
    """
    Creates a card to display a single metric.
    """
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H5(title, className="text-center", style={'font-weight': 'bold', 'color': 'white'}),  # Metric title
                html.H2(id=value_id, className="text-center", style={'color': '#ff8c00', 'font-weight': 'bold'})  # Metric value
            ]),
            className='shadow-sm',
            style={'background-color': '#161b22'}  # Card background color
        ),
        width=3  # Column width
    )

def create_graph(id):
    """
    Creates a graph component.
    """
    return dcc.Graph(
        id=id,
        config={'displayModeBar': False},  # Hides toolbar
        style={'background-color': '#0d1117'}  # Graph background color
    )

# ====================== LAYOUT DEFINITION ======================
app.layout = dbc.Container([
    # Title Section
    html.Div([
        html.H1(
            'Amazon Remote Work Productivity Dashboard',
            className='text-center mb-4',
            style={
                'color': 'orange',
                'background-color': '#0d1117',
                'padding': '10px',
                'border-radius': '5px'
            }
        )
    ]),
    
    # ====================== YEAR AND DEPARTMENT FILTERS ======================
    # Department & Year Filter Row
    dbc.Row([
        # Department Filter
        dbc.Col([
            html.Label("Select Department", style={'color': 'white', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='dept-filter',
                options=[{'label': dept, 'value': dept} for dept in DEPARTMENTS],
                value=[],  # Default to no selection
                placeholder="All Departments",
                multi=True,  # Allows multiple selections
                style={'color': '#000000'}  # Text color inside dropdown
            )
        ], width=4),

        # Year Filter
        dbc.Col([
            html.Label("Select Year", style={'color': 'white', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': y, 'value': y} for y in YEARS],
                value=[],  # Default to no selection
                placeholder="All Years",
                multi=True,  # Allows multiple selections
                style={'color': '#000000'}  # Text color inside dropdown
            )
        ], width=4),
    ],
    className="mb-4",
    style={
        'background-color': '#0d1117',
        'padding': '10px',
        'border-radius': '5px'
    }),
    # ==================================================================================

    # Overview Metrics
    dbc.Row([
        create_metric_card('Total Employees', 'total_employees'),
        create_metric_card('Avg Satisfaction Score', 'avg_satisfaction'),
        create_metric_card('Avg Email Response Rate', 'avg_email_response'),
        create_metric_card('Avg Project Completion Time', 'avg_project_completion')
    ],
    className="mb-4",
    style={
        'background-color': '#0d1117',
        'padding': '20px',
        'border-radius': '5px'
    }),
    
    # Graphs Section: Row 1
    dbc.Row([
        dbc.Col(create_graph('work_hours_chart'), width=6),
        dbc.Col(create_graph('communication_chart'), width=6)
    ]),
    
    # Graphs Section: Row 2
    dbc.Row([
        dbc.Col(create_graph('environmental_chart'), width=6),
        dbc.Col(create_graph('work_tools_chart'), width=6)
    ]),
    
    # Graphs Section: Row 3
    dbc.Row([
        dbc.Col(create_graph('engagement_chart'), width=12)
    ])
],
fluid=True,
style={'backgroundColor': '#0d1117'}
)

# ====================== CALLBACK FUNCTION ======================
@app.callback(
    [
        Output('work_hours_chart', 'figure'),
        Output('communication_chart', 'figure'),
        Output('environmental_chart', 'figure'),
        Output('work_tools_chart', 'figure'),
        Output('engagement_chart', 'figure'),
        Output('total_employees', 'children'),
        Output('avg_satisfaction', 'children'),
        Output('avg_email_response', 'children'),
        Output('avg_project_completion', 'children')
    ],
    [
        Input('dept-filter', 'value'),
        Input('year-filter', 'value')  # <-- NEW YEAR FILTER INPUT
    ]
)
def update_dashboard(selected_depts, selected_years):
    # Updates dashboard based on selected departments and selected years
    
    # ====================== NEW CODE: FILTERING DATA BY YEAR & DEPARTMENT ======================
    filtered_employee_df = employee_productivity.copy()
    filtered_satisfaction_df = productivity_satisfaction.copy()
    
    # Filter by Department if departments are selected
    if selected_depts:
        filtered_employee_df = filtered_employee_df[filtered_employee_df['Department'].isin(selected_depts)]
        filtered_satisfaction_df = filtered_satisfaction_df[filtered_satisfaction_df['Department'].isin(selected_depts)]
    
    # Filter by Year if years are selected
    if selected_years:
        filtered_employee_df = filtered_employee_df[filtered_employee_df['Year'].isin(selected_years)]
        filtered_satisfaction_df = filtered_satisfaction_df[filtered_satisfaction_df['Year'].isin(selected_years)]
    # ===========================================================================================
    
    # Calculate metrics
    total_employees = len(filtered_employee_df)  # Total number of employees
    avg_satisfaction_score = round(filtered_employee_df['Satisfaction_Score'].mean(), 2) if not filtered_employee_df.empty else 0
    avg_email_response = round(filtered_satisfaction_df['Email_Response_Rate'].mean(), 2) if not filtered_satisfaction_df.empty else 0
    avg_project_completion = round(filtered_employee_df['Project_Completion_Times'].mean(), 2) if not filtered_employee_df.empty else 0

    # Work Hours and Task Productivity (Line Chart)
    fig1 = px.line(
        filtered_employee_df,
        x=filtered_employee_df.index,  # X-axis as index
        y=['Task_Duration', 'Project_Completion_Times'],  # Multiple lines
        labels={'value': 'Time (hours)', 'index': 'Magnitude'},  # Axis labels
        title='<b>Work Hours and Task Productivity</b>',
        template='plotly_dark'
    )
    variable_colors_fig1 = {'Task_Duration': 'lime', 'Project_Completion_Times': 'fuchsia'}
    for trace in fig1.data:
        trace.line.color = variable_colors_fig1.get(trace.name, 'white')  # Set line colors
    fig1.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='white',
        xaxis=dict(showgrid=False, title='Magnitude'),  # X-axis settings
        yaxis=dict(showgrid=False, title='Time in Hrs')  # Y-axis settings
    )

    # Communication Metrics (Bar Chart)
    fig2 = px.bar(
        filtered_satisfaction_df,
        x='Department',
        y='Email_Response_Rate',
        color='Department',
        color_discrete_map=DEPARTMENT_COLORS,  # Assign colors
        title='<b>Communication Metrics</b>',
        template='plotly_dark'
    )
    fig2.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='white',
        xaxis=dict(showgrid=False, title='Department'),  # X-axis settings
        yaxis=dict(showgrid=False, title='Email Response Rate')  # Y-axis settings
    )

    # Environmental Context (Heatmap)
    environmental_pivot = filtered_satisfaction_df.pivot_table(
        index='Department',
        values=['Internet_Stability', 'Workspace_Setup'],
        aggfunc='mean'
    )  # Pivot data for heatmap
    fig3 = px.imshow(
        environmental_pivot,
        labels={'color': 'Average Score'},
        title='<b>Environmental Context</b>',
        width=650,
        height=500,
        color_continuous_scale='Viridis'  # Color scale
    )
    fig3.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='white'
    )
    fig3.update_xaxes(showgrid=False, zeroline=False)  # Remove grid and lines
    fig3.update_yaxes(showgrid=False, zeroline=False)

    # Work Tools Usage (Line Chart)
    fig4 = px.line(
        filtered_satisfaction_df,
        x=filtered_satisfaction_df.index,
        y=['Work_Tool_Hours', 'Downtime'],
        labels={'value': 'Time in Hrs', 'index': 'Magnitude'},
        title='<b>Work Tools Usage</b>',
        template='plotly_dark'
    )
    variable_colors_fig4 = {'Work_Tool_Hours': 'yellow', 'Downtime': 'red'}
    for trace in fig4.data:
        trace.line.color = variable_colors_fig4.get(trace.name, 'white')  # Set line colors
    fig4.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='white',
        xaxis=dict(showgrid=False, title='Magnitude'),  # X-axis settings
        yaxis=dict(showgrid=False, title='Time in Hrs')  # Y-axis settings
    )

    # Engagement and Well-being (Scatter Plot)
    fig5 = px.scatter(
        filtered_employee_df,
        x='Satisfaction_Score',
        y='Burnout_Indicator',
        color='Department',
        color_discrete_map=DEPARTMENT_COLORS,  # Assign colors
        title='<b>Engagement and Well-being</b>',
        template='plotly_dark'
    )
    fig5.update_traces(marker=dict(size=12))  # Marker size
    fig5.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='white',
        xaxis=dict(showgrid=False, title='Satisfaction Score'),  # X-axis settings
        yaxis=dict(showgrid=False, title='Burnout Indicator')  # Y-axis settings
    )

    # Return all figures and metrics
    return (
        fig1,
        fig2,
        fig3,
        fig4,
        fig5,
        total_employees,
        f"{avg_satisfaction_score}",
        f"{avg_email_response}%",
        f"{avg_project_completion} hrs"
    )

# ====================== RUN THE DASHBOARD ======================
if __name__ == '__main__':
    app.run_server(debug=True)  # Starts the dashboard
