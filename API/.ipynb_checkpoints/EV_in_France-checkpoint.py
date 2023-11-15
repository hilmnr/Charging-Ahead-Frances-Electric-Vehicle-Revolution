from flask import Flask
from flask import abort
from flask import request
from urllib.parse import quote
from flask import jsonify
import pymysql
import math

app = Flask(__name__)
MAX_PAGE_SIZE = 10


@app.route("/")
def greetings():
    return """<html> 
    <h1 style="color:olive;"> Hello, Welcome to the Charging Ahead EV API documentation!🔋⚡️ </h1>
    <p> To use it, please read the information below: </p>
    <h2 style="color:teal;"> EV Sales  </h2>
    <p> To find the information related to EV Sales Worldwive, try the <b>/evsales</b> endpoint. At the <b>bottom</b> of each page, you'll find the links to access the next and last pages </p>
    <p> To find the information related to EV Sales in France or any other country, try the <b>/evsales/{country}</b> endpoint. </p>
    <h2 style="color:teal;"> Charging Points </h2>
    <p> To find the information related to Charging Points Worldwive, try the <b>/chargingpoints</b> endpoint. At the <b>bottom</b> of each page, you'll find the links to access the next and last pages </p> 
    <p> To find the information related to Charging Points in France or any other country, try the <b>/chargingpoints/{country}</b> endpoint. </p>
    <p> To filter Charging Points in France or any other country by power train type (fast/slow) try the <b>/chargingpoints/{country}?powertrain={fast_charging/slow_charging}</b> endpoint. </p>
    <p> </p>
    <h2 style="color:teal;"> Top Selling Vehicles </h2>
    <p> To find the information related to the top selling vehicles in France from (2019 - 2022), try the <b>/topvehiclesfrance</b> endpoint. At the <b>top</b> of each page, you'll find the links to access the next and last pages </p> 
</br>
Happy searching!🙂
    
    </html>"""


@app.route("/evsales")
def evsales():
    name = request.args.get('name')
    page = int(request.args.get('page', 1))  
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            if name:
                sql_query = """SELECT region as country, 
                               CASE WHEN powertrain = 'BEV' THEN '100% Electric'
                               ELSE 'N/A' END AS power_train,
                               year,
                               CONCAT_WS(' ', value, unit) AS cars_sold
                               FROM sales_ev_world
                               WHERE year IN (2018, 2019, 2020, 2021, 2022)"""
            else:
                sql_query = """SELECT region as country, 
                               CASE WHEN powertrain = 'BEV' THEN '100% Electric'
                               ELSE 'N/A' END AS power_train,
                               year,
                               CONCAT_WS(' ', value, unit) AS cars_sold
                               FROM sales_ev_world
                               WHERE year IN (2018, 2019, 2020, 2021, 2022)"""

            sql_query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"

            cursor.execute(sql_query)
            ev_sales = cursor.fetchall()

        with db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM sales_ev_world")
            total = cursor.fetchone()
            total_count = total['total']
            last_page = math.ceil(total_count / page_size)

        next_page = f'/evsales?page={page + 1}&page_size={page_size}&name={name}' if page < last_page else None
        last_page_url = f'/evsales?page={last_page}&page_size={page_size}&name={name}'

        response_data = {
            'evsales': ev_sales,
            'next_page': next_page,
            'last_page': last_page_url,
        }

        return jsonify(response_data)

    finally:
        db_conn.close()

if __name__ == "__main__":
    app.run()




@app.route("/evsales/<country>")
def evcountry(country):
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(400, "Invalid 'page' parameter")

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            query = f"""SELECT
            region as country,
            CASE WHEN powertrain = 'BEV' THEN '100% Electric'
            ELSE 'N/A' END AS power_train,
            year,
            CONCAT_WS(' ', value, unit) AS cars_sold
            FROM sales_ev_world
            WHERE year IN (2018, 2019, 2020, 2021, 2022)
            AND region = '{country}'"""
            
            cursor.execute(query)
            
            country_data = cursor.fetchall()
            
            if not country_data:
                abort(404)
    finally:
        db_conn.close()

    return jsonify(country_data)

if __name__ == '__main__':
    app.run()
    
    

@app.route("/chargingpoints")
def charging():
    name = request.args.get('name')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            if name:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available fast' THEN 'Fast charging'
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available slow' THEN 'Slow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022)"""
            else:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available fast' THEN 'Fast charging'
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available slow' THEN 'Slow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022)"""

            sql_query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"

            cursor.execute(sql_query)
            charging_points = cursor.fetchall()

        with db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM charging_points_world")
            total = cursor.fetchone()
            total_count = total['total']
            last_page = math.ceil(total_count / page_size)

        next_page = f'/chargingpoints?page={page + 1}&page_size={page_size}&name={name}' if page < last_page else None
        last_page_url = f'/chargingpoints?page={last_page}&page_size={page_size}&name={name}'

        response_data = {
            'chargingpoints': charging_points,
            'next_page': next_page,
            'last_page': last_page_url,
        }

        return jsonify(response_data)

    finally:
        db_conn.close()

if __name__ == "__main__":
    app.run()



@app.route("/chargingpoints/<country>")
def chargingpoints(country):
    name = request.args.get('name')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            if name:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available fast' THEN 'fast charging'
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available slow' THEN 'flow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022) AND region = %s"""
            else:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available fast' THEN 'fast charging'
                    WHEN LOWER(TRIM(powertrain)) = 'publicly available slow' THEN 'slow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022) AND region = %s"""

            sql_query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"

            cursor.execute(sql_query, (country,))
            charging_points = cursor.fetchall()

        with db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM charging_points_world WHERE region = %s", (country,))
            total = cursor.fetchone()
            total_count = total['total']
            last_page = -(-total_count // page_size)  # Ceiling division

        next_page = f'/chargingpoints/{country}?page={page + 1}&page_size={page_size}&name={name}' if page < last_page else None
        last_page_url = f'/chargingpoints/{country}?page={last_page}&page_size={page_size}&name={name}'

        response_data = {
            'chargingpoints': charging_points,
            'next_page': next_page,
            'last_page': last_page_url,
        }

        return jsonify(response_data)

    finally:
        db_conn.close()

if __name__ == "__main__":
    app.run()



@app.route("/chargingpoints/<country>")
def charging_by_country_and_powertrain(country):
    name = request.args.get('name')
    powertrain = request.args.get('powertrain')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            if name:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN powertrain = 'publicly available fast' THEN 'fast charging'
                    WHEN powertrain = 'publicly available slow' THEN 'slow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022) AND region = %s"""

                if powertrain:
                    sql_query += f" AND powertrain = %s"
                    cursor.execute(sql_query, (country, powertrain))
                else:
                    cursor.execute(sql_query, (country,))

            else:
                sql_query = f"""SELECT region AS country,
                CASE
                    WHEN powertrain = 'publicly available fast' THEN 'fast charging'
                    WHEN powertrain = 'publicly available slow' THEN 'slow charging'
                    ELSE powertrain
                END AS power_train,
                year,
                CONCAT_WS(' ', value, unit) AS charging_points
                FROM charging_points_world
                WHERE year IN (2018, 2019, 2020, 2021, 2022) AND region = %s"""

                if powertrain:
                    sql_query += f" AND powertrain = %s"
                    cursor.execute(sql_query, (country, powertrain))
                else:
                    cursor.execute(sql_query, (country,))

            charging_points = cursor.fetchall()

            if not charging_points:
                abort(404)
    finally:
        db_conn.close()

    return jsonify(charging_points)

if __name__ == '__main__':
    app.run()

    

@app.route("/topvehiclesfrance")
def topvehiclesfrance():
    name = request.args.get('name')
    page = int(request.args.get('page', 1))  
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(
        user='root',
        host="localhost",
        password="N956124A",
        database="EV_in_France",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_conn.cursor() as cursor:
            sql_query = """SELECT modele as car_model,
            ventes as units_sold_france, annee as year
            FROM sales_top_selling_models"""

            if name:  # Filter by name if the name parameter is provided
                sql_query += " WHERE modele LIKE %s"
                sql_query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"
                cursor.execute(sql_query, ('%' + name + '%',))
            else:
                sql_query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"
                cursor.execute(sql_query)
                
            top_models = cursor.fetchall()

        with db_conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM sales_top_selling_models")
            total = cursor.fetchone()
            total_count = total['total']
            last_page = math.ceil(total_count / page_size)

        next_page = f'/topvehiclesfrance?page={page + 1}&page_size={page_size}&name={name}' if page < last_page else None
        last_page_url = f'/topvehiclesfrance?page={last_page}&page_size={page_size}&name={name}'

        response_data = {
            'top_vehicles_france': top_models,
            'next_page': next_page,
            'last_page': last_page_url,
        }

        return jsonify(response_data)

    finally:
        db_conn.close()

if __name__ == "__main__":
    app.run(debug=True)  # Added debug=True for development purposes



    
