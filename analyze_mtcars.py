import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
import scipy.stats as stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.graphics.tsaplots import plot_acf

# Load mtcars dataset
mtcars = sm.datasets.get_rdataset("mtcars", "datasets", cache=True).data

# a) Linear model
model = smf.ols('mpg ~ wt + hp', data=mtcars).fit()

# (i) Fitted model
# Results: Intercept=37.22727, wt=-3.87783, hp=-0.03177

# b) Regression assumptions plots

# 1. Linearity & Homoscedasticity & Normality
# We'll regenerate some plots to ensure they match the style requested.

# Linearity Check
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

# Independence (ACF)
plt.figure()
plot_acf(model.resid)
plt.savefig('acf_plot.png')
plt.close()

# Normality & Homoscedasticity
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
stats.probplot(model.resid, dist="norm", plot=plt)
plt.title('Normal Q-Q')
plt.subplot(1, 2, 2)
plt.scatter(model.fittedvalues, np.sqrt(np.abs(model.get_influence().resid_studentized_internal)))
plt.title('Scale-Location')
plt.savefig('homoscedasticity_check.png') # Note: reuse name
plt.savefig('normality_check.png') # Reuse for report consistency
plt.close()

# Case Diagnostics
influence = model.get_influence()
cooks_d = influence.cooks_distance[0]
leverage = influence.hat_matrix_diag

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.stem(cooks_d, markerfmt=" ", basefmt="b-")
plt.axhline(y=4/32, color='red', linestyle='--')
plt.title("Cook's Distance")

plt.subplot(1, 2, 2)
plt.stem(leverage, markerfmt=" ", basefmt="b-")
plt.axhline(y=2*(3)/32, color='blue', linestyle='--')
plt.title("Leverage Values")

plt.tight_layout()
plt.savefig('case_diagnostics.png')
plt.close()
