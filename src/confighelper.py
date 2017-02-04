# Copyright (C) 2017 Andrea Cervesato
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
	These functions have nothing to do with the API, they just help ease
	issues between Python 2 and 3
'''

def get_input(string):
	''' Get input from console regardless of python 2 or 3 '''
	try:
		return raw_input(string)
	except:
		return input(string)

def get_config():
	''' Create a config parser for reading INI files '''
	try:
		import ConfigParser
		return ConfigParser.ConfigParser()
	except:
		import configparser
        return configparser.ConfigParser()
