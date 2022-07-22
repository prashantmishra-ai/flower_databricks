from flask import Flask, render_template,request
app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        import os
        import pandas as pd
        os.environ["DATABRICKS_TOKEN"] = "dapif1f996267465ffc54c20b3736ad61a12-2"
        import requests
        def create_tf_serving_json(data):
          return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}
        os.environ["DATABRICKS_TOKEN"] = "dapif1f996267465ffc54c20b3736ad61a12-2"
        def score_model(dataset):
          url = 'https://adb-2545852770213014.14.azuredatabricks.net/model/flower_class/1/invocations'
          headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}'}
          data_json = dataset.to_dict(orient='split') if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
          response = requests.request(method='POST', headers=headers, url=url, json=data_json)
          if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}, {response.text}')
          return response.json()
        dataset = pd.DataFrame([{
          "sepal length":request.form.get("sepal_length"),
          "sepal width":request.form.get("sepal_width"),
          "petal length":request.form.get("petal_length"),
          "petal width":request.form.get("petal_width")
        }])
        response = score_model(dataset)[0]
        print(response)
        if (int(response) == 0):
          message = "setosa"
        elif (int(response) ==1):
          message = "Versicolour"
        elif (int(response) == 2):
          message = "Virginica"
        return render_template('index.html', message=message)
    return render_template('index.html')