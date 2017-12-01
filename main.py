from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.config import Config

import time

class RPiClock(BoxLayout):
	timeString = StringProperty()
	dateString = StringProperty()

	def __init__(self, **kwargs):
		super(RPiClock, self).__init__(**kwargs)
	
	def update(self, *args):
		self.timeString = str(time.strftime("%I:%M:%S %p"))
		self.dateString = str(time.strftime("%A, %B %d, %Y"))


class RPiClockApp(App):

	def build(self):
		Config.set('graphics', 'width', '800')
		Config.set('graphics', 'height', '480')
		appWindow = RPiClock()
		Clock.schedule_interval(appWindow.update, 1)
		return appWindow

if __name__ == "__main__":
	RPiClockApp().run()