from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.config import Config

import time

import Disneyland, weather, shuttle

class RPiClock(BoxLayout):

	def __init__(self, **kwargs):
		super(RPiClock, self).__init__(**kwargs)

	def setContainer(self, cont):
		self.container = cont;

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update()

class TimeModule(RelativeLayout):
	timeString = StringProperty()
	dateString = StringProperty()

	def __init__(self, **kwargs):
		super(TimeModule, self).__init__(**kwargs)

	def update(self, *args):
		self.timeString = str(time.strftime("%I:%M:%S %p").lstrip("0"))
		self.dateString = str(time.strftime("%A, %B %d, %Y"))

class WeatherModule(BoxLayout):
	currentTempString = StringProperty()
	todayForecastString = StringProperty()
	descriptionString = StringProperty()

	def __init__(self, **kwargs):
		super(WeatherModule, self).__init__(**kwargs)
		currentTempString = "--"
		self.weatherModule = weather.Weather()

	def update(self, *args):
		self.currentTempString = self.weatherModule.temperature + " F"
		self.descriptionString = self.weatherModule.generateString()
		self.todayForecastString = self.weatherModule.todayForecastString()

		##TODO: Implement multithreading here so you don't freeze the UI waiting for a connection.
		if (int(time.time()) % 300 == 0):
			if (not self.moduleUpdated):
				self.weatherModule.update()
				self.moduleUpdated = True
		else:
			self.moduleUpdated = False


class ShuttleModule(RelativeLayout):
	nextShuttleString = StringProperty()
	def __init__(self, **kwargs):
		super(ShuttleModule, self).__init__(**kwargs)
		self.shuttleModule = shuttle.Shuttle()
		self.nextShuttleString = "Getting next shuttle..."
	def update(self, *args):
		t = self.shuttleModule.getUpcoming()
		self.nextShuttleString = "Next shuttles: "+t[0]+",  "+t[1]

class DisneyModule(RelativeLayout):
	rideString = StringProperty()
	counter = 0
	counterUpdated = False
	moduleUpdated = False;

	def __init__(self, **kwargs):
		super(DisneyModule, self).__init__(**kwargs)
		self.rideString = "Getting Ride Times..."
		self.disneyModule = Disneyland.DisneyTimes()

	def update(self, *args):
		strings = self.disneyModule.waitStrings
		if len(strings) == 0:
			strings = ["Disneyland is closed."]
		if (int(time.time()) % 4 == 0):
			if (not self.counterUpdated):
				self.counter += 1
				if (self.counter == len(strings)):
					self.counter = 0;
				self.counterUpdated = True
				self.rideString = str(strings[self.counter])
		else:
			self.counterUpdated = False

		if (int(time.time()) % 300 == 0):
			if (not self.moduleUpdated):
				self.disneyModule.update()
				self.moduleUpdated = True
		else:
			self.moduleUpdated = False

class RPiClockApp(App):

	def build(self):
		Config.set('graphics', 'width', '800')
		Config.set('graphics', 'height', '480')
		self.load_kv('RPiClock.kv')
		appWindow = RPiClock()
		appWindow.setContainer(self)
		Clock.schedule_interval(appWindow.update, .5)
		return appWindow

if __name__ == "__main__":
	RPiClockApp().run()