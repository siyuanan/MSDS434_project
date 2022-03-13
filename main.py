import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from google.cloud import bigquery

project_id  = 'msds434-2022-sa'
dataset_id  = 'mobile_data'
table_train = 'train'
table_test  = 'test'
table_synth = 'synthetic'

var_list = ['battery_power', 'px_height', 'px_width', 'ram']

app = Flask(__name__)

def model_train():
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


@app.route("/", methods=['GET', 'POST'])
def home_page():

    # get input from user
    input_data = request.form
    input_df = pd.DataFrame.from_dict(input_data)

    # retrieve average parameters
    query = f'''
    SELECT avg(ram) as ram
        , avg(battery_power) as battery_power
        , avg(px_height) as px_height
        , avg(px_width) as px_width
    FROM {project_id}.{dataset_id}.rf_pred
    '''
    client = bigquery.Client(project = project_id)
    query_job = client.query(query)
    avg_param = query_job.to_dataframe().round(0)

    return render_template('main.html'
                           , var_list = var_list
                           , input_data = input_data
                           , table1 = [avg_param.to_html(classes='data')]
                           , title1 = avg_param.columns.values
                           )


# @app.route('/data/', methods=['GET', 'POST'])
# def form():
#     form_data = request.form
#     return render_template('data.html', var_list = var_list, form_data = form_data)


@app.route('/pred/', methods=['GET', 'POST'])
def pred_page():
    form_data = request.form
    ram = form_data['ram']
    battery_power = form_data['battery_power']
    px_height = form_data['px_height']
    px_width = form_data['px_width']

    # retrieve prediction
    query = f'''
    SELECT predicted_label
    , predicted_label_probs
    , battery_power
    , ram
    , px_height
    , px_width
    FROM {project_id}.{dataset_id}.rf_pred
    '''
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    df_pred = query_job.to_dataframe()
    df_pred['diff_ram'] = (df_pred['ram'] - ram).abs()
    df_pred['diff_power'] = (df_pred['battery_power'] - battery_power).abs()
    df_pred['diff_height'] = (df_pred['px_height'] - px_height).abs()
    df_pred['diff_width'] = (df_pred['px_width'] - px_width).abs()
    df_pred['score'] = 310 * df_pred['diff_ram'] + 185 * df_pred['diff_power'] \
                       + 137 * df_pred['diff_width'] + 128 * df_pred['diff_height']
    df_pred.sort_values(by = 'score', inplace = True, ignore_index = True)
    pred = df_pred.loc[0, 'predicted_label']
    probs = df_pred.loc[0, 'predicted_label_probs']


    return render_template('pred.html'
                           , form_data = form_data
                           , pred = pred
                           , probs = probs
                           )


@app.route("/billing/", methods=['GET', 'POST'])
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
    app.run(host = '127.0.0.1', debug = True, port=int(os.environ.get("PORT", 8080)))
