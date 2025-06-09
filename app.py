from flask import Flask
app=Flask(__name__)

@app.route('/')

def welcome():
    return "Welcme guys"

@app.route('/success/<int:score>')

def success(score):
    return "The person got "+ str(score)

@app.route('/fail/<int:score>')

def fail(score):
    return "The person is fail and got "+ str(score)

if __name__=='__main__':
    app.run(debug=True)