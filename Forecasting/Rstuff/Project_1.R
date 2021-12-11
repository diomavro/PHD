data <- read.csv("C:/Users/DavidEttinger02/Desktop/Forecasting/Bi-weekly assignment data.csv")
View(data)
# window(data$Date, start=c(day=1, month=1,  year=2019) ,end= c(day=31 , month=12, year=2021 ), frequency = 1 ) 
library(forecast)
#Part A

#x <- as.Date(data$Date, format = "%d-%m-%y")
# Visualize
plot(data$Company.Sales , type = "l", main = "Shopping", ylab = "Company.sales", xlab = "Date" )

#data$prices <- data$Company.Sales/data$Product.Sales #deduce the price

#missing values
for (i in (frequency(data$Company.Sales)+1): (length(data$Company.Sales)-12)){
  if (is.na(data$Company.Sales[i])==TRUE){
    print(i)
    data$Company.Sales[i] <- mean(c(data$Company.Sales[i-frequency(data$Company.Sales)], data$Company.Sales[i+frequency(data$Company.Sales)]))
    if (is.na(data$Company.Sales[i])==TRUE){
      data$Company.Sales[i] <- mean(c(data$Company.Sales[i-frequency(data$Company.Sales) ], data$Company.Sales[i-1 - frequency(data$Company.Sales)]))
      #if the forward slots are empty we simply take the average of the two older slots
    }
  }
}

#outliers
lowerlimit <- quantile(data$Company.Sales,0.95)
upperlimit <- quantile(data$Company.Sales,0.05)
n_data1 <- data$Company.Sales
n_data1[n_data1>lowerlimit] <- lowerlimit
n_data1[n_data1<upperlimit] <- upperlimit

plot(data$Company.Sales, type = "l", ylab = "Company sales", xlab = "year", main = "Company Sales")
lines(n_data1, col = "red")
legend("center", legend = c("Original", "Trimmed"),col, c("black","red"),lty=1)

#limit <- quantile(data$Product.Sales,0.80)
#n_data2 <- data$Product.Sales
#n_data2[n_data2>limit] <- limit
#plot(data$Product.Sales, type = "l", ylab = "Company sales", xlab = "year", main = "Company Sales")
#lines(n_data1, col = "red")
#legend("center", legend = c("Original", "Trimmed"),col, c("black","red"),lty=1)

#makeweekly

# Coerce to Date class(it says double)
data$Date <- as.Date(data$Date , format = '%d-%m-%Y')
# Extract day of the week (Saturday = 6)
data$Week_Day <- as.numeric(format(data$Date, format='%w'))
# Adjust end-of-week date (first saturday from the original Date)
data$End_of_Week <- data$Date + (6 - data$Week_Day)
# Aggregate over week and climate division
weeklydata <- aggregate(data$Company.Sales~data$End_of_Week, FUN=mean, data=data, na.rm=TRUE)

#makemonthly
short.date = strftime(data$Date , "%Y/%m")
monthlydata = aggregate(data$Company.Sales ~ short.date, FUN = sum)

#rename
names(weeklydata)[names(weeklydata) == "data$End_of_Week"] <- "Endofweek"
names(weeklydata)[names(weeklydata) == "data$Company.Sales"] <- "weekly"

names(monthlydata)[names(monthlydata) == "short.date"] <- "Month"
names(monthlydata)[names(monthlydata) == "data$Company.Sales"] <- "monthlysales"



#visualize monthly
plot(monthlydata$monthlysales , type = "l", main = "Monthly", ylab = "monthlysales", xlab = "Date" )
plot(weeklydata$weekly , type = "l", main = "Weekly", ylab = "WeeklySales", xlab = "Date" )


#decompose monthly
TS <- ts(monthlydata$monthlysales, frequency = 12)
dec <- decompose(TS , type = "additive")
#dec <- decompose(TS , type = c("additive", "multiplicative"))
plot(dec, type = "l", ylab = "Index", xlab = "Period")

#Average

mean(data$Company.Sales)

mean(monthlydata$monthlysales)


#Part B

#visualize
plot(data$Product.Sales , type = "l", main = "Shopping", ylab = "Product.sales", xlab = "Date" )

#Average Daily demand
mean(data$Product.Sales)
#Coefficient of Variation
sd(data$Product.Sales[0<data$Product.Sales])*100/mean(data$Product.Sales[0<data$Product.Sales])
#ADI
nonzero <- length(which(data$Product.Sales != 0))
zero <- length(which(data$Product.Sales != 0))
#the rate is: 
rate <-zero/(nonzero+zero)
#So we inverse this to get the average expected days
Avgwait <- 1/rate

library(fpp)
library(forecast)

plot(data$Product.Sales , type = "l", ylab = "Quantity", xlab = "days", main = "Sold product")

par(mfrow = c(1,3))
boxplot(data$Product.Sales, main = "Boxplot Quantity" )
hist(data$Product.Sales )
plot(density(data$Product.Sales), main = "Kernel Density of Quantity")

density(data$Product.Sales)

quantile(data$Product.Sales,0.05)
quantile(data$Product.Sales,0.5)
quantile(data$Product.Sales,0.95)

#makemonthly
qdate = strftime(data$Date , "%Y/%m")
qmonthlydata = aggregate(data$Product.Sales ~ qdate, FUN = sum)

#rename
names(qmonthlydata)[names(qmonthlydata) == "qdate"] <- "Month"
names(qmonthlydata)[names(qmonthlydata) == "data$Product.Sales"] <- "monthlysales"

#visualize monthly
plot(qmonthlydata$monthlysales , type = "l", main = "Monthly", ylab = "monthlysales", xlab = "Date" )

#decompose monthly
TS <- ts(qmonthlydata$monthlysales, frequency = 12)
dec <- decompose(TS , type = "additive")
#dec <- decompose(TS , type = c("additive", "multiplicative"))
plot(dec, type = "l", ylab = "Index", xlab = "Period")
#It appears like the trend is that 2 small spikes and one big one every 12 months. 
#Checking this effect manually confirms the intuition that it must be Christmas

#
#plot(forecast(etc(time_series$Company.Sales, 1 )))