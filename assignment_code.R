data(mtcars)
attach(mtcars)
model <- lm(mpg~wt+hp,data=mtcars)
summary(model)
# Fitted model equation:
# mpg= 37.22727- 3.87783*wt -0.03177*hp

# a) Linear model checks

# linearity
plot(wt,mpg, main='mpg vs wt', pch=19,col='green')
abline(lm(mpg~wt),col='yellow',lwd=2)
plot(hp,mpg,main='mpg vs hp', pch=19,col='pink')
abline(lm(mpg~hp),col='blue',lwd=2)
plot(model,which=1)

# independence of errors
library(car)
durbinWatsonTest(model)
acf(residuals(model))

# constant variance(homoscedasticity)
library(lmtest)
bptest(model)
plot(model,which=3)

# normality of residuals
shapiro.test(residuals(model))
plot(model,which=2)
hist(residuals(model),freq=FALSE,breaks=12)
curve(dnorm(x,mean=mean(residuals(model)),sd=sd(residuals(model))),add=TRUE,col='purple')

# MULTICOLLINEARITY
library(car)
vif(model)
1/vif(model)
mean(vif(model))
cor(mtcars[,c('wt','hp')])

# CASE DIAGNOSTICS
std_resid<-rstandard(model)
std_resid
cooks_d<-cooks.distance(model)
cooks_d
leverage<-hatvalues(model)
leverage
cvr<-covratio(model)
cvr

par(mfrow=c(2,2))
plot(std_resid);abline(h=c(-2,2),col="pink")
plot(cooks_d);abline(h=4/30,col="purple")
plot(leverage,cooks_d);abline(h=4/30,col="yellow")
plot(cvr);abline(h=1,col="pink")
par(mfrow=c(1,1))
