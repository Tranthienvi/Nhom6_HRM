from django import forms
from .models import Employee, WorkHistory, SalaryHistory, Position
from django.utils.translation import gettext_lazy as _

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'code', 'full_name', 'gender', 'date_of_birth', 'id_number',
            'phone', 'email', 'address', 'position', 'join_date', 'is_active', 'photo',
            'employment_type', 'basic_salary', 'salary_rate',  'personal_tax',
            'deduction', 'performance_bonus', 'dependents',
            'education_level', 'degree', 'major'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100000'}),
        }
        labels = {
            'code': _('Mã nhân viên'),
            'full_name': _('Họ và tên'),
            'gender': _('Giới tính'),
            'date_of_birth': _('Ngày sinh'),
            'id_number': _('Số CMND/CCCD'),
            'phone': _('Số điện thoại'),
            'email': _('Email'),
            'address': _('Địa chỉ'),
            'position': _('Vị trí công việc'),
            'join_date': _('Ngày vào làm'),
            'is_active': _('Đang làm việc'),
            'education_level': _('Trình độ học vấn'),
            'degree': _('Bằng cấp'),
            'major': _('Chuyên ngành'),
            'basic_salary': _('Lương cơ bản (VNĐ)'),
            'photo': _('Ảnh đại diện'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm placeholder và các thuộc tính khác
        self.fields['code'].widget.attrs.update({'placeholder': 'Ví dụ: NV001'})
        self.fields['full_name'].widget.attrs.update({'placeholder': 'Nhập họ và tên'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Nhập số điện thoại'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Nhập email'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Nhập địa chỉ'})
        self.fields['id_number'].widget.attrs.update({'placeholder': 'Nhập số CMND/CCCD'})
        self.fields['degree'].widget.attrs.update({'placeholder': 'Ví dụ: Cử nhân Anh ngữ'})
        self.fields['major'].widget.attrs.update({'placeholder': 'Ví dụ: Ngôn ngữ Anh'})
        self.fields['basic_salary'].widget.attrs.update({'placeholder': 'Ví dụ: 10000000'})

        # Chỉ hiển thị các vị trí đang hoạt động
        self.fields['position'].queryset = Position.objects.filter(is_active=True)

        # Thêm class cho các trường
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Đánh dấu các trường bắt buộc
        required_fields = ['code', 'full_name', 'gender', 'date_of_birth',
                           'id_number', 'phone', 'email', 'position', 'join_date']
        for field_name in required_fields:
            self.fields[field_name].required = True

    def clean_code(self):
        code = self.cleaned_data.get('code')
        # Kiểm tra xem mã đã tồn tại chưa (trừ instance hiện tại nếu đang edit)
        if Employee.objects.filter(code=code).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError("Mã nhân viên này đã tồn tại")
        return code

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        # Kiểm tra xem CMND/CCCD đã tồn tại chưa
        if Employee.objects.filter(id_number=id_number).exclude(
                pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError("Số CMND/CCCD này đã tồn tại")
        return id_number

class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkHistory
        fields = ['company', 'position', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SalaryHistoryForm(forms.ModelForm):
    class Meta:
        model = SalaryHistory
        fields = ['employee', 'effective_date', 'old_salary', 'new_salary', 'reason']
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
        }