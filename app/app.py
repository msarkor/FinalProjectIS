from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'nilefloodData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Marlon Sarkor Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM nilefloodData')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, nile_flood=result)


@app.route('/view/<int:flood_id>', methods=['GET'])
def record_view():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM nilefloodData WHERE id=%s', flood_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', nile_flood=result[0])


@app.route('/edit/<int:flood_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM nilefloodData WHERE id=%s', flood_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', nile_flood=result[0])


@app.route('/edit/<int:flood_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Flood_Height'), flood_id)
    sql_update_query = """UPDATE nilefloodData t SET t.Year = %s, t.Flood_Height = %s  WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/nile_flood/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Flood Form')


@app.route('/nile_flood/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Flood_Height'))
    sql_insert_query = """INSERT INTO nilefloodData (Year, Flood) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:flood_id>', methods=['POST'])
def form_delete_post(flood_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM nilefloodData WHERE id = %s """
    cursor.execute(sql_delete_query, flood_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


#@app.route('/api/v1/cities', methods=['GET'])
#def api_browse() -> str:
#    cursor = mysql.get_db().cursor()
#    cursor.execute('SELECT * FROM tblCitiesImport')
#    result = cursor.fetchall()
#    json_result = json.dumps(result);
#    resp = Response(json_result, status=200, mimetype='application/json')
#    return resp


#@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
#def api_retrieve(city_id) -> str:
#    cursor = mysql.get_db().cursor()
#    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
 #   result = cursor.fetchall()
  #  json_result = json.dumps(result);
   # resp = Response(json_result, status=200, mimetype='application/json')
#    return resp


#@app.route('/api/v1/cities/', methods=['POST'])
#def api_add() -> str:
#    resp = Response(status=201, mimetype='application/json')
#    return resp


#@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
#def api_edit(city_id) -> str:
#    resp = Response(status=201, mimetype='application/json')
#    return resp


#@app.route('/api/cities/<int:city_id>', methods=['DELETE'])
#def api_delete(city_id) -> str:
#    resp = Response(status=210, mimetype='application/json')
#    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)