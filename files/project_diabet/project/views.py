from django.http import HttpResponse
from django.shortcuts import render, redirect
import joblib
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def home(request):
    return render(request, 'home.html')

def res(request):
    if request.method == 'POST':
        try:
            weight = float(request.POST.get('weight'))
            height = float(request.POST.get('height'))
            age = float(request.POST.get('age'))
            HbA1c_level = float(request.POST.get('a1c_level'))
            blood_glucose_level = float(request.POST.get('blood_sugar'))

            if weight <= 0 or weight > 300:
                return render(request, 'home.html', {'error': 'وزن غیرمعقول است.'})
            if height <= 0 or height > 250:
                return render(request, 'home.html', {'error': 'قد غیرمعقول است.'})
            if age <= 0 or age > 120:
                return render(request, 'home.html', {'error': 'سن غیرمعقول است.'})
            if HbA1c_level < 0 or HbA1c_level > 20:
                return render(request, 'home.html', {'error': 'سطح هموگلوبین A1c غیرمعقول است.'})
            if blood_glucose_level < 0 or blood_glucose_level > 1000:
                return render(request, 'home.html', {'error': 'سطح قند خون غیرمعقول است.'})

            model = joblib.load('modele.pkl')
            label_encoder = LabelEncoder()

            gender = label_encoder.fit_transform([request.POST.get('gender')])[0]
            hypertension = float(request.POST.get('blood_pressure'))
            heart_disease = label_encoder.fit_transform([request.POST.get('heart_disease')])[0]
            smoking_history = int(request.POST.get('smoking'))

            bmi = weight / (height ** 2)

            smoking_history_0, smoking_history_1, smoking_history_2, smoking_history_3 = 0, 0, 0, 0
            if smoking_history == 0:
                smoking_history_0 = 1
            elif smoking_history == 1:
                smoking_history_1 = 1
            elif smoking_history == 2:
                smoking_history_2 = 1
            elif smoking_history == 3:
                smoking_history_3 = 1

            data_columns = [
                "gender",
                "age",
                "hypertension",
                "heart_disease",
                "bmi",
                "HbA1c_level",
                "blood_glucose_level",
                "smoking_history_0",
                "smoking_history_1",
                "smoking_history_2",
                "smoking_history_3"
            ]

            test = pd.DataFrame([[gender, age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level,
                                  smoking_history_0, smoking_history_1, smoking_history_2, smoking_history_3]],
                                columns=data_columns)

            print(test)

            ans = model.predict(test)

            return render(request, 'res.html', {'ans': ans[0]})
        except Exception as e:
            return render(request, 'home.html', {'error': f'خطا در پردازش داده‌ها: {str(e)}'})
    else:
        return redirect('home')