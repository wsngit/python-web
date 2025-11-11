from django import forms
import os
from django.core.files.storage import FileSystemStorage

class PythonSyntaxTestForm(forms.Form):
    # Вопрос 1: TextInput (одиночная строка)
    question_1 = forms.CharField(
        label="1. Какой оператор используется для создания комментария в Python?",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите оператор'
        })
    )

    # Вопрос 2: RadioSelect (один из нескольких вариантов)
    QUESTION_2_CHOICES = [
        ('list', 'list'),
        ('array', 'array'),
        ('sequence', 'sequence'),
        ('collection', 'collection'),
    ]
    question_2 = forms.ChoiceField(
        label="2. Как называется изменяемая последовательность элементов в Python?",
        choices=QUESTION_2_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )

    # Вопрос 3: Select (выпадающий список)
    QUESTION_3_CHOICES = [
        ('', '-- Выберите ответ --'),
        ('def', 'def'),
        ('function', 'function'),
        ('func', 'func'),
        ('define', 'define'),
    ]
    question_3 = forms.ChoiceField(
        label="3. Какое ключевое слово используется для определения функции?",
        choices=QUESTION_3_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    # Вопрос 4: CheckboxSelectMultiple (несколько вариантов)
    QUESTION_4_CHOICES = [
        ('indentation', 'Отступы'),
        ('semicolon', 'Точка с запятой в конце строки'),
        ('brackets', 'Фигурные скобки'),
        ('parentheses', 'Круглые скобки для блоков кода'),
    ]
    question_4 = forms.MultipleChoiceField(
        label="4. Что используется для обозначения блоков кода в Python? (выберите все верные)",
        choices=QUESTION_4_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )

    # Вопрос 5: Textarea (многострочный ввод)
    question_5 = forms.CharField(
        label="5. Напишите пример создания словаря с ключами 'name' и 'age':",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Например: {"key": "value"}'
        })
    )

    # Вопрос 6: NumberInput (числовой ввод)
    question_6 = forms.IntegerField(
        label="6. Сколько элементов будет в списке после выполнения: list(range(5))?",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите число'
        })
    )

    # Вопрос 7: BooleanField (чекбокс да/нет)
    question_7 = forms.BooleanField(
        label="7. В Python строки являются изменяемыми объектами",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )