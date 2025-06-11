from flask import Flask,redirect,render_template,request,url_for

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    total_score=0
    if request.method=='POST':
        science=float(request.form['science'])
        maths=float(request.form['maths'])
        DS=float(request.form['ds'])
        total_score=(science+maths+DS)/3

    return redirect(url_for('success', score=int(total_score)))    

@app.route('/success/<int:score>')
def success(score):
    res=''
    if score>=50:
        res='PASS'

    else:
        res='FAIL'

    exp={'score':score, "res":res}        
    return render_template('result.html', result=exp)        

if __name__=='__main__':
    app.run(debug=True)