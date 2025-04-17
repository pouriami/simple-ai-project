import pandas as pd
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score, accuracy_score
import pickle

def load_data(filepath):
    df = pd.read_csv(filepath)
    df.dropna(inplace=True)  
    df = df[(df >= df.quantile(0.01)) & (df <= df.quantile(0.99))].dropna()  
    important_features = ["age", "male", "cigsPerDay", "totChol", "sysBP", "diaBP", "BMI", "glucose"]
    return df[important_features + ["TenYearCHD"]]

def preprocess_data(df):
    X = df.drop(columns=["TenYearCHD"])
    y = df["TenYearCHD"]
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X_resampled)
    return train_test_split(X_scaled, y_resampled, test_size=0.2, random_state=42)

def build_stacking_model():
    rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
    svm_model = SVC(probability=True, kernel='rbf', C=1.0, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=5)
    lr = LogisticRegression()
    return StackingClassifier(
        estimators=[('rf', rf_model), ('svm', svm_model), ('knn', knn)],
        final_estimator=lr,
        passthrough=True
    )

def main():
    filepath = "../data/framingham.csv"
    df = load_data(filepath)
    X_train, X_test, y_train, y_test = preprocess_data(df)
    stacking_model = build_stacking_model()
    stacking_model.fit(X_train, y_train)
    
    y_pred_prob_stack = stacking_model.predict_proba(X_test)[:, 1]
    roc_auc_stack = roc_auc_score(y_test, y_pred_prob_stack)
    print(f"ROC-AUC Stacking: {roc_auc_stack:.4f}")
    
    y_pred_stack = stacking_model.predict(X_test)
    accuracy_stack = accuracy_score(y_test, y_pred_stack)
    print(f"Accuracy Stacking: {accuracy_stack:.4f}")
    
    with open("model.pkl", "wb") as model_file:
        pickle.dump(stacking_model, model_file)

if __name__ == "__main__":
    main()
