from zxcvbn import zxcvbn


password = input("enter your password to test: ")

result = zxcvbn(password)
print ("password strengh score: ", result['score'])
print("Feedback(its ass): ", result['feedback'])