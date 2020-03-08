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
        if request.files["shapefileInput"].filename == "":
            if countryVal == "0":
                return render_template("failure.html")
            else:
                selectedCountry = request.form["country"]
                os.chdir("\\shapefiles")
                if selectedCountry == "ARG":
                    currentShapefile = glob.glob("*_ARG_shp")[0]
                elif selectedCountry == "BOL":
                    currentShapefile = glob.glob("*_BOL_shp")[0]
                elif selectedCountry == "BRA":
                    currentShapefile = glob.glob("*_BRA_shp")[0]
                elif selectedCountry == "CHL":
                    currentShapefile = glob.glob("*_CHL_shp")[0]
                elif selectedCountry == "COL":
                    currentShapefile = glob.glob("*_COL_shp")[0]
                elif selectedCountry == "ECU":
                    currentShapefile = glob.glob("*_ECU_shp")[0]
                elif selectedCountry == "GUY":
                    currentShapefile = glob.glob("*_GUY_shp")[0]
                elif selectedCountry == "PRY":
                    currentShapefile = glob.glob("*_PRY_shp")[0]
                elif selectedCountry == "PER":
                    currentShapefile = glob.glob("*_PER_shp")[0]
                elif selectedCountry == "SUR":
                    currentShapefile = glob.glob("*_SUR_shp")[0]
                elif selectedCountry == "URY":
                    currentShapefile = glob.glob("*_URY_shp")[0]
                elif selectedCountry == "VEN":
                    currentShapefile = glob.glob("*_VEN_shp")[0]
                os.chdir("..")
        else:
            # Take in file string
            currentShapefile = request.files["shapefileInput"]

            # Change directory to temporary folder
            os.chdir("\\shapefiles\\temporary")

            # Save zip file to current directory
            currentShapefile.save(currentShapefile.filename)

            # Extract zip file in order to access .shp file
            ZIP = zpf.ZipFile(currentShapefile)
            ZIP.extractall("\\shapefiles\\temporary")

            # Search for files that have string .shp
            gpdfile = glob.glob("*.shp")[0]

            # Read in file with geopandas
            # read_file returns GeoDataFrame which contains a GeoSeries
            readfile = gpd.read_file(gpdfile)

            # Test validity of the shapefile
            # geometry is the GeoSeries of GeoDataFrame
            # GeoSeries has is_valid which returns dtype('bool')
            # Take first element of series (True or False)
            if not (readfile.geometry.is_valid[0]):
                geomValid = False

        # Send <<currentShapefile>> (selected variable) to Monsoon here
        # Demo stats functions here also
        ObList = [1, 21, 4, 4, 5, 1, 54, 75, 2, 12, 43, 2, 12, 21, 34]
        Area=100

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


    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return ( '', 204 )

if __name__ == "__main__":
    app.run(debug=True)