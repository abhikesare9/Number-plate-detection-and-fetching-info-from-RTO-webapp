from detection import *
from flask import Flask,render_template,Response,request


app = Flask(__name__)
savedCarDetails=dict()
@app.route('/fetch',methods=["POST","GET"])
def fetch():
    file=request.files['file']
    fname='test.'+file.filename.split('.')[-1]
    file.save(fname)
    plateNo= noPlateRecognization(fname)
    if plateNo not in savedCarDetails.keys():
        dt=getVehicalInfo(plateNo,'prasadkesare')
        savedCarDetails[plateNo]=dt
    return render_template('output.html',dt=savedCarDetails[plateNo])

@app.route('/')
def index():
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)

