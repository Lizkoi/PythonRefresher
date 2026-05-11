data(mtcars)
attach(mtcars) #makes column names available directly

# Preview data
head(mtcars)

# Fit a linear model with mpg as the dependent variable and wt and hp as the independent variables.
model <- lm(mpg ~ wt + hp)

# View full summary(coefficients, R-squared, F-test, p-values)
summary(model)

# b) Regression assumptions

# 1. Linearity
plot(model, which = 1)

# 2. Independence of errors - Durbin-Watson test
library(lmtest)
dwtest(model)

# 3. Homoscedasticity - Scale location plot
plot(model, which = 3)
bptest(model) #Breusch-Pagan test

# 4. Normality of Residuals
plot(model, which = 2) #Q-Q plot
shapiro.test(residuals(model))

# 5. Multicollinearity : VIF
library(car)
vif(model)

# Perform case diagnostics i.e checking outliers and influential cases

# 1. Standard residuals
std_res <- rstandard(model)
std_res

# 2. Cook's distance
cooksd <- cooks.distance(model)
plot(cooksd, type = 'h', main = "Cook's Distance") # h= histogram, main = title
abline(h = 4/nrow(mtcars), col = 'red', lty = 2)

# 3. Leverage(Hat values)
leverage <- hatvalues(model)
plot(leverage, type = 'h', main = 'Leverage Values')
abline(h = 2 *(2+1)/nrow(mtcars),col = 'blue', lty = 2)

# 4. Covariance ratio
cvr <- covratio(model)
cvr

# All diagnostic plots at once
par(mfrow = c(2,2))
plot(model)
