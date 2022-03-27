import pandas as pd
import xgboost as xgb
from sklearn import metrics
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib

from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost.sklearn import XGBClassifier


def dataPreprocessing(df, columnName):
    le = LabelEncoder()

    df[columnName] = le.fit_transform(df[columnName])


df = pd.read_csv(r"E:\ProjectWorkspace\project\static\adminResources\dataset\train.csv")

df['Gender'] = df['Gender'].fillna(df['Gender'].dropna().mode().values[0])
df['Married'] = df['Married'].fillna(df['Married'].dropna().mode().values[0])
df['Dependents'] = df['Dependents'].fillna(df['Dependents'].dropna().mode().values[0])
df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].dropna().mode().values[0])
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].dropna().mean())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].dropna().mode().values[0])
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].dropna().mode().values[0])
df['Dependents'] = df['Dependents'].str.rstrip('+')
dataPreprocessing(df, 'Gender')
dataPreprocessing(df, 'Married')
dataPreprocessing(df, 'Education')
dataPreprocessing(df, 'Self_Employed')
dataPreprocessing(df, 'Loan_Status')
dataPreprocessing(df, 'Dependents')
dataPreprocessing(df, 'Property_Area')

# df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1})
# df['Married'] = df['Married'].map({'No': 0, 'Yes': 1})
# df['Education'] = df['Education'].map({'Not Graduate': 0, 'Graduate': 1})
# df['Self_Employed'] = df['Self_Employed'].map({'No': 0, 'Yes': 1})
# df['Loan_Status'] = df['Loan_Status'].map({'N': 0, 'Y': 1})
# df['Dependents'] = df['Dependents']

X, y = df.iloc[:, 1:-1], df.iloc[:, -1]

X = pd.get_dummies(X)

dtrain = pd.get_dummies(df)

train = dtrain
target = 'Loan_Status'
IDcol = 'Loan_ID'


def modelfit(alg, dtrain, predictors, useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'],
                          nfold=cv_folds, metrics='auc', early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])

    alg.fit(dtrain[predictors], dtrain['Loan_Status'], eval_metric='auc')

    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:, 1]

    print("\nModel Report")
    print("Accuracy : %.4g" % metrics.accuracy_score(dtrain['Loan_Status'].values, dtrain_predictions))
    print("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['Loan_Status'], dtrain_predprob))


predictors = [x for x in train.columns if x not in [target, IDcol]]
xgb1 = XGBClassifier(learning_rate=0.1, n_estimators=1000, max_depth=5, min_child_weight=1, gamma=0, subsample=0.8,
                     colsample_bytree=0.8, objective='binary:logistic', nthread=4, scale_pos_weight=1, seed=27)
modelfit(xgb1, train, predictors)

slc = StandardScaler()
X_train_std = slc.fit_transform(X)

eclf = VotingClassifier(estimators=[('xgb', xgb1)], voting='hard')

eclf.fit(X_train_std, y)

joblib.dump(eclf, r'E:\ProjectWorkspace\project\static\adminResources\modelDump\loan.pkl')

dtest = pd.read_csv(r"E:\ProjectWorkspace\project\static\adminResources\dataset\test.csv")

dtest['Gender'] = dtest['Gender'].fillna(dtest['Gender'].dropna().mode().values[0])
dtest['Dependents'] = dtest['Dependents'].fillna(dtest['Dependents'].dropna().mode().values[0])
dtest['Self_Employed'] = dtest['Self_Employed'].fillna(dtest['Self_Employed'].dropna().mode().values[0])
dtest['LoanAmount'] = dtest['LoanAmount'].fillna(dtest['LoanAmount'].dropna().mode().values[0])
dtest['Loan_Amount_Term'] = dtest['Loan_Amount_Term'].fillna(dtest['Loan_Amount_Term'].dropna().mode().values[0])
dtest['Credit_History'] = dtest['Credit_History'].fillna(dtest['Credit_History'].dropna().mode().values[0])

dataPreprocessing(dtest, 'Gender')
dataPreprocessing(dtest, 'Married')
dataPreprocessing(dtest, 'Education')
dataPreprocessing(dtest, 'Self_Employed')
dataPreprocessing(dtest, 'Dependents')
dataPreprocessing(dtest, 'Property_Area')
X_test = dtest.iloc[:, 1:]

X_test = pd.get_dummies(X_test)

X_test_std = slc.transform(X_test)

job_lib = joblib.load(r'E:\ProjectWorkspace\project\static\adminResources\modelDump\loan.pkl')

y_test_pred = job_lib.predict(X_test_std)

dtest['Loan_Status'] = y_test_pred
df_final = dtest.drop(
    ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
     'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'], axis=1)

df_final['Loan_Status'] = df_final['Loan_Status'].map({0: 'N', 1: 'Y'})

df_final.to_csv(r"E:\ProjectWorkspace\project\static\adminResources\dataset\result.csv", index=False)

print(df_final)
