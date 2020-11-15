from sklearn.datasets import make_classification
X, Y = make_classification(n_samples=200000, n_features=20, n_informative=2, n_redundant=2)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=0) # 50%のデータを学習データに、50%を検証データにする

lr = LogisticRegression() # ロジスティック回帰モデルのインスタンスを作成
lr.fit(X_train, Y_train) # ロジスティック回帰モデルの重みを学習

print("coefficient = ", lr.coef_)
print("intercept = ", lr.intercept_)

probs = lr.predict_proba(X_test)
print("probs", probs)

print(lr.get_params())
