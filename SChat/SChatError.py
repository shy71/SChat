from SChat import ServerError
def toSChatError(serverError):
	return SChatError('Server Error: '+ServerError.errorsStr[int(serverError)])
class SChatError(Exception):
	def __init__(self,msg):
		self.msg=msg
	def __str__(self):
		return self.msg
	def __radd__(self,x):
		return str(x)+str(self) + self.ormsg
