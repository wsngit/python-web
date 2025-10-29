from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название курса'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите код курса'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание курса',
                'rows': 4
            }),
        }
        labels = {
            'name': 'Название курса',
            'code': 'Код курса',
            'description': 'Описание курса'
        }
        help_texts = {
            'code': 'Уникальный идентификатор курса (например: MATH-101)',
        }

    def clean_code(self):
        code = self.cleaned_data['code']
        # Проверка на уникальность (исключая текущий объект при редактировании)
        if Course.objects.filter(code=code).exists():
            if self.instance and self.instance.code == code:
                return code
            raise forms.ValidationError('Курс с таким кодом уже существует')
        return code