import requests, json, time

codeStrings = { 
		0	: "Expect tornadoes",
		1	: "Expect a tropical storm",
		2	: "Expect a hurricane",
		3	: "Expect severe thunderstorms",
		4	: "Expect thunderstorms",
		5	: "Expect mixed rain and snow",
		6	: "Expect mixed rain and sleet",
		7	: "Expect mixed snow and sleet",
		8	: "Expect a freezing drizzle",
		9	: "Expect a drizzle",
		10	: "Expect freezing rain",
		11	: "Expect showers",
		12	: "Expect showers",
		13	: "Expect snow flurries",
		14	: "Expect light snow showers",
		15	: "Expect blowing snow",
		16	: "Expect snow",
		17	: "Expect hail",
		18	: "Expect sleet",
		35	: "Expect mixed rain and hail",
		37	: "Expect isolated thunderstorms",
		38	: "Expect scattered thunderstorms",
		39	: "Expect scattered thunderstorms",
		40	: "Expect scattered showers",
		41	: "Expect heavy snow",
		42	: "Expect scattered snow showers",
		43	: "Expect heavy snow",
		45	: "Expect thundershowers",
		46	: "Expect snow showers",
		47	: "Expect isolated thundershowers"
	}

class Weather():
	def __init__(self):
		self.location="Orange,CA"
		self.update()
	def update(self):
		baseurl = "https://query.yahooapis.com/v1/public/yql?q="
		query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+self.location+'")'
		form = "&format=json"
		r = requests.get(baseurl+query+form)

		if (r.status_code==200):
			jsonData = json.loads(r.text)
			forecasts = jsonData["query"]["results"]["channel"]["item"]["forecast"]

			for forecast in forecasts:
				forecast["high"] = int(forecast["high"])
				forecast["low"] = int(forecast["low"])
				forecast["code"] = int(forecast["code"])
				forecast["date"] = time.strptime(forecast["date"], "%d %b %Y")

			self.forecasts = forecasts

			self.temperature = jsonData["query"]["results"]["channel"]["item"]["condition"]["temp"]
			self.condition = jsonData["query"]["results"]["channel"]["item"]["condition"]["text"]

	def todayForecastString(self):
		f = self.forecasts[0]
		return self.condition + "\n" + str(f["high"]) + "/" + str(f["low"])

	def generateString(self, threshold=10):
		today = self.forecasts[0]

		for i in range(1,len(self.forecasts)):
			forecast = self.forecasts[i]
			nextString = ""

			#If it's the next week, specify that.
			if i >= 7:
				nextString = "next "

			weekday = nextString + time.strftime("%A",forecast["date"])

			if forecast["code"] in codeStrings:
				return codeStrings[forecast["code"]] + " for " + weekday + "."

			if forecast["high"] >= today["high"]+threshold:
				return "Expect a warm up by " + weekday + "."

			if forecast["high"] <= today["high"]-threshold:
				return "Expect a cool down by " + weekday + "."

			if forecast["low"] >= today["low"]+threshold:
				return "Expect a warm up by " + weekday + "."

			if forecast["low"] <= today["low"]-threshold:
				return "Expect a cool down by " + weekday + "."

		return "The forecast is clear."


if __name__ == "__main__":
	w = Weather()
	print(w.generateString())
	print(w.temperature)