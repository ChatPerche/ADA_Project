import json
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    #df = pd.read_csv('data').drop('Open', axis=1)
    #chart_data = df.to_dict(orient='records')
    #chart_data = json.dumps(chart_data, indent=2)
    #data = {'chart_data': chart_data}
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)