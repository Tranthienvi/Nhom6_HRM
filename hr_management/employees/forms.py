from django import forms
from .models import Employee, Contract, WorkHistory, SalaryHistory


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'code', 'first_name', 'last_name', 'full_name', 'gender', 'date_of_birth', 'id_number',
            'phone', 'email', 'position', 'department', 'join_date', 'is_active', 'photo', 'labor_status',
            'employment_type', 'contract_type', 'dependents'
        ]
        widgets = {
            'join_date': forms.SelectDateWidget(years=range(2000, 2031)),
        }


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_type', 'start_date', 'end_date', 'basic_salary', 'position']



class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkHistory
        fields = ['company', 'position', 'start_date', 'end_date', 'description']



class SalaryHistoryForm(forms.ModelForm):
    class Meta:
        model = SalaryHistory
        fields = ['employee', 'effective_date', 'old_salary', 'new_salary', 'reason']
