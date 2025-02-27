# Import library yang diperlukan
from jupyter_dash import JupyterDash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Muat dan pra-proses dataset Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_df = pd.read_csv(url)

# Hapus kolom 'Cabin'
titanic_df = titanic_df.drop('Cabin', axis=1)

# Isi nilai yang hilang pada kolom 'Age' dengan median
titanic_df['Age'] = titanic_df['Age'].fillna(titanic_df['Age'].median())

# Isi nilai yang hilang pada kolom 'Embarked' dengan modus
titanic_df['Embarked'] = titanic_df['Embarked'].fillna(titanic_df['Embarked'].mode()[0])

# Buat histogram distribusi umur penumpang
fig_histogram = px.histogram(
    titanic_df, 
    x='Age', 
    nbins=20,
    title='Histogram Distribusi Umur Penumpang Titanic',
    labels={'Age': 'Umur', 'count': 'Jumlah'}
)
fig_histogram.update_layout(bargap=0.2, yaxis_title='Jumlah')

# Buat histogram kelas penumpang vs. kelangsungan hidup yang dikelompokkan berdasarkan jenis kelamin
fig_histogram2 = px.histogram(
    titanic_df,
    x='Pclass',
    color='Survived',  # 1: Selamat, 0: Tidak selamat
    facet_col="Sex",
    barmode="group",
    title='Histogram Kelas Penumpang dan Kelangsungan Hidup',
    labels={'Pclass': 'Kelas Penumpang', 'Survived': 'Survivor'},
    color_discrete_map={0: 'red', 1: 'blue'}
)
fig_histogram2.update_layout(yaxis_title='Jumlah')

# Buat violin plot: distribusi umur berdasarkan kelas penumpang dengan informasi kelangsungan hidup
fig_violin = px.violin(
    titanic_df,
    x='Pclass',
    y='Age',
    color='Survived',
    box=True,
    points='all',
    title='Distribusi Umur Berdasarkan Kelas dan Kelangsungan Hidup',
    labels={'Pclass': 'Kelas Penumpang', 'Survived': 'Survivor'},
    color_discrete_map={0: 'red', 1: 'blue'}
)
fig_violin.update_layout(yaxis_title='Jumlah')

# Inisialisasi aplikasi JupyterDash
app = JupyterDash(__name__)

# Definisikan layout dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard Titanic'),
    html.Div(children='Dashboard visualisasi data penumpang Titanic.'),

    # Menampilkan histogram umur
    dcc.Graph(
        id='histogram-age',
        figure=fig_histogram
    ),

    # Menampilkan histogram kelas penumpang vs. kelangsungan hidup
    dcc.Graph(
        id='histogram-pclass-survived',
        figure=fig_histogram2
    ),

    # Menampilkan violin plot distribusi umur berdasarkan kelas
    dcc.Graph(
        id='violin-pclass-age',
        figure=fig_violin
    )
])

# Jalankan server secara inline di Google Colab
app.run_server(mode='inline', debug=True)
