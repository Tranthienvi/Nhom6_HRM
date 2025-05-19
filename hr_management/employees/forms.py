from django import forms
from .models import Employee, Position, Contract
from django.utils.translation import gettext_lazy as _


class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = [
			'code', 'first_name', 'last_name', 'gender', 'date_of_birth', 'id_number',
			'phone', 'email', 'address', 'position', 'join_date', 'is_active',
			'education_level', 'degree', 'major', 'basic_salary', 'photo'
		]
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100000'}),
		}
		labels = {
			'code': _('Mã nhân viên'),
			'first_name': _('Tên'),
			'last_name': _('Họ'),
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
		self.fields['first_name'].widget.attrs.update({'placeholder': 'Nhập tên'})
		self.fields['last_name'].widget.attrs.update({'placeholder': 'Nhập họ'})
		self.fields['phone'].widget.attrs.update({'placeholder': 'Nhập số điện thoại'})
		self.fields['email'].widget.attrs.update({'placeholder': 'Nhập email'})
		self.fields['address'].widget.attrs.update({'placeholder': 'Nhập địa chỉ'})
		self.fields['id_number'].widget.attrs.update({'placeholder': 'Nhập số CMND/CCCD'})
		self.fields['degree'].widget.attrs.update({'placeholder': 'Ví dụ: Cử nhân Anh ngữ'})
		self.fields['major'].widget.attrs.update({'placeholder': 'Ví dụ: Ngôn ngữ Anh'})
		self.fields['basic_salary'].widget.attrs.update({'placeholder': 'Ví dụ: 10000000'})


class ContractForm(forms.ModelForm):
	class Meta:
		model = Contract
		fields = [
			'employee', 'contract_number', 'contract_type', 'position',
			'start_date', 'end_date', 'basic_salary', 'allowance',
			'insurance_salary', 'status', 'signed_date', 'notes', 'file'
		]
		widgets = {
			'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'signed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100000'}),
			'allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '100000'}),
			'insurance_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100000'}),
			'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
		}

	def __init__(self, *args, **kwargs):
		employee_id = kwargs.pop('employee_id', None)
		super().__init__(*args, **kwargs)

		# Thêm placeholder và các thuộc tính khác
		self.fields['contract_number'].widget.attrs.update({'placeholder': 'Ví dụ: HD-2025/001'})

		# Nếu có employee_id, chỉ hiển thị nhân viên đó và đặt làm mặc định
		if employee_id:
			self.fields['employee'].queryset = Employee.objects.filter(id=employee_id)
			self.fields['employee'].initial = employee_id
			self.fields['employee'].widget.attrs['disabled'] = True
			self.fields['employee'].required = False

			# Thêm trường ẩn để lưu employee_id
			self.fields['employee_id'] = forms.IntegerField(
				widget=forms.HiddenInput(),
				initial=employee_id
			)
		else:
			# Chỉ hiển thị nhân viên đang làm việc
			self.fields['employee'].queryset = Employee.objects.filter(is_active=True)

	def clean(self):
		cleaned_data = super().clean()
		contract_type = cleaned_data.get('contract_type')
		end_date = cleaned_data.get('end_date')

		# Kiểm tra nếu là hợp đồng không xác định thời hạn thì không cần end_date
		if contract_type == 'indefinite' and end_date:
			self.add_error('end_date', 'Hợp đồng không xác định thời hạn không cần ngày kết thúc')

		# Kiểm tra nếu không phải hợp đồng không xác định thời hạn thì phải có end_date
		if contract_type != 'indefinite' and not end_date:
			self.add_error('end_date', 'Hợp đồng xác định thời hạn phải có ngày kết thúc')

		# Kiểm tra ngày bắt đầu phải trước ngày kết thúc
		start_date = cleaned_data.get('start_date')
		if start_date and end_date and start_date >= end_date:
			self.add_error('end_date', 'Ngày kết thúc phải sau ngày bắt đầu')

		return cleaned_data

	def save(self, commit=True):
		instance = super().save(commit=False)

		# Nếu form được tạo với employee_id, sử dụng giá trị đó
		if 'employee_id' in self.cleaned_data:
			instance.employee_id = self.cleaned_data['employee_id']

		if commit:
			instance.save()
		return instance
