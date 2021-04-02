from flask import Flask, render_template, url_for
import matplotlib.pyplot as plt
import requests
import numpy as np
from datetime import datetime
import os
import time
import datetime as DT
from dateutil.relativedelta import relativedelta
import uuid
import glob

app = Flask(__name__)

def make_two_lists_one(list1, list2, extra=""):
    returnedlist = []
    for i, item in enumerate(list1):
        returnedlist.append((item, extra+list2[i]))
    return returnedlist

def parse_json_data(data):
    timestampList = []
    rateList = []

    for x in data:
        timestamp = x['timestamp']
        timestamp = timestamp.replace("T00:00:00Z", "")
        timestampList.append(timestamp)
        rate = x["rate"]
        rate = float(rate)
        rate = round(rate, 2)
        rate = str(rate)
        rateList.append(rate)
    return timestampList, rateList

def get_data(formatdateweek, formatdatetoday, formatdatemonth, formatdateyear, sleeptime):
    urlweek = f"https://api.nomics.com/v1/exchange-rates/history?key=XXXXXX&currency=BTC&start={formatdateweek}T00%3A00%3A00Z&end={formatdatetoday}T00%3A00%3A00Z"

    dataweek = requests.get(urlweek)
    dataweek = dataweek.json()

    time.sleep(1)

    urlmonth = f"https://api.nomics.com/v1/exchange-rates/history?key=XXXXXX&currency=BTC&start={formatdatemonth}T00%3A00%3A00Z&end={formatdatetoday}T00%3A00%3A00Z"

    datamonth = requests.get(urlmonth)
    datamonth = datamonth.json()

    time.sleep(1)

    urlyear = f"https://api.nomics.com/v1/exchange-rates/history?key=XXXXXXXXXX&currency=BTC&start={formatdateyear}T00%3A00%3A00Z&end={formatdatetoday}T00%3A00%3A00Z"

    datayear = requests.get(urlyear)
    datayear = datayear.json()

    
    # time.sleep(sleeptime)

    return dataweek, datamonth, datayear

def remove_file(graphfilter):
    for name in glob.glob(f"static/{graphfilter}*.png"):
        os.remove(name)
        print(f"{name} was removed")

def gen_graph(timestamp, timestamplist, ratelist, fsize=(11, 11)):
    global counter
    #now plot a graph using this data
    style = "ggplot"
    bad = "dark_background"
    plt.style.use(style)
    plt.figure(figsize=fsize)
    plt.plot(np.array(timestamplist), np.array(ratelist), "r-o")
    plt.title(f"Price of Bitcoin over a {timestamp}")
    plt.xlabel("Date")
    plt.ylabel("Prize")
    ect = uuid.uuid4()
    filename = f"graph{timestamp}{ect}.png"
    # print(filename)
    remove_file("graph" + timestamp)
    print(f"{filename} was added")
    plt.savefig("static/"+filename)
    return filename


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/week")
def week():
    date = datetime.now()
    year = date.year

    formatdatetoday = date.strftime("%Y-%m-%d")

    formatdateweek = date - DT.timedelta(days=7)
    formatdateweek = formatdateweek.strftime("%Y-%m-%d")

    formatdatemonth = date - relativedelta(months=+1)
    formatdatemonth = str(formatdatemonth).split()[0]

    formatdateyear = date - relativedelta(years=+1)
    formatdateyear = str(formatdateyear).split()[0]
    dataweek, datamonth, datayear = get_data(formatdateweek, formatdatetoday, formatdatemonth, formatdateyear, 1.5)
    timestampListweek, rateListweek = parse_json_data(dataweek)
    timestampListweekgraph, rateListweekgraph = parse_json_data(dataweek)
    filename = gen_graph("week", timestampListweekgraph, rateListweekgraph, fsize=(11, 11))
    rateandtimeweek = make_two_lists_one(timestampListweek, rateListweek, extra="$")
    return render_template("week.html", filename=filename, dataweek=rateandtimeweek)

@app.route("/month")
def month():
    date = datetime.now()
    year = date.year

    formatdatetoday = date.strftime("%Y-%m-%d")

    formatdateweek = date - DT.timedelta(days=7)
    formatdateweek = formatdateweek.strftime("%Y-%m-%d")

    formatdatemonth = date - relativedelta(months=+1)
    formatdatemonth = str(formatdatemonth).split()[0]

    formatdateyear = date - relativedelta(years=+1)
    formatdateyear = str(formatdateyear).split()[0]
    dataweek, datamonth, datayear = get_data(formatdateweek, formatdatetoday, formatdatemonth, formatdateyear, 1.5)
    timestampListmonth, rateListmonth = parse_json_data(datamonth)
    timestampListmonthgraph, rateListmonthgraph = parse_json_data(datamonth)
    filenamemonth = gen_graph("month", timestampListmonthgraph, rateListmonthgraph, fsize=(11, 11))
    rateandtimemonth = make_two_lists_one(timestampListmonth, rateListmonth, extra="$")
    return render_template("month.html", filenamemonth=filenamemonth, datamonth=rateandtimemonth)


@app.route("/year")
def year():
    date = datetime.now()
    year = date.year

    formatdatetoday = date.strftime("%Y-%m-%d")

    formatdateweek = date - DT.timedelta(days=7)
    formatdateweek = formatdateweek.strftime("%Y-%m-%d")

    formatdatemonth = date - relativedelta(months=+1)
    formatdatemonth = str(formatdatemonth).split()[0]

    formatdateyear = date - relativedelta(years=+1)
    formatdateyear = str(formatdateyear).split()[0]
    dataweek, datamonth, datayear = get_data(formatdateweek, formatdatetoday, formatdatemonth, formatdateyear, 1.5)
    timestampListyear, rateListyear = parse_json_data(datayear)
    timestampListyeargraph, rateListyeargraph = parse_json_data(datayear)
    filenameyear = gen_graph("month", timestampListyeargraph, rateListyeargraph, fsize=(11, 11))
    rateandtimeyear = make_two_lists_one(timestampListyear, rateListyear, extra="$")
    return render_template("year.html", filenameyear=filenameyear, datayear=rateandtimeyear)


if __name__ == "__main__":
    app.run(debug=True)
