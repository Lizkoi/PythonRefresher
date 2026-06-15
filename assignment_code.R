# STATISTICAL MODELLING ASSIGNMENT 1
# Analysis of the mtcars Dataset

# 1. Data Preparation
data(mtcars)
attach(mtcars)

# Preview the dataset
head(mtcars)

# 2. Linear Model Fitting
# Fit a multiple linear regression model with mpg as the dependent variable
# and wt (weight) and hp (horsepower) as independent variables.
model <- lm(mpg ~ wt + hp, data = mtcars)

# Display the full summary of the fitted model
summary(model)

# ---------------------------------------------------------
# a) Linear Model Results (Interpretations in Report)
# ---------------------------------------------------------

# (i) Fitted model equation can be extracted from coefficients:
# mpg = 37.227 - 3.878*wt - 0.032*hp

# (ii) Model Significance: Check F-statistic p-value in summary(model)

# ---------------------------------------------------------
# b) Regression Assumptions
# ---------------------------------------------------------

# Set up plotting area for assumption checks
par(mfrow = c(2, 2))

# 1. Linearity
# Observed vs Predicted and Residuals vs Fitted
plot(model, which = 1, main = "Residuals vs Fitted (Linearity)")

# 2. Independence of Errors
# Using Durbin-Watson test
library(lmtest)
dwtest(model)
# Visual check: ACF plot
acf(residuals(model), main = "ACF of Residuals")

# 3. Constant Variance (Homoscedasticity)
# Visual check: Scale-Location plot
plot(model, which = 3, main = "Scale-Location (Homoscedasticity)")
# Statistical check: Breusch-Pagan test
bptest(model)

# 4. Normality of Residuals
# Visual check: Normal Q-Q plot and Histogram
plot(model, which = 2, main = "Normal Q-Q (Normality)")
hist(residuals(model), freq = FALSE, breaks = 10, main = "Histogram of Residuals", col = "lightblue")
curve(dnorm(x, mean = mean(residuals(model)), sd = sd(residuals(model))), add = TRUE, col = "red", lwd = 2)
# Statistical check: Shapiro-Wilk test
shapiro.test(residuals(model))

# 5. Multicollinearity
library(car)
vif(model)
# Correlation between predictors
cor(mtcars[, c("wt", "hp")])

# ---------------------------------------------------------
# Case Diagnostics: Influence and Outliers
# ---------------------------------------------------------

# Reset plotting area
par(mfrow = c(1, 1))

# 1. Standardized Residuals (Outliers)
std_res <- rstandard(model)
plot(std_res, type = "h", main = "Standardized Residuals")
abline(h = c(-2, 2), col = "red", lty = 2)

# 2. Cook's Distance (Influence)
cooksd <- cooks.distance(model)
plot(cooksd, type = "h", main = "Cook's Distance", ylab = "Cook's distance")
abline(h = 4 / nrow(mtcars), col = "red", lty = 2)

# 3. Leverage Values (Hat values)
leverage <- hatvalues(model)
plot(leverage, type = "h", main = "Leverage Values")
# Threshold: 2*(k+1)/n where k=2
abline(h = 2 * (2 + 1) / nrow(mtcars), col = "blue", lty = 2)

# 4. Covariance Ratio
cvr <- covratio(model)
plot(cvr, main = "Covariance Ratio (COVRATIO)")
abline(h = 1, col = "darkgreen", lty = 2)

# Summary diagnostic plot
par(mfrow = c(2, 2))
plot(model)
par(mfrow = c(1, 1))
