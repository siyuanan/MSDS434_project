from flask import Flask
from google.cloud import bigquery
from datetime import datetime

project_id  = 'msds434-2022-sa'
dataset_id  = 'mobile_data'
table_train = 'train'
table_test  = 'test'
table_synth = 'synthetic'

app = Flask(__name__)

def welcome():
    return "Welcome to the new app!"

def title_line():
    return "<br/><br/>This is for mobile price prediction"

def model_train():
#     t1 = datetime.now()
    query_train = f'''
        CREATE OR REPLACE MODEL {project_id}.{dataset_id}.lr_model2
          OPTIONS
          ( MODEL_TYPE = 'LOGISTIC_REG',
            AUTO_CLASS_WEIGHTS = TRUE )
        AS SELECT 
        battery_power,
        blue,
        clock_speed,
        dual_sim,
        fc,
        four_g,
        int_memory,
        m_dep,
        mobile_wt,
        n_cores,
        pc,
        px_height,
        px_width,
        ram,
        sc_h,
        sc_w,
        talk_time,
        three_g,
        touch_screen,
        wifi,
        price_range as label
        FROM `{project_id}.{dataset_id}.{table_train}`
        order by rand() limit 100
        '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query_train)
    query_job.result()
#     t2 = datetime.now()
#     exe_time = (t2 - t1).total_seconds()
    
    return f"<br/><br/>Model training finished"

def model_test():
    query_train = f'''
        SELECT * FROM
            ML.PREDICT(MODEL `msds434-2022-sa.mobile_data.lr_model`,
              (
              SELECT
                *
              FROM
                `msds434-2022-sa.mobile_data.test`
                )
              )
            LIMIT 10
        '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query_train)
    query_job.result()
    
    return f"<br/><br/>Model prediction finished"


@app.route("/")
def main_func(): 
    return welcome() + title_line() + model_test()

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 8080, debug = True)
