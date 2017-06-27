

class ServerError(Exception):
	def __init__(self,code):
		self.code=int(code)
	def __str__(self):
		return self.errorsStr[self.code]
	def __radd__(self,x):
		return str(x)+str(self)
	errorsStr={11:'The usename is already registered',
		12:'Username isn\'t valid, only lowercase and numbers',
		21:'authnticaion token isn\'t valid, wrong username',
		22:'authnticaion token isn\'t valid, timestamp expired',
		31:'You are not connected!',
		32:'Desired username isn\'t registered',
		33:'Desired user isn\'t connected'}
