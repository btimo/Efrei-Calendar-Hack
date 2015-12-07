#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2, logging
from google.appengine.api import urlfetch


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("Deployment successful!")

class CalendarHandler(webapp2.RequestHandler):
	def get(self):

		line_sep = '\r\n'

		key = self.request.get("key")

		defaultUrl = "http://extranet.groupe-efrei.fr/Student/OpenCalendar?key=";

		if not key:
			self.error(304)

		calendarUrl = defaultUrl + key + "&langue=FR"

		# get calendar from EFREI server
		resp = urlfetch.fetch(calendarUrl);



		calendar = resp.content

		keywords = [
			'BEGIN',
			'METHOD',
			'VERSION',
			'PRODID',
			'X-WR-TIMEZONE',
			'X-WR-CALNAME',
			'BEGIN',
			'SUMMARY',
			'DTSTART',
			'DTEND',
			'UID',
			'DTSTAMP',
			'END'
		]

		calendarLines = calendar.split(line_sep)
		lineCount = len(calendarLines) - 1

		while lineCount > 0:
			line = calendarLines[lineCount]

			colonIndex = line.find(':')

			if colonIndex != -1:
				lineKeyword = line[:colonIndex]

				if lineKeyword == 'X-WR-CALNAME':
					calendarLines[lineCount] = 'X-WR-CALNAME:EFREI by Tim'
				elif lineKeyword == "PRODID":
					calendarLines[lineCount] = "PRODID: Btimo"

			if colonIndex == -1 or line[:colonIndex] not in keywords:
				calendarLines.pop(lineCount)

			lineCount -= 1

		corrected = line_sep.join(calendarLines)

		self.response.write(corrected);
		self.response.headers['Content-type'] = 'text/plain; charset: utf-8'

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/efrei_calendar', CalendarHandler)
], debug=True)