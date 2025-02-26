import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load and preprocess the dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_df = pd.read_csv(url)

# Drop the 'Cabin' column
titanic_df = titanic_df.drop('Cabin', axis=1)

# Fill missing 'Age' values with the median
titanic_df['Age'] = titanic_df['Age'].fillna(titanic_df['Age'].median())

# Fill missing 'Embarked' values with the mode
titanic_df['Embarked'] = titanic_df['Embarked'].fillna(titanic_df['Embarked'].mode()[0])

# Create the first histogram: Distribution of Passenger Age
fig_histogram = px.histogram(
    titanic_df, 
    x='Age', 
    nbins=20,
    title='Histogram Distribusi Umum Penumpang Titanic',
    labels={'Age': 'Umur', 'count': 'Jumlah'}
)
fig_histogram.update_layout(bargap=0.2, yaxis_title='Jumlah')

# Create the second histogram: Passenger Class vs. Survival grouped by Sex
fig_histogram2 = px.histogram(
    titanic_df,
    x='Pclass',
    color='Survived',  # 1: Survived, 0: Did not survive
    facet_col="Sex",
    barmode="group",
    title='Histogram Distribusi Umum Penumpang Titanic',
    labels={'Pclass': 'Kelas Penumpang', 'Survived': 'Survivor'},
    color_discrete_map={0: 'red', 1: 'blue'}
)
fig_histogram2.update_layout(yaxis_title='Jumlah')

# Create the violin plot: Distribution of Age by Passenger Class with Survival
fig_violin = px.violin(
    titanic_df,
    x='Pclass',
    y='Age',
    color='Survived',
    box=True,
    points='all',
    title='Distribusi Kelas dan Kelangsungan Hidup Penumpang Titanic',
    labels={'Pclass': 'Kelas Penumpang', 'Survived': 'Survivor'},
    color_discrete_map={0: 'red', 1: 'blue'}
)
fig_violin.update_layout(yaxis_title='Jumlah')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard Titanic'),

    html.Div(children='''
        Dashboard visualisasi data penumpang Titanic.
    '''),

    # Display the Age Histogram
    dcc.Graph(
        id='histogram-age',
        figure=fig_histogram
    ),

    # Display the Passenger Class vs. Survival Histogram
    dcc.Graph(
        id='histogram-pclass-survived',
        figure=fig_histogram2
    ),

    # Display the Violin Plot for Age vs. Passenger Class
    dcc.Graph(
        id='violin-pclass-age',
        figure=fig_violin
    )
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
