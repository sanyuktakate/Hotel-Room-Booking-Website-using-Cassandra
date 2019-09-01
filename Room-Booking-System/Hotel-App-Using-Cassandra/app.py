from flask import Flask, request, render_template
from cassandra.cluster import Cluster
import pandas as pd

app = Flask(__name__)
cluster = Cluster(['192.168.75.128', '172.20.20.20'])
keyspace = 'hotel'
hotels=""
global hotelId
connection = cluster.connect(keyspace)


@app.route("/")
def home():
    location = connection.execute("SELECT * FROM Location")
    print locals()
    return render_template('index.html', **locals())


@app.route("/hotelByLocation", methods=['GET', 'POST'])
def hotelByLocation():
    if request.method == "POST":
        select1 = request.form.get('comp_select', None)
        if select1 != None:
            print select1
            print "1"
            temp = "\'" + select1 + "\';"
            query1 = "select hotels from HotelByCities where city="+temp+""
            print query1

            location = connection.execute(query1)
            df = pd.DataFrame(location)
            hotels = df['hotels'][0]
            print hotels
            return render_template("city.html", hotels=hotels)
    return render_template('city.html', **locals())


@app.route("/hotelByCity", methods=['GET', 'POST'])
def hotelByCity():
    global hotelId
    if request.method == "POST":
        select1 = request.form.get('hotel_By_City', None)
        print  select1
        print "2"
        if select1 != None:
            temp = "\'" + select1 + "\' ALLOW FILTERING;"
            query = "select * from Hotelss where name=" + temp + ""
            print query
            id = connection.execute(query)
            df = pd.DataFrame(id)
            print df
            hotelId1 = df['hotelid'][0]
            hotelId= hotelId1
            print hotelId
            print "hereeeeeeeeeeeeeeeeeeeeeeeeee"
            avail = "select * from availbility where hotelid="+str(hotelId)+";"
            print avail
            rooms = connection.execute(avail)
            rooms_df=pd.DataFrame(rooms)
            rooms_list=rooms_df['rooms_available'][0]
            print rooms_list
            # hotelId = df['hotelid'][0]
            # print rooms_df[0]

            return render_template("hotel.html", rooms=rooms_list,hotel= hotelId)
    return render_template('hotel.html', **locals())

@app.route("/bookRoom", methods=['GET', 'POST'])
def bookRoom():
    if request.method == "POST":
        select1 = request.form.get('Book_room', None)
        if select1 != None:
            print select1
            print hotelId
            print "3"
            val= "\'"+select1+"\'"
            query= "UPDATE availbility SET rooms_available = rooms_available - ["+val+"] WHERE hotelId = "+str(hotelId)+";"
            print query
            connection.execute(query)


            return render_template("final.html",select=select1)
    return render_template('final.html', **locals())

@app.route("/final", methods=['GET', 'POST'])
def final():
    if request.method == "POST":
        select1 = request.form.get('Book_room', None)
        if select1 != None:
            print select1
            print "4"

            return render_template("final.html")
    return render_template('final.html', **locals())



if __name__ == "__main__":
    app.run(debug=True)
