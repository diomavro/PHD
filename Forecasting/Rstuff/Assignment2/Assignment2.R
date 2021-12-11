data2 <- read.csv("C:/Users/Dio and Nono/Desktop/Forecasting/Rstuff/Assignment2/Second bi-weekly assignment Train data.csv", sep=";")
data3 <- read.csv("C:/Users/Dio and Nono/Desktop/Forecasting/Rstuff/Assignment2/Second bi-weekly assignment Test data.csv", sep=";")
library(forecast)
library(Mcomp)
library(fpp)


#set to time series monthly
tspassengers <- ts(data2$AirPassengers , frequency = 12)

tspassengers_test <- ts(data3$AirPassengers , frequency = 12)


#drop missing
dtspassengers  <-  na.omit(tspassengers)

#decompose monthly

adec <- decompose(dtspassengers , type = "additive")
mdec <- decompose(dtspassengers , type = "multiplicative")
#dec <- decompose(TS , type = c("additive", "multiplicative"))
plot(mdec, type = "l", ylab = "Index", xlab = "Period")

# Because the sales are changing over time, the additive adjustment risks over adjusting in years where the sales are below average
# and under adjusting in years years where sales are above average, as such the multiplicative adjustment is more appropriate

adtspassengers <- data2$AirPassengers / mdec$seasonal

#Create a seasonally adjusted and non adjusted dataset without missing values
series1 <- na.omit(adtspassengers)
series2 <- na.omit(dtspassengers)

plot(series2, type = "l", ylab = "Number of Passengers", xlab = "Months" )
lines(series1, col = 'red')
legend('topleft', legend = c('Original', 'With adjustment'), 
       col = c('black', 'red'), lty = 1 )

#forecast

fit1  <- ses(series1, alpha = 0.2, h=6)
fit2  <- ses(series1, alpha = 0.8, h=6)

#Fit 2 looks better so we will use that

plot(series1, type = 'l')
lines(fit1$fitted, col= 'red')
lines(fit1$mean, col= 'green')
lines(fit2$fitted, col= 'blue')
lines(fit2$mean, col= 'yellow')
legend('topleft', legend = c('a = 0.2','a = 0.8'),
       col = c('red', 'blue'), lty = 1, cex = 0.8)

model1 <- holt(series1, h=3)
model2 <- holt(series1, damped = TRUE,  h=3)

plot(series1, type = 'l')
lines(model1$fitted , col= 'red')
lines(model2 $fitted , col= 'green')
legend('topleft', legend = c('holt','dampened'),
       col = c('red', 'blue'), lty = 1, cex = 0.8)

#To compare we split our series1 into train and test

train <- series1
test <- tspassengers_test

trainsimple <- ses(train, alpha = 0.8, h=12)
trainholt <- holt(train, h=12)
traindamped <- holt(train, damped = TRUE,  h=12)

#Compute the in sample accuracy
mse_in_simple  <- mean( (train - trainsimple$fitted )^2 )
mse_in_holt  <- mean( (train - trainholt$fitted )^2 )
mse_in_damped  <- mean( (train - traindamped$fitted )^2 )

#Compute the out sample accuracy

mse_out_simple  <- mean( (test - trainsimple$mean )^2 )
mse_out_holt  <- mean( (test - trainholt$mean )^2 )
mse_out_damped  <- mean( (test - traindamped$mean )^2 )

c(mse_in_simple, mse_out_simple)
c(mse_in_holt,mse_out_holt )
c(mse_in_damped, mse_out_damped)

#So the lowest MSE error is the Holt

model1 <- ses(series1, alpha = 0.2, h=12)
model2 <- ses(series1, alpha = 0.8, h=12)
model3 <- holt(series1, h=12)
model4 <- holt(series1, damped = TRUE, h=12)

par(mfrow = c(2,2))
plot(model1);plot(model2)
plot(model3);plot(model4)

#So the intervals are seen in the graphs

#Exercise B

#Make dataset without the first column the data
trainset <- data2[-1]
testset <- data3[-1]

mlr <- lm(power ~ speed, data=trainset)
frc_mlr <- as.numeric(predict(mlr, testset))


plot(data2$power , type = "l", ylab = "power", xlab = "Hours" )

plot(x =data2$power, y = data2$speed, xlab = 'Power', ylab = 'Speed' )

cor(data2$power,data2$speed)
#This is a pretty high level of correlation


#Neural network

#Rescale the data
trainset_s <- trainset
trainset_s$speed <- (trainset_s$speed-min(trainset_s$speed))/(max(trainset_s$speed)-min(trainset_s$speed))
trainset_s$power <- (trainset_s$power-min(trainset_s$power))/(max(trainset_s$power)-min(trainset_s$power))

#Rescale the data
testset_s <- testset
testset_s$speed <- (testset_s$speed-min(testset_s$speed))/(max(testset_s$speed)-min(testset_s$speed))
testset_s$power <- (testset_s$power-min(testset_s$power))/(max(testset_s$power)-min(testset_s$power))

library(neuralnet)
set.seed(512)
mlp1 <- neuralnet(power ~ speed, data=trainset_s,
                  hidden = 1, act.fct = "logistic", linear.output = FALSE)
#This is our forecast but scaled
frc_mlp_s <- as.numeric(predict(mlp1, testset_s))

#Now we unscale it
frc_mlp <- frc_mlp_s*(max(trainset$power)-min(trainset$power))+min(trainset$power)
data.frame(frc_mlp,testset$power)
#So this is our prediction  the data

#RMSE of regression and neural network
sqrt(mean((testset$Weight-frc_mlr)^2))
sqrt(mean((testset$power-frc_mlp)^2))


