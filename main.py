from flask import Flask
from google.cloud import bigquery

project_id  = 'msds434-2022-sa'
dataset_id  = 'mobile_data'
table_train = 'train'
table_test  = 'test'
table_synth = 'synthetic'

app = Flask(__name__)

def welcome():
    return "Welcome to the new app!"

def title_line():
    return "This is for mobile price prediction"

def pred_test():
    query = f'''
    SELECT * FROM {project_id}.{dataset_id}.synthetic order by rand() limit 10
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    data = query_job.to_dataframe()
    
    return


@app.route("/")
def main_func(): 
    return welcome() + '<br/><br/>' + title_line()

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 8080, debug = True)
