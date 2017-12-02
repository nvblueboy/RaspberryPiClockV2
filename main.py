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

class DisneyModule(RelativeLayout):
	rideString = StringProperty()
	counter = 0
	counterUpdated = False

	def __init__(self, **kwargs):
		super(DisneyModule, self).__init__(**kwargs)
		self.rideString = "Getting Ride Times..."

	def update(self, *args):
		strings = ["Space Mountain: 25 minutes", "Indiana Jones: 35 minutes","California Screamin': 10 minutes"]
		if (int(time.time()) % 4 == 0):
			if (not self.counterUpdated):
				self.counter += 1
				if (self.counter == len(strings)):
					self.counter = 0;
				self.counterUpdated = True
				self.rideString = str(strings[self.counter])
		else:
			self.counterUpdated = False

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