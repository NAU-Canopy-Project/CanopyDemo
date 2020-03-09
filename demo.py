from flask import Flask, request, render_template, request, url_for
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
    return render_template("index.html")

# Takes in shapefile, tests validity
@app.route("/success/", methods = ["GET", "POST"] )
def readShapefile():
    geomValid = True
    countryVal = request.form["country"]
    functionList = request.form.getlist("function")
    if request.method == "POST":
        if request.files["shapefileInput"].filename == "":
            if countryVal == "0":
                return render_template("",204)
            else:
                selectedCountry = request.form["country"]
                os.chdir("\\shapefiles")
                if selectedCountry == "ARG":
                    currentShapefile = glob.glob("*_ARG_shp")
                elif selectedCountry == "BOL":
                    currentShapefile = glob.glob("*_BOL_shp")
                elif selectedCountry == "BRA":
                    currentShapefile = glob.glob("*_BRA_shp")
                elif selectedCountry == "CHL":
                    currentShapefile = glob.glob("*_CHL_shp")
                elif selectedCountry == "COL":
                    currentShapefile = glob.glob("*_COL_shp")
                elif selectedCountry == "ECU":
                    currentShapefile = glob.glob("*_ECU_shp")
                elif selectedCountry == "GUY":
                    currentShapefile = glob.glob("*_GUY_shp")
                elif selectedCountry == "PRY":
                    currentShapefile = glob.glob("*_PRY_shp")
                elif selectedCountry == "PER":
                    currentShapefile = glob.glob("*_PER_shp")
                elif selectedCountry == "SUR":
                    currentShapefile = glob.glob("*_SUR_shp")
                elif selectedCountry == "URY":
                    currentShapefile = glob.glob("*_URY_shp")
                elif selectedCountry == "VEN":
                    currentShapefile = glob.glob("*_VEN_shp")
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
            os.chdir("..")
            os.chdir("..")
        # Send <<currentShapefile>> (selected variable) to Monsoon here
        # Demo stats functions here also
        ObList = [1, 21, 4, 4, 5, 1, 54, 75, 2, 12, 43, 2, 12, 21, 34]
        Area=100

        #list store the result
        result = [' ',' ',' ',' ',' ',' ',' ',' ',' ']



        if "1" in functionList:
            result[1] = StatisticFunctions.NumberofObservations(ObList)
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


        emailReceiver = request.form["emailInput"]
        message = Message("Test",
                sender = "naucanopyproject@gmail.com",
                recipients = [emailReceiver])
        with app.open_resource("static\\bg.jpg") as fp:
            message.attach("static\\bg.jpg", "img/png", fp.read())
        #mail.send(message)

    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
