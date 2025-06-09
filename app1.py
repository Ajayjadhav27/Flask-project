from flask import Flask,redirect,url_for

app=Flask(__name__)

@app.route('/')
def welcome():
    return "My new project"

@app.route("/success/<int:score>")
def success(score):
    return "The student is passed and he got "+ str(score)

@app.route('/fail/<int:score>')
def fail(score):
    return "the student is fail and got "+ str(score)

@app.route('/result/<int:marks>')
def results(marks):
    result=''
    if marks<50:
        result='fail'

    else:
        result='success'

    return redirect(url_for(result, score=marks))    

if __name__=='__main__':
    app.run(debug=True)