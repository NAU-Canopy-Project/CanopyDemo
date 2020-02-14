from flask import Flask, render_template,request
import StatisticFunctions

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getData():
    ObList = [1, 21, 4, 4, 5, 1, 54, 75, 2, 12, 43, 2, 12, 21, 34]
    Aera=100
    country = request.form['country']
    function = request.form['function']

    if function == '1':
        return render_template('index.html', value=StatisticFunctions.NumberofObservations(ObList))
    elif function == '3':
        return render_template('index.html', value=StatisticFunctions.DensityofObservations(ObList,Aera))
    elif function == '4':
        return render_template('index.html', value=StatisticFunctions.MeanVegetationHeight(ObList))
    elif function == '5':
        return render_template('index.html', value=StatisticFunctions.StandardDeviationOfVegetationHeight(ObList))
    elif function == '6':
        return render_template('index.html', value=StatisticFunctions.DataQuality(ObList))
    else:
        return render_template('index.html', value="error")




if __name__ == '__main__':
    app.run()
