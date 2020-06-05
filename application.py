import app as application

app = application.app

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")