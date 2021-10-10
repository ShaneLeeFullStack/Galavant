from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello World 1"
@app.route('/index')
def index():
    return "Hey This is an index page"
if __name__ == "__main__":
    #app.run(host="ec2-54-215-40-76.us-west-1.compute.amazonaws.com", port=80)
 	app.run(host="0.0.0.0", port=80)