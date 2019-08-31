
"""@app.route('/', methods=['POST','GET'])
def signup():
    try:
        _name = request.form['username']
        _password = request.form['password']


        if _name and _password:
            # create the connections

            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()"""