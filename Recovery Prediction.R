

library(quantmod)
library(stargazer)
library(fredr)
library(tidyr)
library(PASWR2)
library(MASS)
library(repmis)
library(latex2exp)
library(dplyr)
library(ggplot2)
library(tidyverse)
library(RCurl)
library(haven)
library(forecast)
library(depmixS4)
library(do)
library(tseries)
library(mFilter)
library(ggplot2)
library(forecast)
library(psych)
install.packages(psych)
fredr_set_key('30e6ecb242a73869e11cb35f6aa3afc3') # Copy and paste your FREDR key.

#identify potential influential variables / data and plot to assess trends
#recovery indicator 
#yield curve inverted or not
#gdp growth - do we have this

rm(list = ls())
recovery = drop_na(fredr('USREC',observation_start = as.Date("1989-01-01")))
recovery[which(recovery$value==0),]$value=2
recovery[which(recovery$value==1),]$value=0
recovery[which(recovery$value==2),]$value=1
plot(recovery$date, recovery$value)
yieldcurve = fredr('T10Y3MM')

# Variable yieldcurve
plot(yieldcurve$date, yieldcurve$value,pch=16)
lines(yieldcurve$date, yieldcurve$value)

#US GDP Growth Y/Y (Quarterly)
gdpgrowth = drop_na(fredr("A191RO1Q156NBEA",observation_start = as.Date("1989-01-01")))
plot(gdpgrowth$date, gdpgrowth$value, pch=16, col='blue',
     xlab="Date", ylab="Y/Y % Change",
     main="US Real Quarterly GDP Y/Y Growth")
grid(lw=2)
lines(gdpgrowth$date, gdpgrowth$value, col='blue')
abline(v=as.Date("2008-09-30"), col="red")  
gdpgrowth

#PCchange
pcchange = drop_na(fredr("DPCERL1Q225SBEA",observation_start = as.Date("1989-01-01")))
plot(pcchange$date, pcchange$value,pch=8)
lines(pcchange$date, pcchange$value)
pcchange
unrate = fredr(series_id = "UNRATE")
pcchange 
#

#US Employment Growth Rate
empgrowth = drop_na(fredr(series_id = "PRS85006012", observation_start = as.Date("1989-01-01")))
plot(empgrowth$date, empgrowth$value, col = 'blue', main="US Employment Growth",
     pch=16, ylab = "Rate", xlab = "Date")
grid(lw=2)
lines(empgrowth$date, empgrowth$value, col = 'blue')
abline(v=as.Date("2008-09-30"), col="red")


#Weekly Unemployment Insurance Claims 
claims = drop_na(fredr(series_id = "ICSA", observation_start = as.Date("1989-01-01")))
claims$value = claims$value / 10000000
plot(claims$date, claims$value, col = 'blue', main="Weekly UI Claims",
     pch=16, ylab = "Claims (Millions)", xlab = "Date")
grid(lw=2)
lines(claims$date, claims$value, col = 'blue')
abline(v=as.Date("2008-09-30"), col="red")
claims

## Merge into single time-series dataset
data = merge(recovery, yieldcurve, by.x='date', by.y='date')
data = merge(data, gdpgrowth, by.x='date', by.y='date')
data=merge(data,pcchange,by.x='date', by.y='date')
data=merge(data,unrate,by.x='date', by.y='date')
data

names = c("date", "rec", "recovery","y", "yieldcurve", "g", "gdpgrowth","pc","pcchange"
          ,"u","unrate" )
colnames(data)=names
sub=subset(data, select = c(recovery,yieldcurve,gdpgrowth,pcchange,unrate))
head(sub)
corr.test(sub,use='complete')

data$yieldcurve = data$yieldcurve * 100
plot(data$date,data$recovery,pch=8)
lines(data$date,data$recovery)
par(new=TRUE)
plot(data$date,data$yieldcurve,pch=8,col='blue')
lines(data$date,data$yieldcurve,col='blue')
par(new=TRUE)
plot(data$date,data$gdp,pch=8,col='red')
summary(data)
data

data$yieldcurve.l1 = lag(data$yieldcurve, 1)
data
data=subset(data, select = c(recovery,yieldcurve.l1,gdpgrowth,pcchange,unrate))
data

# Linear Regression
model = lm(recovery ~ yieldcurve.l1+gdpgrowth+pcchange+unrate, data=data)
stargazer(model, type="text", title="Recovery Predictor", single.row=TRUE, 
          ci=TRUE, ci.level=0.95)
#Arima

arima = Arima(data$yieldcurve,order=c(1, 0, 1)) 
summary(arima)
plot(forecast(arima, h=8), include=80, col="blue")
fore_yield=data.frame(forecast(arima, h=8))
colnames(fore_yield)=c('yieldcurve.l1',1,2,3,4)
fore_yield

arima = Arima(data$gdpgrowth,order=c(1, 0, 1))
summary(arima)
plot(forecast(arima, h=8), include=80, col="blue")
fore_gdp=data.frame(forecast(arima, h=8))
fore_gdp
colnames(fore_gdp)=c('gdpgrowth',1,2,3,4)

arima = Arima(data$pcchange,order=c(1, 1, 0))
summary(arima)
plot(forecast(arima, h=8), include=80, col="blue")
fore_pcchange=data.frame(forecast(arima, h=8))
fore_pcchange
colnames(fore_pcchange)=c('pcchange',1,2,3,4)

arima = Arima(data$unrate,order=c(1, 0, 1))
summary(arima)
plot(forecast(arima, h=8), include=80, col="blue")
fore_unrate=data.frame(forecast(arima, h=8))
colnames(fore_unrate)=c('unrate',1,2,3,4)


#=============================Prediction Start============================
newdata=cbind(fore_yield,fore_gdp,fore_pcchange,fore_unrate)
newdata=subset(newdata, select= c(yieldcurve.l1,gdpgrowth,pcchange,unrate))
newdata         
recovery<-predict(model,newdata,interval="prediction")
recovery
plot(recovery)
#============================Prediction End============================


