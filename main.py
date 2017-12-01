from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.config import Config

import time

class RPiClock(BoxLayout):

	def __init__(self, **kwargs):
		super(RPiClock, self).__init__(**kwargs)

class TimeModule(BoxLayout):
	timeString = StringProperty()
	dateString = StringProperty()

	def __init__(self, **kwargs):
		super(TimeModule, self).__init__(**kwargs)

	def update(self, *args):
		lt = time.localtime()
		self.timeString = str(time.strftime("%I:%M:%S %p").lstrip("0"))
		self.dateString = str(time.strftime("%A, %B %d, %Y"))

class UpperRowModule(BoxLayout):
	def __init__(self, **kwargs):
		super(UpperRowModule, self).__init__(**kwargs)

	def update(self, *args):
		self.ids.timeMod.update(*args);

class LowerRowModule(BoxLayout):
	pass

class RPiClockApp(App):

	def build(self):
		Config.set('graphics', 'width', '800')
		Config.set('graphics', 'height', '480')
		self.load_kv('RPiClock.kv')
		appWindow = RPiClock()
		Clock.schedule_interval(appWindow.ids.UpperRow.update, 1)
		return appWindow

if __name__ == "__main__":
	RPiClockApp().run()