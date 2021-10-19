from json import loads

# Reading JSON files
filename = 'config.json'
js = open(filename, 'r')
f = loads(js.read())
js.close()
