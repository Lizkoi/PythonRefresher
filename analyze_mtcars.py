import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from statsmodels.stats.stattools import durbin_watson
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.graphics.tsaplots import plot_acf

# Load mtcars dataset
mtcars = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data

# a) Linear model
model = smf.ols('mpg ~ wt + hp', data=mtcars).fit()

print("--- Model Summary ---")
print(model.summary())

# (i) Fitted model
print(f"\nFitted Model: mpg = {model.params['Intercept']:.5f} - {-model.params['wt']:.5f}*wt - {-model.params['hp']:.5f}*hp")

# b) Regression assumptions

# 1. Linearity
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.scatter(mtcars['wt'], mtcars['mpg'], color='green')
plt.title('mpg vs wt')
plt.subplot(1, 3, 2)
plt.scatter(mtcars['hp'], mtcars['mpg'], color='pink')
plt.title('mpg vs hp')
plt.subplot(1, 3, 3)
sns.residplot(x=model.fittedvalues, y=mtcars['mpg'], lowess=True, line_kws={'color': 'red'})
plt.title('Residuals vs Fitted')
plt.tight_layout()
plt.savefig('linearity_check.png')
plt.close()

# 2. Independence
dw_stat = durbin_watson(model.resid)
print(f"\nDurbin-Watson: {dw_stat:.4f}")
plt.figure()
plot_acf(model.resid)
plt.savefig('acf_plot.png')
plt.close()

# 3. Constant Variance
bp_test = het_breuschpagan(model.resid, model.model.exog)
print(f"\nBreusch-Pagan test p-value: {bp_test[1]:.4f}")
# Scale-location plot (already in previous step, but let's keep it simple)

# 4. Normality
shapiro_test = stats.shapiro(model.resid)
print(f"Shapiro-Wilk test p-value: {shapiro_test.pvalue:.4f}")

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
stats.probplot(model.resid, dist="norm", plot=plt)
plt.title('Normal Q-Q')
plt.subplot(1, 2, 2)
sns.histplot(model.resid, kde=True, color='purple')
plt.title('Histogram of Residuals')
plt.savefig('normality_check.png')
plt.close()

# 5. Multicollinearity
X = mtcars[['wt', 'hp']]
X = sm.add_constant(X)
vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns)
print("\nVIF:")
print(vif)

# 6. Case Diagnostics
influence = model.get_influence()
std_resid = influence.resid_studentized_internal
cooks_d = influence.cooks_distance[0]
leverage = influence.hat_matrix_diag
cvr = influence.cov_ratio

print("\nCase Diagnostics (Samples):")
print(f"Std Residuals (first 5): {std_resid[:5]}")
print(f"Cook's D (first 5): {cooks_d[:5]}")

plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.plot(std_resid, 'o')
plt.axhline(y=2, color='pink'); plt.axhline(y=-2, color='pink')
plt.title('Std Residuals')

plt.subplot(2, 2, 2)
plt.plot(cooks_d, 'o')
plt.axhline(y=4/32, color='purple') # 4/n
plt.title("Cook's D")

plt.subplot(2, 2, 3)
plt.scatter(leverage, cooks_d)
plt.axhline(y=4/32, color='yellow')
plt.title('Leverage vs Cook\'s D')

plt.subplot(2, 2, 4)
plt.plot(cvr, 'o')
plt.axhline(y=1, color='pink')
plt.title('COVRATIO')

plt.tight_layout()
plt.savefig('case_diagnostics.png')
plt.close()
