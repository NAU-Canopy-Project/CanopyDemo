from flask import Flask, request, render_template, request
from flask_mail import Mail
from flask_mail import Message
import geopandas as gpd
import zipfile as zpf
import glob
import os

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
    if request.method == "POST":
        # Take in file string
        inShapefile = request.files[ "shapefileInput" ]

        # Change directory to temporary folder
        os.chdir( "\\shapefiles\\temporary" )

        # Save zip file to current directory
        inShapefile.save( inShapefile.filename )

        # Extract zip file in order to access .shp file
        ZIP = zpf.ZipFile( inShapefile )
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
        if readfile.geometry.is_valid[0]:
            return "Valid shapefile"
        else:
            return "Invalid shapefile"

    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return ( '', 204 )

if __name__ == "__main__":
    app.run(debug=True)
