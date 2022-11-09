from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


from phonenumber_field.formfields import PhoneNumberField

from JunJob.models import Application, Vacancy, Company, Resume, Profile
from JunJob.accounts.Choices import SPECIALTY_CHOICES, GRADE, STATUS


# формы аутентификации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(min_length=5,
                                label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# формы приложения


class ApplicationForm(forms.ModelForm):   # отклик на вакансию
    written_username = forms.CharField(label='Вас зовут', widget=forms.TextInput(attrs={'class': 'form-control'}))
    written_phone = PhoneNumberField(label='Ваш телефон', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'name': 'phone_number'}))
    written_cover_letter = forms.CharField(label='Сопроводительное письмо',
                                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}))
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    vacancy = forms.ModelChoiceField(queryset=Vacancy.objects.all(), empty_label=None)

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields.pop('user')
        self.fields.pop('vacancy')


class MyCompanyForm(forms.ModelForm):   # форма редактирования информации о компании
    name = forms.CharField(label='Название компании', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='География', widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label='Логотип', max_length=40000)
    description = forms.CharField(label='Информация о компании',
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': 4,
                                                               'style': 'color: #000;'}))
    employee_count = forms.IntegerField(label='Количество человек в компании',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')
        # widget = {'logo': forms.ImageField(label='Логотип', initial='https://place-hold.it/120x40')}


class MyVacancyForm(forms.ModelForm):  # форма редактирования информации о вакансии
    title = forms.CharField(label='Название вакансии', widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                    'rows': 3,
                                                                                    'style': 'color:#000;'}))
    description = forms.CharField(label='Описание вакансии', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                          'rows': 13,
                                                                                          'style': 'color:#000;'}))
    salary_min = forms.IntegerField(label='Зарплата от', widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(label='Зарплата до', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = ('title', 'skills', 'description', 'salary_min', 'salary_max')


class ResumeForm(forms.ModelForm):  # форма резюме
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label='Готовность к работе', choices=STATUS,
                               widget=forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
                               initial='3', required=True)
    salary = forms.FloatField(label='Ожидаемая зарплата', widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.ChoiceField(label='Специализация', choices=SPECIALTY_CHOICES,
                                  widget=forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
                                  initial='', required='True')
    grade = forms.ChoiceField(label='Квалификация', widget=forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
                              choices=GRADE, initial='2', required=True)
    education = forms.CharField(label='Образование',
                                widget=forms.Textarea(attrs={'class': 'form-control text-uppercase',
                                                             'rows': 4,
                                                             'style': 'color:#000;'}))
    experience = forms.CharField(label='Опыт работы', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                   'rows': 4,
                                                                                   'style': 'color:#000;'}))
    portfolio = forms.CharField(label='Ссылка на портфолио', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')


class ProfileForm(forms.ModelForm):
    birthday = forms.DateField(required=False, label='Дата рождения',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(required=False, label='Страна',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=False, label='город',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('birthday', 'country', 'city')


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='email',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name')
