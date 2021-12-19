library(Quandl)
library(tidyverse)
library(tidyquant)
library(timetk)
library(forecast)
library(highcharter)

install.packages("RTL")

oil_daily <- Quandl("FRED/DCOILWTICO", 
                    type = "raw", 
                    collapse = "daily",  
                    start_date = "install_github("risktoollib/RTL")2008-01-01", 
                    end_date = "2021-11-11")
                    