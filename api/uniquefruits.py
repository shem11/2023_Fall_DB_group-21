from flask import Flask, render_template
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'database': 'dvdrental',
    'user': 'raywu1990',
    'password': 'test',
}

# Function to execute SQL query
def execute_query(query, fetch=False):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        if fetch:
            result = cursor.fetchall()
            return True, result
        return True, "Success!"
    except Error as e:
        return False, str(e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Route to insert a new row into basket_a
@app.route('/api/update_basket_a')
def update_basket_a():
    query = "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');"
    success, message = execute_query(query)
    if success:
        return "Success!"
    else:
        return message

# Route to show unique fruits in basket_a and basket_b
@app.route('/api/unique')
def show_unique_fruits():
    query_a = "select distinct basket_a.fruit_a from basket_a left join basket_b on basket_a.fruit_a=basket_b.fruit_b where basket_b.fruit_b is null;"
    
    query_b = "select distinct basket_b.fruit_b from basket_b left join basket_a on basket_b.fruit_b=basket_a.fruit_a where basket_a.fruit_a is null;"
    
    success_a, result_a = execute_query(query_a, fetch=True)
    success_b, result_b = execute_query(query_b, fetch=True)
    
    if success_a and success_b:
        unique_fruits_a = [row[0] for row in result_a]
        unique_fruits_b = [row[0] for row in result_b]
        
        return render_template('uniquefruits.html', unique_fruits_a=unique_fruits_a, unique_fruits_b=unique_fruits_b)
    else:
        error_message = "Error occurred while fetching data"
        return render_template('error.html', error=error_message)

if __name__ == '__main__':
    app.run(host='127.0.0.1')
