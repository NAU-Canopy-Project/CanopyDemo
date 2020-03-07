from flask import Flask, request, render_template, request
from flask_mail import Mail
from flask_mail import Message
import geopandas as gpd
import zipfile as zpf
import glob
import os

# call statistic functions
import StatisticFunctions

# call generate csv file
import output

import csv
app = Flask(__name__, template_folder = 'templates')
mail = Mail(app)

@app.route("/")
def index():
#    message = Message("Test",
#            sender = "naucanopyproject@gmail.com",
#            recipients = ["naucanopyproject@gmail.com"])
#    with app.open_resource("static\\samplegraph.png") as fp:
#        message.attach("static\\samplegraph.png", "img/png", fp.read())
#    mail.send(message)
    return render_template("index.html")

# Takes in shapefile, tests validity
@app.route("/", methods = ["GET", "POST"] )
def readShapefile():
    geomValid = True
    countryVal = request.form["country"]
    functionList = request.form.getlist("function")
    if request.method == "POST":

        # Send <<currentShapefile>> (selected variable) to Monsoon here
        # Demo stats functions here also
        ObList = [1, 21, 4, 4, 5, 1, 54, 75, 2, 12, 43, 2, 12, 21, 34]
        Area=100

        # the title of statistic function
        RowList =["Number of Observation","Time of Year","Density of Observations","Standard Deviation of Denstiy of Observations",
                      "Average Canopy Height","Standard Deviation of Canopy Height","Data Quality","Classify Forest Types","Raw Data"]

        #list store the result
        result = [' ',' ',' ',' ',' ',' ',' ',' ',' ']



        if "1" in functionList:
            result[1] = StatisticFunctions.NumberofObservations(ObList)
            emailReceiver = request.form["emailInput"]
            message = Message("Test",
                    sender = "naucanopyproject@gmail.com",
                    recipients = [emailReceiver])
            with app.open_resource("static\\bg.jpg") as fp:
                message.attach("static\\bg.jpg", "img/png", fp.read())
            mail.send(message)

            output.writeCSV(result)

        if "3" in functionList:
            result[3] = StatisticFunctions.DensityofObservations(ObList,Area)
            output.writeCSV(result)
        if "4" in functionList:

            result[4] = StatisticFunctions.StandardDeviationOfDensityOfObservations(ObList)
            output.writeCSV(result)
        if "5" in functionList:
            result[5] = StatisticFunctions.MeanVegetationHeight(ObList)
            output.writeCSV(result)
        if "6" in functionList:
            result[6] = StatisticFunctions.StandardDeviationOfVegetationHeight(ObList)
            output.writeCSV(result)
        if "7" in functionList:
            result[7] = StatisticFunctions.DataQuality(ObList)
            output.writeCSV(result)
        else:
            return render_template('success.html')

    output.writeCSV(result)

    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return ( '', 204 )

if __name__ == "__main__":
    app.run(debug=True)
