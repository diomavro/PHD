x = 2
#Piecewise 
y = x^2
# Comparing with logical conditions, simply type vectors and <, ==, !=
#Remove variables using remove=rm, rm(x)
# Vector x= c(1,2,3,4) = 1:4
# You can add vectors, so z = x+y, will add each components
# you can make a vector of five tens by doing Rep(10,5)
#To reference the third element you simply say x[3] 
#or you can use it to set that value, x[3] or set last 2 values x[4:5]=c(1,12)
#conditional operations on vectors:
# to make all values greater than 2 into a 5 we do x[x>2]=5
# or x[x==12] = 5 or into a the mean of x, x[x==12] = mean(x)
# Creating a sequence
# y = seq(1, 100, by = 2)
# You can also z = c(1:4,4,10, Inf)
#Check to see if condition is met, is.na(z). 
#Make all na into 0 z[is.na(z)==T]=0
# Names list: z = c('BOB', 'STEVE')
# Arrays and matrices
# Make an array, x = 1:10
# put x in an matrix dim(x) = c(1,10) horizontal or c(10,1) vertical
# We can also put it on two rows, with dim(x) = c(2,5) 
# We can reference specific things the matrix with square brackets [1,2]
# Transposing the matrix is t(x)
# Matrix directly: M = array(c(1,2,3,4),dim=c(2,2)), H=array(0,c(10,2))
#Matrix commands, det, diag, sum(diag()), for inverting we do 'solve', 
#make a matrix with 1 on the diagonal diag(10), *3
#Naming stuff: 
#Commands: View(M), colnames(M)=c('Variable 1', 'Another Thing')
#runif(200, -50, 50)



#How to make a matrix with which is a sum of two random variables
# x = runif(200, -50, 50)
# dim(x) = c(200,1)
# y = runif(200, -50, 50)
# dim(y) = c(200,1)
# z = x+y
#mat = cbind(x,y,z)


#sd(mat(V1))
#plot(x,y)
#data=mat(mat$Day==2,)

#Alternative
#data=runif(100,0,1)
#hist(data)
#hist(data,col2)
#monthly data
#time_series=ts(data,start=c(200,1),frequency=12)
#plot.ts(time_series)
#
#Partition data into in sample and out of sample
#data1 = data[1:80]
#data2 = data[81:length(data)]

#DON't DO THIS!
#ts1 = time_series[1:80]
#ts1

#For time series, do this: 
#ts2=window(time_series, start=c(2001,1),end=c(2002,9))

#tapply(time_series,cycle(time_series), mean)
#?tapply
#tapply(time_series,cycle(time_series), variance)
#
#

