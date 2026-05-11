# STATISTICAL MODELLING ASSIGNMENT ONE
**The Analysis of the Fuel Consumption (mtcars) Dataset**

---

## 1. Introduction and Data Overview
The `mtcars` (Motor Trend Car Road Tests) dataset is a cornerstone of statistical education, originally appearing in the 1974 issue of Motor Trend magazine. It comprises fuel consumption and ten aspects of automobile design and performance for 32 automobiles (1973–74 models).

This report provides a rigorous multiple linear regression analysis to investigate the impact of car weight (`wt`) and gross horsepower (`hp`) on fuel efficiency, measured in Miles Per Gallon (`mpg`). The objective is to fit a predictive model, interpret the underlying dynamics of these variables, and validate the model through extensive diagnostic testing of regression assumptions.

## 2. Methodology and Model Fitting
To begin the analysis, the dataset is loaded into the R environment, and a multiple linear regression model is specified.

```r
# Load and prepare data
data(mtcars)
attach(mtcars)

# Fit the multiple linear regression model
# mpg: Dependent variable
# wt, hp: Independent variables
model <- lm(mpg ~ wt + hp, data = mtcars)

# Display regression summary
summary(model)
```

### 2.1. Linear Model Results

#### (i) The Fitted Model
From the regression coefficients (Estimates) provided by the `summary(model)` output, the fitted regression equation is:
$$\widehat{mpg} = 37.2273 - 3.8778(wt) - 0.0318(hp)$$
Where:
- **wt** is measured in 1,000 lbs.
- **hp** is measured in gross horsepower.

#### (ii) Model Significance
To evaluate if the model is significant at the **5% level** ($\alpha = 0.05$):
- **F-statistic:** 69.21
- **p-value:** $9.11 \times 10^{-12}$

**Conclusion:** Since the p-value is extremely small ($< 0.05$), we reject the null hypothesis ($H_0: \beta_1 = \beta_2 = 0$). There is overwhelming evidence that at least one of the predictors (weight or horsepower) has a significant linear relationship with fuel efficiency. The overall model is statistically significant.

#### (iii) Interpretation of Regression Coefficients
*   **Intercept (37.2273):** This represents the theoretical fuel efficiency of a car with zero weight and zero horsepower. While practically impossible, it serves as the baseline for the model.
*   **Weight (wt) coefficient (-3.8778):** Holding horsepower constant, each additional 1,000 lbs of weight is associated with an average decrease of **3.878 mpg**. This relationship is statistically significant ($p < 0.001$).
*   **Horsepower (hp) coefficient (-0.0318):** Holding weight constant, each additional unit of horsepower is associated with an average decrease of **0.032 mpg**. This relationship is also statistically significant ($p = 0.001$).

#### (iv) R-squared and Adjusted R-squared
*   **R-squared (0.8268):** This value indicates that approximately **82.68%** of the total variance in `mpg` is explained by the combination of vehicle weight and horsepower. It measures the proportion of variation in the dependent variable that is predictable from the independent variables.
*   **Adjusted R-squared (0.8148):** This is a modified version of R-squared that has been adjusted for the number of predictors in the model. Since adding more variables (even irrelevant ones) always increases R-squared, the Adjusted R-squared provides a more realistic estimate of the model's explanatory power and generalizability. Here, 81.48% of the variance is explained after accounting for the degrees of freedom.

---

## 3. Regression Assumptions and Diagnostic Checks
A valid linear regression model requires the fulfillment of several key assumptions. Each is checked below using both graphical and statistical methods.

### 3.1. Linearity
**Check:** The relationship between the independent variables and the dependent variable should be linear. This is checked using the **Residuals vs Fitted** plot and raw scatter plots.

```r
# Linearity check
plot(model, which = 1)
```
![Linearity Check](linearity_check.png)

**Interpretation:** In the Residuals vs Fitted plot, the points are randomly scattered around the zero line without any distinctive non-linear shape (such as a U-curve). This indicates that the linearity assumption is satisfied.

### 3.2. Independence of Errors
**Check:** Residuals should not be correlated with each other. This is tested using the **Durbin-Watson test** and the **ACF** plot.

```r
library(lmtest)
dwtest(model)
acf(residuals(model))
```
![ACF Plot](acf_plot.png)

**Interpretation:** The Durbin-Watson statistic is **1.362**. Typically, a value near 2 suggests no autocorrelation. While 1.362 indicates a slight positive autocorrelation, it is within the acceptable range for a small cross-sectional dataset like `mtcars`. The ACF plot shows no significant lags, confirming independence.

### 3.3. Constant Variance (Homoscedasticity)
**Check:** The variance of the residuals should be constant across all levels of the independent variables. This is checked via the **Scale-Location** plot and the **Breusch-Pagan test**.

```r
# Homoscedasticity check
bptest(model)
plot(model, which = 3)
```
![Homoscedasticity Check](homoscedasticity_check.png)

**Interpretation:** The Breusch-Pagan test yields a p-value of **0.6438** ($> 0.05$), failing to reject the null hypothesis of homoscedasticity. The Scale-Location plot shows a relatively horizontal line with points spread evenly, confirming that the assumption of constant variance holds.

### 3.4. Normality of Residuals
**Check:** The residuals of the model should follow a normal distribution. This is verified using the **Normal Q-Q** plot and the **Shapiro-Wilk test**.

```r
# Normality check
shapiro.test(residuals(model))
plot(model, which = 2)
```
![Normality Check](normality_check.png)

**Interpretation:** The Shapiro-Wilk test p-value is **0.0343**. While slightly below 0.05, the Q-Q plot shows that most residuals fall closely along the diagonal line, with only minor deviations at the tails. Given the robustness of the t-test and F-test, this slight deviation is generally considered acceptable for this sample size ($n=32$).

### 3.5. Multicollinearity
**Check:** Independent variables should not be highly correlated with each other. This is measured using the **Variance Inflation Factor (VIF)**.

```r
library(car)
vif(model)
```
**Interpretation:** The VIF for both `wt` and `hp` is **1.767**. Since these values are well below the common threshold of 5 (or 10), we conclude that multicollinearity is not an issue in this model. The predictors are sufficiently independent.

---

## 4. Case Diagnostics and Influential Observations
Beyond the basic assumptions, it is crucial to identify outliers or cases that disproportionately influence the model's parameters.

```r
# Influential case diagnostics
# Thresholds: Cook's D > 4/n, Leverage > 2(k+1)/n
par(mfrow = c(2, 2))
plot(model)
```
![Case Diagnostics](case_diagnostics.png)

### 4.1. Standardized Residuals
Most standardized residuals fall within the $[-2, 2]$ range, indicating that there are no extreme outliers in the response variable (`mpg`).

### 4.2. Cook's Distance
Using the threshold of $4/32 = 0.125$, we observe that a few points (e.g., Maserati Bora) have higher influence than others. However, they do not exceed values that would typically necessitate removal (such as 1.0).

### 4.3. Leverage (Hat Values)
The leverage threshold is calculated as $2(k+1)/n = 2(3)/32 = 0.1875$. Points above this line have "unusual" values for `wt` or `hp`. While some cars have high leverage, they do not necessarily distort the model unless they also have high residuals.

### 4.4. Covariance Ratio (COVRATIO)
The COVRATIO values for most cars are near 1, suggesting that no single observation is having an outsized impact on the precision of the model's coefficient estimates.

---

## 5. Conclusion
The multiple linear regression model successfully explains over **82%** of the variation in car fuel efficiency using weight and horsepower as predictors. Both weight and horsepower have significant negative impacts on `mpg`, which aligns with physical and engineering expectations.

Diagnostic testing confirms that the model satisfies the assumptions of linearity, independence, and homoscedasticity. While there is a minor departure from perfect normality in the residuals, the model remains robust and provides a highly reliable framework for understanding the factors that influenced fuel economy in vehicles from the mid-1970s.
