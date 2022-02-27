import pandas as pd
from flask import Flask, render_template
from google.cloud import bigquery
from datetime import datetime

project_id  = 'msds434-2022-sa'
dataset_id  = 'mobile_data'
table_train = 'train'
table_test  = 'test'
table_synth = 'synthetic'

app = Flask(__name__)

# @app.route("/")
def test_df(): 
    data = pd.DataFrame({
        'A': [1,2,3],
        'B': [4,5,6],
        'C': [7,8,9]
    })
    return render_template('view.html',tables=[data.to_html(classes='data')], titles = data.columns.values)

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
    query_test = f'''
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
    query_job = client.query(query_test)
    query_job.result()
    
    return f"<br/><br/>Model prediction finished"

@app.route("/")
def pred_result(): 
    query = f'''
    SELECT * FROM {project_id}.{dataset_id}.lr_pred
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    data = query_job.to_dataframe()
    
    return render_template('view.html',tables=[data.to_html(classes='data')], titles = data.columns.values)
    

@app.route("/billing")
def bill_plot(): 
    query = f'''
    SELECT usage_start_time AS time_label, sum(cost) as cost
    FROM `{project_id}.billing.sample2`
    WHERE usage_start_time >= '2022-02-01'
    GROUP by 1
    ORDER BY 1
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    df1 = query_job.to_dataframe()
    
    query = f'''
    SELECT forecast_timestamp AS time_label, forecast_value as cost
    FROM `{project_id}.billing.sample2_pred`
    ORDER BY 1
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    df2 = query_job.to_dataframe()
    
    data = pd.concat([df1, df2], ignore_index = True)
    labels = list(data['time_label'])
    values = list(data['cost'])
    
#     return render_template('view.html',tables = [data.to_html(classes='data')], titles = data.columns.values)
    return render_template("bill.html", labels = labels, values = values)

if __name__ == "__main__":
    app.run(host = '127.0.0.1', debug = True)
