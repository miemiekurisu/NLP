import bayes


total=0.0
reload(bayes)

for i in range(1,20):
     total+=bayes.spamTest()

print total/100