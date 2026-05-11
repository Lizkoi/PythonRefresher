# Load the mtcars dataset
data(mtcars)
# attach(mtcars) # Optional, but requested in prompt

# a) Linear model
# Fit a linear model with mpg as the dependent variable and wt and hp as the independent variables.
model <- lm(mpg ~ wt + hp, data = mtcars)

# Display the summary of the model
summary(model)

# (i) The fitted model can be written as:
# mpg = 37.227 - 3.878 * wt - 0.032 * hp

# (ii) Significance at 5% level:
# The F-statistic is 69.21 with a p-value of 9.109e-12, which is < 0.05.
# Thus, the model is significant.

# (iii) Interpretation of regression coefficients:
# Intercept (37.227): The predicted mpg for a car with 0 weight and 0 horsepower.
# wt (-3.878): For each 1000lb increase in weight, mpg decreases by 3.878, holding hp constant.
# hp (-0.032): For each unit increase in horsepower, mpg decreases by 0.032, holding wt constant.

# (iv) R-squared and Adjusted R-squared:
# R-squared (0.8268): 82.68% of the variance in mpg is explained by wt and hp.
# Adjusted R-squared (0.8148): Adjusts R-squared for the number of predictors.

# b) Regression assumptions

# Set up a 2x2 grid for plots
par(mfrow = c(2, 2))

# 1. Linearity: Residuals vs Fitted plot
plot(model, which = 1)
# Interpretation: Points should be randomly scattered around the horizontal line.

# 2. Independence of errors:
# A plot of residuals vs order can be used.
plot(residuals(model), type = 'b', main = "Residuals vs Order", ylab = "Residuals")
# Alternatively, use Durbin-Watson test if library(car) is available
# library(car)
# durbinWatsonTest(model)

# 3. Constant variance (Homoscedasticity): Scale-Location plot
plot(model, which = 3)
# Interpretation: The line should be approximately horizontal.

# 4. Normality of residuals: Normal Q-Q plot
plot(model, which = 2)
# Interpretation: Points should follow the diagonal dashed line.
shapiro.test(residuals(model))

# 5. Multicollinearity:
# Using Variance Inflation Factor (VIF)
# library(car)
# vif(model)
# For 2 predictors, we can also check correlation:
cor(mtcars$wt, mtcars$hp)
