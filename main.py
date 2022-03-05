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
    
    return render_template('main.html',tables=[data.to_html(classes='data')], titles = data.columns.values)
    

@app.route("/billing")
def bill_plot(): 
    query = f'''
    SELECT DATE(usage_start_time) AS usage_date, sum(cost) as actual
    FROM `{project_id}.billing.sample2`
    WHERE usage_start_time >= '2022-02-01'
    GROUP by 1
    ORDER BY 1
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    df1 = query_job.to_dataframe()
    
    query = f'''
    SELECT DATE(forecast_timestamp) AS usage_date, sum(forecast_value) as forecast
    FROM `{project_id}.billing.sample2_pred`
    GROUP BY 1
    ORDER BY 1
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    df2 = query_job.to_dataframe()
    
    data = df1.merge(df2, on = 'usage_date', how = 'outer').fillna(0)
    labels = list(pd.to_datetime(data['usage_date']).dt.strftime('%Y-%m-%d'))
    value1 = data['actual'].values.tolist()
    value2 = data['forecast'].values.tolist()

    return render_template("bill.html", labels = labels, value1 = value1, value2 = value2)


if __name__ == "__main__":
    app.run(host = '127.0.0.1', debug = True)
