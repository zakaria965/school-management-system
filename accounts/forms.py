from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import StudentProfile, TeacherProfile, ParentProfile
from academics.models import ClassSection

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo', 'date_of_birth']


class StudentProfileForm(forms.ModelForm):
    student_id = forms.CharField(max_length=20, required=True)
    class_section = forms.ModelChoiceField(queryset=ClassSection.objects.all(), required=False)
    admission_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    emergency_contact = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'class_section', 'admission_date', 'blood_group', 'emergency_contact']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blood_group'].required = False


class TeacherProfileForm(forms.ModelForm):
    employee_id = forms.CharField(max_length=20, required=True)
    designation = forms.CharField(max_length=100, required=True)
    qualification = forms.CharField(max_length=200, required=True)
    department = forms.CharField(max_length=100, required=True)
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    specializations = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'designation', 'qualification', 'department', 'joining_date', 'specializations']


class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ['occupation', 'children']