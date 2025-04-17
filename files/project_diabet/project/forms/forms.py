from django import forms

class DiabetesForm(forms.Form):
    weight = forms.FloatField(label='وزن (کیلوگرم)')
    height = forms.IntegerField(label='قد (سانتی‌متر)')
    age = forms.IntegerField(label='سن')
    a1c_level = forms.FloatField(label='سطح هموگلوبین A1c (بر حسب درصد)')
    blood_sugar = forms.FloatField(label='سطح قند خون (بر حسب میلی گرم در دسی لیتر)')
    gender = forms.ChoiceField(label='جنسیت', choices=[(0, 'زن'), (1, 'مرد')])
    blood_pressure = forms.ChoiceField(label='آیا شما سابقه فشار خون دارید؟', choices=[(0, 'خیر'), (1, 'بله')])
    heart_disease = forms.ChoiceField(label='آیا شما سابقه بیماری قلبی دارید؟', choices=[(0, 'خیر'), (1, 'بله')])
    smoking = forms.ChoiceField(
        label='آیا شما سیگار می‌کشید یا سابقه سیگار کشیدن دارید؟',
        choices=[
            (0, 'سابقه سیگار ندارم'),
            (1, 'سابقه دارم اما ترک کردم'),
            (2, 'گاهی سیگار می کشم'),
            (3, 'معتادم'),
        ]
    )
    