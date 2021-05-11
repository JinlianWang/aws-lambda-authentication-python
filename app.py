from flask import Flask, jsonify

app = Flask(__name__)
secret = "abcd"

@app.route('/api/authentication/login')
def login_url():
    return jsonify({"message": "Hello World2!"})


@app.route('/api/authentication/status')
def login_status():
    return jsonify({"message": "Status!" + secret})


@app.route('/api/authentication/exchange')
def exchange_code():
    return jsonify({"message": "Exchange for session token!"})


@app.route('/api/authentication/logout')
def logout():
    return jsonify({"message": "Logout!"})

if __name__ == '__main__':
    app.run()
