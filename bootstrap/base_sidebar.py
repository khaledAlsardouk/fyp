from File_flask import Flask, redirect, url_for,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base_sidebar.html")

if __name__=="__main__":
    app.run()