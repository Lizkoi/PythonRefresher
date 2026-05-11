import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
import scipy.stats as stats

# Load mtcars dataset
# Since I don't have R, I'll download it or use a common source.
# mtcars is available in statsmodels
mtcars = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data

print("Dataset Head:")
print(mtcars.head())

# a) Linear model
# mpg as dependent, wt and hp as independent
model = smf.ols('mpg ~ wt + hp', data=mtcars).fit()

print("\nModel Summary:")
print(model.summary())

# (i) Fitted model: mpg = beta0 + beta1*wt + beta2*hp
print(f"\nFitted Model: mpg = {model.params['Intercept']:.4f} + ({model.params['wt']:.4f})*wt + ({model.params['hp']:.4f})*hp")

# (ii) Significance
print(f"\nModel F-statistic p-value: {model.f_pvalue:.4e}")

# (iii) Coefficients
print("\nCoefficients:")
print(model.params)
print("\nCoefficients P-values:")
print(model.pvalues)

# b) Regression assumptions

# 1. Linearity: Plot Observed vs Predicted or Residuals vs Predicted
plt.figure(figsize=(10, 6))
sns.residplot(x=model.fittedvalues, y=mtcars['mpg'], lowess=True, line_kws={'color': 'red', 'lw': 1})
plt.title('Residuals vs Fitted (Linearity check)')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.savefig('linearity_check.png')
plt.close()

# 2. Independence of errors: Durbin-Watson
dw_stat = durbin_watson(model.resid)
print(f"\nDurbin-Watson statistic: {dw_stat:.4f}")

# 3. Constant variance: Breusch-Pagan test or Scale-Location plot
plt.figure(figsize=(10, 6))
plt.scatter(model.fittedvalues, np.sqrt(np.abs(model.get_influence().resid_studentized_internal)))
sns.regplot(x=model.fittedvalues, y=np.sqrt(np.abs(model.get_influence().resid_studentized_internal)), lowess=True, scatter=False, line_kws={'color': 'red'})
plt.title('Scale-Location (Homoscedasticity check)')
plt.xlabel('Fitted values')
plt.ylabel('sqrt(|Standardized Residuals|)')
plt.savefig('homoscedasticity_check.png')
plt.close()

# 4. Normality of residuals: Q-Q plot
plt.figure(figsize=(10, 6))
stats.probplot(model.resid, dist="norm", plot=plt)
plt.title('Normal Q-Q (Normality check)')
plt.savefig('normality_check.png')
plt.close()

# 5. Multicollinearity: VIF
X = mtcars[['wt', 'hp']]
X = sm.add_constant(X)
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
print("\nVIF Data:")
print(vif_data)
