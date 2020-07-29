import os
import requests
import urllib.parse

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#stores the name of the selected country
country = ""

#calls the API for the selected country
def lookup():
    """Look up cases for the country."""

    # Contact API
    response = requests.get(f"https://api.covid19api.com/dayone/country/{country}/status/confirmed/live", stream=True)
    responsen = requests.get(f"https://api.covid19api.com/dayone/country/{country}/status/deaths/live", stream=True)
    response.raise_for_status()
    responsen.raise_for_status()

    dates = []
    cases = []
    newcases = []
    deaths = []
    count = 0;
    datesnew = []
    newdeaths = []
    # Parse response

    quote = response.json()
    quoten = responsen.json()

    for date in quote:
        if date["Date"] in dates:
            i = dates.index(date["Date"])
            cases[i] += date["Cases"]
            if i > 0:
                newcases[i] = cases[i] - cases[i - 1]
            else:
                newcases[i] = cases[i]

        else:
            dates.append(date["Date"])
            cases.append(date["Cases"])
            count += 1;
            if count > 1:
                newcases.append(cases[count - 1] - cases[count - 2])
            else:
                newcases.append(cases[count - 1])

    count = 0

    for death in quoten:
        if death["Date"] in datesnew:
            i = datesnew.index(death["Date"])
            deaths[i] += death["Cases"]
            if i > 0:
                newdeaths[i] = deaths[i] - deaths[i - 1]
            else:
                newdeaths[i] = deaths[i]
        else:
            datesnew.append(death["Date"])
            deaths.append(death["Cases"])
            count += 1;
            if count > 1:
                newdeaths.append(deaths[count - 1] - deaths[count - 2])
            else:
                newdeaths.append(deaths[count - 1])


    return (dates, cases, newcases, newdeaths)

def usdata():
    response = requests.get(f"https://covidtracking.com/api/us/daily", stream=True)
    response.raise_for_status()
    quote = response.json()
    quote.reverse()

    dates = []
    cases = []
    deaths = []
    newcases = []

    for row in quote:
        cases.append(row["total"])
        s = str(row["date"])
        date = s[0:4] + "-" + s[4:6] + "-" + s[6:8]
        dates.append(date)
        deaths.append(row["deathIncrease"])
        newcases.append(row["positiveIncrease"])

    return (dates, cases, newcases, deaths)

@app.route("/data")
def data():
    if country == "USA":
        dates, cases, newcases, deaths = usdata()
    else:
        dates, cases, newcases, deaths = lookup()
    total = []
    total.append(dates)
    total.append(cases)
    total.append(newcases)
    total.append(deaths)
    return jsonify(total)



@app.route("/")
def index():
    response = requests.get(f"https://api.thevirustracker.com/free-api?global=stats", stream=True)
    response.raise_for_status()
    quote = response.json()
    results = quote["results"]
    return render_template("index.html",
        total = "{:,}".format(results[0]["total_cases"]),
        recovered = "{:,}".format(results[0]["total_recovered"]),
        deaths = "{:,}".format(results[0]["total_deaths"]),
        new = "{:,}".format(results[0]["total_new_cases_today"]),
        newdeaths = "{:,}".format(results[0]["total_new_deaths_today"]),
        affected = "{:,}".format(results[0]["total_affected_countries"]))

#routes for individual countries

@app.route("/india")
def india():
    global country
    country = "india"
    return render_template("country.html", name = "India")

@app.route("/canada")
def canada():
    global country
    country = "canada"
    return render_template("country.html", name = "Canada")

@app.route("/usa")
def usa():
    global country
    country = "USA"
    return render_template("country.html", name = "USA")

@app.route("/mexico")
def mexico():
    global country
    country = "mexico"
    return render_template("country.html", name = "Mexico")

@app.route("/colombia")
def colombia():
    global country
    country = "colombia"
    return render_template("country.html", name = "Colombia")

@app.route("/venezuela")
def venezuela():
    global country
    country = "venezuela"
    return render_template("country.html", name = "Venezuela")

@app.route("/suriname")
def suriname():
    global country
    country = "suriname"
    return render_template("country.html", name = "Suriname")

@app.route("/guyana")
def guyana():
    global country
    country = "guyana"
    return render_template("country.html", name = "Guyana")

@app.route("/ecuador")
def ecuador():
    global country
    country = "ecuador"
    return render_template("country.html", name = "Ecuador")

@app.route("/peru")
def peru():
    global country
    country = "peru"
    return render_template("country.html", name = "Peru")

@app.route("/bolivia")
def bolivia():
    global country
    country = "bolivia"
    return render_template("country.html", name = "Bolivia")

@app.route("/paraguay")
def paraguay():
    global country
    country = "paraguay"
    return render_template("country.html", name = "Paraguay")

@app.route("/brazil")
def brazil():
    global country
    country = "brazil"
    return render_template("country.html", name = "Brazil")

@app.route("/chile")
def chile():
    global country
    country = "chile"
    return render_template("country.html", name = "Chile")

@app.route("/argentina")
def argentina():
    global country
    country = "argentina"
    return render_template("country.html", name = "Argentina")

@app.route("/uruguay")
def uruguay():
    global country
    country = "uruguay"
    return render_template("country.html", name = "Uruguay")

@app.route("/iceland")
def iceland():
    global country
    country = "iceland"
    return render_template("country.html", name = "Iceland")

@app.route("/ireland")
def ireland():
    global country
    country = "ireland"
    return render_template("country.html", name = "Ireland")

@app.route("/portugal")
def portugal():
    global country
    country = "portugal"
    return render_template("country.html", name = "Portugal")

@app.route("/united-kingdom")
def unitedkingdom():
    global country
    country = "united-kingdom"
    return render_template("country.html", name = "United Kingdom")

@app.route("/norway")
def norway():
    global country
    country = "norway"
    return render_template("country.html", name = "Norway")

@app.route("/finland")
def finland():
    global country
    country = "finland"
    return render_template("country.html", name = "Finland")

@app.route("/sweden")
def sweden():
    global country
    country = "sweden"
    return render_template("country.html", name = "Sweden")

@app.route("/estonia")
def estonia():
    global country
    country = "estonia"
    return render_template("country.html", name = "Estonia")

@app.route("/latvia")
def latvia():
    global country
    country = "latvia"
    return render_template("country.html", name = "Latvia")

@app.route("/lithuania")
def lithuania():
    global country
    country = "lithuania"
    return render_template("country.html", name = "Lithuania")

@app.route("/belarus")
def belarus():
    global country
    country = "belarus"
    return render_template("country.html", name = "belarus")

@app.route("/denmark")
def denmark():
    global country
    country = "denmark"
    return render_template("country.html", name = "denmark")

@app.route("/belgium")
def belgium():
    global country
    country = "belgium"
    return render_template("country.html", name = "belgium")

@app.route("/netherlands")
def netherlands():
    global country
    country = "netherlands"
    return render_template("country.html", name = "netherlands")

@app.route("/poland")
def poland():
    global country
    country = "poland"
    return render_template("country.html", name = "poland")

@app.route("/germany")
def germany():
    global country
    country = "germany"
    return render_template("country.html", name = "germany")

@app.route("/france")
def france():
    global country
    country = "france"
    return render_template("country.html", name = "france")

@app.route("/spain")
def spain():
    global country
    country = "spain"
    return render_template("country.html", name = "spain")

@app.route("/czech-republic")
def czechrepublic():
    global country
    country = "czech-republic"
    return render_template("country.html", name = "Czech Republic")

@app.route("/italy")
def italy():
    global country
    country = "italy"
    return render_template("country.html", name = "Italy")

@app.route("/ukraine")
def ukraine():
    global country
    country = "ukraine"
    return render_template("country.html", name = "Ukraine")

@app.route("/moldova")
def moldova():
    global country
    country = "moldova"
    return render_template("country.html", name = "Moldova")

@app.route("/romania")
def romania():
    global country
    country = "romania"
    return render_template("country.html", name = "romania")

@app.route("/greece")
def greece():
    global country
    country = "greece"
    return render_template("country.html", name = "greece")

@app.route("/bulgaria")
def bulgaria():
    global country
    country = "bulgaria"
    return render_template("country.html", name = "bulgaria")

@app.route("/armenia")
def armenia():
    global country
    country = "armenia"
    return render_template("country.html", name = "armenia")

@app.route("/azerbaijan")
def azerbaijan():
    global country
    country = "azerbaijan"
    return render_template("country.html", name = "azerbaijan")

@app.route("/georgia")
def georgia():
    global country
    country = "georgia"
    return render_template("country.html", name = "georgia")

@app.route("/turkey")
def turkey():
    global country
    country = "turkey"
    return render_template("country.html", name = "turkey")

@app.route("/cyprus")
def cyprus():
    global country
    country = "cyprus"
    return render_template("country.html", name = "cyprus")

@app.route("/lebanon")
def lebanon():
    global country
    country = "lebanon"
    return render_template("country.html", name = "lebanon")

@app.route("/jordan")
def jordan():
    global country
    country = "jordan"
    return render_template("country.html", name = "jordan")

@app.route("/syria")
def syria():
    global country
    country = "syria"
    return render_template("country.html", name = "syria")

@app.route("/iraq")
def iraq():
    global country
    country = "iraq"
    return render_template("country.html", name = "iraq")

@app.route("/israel")
def israel():
    global country
    country = "israel"
    return render_template("country.html", name = "israel")

@app.route("/saudi-arabia")
def saudiarabia():
    global country
    country = "saudi-arabia"
    return render_template("country.html", name = "Saudi Arabia")

@app.route("/united-arab-emirates")
def unitedarabemirates():
    global country
    country = "united-arab-emirates"
    return render_template("country.html", name = "United Arab Emirates")

@app.route("/qatar")
def qatar():
    global country
    country = "qatar"
    return render_template("country.html", name = "qatar")

@app.route("/kuwait")
def kuwait():
    global country
    country = "kuwait"
    return render_template("country.html", name = "kuwait")

@app.route("/iran")
def iran():
    global country
    country = "iran"
    return render_template("country.html", name = "iran")

@app.route("/yemen")
def yemen():
    global country
    country = "yemen"
    return render_template("country.html", name = "yemen")

@app.route("/oman")
def oman():
    global country
    country = "oman"
    return render_template("country.html", name = "oman")

@app.route("/uzbekistan")
def uzbekistan():
    global country
    country = "uzbekistan"
    return render_template("country.html", name = "uzbekistan")

@app.route("/afghanistan")
def afghanistan():
    global country
    country = "afghanistan"
    return render_template("country.html", name = "afghanistan")

@app.route("/pakistan")
def pakistan():
    global country
    country = "pakistan"
    return render_template("country.html", name = "pakistan")

@app.route("/kyrgyzstan")
def kyrgyzstan():
    global country
    country = "kyrgyzstan"
    return render_template("country.html", name = "kyrgyzstan")

@app.route("/tajikistan")
def tajikistan():
    global country
    country = "tajikistan"
    return render_template("country.html", name = "tajikistan")

@app.route("/bhutan")
def bhutan():
    global country
    country = "bhutan"
    return render_template("country.html", name = "bhutan")

@app.route("/bangladesh")
def bangladesh():
    global country
    country = "bangladesh"
    return render_template("country.html", name = "bangladesh")

@app.route("/nepal")
def nepal():
    global country
    country = "nepal"
    return render_template("country.html", name = "nepal")

@app.route("/sri-lanka")
def srilanka():
    global country
    country = "sri-lanka"
    return render_template("country.html", name = "Sri Lanka")

@app.route("/myanmar")
def myanmar():
    global country
    country = "myanmar"
    return render_template("country.html", name = "myanmar")

@app.route("/laos")
def laos():
    global country
    country = "laos"
    return render_template("country.html", name = "laos")

@app.route("/thailand")
def thailand():
    global country
    country = "thailand"
    return render_template("country.html", name = "thailand")

@app.route("/cambodia")
def cambodia():
    global country
    country = "cambodia"
    return render_template("country.html", name = "cambodia")

@app.route("/vietnam")
def vietnam():
    global country
    country = "vietnam"
    return render_template("country.html", name = "vietnam")

@app.route("/taiwan")
def taiwan():
    global country
    country = "taiwan"
    return render_template("country.html", name = "taiwan")


@app.route("/malaysia")
def malaysia():
    global country
    country = "malaysia"
    return render_template("country.html", name = "malaysia")


@app.route("/philippines")
def philippines():
    global country
    country = "philippines"
    return render_template("country.html", name = "philippines")


@app.route("/indonesia")
def indonesia():
    global country
    country = "indonesia"
    return render_template("country.html", name = "indonesia")


@app.route("/timor-leste")
def timorleste():
    global country
    country = "timor-leste"
    return render_template("country.html", name = "timor-leste")


@app.route("/papua-new-guinea")
def papuanewguinea():
    global country
    country = "papua-new-guinea"
    return render_template("country.html", name = "papua-new-guinea")


@app.route("/fiji")
def fiji():
    global country
    country = "fiji"
    return render_template("country.html", name = "fiji")


@app.route("/australia")
def australia():
    global country
    country = "australia"
    return render_template("country.html", name = "australia")


@app.route("/new-zealand")
def newzealand():
    global country
    country = "new-zealand"
    return render_template("country.html", name = "New Zealand")


@app.route("/japan")
def japan():
    global country
    country = "japan"
    return render_template("country.html", name = "japan")


@app.route("/korea-south")
def koreasouth():
    global country
    country = "korea-south"
    return render_template("country.html", name = "South Korea")


@app.route("/mongolia")
def mongolia():
    global country
    country = "mongolia"
    return render_template("country.html", name = "mongolia")


@app.route("/china")
def china():
    global country
    country = "china"
    return render_template("country.html", name = "china")


@app.route("/kazakhstan")
def kazakhstan():
    global country
    country = "kazakhstan"
    return render_template("country.html", name = "kazakhstan")


@app.route("/russia")
def russia():
    global country
    country = "russia"
    return render_template("country.html", name = "russia")


@app.route("/madagascar")
def madagascar():
    global country
    country = "madagascar"
    return render_template("country.html", name = "madagascar")


@app.route("/western-sahara")
def westernsahara():
    global country
    country = "western-sahara"
    return render_template("country.html", name = "Western Sahara")


@app.route("/senegal")
def senegal():
    global country
    country = "senegal"
    return render_template("country.html", name = "senegal")


@app.route("/gambia")
def gambia():
    global country
    country = "gambia"
    return render_template("country.html", name = "gambia")


@app.route("/guinea-bissau")
def guineabissau():
    global country
    country = "guinea-bissau"
    return render_template("country.html", name = "guinea-bissau")


@app.route("/guinea")
def guinea():
    global country
    country = "guinea"
    return render_template("country.html", name = "guinea")


@app.route("/sierra-leone")
def sierraleone():
    global country
    country = "sierra-leone"
    return render_template("country.html", name = "sierra-leone")


@app.route("/liberia")
def liberia():
    global country
    country = "liberia"
    return render_template("country.html", name = "liberia")

@app.route("/cote-divoire")
def cotedivoire():
    global country
    country = "cote-divoire"
    return render_template("country.html", name = "Cote d'Ivoire")


@app.route("/benin")
def benin():
    global country
    country = "benin"
    return render_template("country.html", name = "benin")


@app.route("/togo")
def togo():
    global country
    country = "togo"
    return render_template("country.html", name = "togo")


@app.route("/equatorial-guinea")
def equatorialguinea():
    global country
    country = "equatorial-guinea"
    return render_template("country.html", name = "Equatorial Guinea")


@app.route("/gabon")
def gabon():
    global country
    country = "gabon"
    return render_template("country.html", name = "gabon")


@app.route("/ghana")
def ghana():
    global country
    country = "ghana"
    return render_template("country.html", name = "ghana")


@app.route("/djibouti")
def djibouti():
    global country
    country = "djibouti"
    return render_template("country.html", name = "djibouti")


@app.route("/uganda")
def uganda():
    global country
    country = "uganda"
    return render_template("country.html", name = "uganda")


@app.route("/rwanda")
def rwanda():
    global country
    country = "rwanda"
    return render_template("country.html", name = "rwanda")


@app.route("/burundi")
def burundi():
    global country
    country = "burundi"
    return render_template("country.html", name = "burundi")


@app.route("/malawi")
def malawi():
    global country
    country = "malawi"
    return render_template("country.html", name = "malawi")


@app.route("/mozambique")
def mozambique():
    global country
    country = "mozambique"
    return render_template("country.html", name = "mozambique")


@app.route("/lesotho")
def lesotho():
    global country
    country = "lesotho"
    return render_template("country.html", name = "lesotho")


@app.route("/morocco")
def morocco():
    global country
    country = "morocco"
    return render_template("country.html", name = "morocco")


@app.route("/tunisia")
def tunisia():
    global country
    country = "tunisia"
    return render_template("country.html", name = "tunisia")


@app.route("/algeria")
def algeria():
    global country
    country = "algeria"
    return render_template("country.html", name = "algeria")


@app.route("/libya")
def libya():
    global country
    country = "libya"
    return render_template("country.html", name = "libya")


@app.route("/egypt")
def egypt():
    global country
    country = "egypt"
    return render_template("country.html", name = "egypt")


@app.route("/eritrea")
def eritrea():
    global country
    country = "eritrea"
    return render_template("country.html", name = "eritrea")


@app.route("/mauritania")
def mauritania():
    global country
    country = "mauritania"
    return render_template("country.html", name = "mauritania")


@app.route("/burkina-faso")
def burkinafaso():
    global country
    country = "burkina-faso"
    return render_template("country.html", name = "Burkina Faso")


@app.route("/mali")
def mali():
    global country
    country = "mali"
    return render_template("country.html", name = "mali")


@app.route("/niger")
def niger():
    global country
    country = "niger"
    return render_template("country.html", name = "niger")


@app.route("/nigeria")
def nigeria():
    global country
    country = "nigeria"
    return render_template("country.html", name = "nigeria")


@app.route("/chad")
def chad():
    global country
    country = "chad"
    return render_template("country.html", name = "chad")


@app.route("/cameroon")
def cameroon():
    global country
    country = "cameroon"
    return render_template("country.html", name = "cameroon")


@app.route("/angola")
def angola():
    global country
    country = "angola"
    return render_template("country.html", name = "angola")


@app.route("/sudan")
def sudan():
    global country
    country = "sudan"
    return render_template("country.html", name = "sudan")


@app.route("/ethiopia")
def ethiopia():
    global country
    country = "ethiopia"
    return render_template("country.html", name = "ethiopia")


@app.route("/somalia")
def somalia():
    global country
    country = "somalia"
    return render_template("country.html", name = "somalia")


@app.route("/central-african-republic")
def centralafricanrepublic():
    global country
    country = "central-african-republic"
    return render_template("country.html", name = "Central African Republic")


@app.route("/congo-brazzaville")
def congobrazzaville():
    global country
    country = "congo-brazzaville"
    return render_template("country.html", name = "congo-brazzaville")


@app.route("/congo-kinshasa")
def congokinshasa():
    global country
    country = "congo-kinshasa"
    return render_template("country.html", name = "congo-kinshasa")


@app.route("/tanzania")
def tanzania():
    global country
    country = "tanzania"
    return render_template("country.html", name = "tanzania")


@app.route("/zambia")
def zambia():
    global country
    country = "zambia"
    return render_template("country.html", name = "zambia")


@app.route("/kenya")
def kenya():
    global country
    country = "kenya"
    return render_template("country.html", name = "kenya")


@app.route("/namibia")
def namibia():
    global country
    country = "namibia"
    return render_template("country.html", name = "namibia")


@app.route("/botswana")
def botswana():
    global country
    country = "botswana"
    return render_template("country.html", name = "botswana")


@app.route("/zimbabwe")
def zimbabwe():
    global country
    country = "zimbabwe"
    return render_template("country.html", name = "zimbabwe")


@app.route("/south-africa")
def southafrica():
    global country
    country = "south-africa"
    return render_template("country.html", name = "South Africa")

lookup()


