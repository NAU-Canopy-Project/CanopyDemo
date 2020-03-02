from flask import Flask, request, render_template, request
from flask_mail import Mail
from flask_mail import Message
import geopandas as gpd
import zipfile as zpf
import glob
import os
import StatisticFunctions

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
@app.route("/", methods = ["POST"] )
def readShapefile():
    geomValid = True
    countryVal = request.form["country"]
    functionVal = request.form["function"]
    if request.method == "POST":
        if request.files["shapefileInput"].filename == "":
            if countryVal == "0":
                return render_template("failure.html")
            else:
                selectedCountry = request.form["country"]
                os.chdir( "\\shapefiles" )
                if selectedCountry == "ARG":
                    currentShapefile = glob.glob( "*_ARG_shp")[0]
                elif selectedCountry == "BOL":
                    currentShapefile = glob.glob( "*_BOL_shp")[0]
                elif selectedCountry == "BRA":
                    currentShapefile = glob.glob( "*_BRA_shp")[0]
                elif selectedCountry == "CHL":
                    currentShapefile = glob.glob( "*_CHL_shp")[0]
                elif selectedCountry == "COL":
                    currentShapefile = glob.glob( "*_COL_shp")[0]
                elif selectedCountry == "ECU":
                    currentShapefile = glob.glob( "*_ECU_shp")[0]
                elif selectedCountry == "GUY":
                    currentShapefile = glob.glob( "*_GUY_shp")[0]
                elif selectedCountry == "PRY":
                    currentShapefile = glob.glob( "*_PRY_shp")[0]
                elif selectedCountry == "PER":
                    currentShapefile = glob.glob( "*_PER_shp")[0]
                elif selectedCountry == "SUR":
                    currentShapefile = glob.glob( "*_SUR_shp")[0]
                elif selectedCountry == "URY":
                    currentShapefile = glob.glob( "*_URY_shp")[0]
                elif selectedCountry == "VEN":
                    currentShapefile = glob.glob( "*_VEN_shp")[0]
                os.chdir( ".." )
        else:
            # Take in file string
            currentShapefile = request.files["shapefileInput"]

            # Change directory to temporary folder
            os.chdir( "\\shapefiles\\temporary" )

            # Save zip file to current directory
            currentShapefile.save( currentShapefile.filename )

            # Extract zip file in order to access .shp file
            ZIP = zpf.ZipFile( currentShapefile )
            ZIP.extractall( "\\shapefiles\\temporary" )

            # Search for files that have string .shp
            gpdfile = glob.glob( "*.shp" )[0]

            # Read in file with geopandas
            # read_file returns GeoDataFrame which contains a GeoSeries
            readfile = gpd.read_file( gpdfile )

            # Test validity of the shapefile
            # geometry is the GeoSeries of GeoDataFrame
            # GeoSeries has is_valid which returns dtype('bool')
            # Take first element of series (True or False)
            if not(readfile.geometry.is_valid[0]):
                geomValid = False

        # Send <<currentShapefile>> (selected variable) to Monsoon here
        # Demo stats functions here also
        ObList = [1, 21, 4, 4, 5, 1, 54, 75, 2, 12, 43, 2, 12, 21, 34]
        Area=100
        tempHolder = None

        if functionVal == "1":
            tempHolder = StatisticFunctions.NumberofObservations(ObList)
            return render_template("success.html")
        elif functionVal == "3":
            tempHolder = StatisticFunctions.DensityofObservations(ObList,Area)
            return render_template("succes.html")
        elif functionVal == "4":
            tempHolder = StatisticFunctions.MeanVegetationHeight(ObList)
            return render_template("success.html")
        elif functionVal == "5":
            tempHolder = StatisticFunctions.StandardDeviationOfVegetationHeight(ObList)
            return render_template("success.html")
        elif functionVal == "6":
            tempHolder = StatisticFunctions.DataQuality(ObList)
        else:
            return render_template('failure.html')

    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return ( '', 204 )

if __name__ == "__main__":
    app.run(debug=True)
