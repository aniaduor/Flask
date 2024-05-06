from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'abc'


@app.route("/")
@app.route("/home")
def home():
    return render_template('login.html')

@app.route("/recentgraphs")
def recentgraphs():
    return render_template('recentgraphs.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Read the CSV file
        file = request.files['file']
        df = pd.read_csv(file)
        
        # Preprocess the data
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Calculate standard deviation
        std_dev = np.std(df['kwh'])
        
        # Identify anomalies
        mean = np.mean(df['kwh'])
        anomaly_threshold = 2 * std_dev
        anomalies = df[df['kwh'] > mean + anomaly_threshold]
        
        # Create interactive plot using Plotly
        fig = px.line(df, x=df.index, y='kwh', title='Energy Consumption with Anomalies')
        fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies['kwh'], mode='markers', marker=dict(color='red'), name='Anomalies'))
        
        # Convert plot to HTML format
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Store the plot data in session
        session['plot_html'] = plot_html
        
        # Redirect to the figure template
        return redirect(url_for('figure'))
    
    return render_template('upload.html')

@app.route("/figure", methods=['GET', 'POST'])
def figure():
    # Retrieve the plot data from session
    plot_html = session.get('plot_html', None)
    
    # Clear the session after retrieving the data
    session.pop('plot_html', None)
    
    return render_template('figure.html', plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
