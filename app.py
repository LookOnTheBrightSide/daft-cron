from celery import Celery

app = Celery('app', broker='amqp://localhost//')

@app.task
def reverse(string):
    return string[::-1]

@app.task
def isPalindrome(string):
	def reverse(string):
		return string[::-1]
	return string == reverse(string)

	





