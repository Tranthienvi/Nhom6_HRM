# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from .models import WorkShift
#
# # Thêm import để lấy model Employee từ ứng dụng employees
# try:
#     from employees.models import Employee
# except ImportError:
#     Employee = None
#
# def dashboard(request):
#     return render(request, 'attendance/dashboard.html')
#
# def work_shift_list(request):
#     work_shifts = WorkShift.objects.all()
#     return render(request, 'attendance/work_shift_list.html', {'work_shifts': work_shifts})
#
# def work_shift_form(request, id=None):
#     if id:
#         work_shift = get_object_or_404(WorkShift, id=id)
#     else:
#         work_shift = None
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         code = request.POST.get('code')
#         start_time = request.POST.get('start_time')
#         check_in_start = request.POST.get('check_in_start')
#         check_in_end = request.POST.get('check_in_end')
#         end_time = request.POST.get('end_time')
#         check_out_start = request.POST.get('check_out_start')
#         check_out_end = request.POST.get('check_out_end')
#         has_break = request.POST.get('has_break') == 'on'
#         work_hours = float(request.POST.get('work_hours', 0))
#         work_days = float(request.POST.get('work_days', 1))
#         normal_day_coefficient = float(request.POST.get('normal_day_coefficient', 1))
#         rest_day_coefficient = float(request.POST.get('rest_day_coefficient', 2))
#         holiday_coefficient = float(request.POST.get('holiday_coefficient', 3))
#         deduct_if_no_check_in = request.POST.get('deduct_if_no_check_in') == 'on'
#         deduct_if_no_check_out = request.POST.get('deduct_if_no_check_out') == 'on'
#         apply_to_all = request.POST.get('apply_to_all') == 'yes'
#         employee_ids = request.POST.getlist('employees')
#
#         if work_shift:  # Sửa ca làm việc
#             work_shift.name = name
#             work_shift.code = code
#             work_shift.start_time = start_time
#             work_shift.check_in_start = check_in_start
#             work_shift.check_in_end = check_in_end
#             work_shift.end_time = end_time
#             work_shift.check_out_start = check_out_start
#             work_shift.check_out_end = check_out_end
#             work_shift.has_break = has_break
#             work_shift.work_hours = work_hours
#             work_shift.work_days = work_days
#             work_shift.normal_day_coefficient = normal_day_coefficient
#             work_shift.rest_day_coefficient = rest_day_coefficient
#             work_shift.holiday_coefficient = holiday_coefficient
#             work_shift.deduct_if_no_check_in = deduct_if_no_check_in
#             work_shift.deduct_if_no_check_out = deduct_if_no_check_out
#             work_shift.apply_to_all = apply_to_all
#             work_shift.save()
#             # Cập nhật danh sách nhân viên
#             if Employee:
#                 work_shift.employees.set(employee_ids)
#             messages.success(request, "Cập nhật ca làm việc thành công!")
#         else:  # Thêm ca làm việc mới
#             work_shift = WorkShift.objects.create(
#                 name=name,
#                 code=code,
#                 start_time=start_time,
#                 check_in_start=check_in_start,
#                 check_in_end=check_in_end,
#                 end_time=end_time,
#                 check_out_start=check_out_start,
#                 check_out_end=check_out_end,
#                 has_break=has_break,
#                 work_hours=work_hours,
#                 work_days=work_days,
#                 normal_day_coefficient=normal_day_coefficient,
#                 rest_day_coefficient=rest_day_coefficient,
#                 holiday_coefficient=holiday_coefficient,
#                 deduct_if_no_check_in=deduct_if_no_check_in,
#                 deduct_if_no_check_out=deduct_if_no_check_out,
#                 apply_to_all=apply_to_all
#             )
#             # Thêm danh sách nhân viên
#             if Employee and employee_ids:
#                 work_shift.employees.set(employee_ids)
#             messages.success(request, "Thêm ca làm việc thành công!")
#
#         return redirect('work_shift_list')
#
#     # Lấy danh sách nhân viên từ ứng dụng employees
#     employees = Employee.objects.all() if Employee else []
#
#     return render(request, 'attendance/work_shift_form.html', {
#         'work_shift': work_shift,
#         'employees': employees
#     })
#
# def work_shift_detail(request, id):
#     work_shift = get_object_or_404(WorkShift, id=id)
#     return render(request, 'attendance/work_shift_detail.html', {'work_shift': work_shift})
#
# def work_shift_delete(request, id):
#     work_shift = get_object_or_404(WorkShift, id=id)
#     work_shift.delete()
#     messages.success(request, f"Đã xóa ca làm việc {work_shift.name} thành công!")
#     return redirect('work_shift_list')
#
# def attendance_detail_list(request):
#     return render(request, 'attendance/attendance_detail_list.html', {})
#
# def attendance_summary(request):
#     return render(request, 'attendance/attendance_summary.html', {})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import WorkShift, AttendanceRecord, DailyAttendance, AttendanceSummary
from employees.models import Employee, Position
from datetime import datetime, timedelta
from django.http import JsonResponse
import json

def dashboard(request):
    return redirect('work_shift_list')

def work_shift_list(request):
    work_shifts = WorkShift.objects.all()
    return render(request, 'attendance/work_shift_list.html', {'work_shifts': work_shifts})

def work_shift_form(request, id=None):
    if id:
        work_shift = get_object_or_404(WorkShift, id=id)
    else:
        work_shift = None

    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        start_time = request.POST.get('start_time')
        check_in_start = request.POST.get('check_in_start')
        check_in_end = request.POST.get('check_in_end')
        end_time = request.POST.get('end_time')
        check_out_start = request.POST.get('check_out_start')
        check_out_end = request.POST.get('check_out_end')
        has_break = request.POST.get('has_break') == 'on'
        work_hours = float(request.POST.get('work_hours', 0))
        work_days = float(request.POST.get('work_days', 1))
        normal_day_coefficient = float(request.POST.get('normal_day_coefficient', 1))
        rest_day_coefficient = float(request.POST.get('rest_day_coefficient', 2))
        holiday_coefficient = float(request.POST.get('holiday_coefficient', 3))
        deduct_if_no_check_in = request.POST.get('deduct_if_no_check_in') == 'on'
        deduct_if_no_check_out = request.POST.get('deduct_if_no_check_out') == 'on'
        apply_to_all = request.POST.get('apply_to_all') == 'yes'
        employee_ids = request.POST.getlist('employees')

        if work_shift:  # Sửa ca làm việc
            work_shift.name = name
            work_shift.code = code
            work_shift.start_time = start_time
            work_shift.check_in_start = check_in_start
            work_shift.check_in_end = check_in_end
            work_shift.end_time = end_time
            work_shift.check_out_start = check_out_start
            work_shift.check_out_end = check_out_end
            work_shift.has_break = has_break
            work_shift.work_hours = work_hours
            work_shift.work_days = work_days
            work_shift.normal_day_coefficient = normal_day_coefficient
            work_shift.rest_day_coefficient = rest_day_coefficient
            work_shift.holiday_coefficient = holiday_coefficient
            work_shift.deduct_if_no_check_in = deduct_if_no_check_in
            work_shift.deduct_if_no_check_out = deduct_if_no_check_out
            work_shift.apply_to_all = apply_to_all
            work_shift.save()
            if Employee:
                work_shift.employees.set(employee_ids)
            messages.success(request, "Cập nhật ca làm việc thành công!")
        else:  # Thêm ca làm việc mới
            work_shift = WorkShift.objects.create(
                name=name,
                code=code,
                start_time=start_time,
                check_in_start=check_in_start,
                check_in_end=check_in_end,
                end_time=end_time,
                check_out_start=check_out_start,
                check_out_end=check_out_end,
                has_break=has_break,
                work_hours=work_hours,
                work_days=work_days,
                normal_day_coefficient=normal_day_coefficient,
                rest_day_coefficient=rest_day_coefficient,
                holiday_coefficient=holiday_coefficient,
                deduct_if_no_check_in=deduct_if_no_check_in,
                deduct_if_no_check_out=deduct_if_no_check_out,
                apply_to_all=apply_to_all
            )
            if Employee and employee_ids:
                work_shift.employees.set(employee_ids)
            messages.success(request, "Thêm ca làm việc thành công!")

        return redirect('work_shift_list')

    employees = Employee.objects.all() if Employee else []

    return render(request, 'attendance/work_shift_form.html', {
        'work_shift': work_shift,
        'employees': employees
    })

def work_shift_detail(request, id):
    work_shift = get_object_or_404(WorkShift, id=id)
    return render(request, 'attendance/work_shift_detail.html', {'work_shift': work_shift})

def work_shift_delete(request, id):
    work_shift = get_object_or_404(WorkShift, id=id)
    work_shift.delete()
    messages.success(request, f"Đã xóa ca làm việc {work_shift.name} thành công!")
    return redirect('work_shift_list')

def attendance_detail_list(request):
    attendance_records = AttendanceRecord.objects.all()
    work_shifts = WorkShift.objects.all()  # Thêm danh sách ca làm việc
    return render(request, 'attendance/attendance_detail_list.html', {
        'attendance_records': attendance_records,
        'work_shifts': work_shifts
    })
def attendance_detail_form(request, id=None):
    if id:
        attendance_record = get_object_or_404(AttendanceRecord, id=id)
    else:
        attendance_record = None

    if request.method == 'POST':
        name = request.POST.get('name')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        attendance_type = request.POST.get('attendance_type')
        position_id = request.POST.get('positions')
        apply_to_all_shifts = request.POST.get('apply_to_all_shifts') == 'on'
        work_shift_ids = request.POST.getlist('work_shifts')

        # Chuyển đổi chuỗi ngày thành đối tượng datetime.date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        position = get_object_or_404(Position, id=position_id)

        # # Lấy ID nhân viên từ form
        # employee_id = request.POST.get('employee')
        # employee = get_object_or_404(Employee, id=employee_id)

        if attendance_record:  # Sửa bảng chấm công chi tiết
            attendance_record.name = name
            attendance_record.start_date = start_date
            attendance_record.end_date = end_date
            attendance_record.attendance_type = attendance_type
            attendance_record.positions = position
            # attendance_record.employee = employee  # Cập nhật nhân viên
            attendance_record.apply_to_all_shifts = apply_to_all_shifts
            attendance_record.save()
            if not apply_to_all_shifts:
                attendance_record.work_shifts.set(work_shift_ids)
            else:
                attendance_record.work_shifts.clear()
            messages.success(request, "Cập nhật bảng chấm công chi tiết thành công!")
        else:  # Thêm mới bảng chấm công chi tiết
            attendance_record = AttendanceRecord.objects.create(
                name=name,
                start_date=start_date,
                end_date=end_date,
                attendance_type=attendance_type,
                positions=position,
                # employee=employee,  # Thêm nhân viên ở đây
                apply_to_all_shifts=apply_to_all_shifts
            )
            if not apply_to_all_shifts:
                attendance_record.work_shifts.set(work_shift_ids)
            messages.success(request, "Thêm bảng chấm công chi tiết thành công!")

        return redirect('attendance_detail_list')

    positions = Position.objects.all()
    work_shifts = WorkShift.objects.all()
    # employees = Employee.objects.all()  # Lấy danh sách nhân viên cho form

    return render(request, 'attendance/attendance_detail_form.html', {
        'attendance_record': attendance_record,
        'positions': positions,
        'work_shifts': work_shifts,
        # 'employees': employees,  # Truyền danh sách nhân viên cho form
    })

def attendance_detail_delete(request, id):
    attendance_record = get_object_or_404(AttendanceRecord, id=id)
    attendance_record.delete()
    messages.success(request, "Đã xóa bảng chấm công chi tiết thành công!")
    return redirect('attendance_detail_list')

def attendance_detail_view(request, id):
    attendance_record = get_object_or_404(AttendanceRecord, id=id)
    position = attendance_record.positions
    employees = Employee.objects.filter(position=position)

    # Tạo danh sách các ngày trong khoảng thời gian
    start_date = attendance_record.start_date
    end_date = attendance_record.end_date
    delta = end_date - start_date
    date_list = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]

    # Lấy dữ liệu chấm công cho từng nhân viên
    daily_attendances = DailyAttendance.objects.filter(attendance_record=attendance_record)
    attendance_data = {}
    for employee in employees:
        employee_attendance = {}
        for date in date_list:
            attendance = daily_attendances.filter(employee=employee, date=date).first()
            if attendance and attendance.check_in_time and attendance.work_shift:
                # So sánh thời gian để xác định đi đúng giờ/sớm hay muộn
                check_in_time = attendance.check_in_time
                check_in_end = attendance.work_shift.check_in_end

                # So sánh thời gian một cách chính xác
                check_in_time_total = check_in_time.hour * 3600 + check_in_time.minute * 60 + check_in_time.second
                check_in_end_total = check_in_end.hour * 3600 + check_in_end.minute * 60 + check_in_end.second

                # So sánh thời gian để xác định đủ công hay thiếu công
                is_enough_work = False
                if attendance.check_out_time:
                    check_out_time = attendance.check_out_time
                    check_out_start = attendance.work_shift.check_out_start

                    check_out_time_total = check_out_time.hour * 3600 + check_out_time.minute * 60 + check_out_time.second
                    check_out_start_total = check_out_start.hour * 3600 + check_out_start.minute * 60 + check_out_start.second

                    is_enough_work = check_out_time_total >= check_out_start_total

                print(f"Employee: {employee}, Date: {date}, check_in_time: {check_in_time}, check_in_end: {check_in_end}, is_on_time: {check_in_time_total <= check_in_end_total}, check_out_time: {attendance.check_out_time}, check_out_start: {attendance.work_shift.check_out_start}, is_enough_work: {is_enough_work}")

                employee_attendance[date] = {
                    'attendance': attendance,
                    'is_on_time': check_in_time_total <= check_in_end_total,
                    'is_enough_work': is_enough_work
                }
            else:
                employee_attendance[date] = {
                    'attendance': attendance,
                    'is_on_time': False,
                    'is_enough_work': False
                }
        attendance_data[employee.id] = employee_attendance

    return render(request, 'attendance/attendance_detail_view.html', {
        'attendance_record': attendance_record,
        'employees': employees,
        'date_list': date_list,
        'attendance_data': attendance_data,
    })

def update_daily_attendance(request, record_id, employee_id, date_str):
    if request.method == 'POST':
        try:
            # Lấy dữ liệu JSON từ request.body
            data = json.loads(request.body)
            print('Dữ liệu nhận được từ client:', data)  # Debug dữ liệu nhận được

            attendance_record = get_object_or_404(AttendanceRecord, id=record_id)
            employee = get_object_or_404(Employee, id=employee_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Lấy hoặc tạo bản ghi chấm công hàng ngày
            daily_attendance, created = DailyAttendance.objects.get_or_create(
                attendance_record=attendance_record,
                employee=employee,
                date=date,
                defaults={'attendance_status': 'not_absent'}  # Mặc định là "Không nghỉ" nếu chưa chấm
            )

            # Lấy dữ liệu từ payload
            paid_work_days = float(data.get('paid_work_days', 1))
            actual_work_days = float(data.get('actual_work_days', 1))
            check_in_time_str = data.get('check_in_time') or None
            check_out_time_str = data.get('check_out_time') or None
            attendance_status = data.get('attendance_status')

            # Kiểm tra attendance_status
            valid_statuses = [choice[0] for choice in DailyAttendance.ATTENDANCE_STATUS_CHOICES]
            if not attendance_status or attendance_status not in valid_statuses:
                return JsonResponse({'status': 'error', 'message': f'Trạng thái nghỉ không hợp lệ! Nhận được: "{attendance_status}", giá trị hợp lệ: {valid_statuses}'})

            # Chuyển đổi thời gian từ chuỗi (HH:MM)
            check_in_time = None
            check_out_time = None
            if check_in_time_str and check_in_time_str != 'null':
                try:
                    check_in_time = datetime.strptime(check_in_time_str, '%H:%M').time()
                except ValueError as e:
                    return JsonResponse({'status': 'error', 'message': f'Định dạng giờ vào không hợp lệ (HH:MM): {check_in_time_str}, lỗi: {str(e)}'})
            if check_out_time_str and check_out_time_str != 'null':
                try:
                    check_out_time = datetime.strptime(check_out_time_str, '%H:%M').time()
                except ValueError as e:
                    return JsonResponse({'status': 'error', 'message': f'Định dạng giờ ra không hợp lệ (HH:MM): {check_out_time_str}, lỗi: {str(e)}'})

            # Gán work_shift từ AttendanceRecord
            # Giả sử chỉ có một ca làm việc được chọn trong AttendanceRecord
            work_shift = None
            if attendance_record.apply_to_all_shifts:
                # Nếu áp dụng tất cả ca, lấy ca phù hợp với employee (cần logic cụ thể hơn)
                work_shift = WorkShift.objects.filter(employees=employee).first()
            else:
                # Lấy ca đầu tiên từ danh sách work_shifts của AttendanceRecord
                work_shift = attendance_record.work_shifts.first()

            if not work_shift:
                return JsonResponse({'status': 'error', 'message': 'Không tìm thấy ca làm việc phù hợp!'})

            # Cập nhật bản ghi
            daily_attendance.paid_work_days = paid_work_days
            daily_attendance.actual_work_days = actual_work_days
            daily_attendance.check_in_time = check_in_time
            daily_attendance.check_out_time = check_out_time
            daily_attendance.attendance_status = attendance_status
            daily_attendance.work_shift = work_shift  # Gán work_shift
            daily_attendance.save()

            return JsonResponse({'status': 'success', 'message': 'Chấm công thành công!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Lỗi khi lưu dữ liệu: {str(e)}'})
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ!'})

def get_daily_attendance(request, record_id, employee_id, date_str):
    try:
        attendance_record = get_object_or_404(AttendanceRecord, id=record_id)
        employee = get_object_or_404(Employee, id=employee_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        daily_attendance = DailyAttendance.objects.filter(
            attendance_record=attendance_record,
            employee=employee,
            date=date
        ).first()

        if daily_attendance:
            data = {
                'paid_work_days': daily_attendance.paid_work_days,
                'actual_work_days': daily_attendance.actual_work_days,
                'check_in_time': daily_attendance.check_in_time.strftime('%H:%M') if daily_attendance.check_in_time else '',
                'check_out_time': daily_attendance.check_out_time.strftime('%H:%M') if daily_attendance.check_out_time else '',
                'attendance_status': daily_attendance.attendance_status,
            }
        else:
            data = {
                'paid_work_days': 1,
                'actual_work_days': 1,
                'check_in_time': '',
                'check_out_time': '',
                'attendance_status': 'not_absent',
            }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Lỗi khi lấy dữ liệu: {str(e)}'})

def attendance_summary(request):
    attendance_summaries = AttendanceSummary.objects.all()
    positions = Position.objects.all()  # Thêm danh sách vị trí
    attendance_records = AttendanceRecord.objects.all()  # Thêm danh sách bảng chấm công chi tiết
    return render(request, 'attendance/attendance_summary.html', {
        'attendance_summaries': attendance_summaries,
        'positions': positions,
        'attendance_records': attendance_records
    })

def attendance_summary_form(request, id=None):
    if id:
        attendance_summary = get_object_or_404(AttendanceSummary, id=id)
    else:
        attendance_summary = None

    if request.method == 'POST':
        name = request.POST.get('name')
        position_id = request.POST.get('position')
        attendance_record_ids = request.POST.getlist('attendance_records')

        position = get_object_or_404(Position, id=position_id)

        if attendance_summary:  # Sửa bảng chấm công tổng hợp
            attendance_summary.name = name
            attendance_summary.position = position
            attendance_summary.save()
            attendance_summary.attendance_records.set(attendance_record_ids)
            messages.success(request, "Cập nhật bảng chấm công tổng hợp thành công!")
        else:  # Thêm mới bảng chấm công tổng hợp
            attendance_summary = AttendanceSummary.objects.create(
                name=name,
                position=position
            )
            attendance_summary.attendance_records.set(attendance_record_ids)
            messages.success(request, "Thêm bảng chấm công tổng hợp thành công!")

        return redirect('attendance_summary')

    positions = Position.objects.all()
    attendance_records = AttendanceRecord.objects.all()
    return render(request, 'attendance/attendance_summary_form.html', {
        'attendance_summary': attendance_summary,
        'positions': positions,
        'attendance_records': attendance_records
    })

def attendance_summary_view(request, id):
    attendance_summary = get_object_or_404(AttendanceSummary, id=id)
    position = attendance_summary.position
    employees = Employee.objects.filter(position=position)

    # Lấy danh sách bảng chấm công chi tiết
    attendance_records = attendance_summary.attendance_records.all()

    # Xác định khoảng thời gian của bảng chấm công tổng hợp
    if attendance_records:
        start_date = min(record.start_date for record in attendance_records)
        end_date = max(record.end_date for record in attendance_records)
    else:
        start_date = datetime.now().date()
        end_date = start_date

    # Tính số ngày làm việc (loại bỏ ngày Chủ nhật)
    delta = (end_date - start_date).days + 1
    working_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() != 6:  # 6 là Chủ nhật
            working_days += 1
        current_date += timedelta(days=1)

    # Chuẩn bị dữ liệu cho từng nhân viên
    employee_data = []
    for employee in employees:
        # Lấy tất cả bản ghi chấm công hàng ngày của nhân viên trong khoảng thời gian
        daily_attendances = DailyAttendance.objects.filter(
            attendance_record__in=attendance_records,
            employee=employee,
            date__range=[start_date, end_date]
        )

        # Tính số công chuẩn (số ngày làm việc × work_days của ca làm việc)
        work_days_per_day = 1.0  # Giá trị mặc định
        if daily_attendances:
            # Lấy ca làm việc từ bản ghi đầu tiên (giả sử nhân viên chỉ có một ca)
            work_shift = daily_attendances.first().work_shift
            if work_shift:
                work_days_per_day = work_shift.work_days
        standard_work_days = working_days * work_days_per_day

        # Tính công ngày thường, công ngày nghỉ, công nghỉ chế độ, đi muộn/về sớm
        normal_work_days = 0.0
        rest_work_days = 0.0
        regime_work_days = 0.0
        late_early_minutes = 0

        for attendance in daily_attendances:
            if not attendance.work_shift:
                continue

            # Xác định hệ số dựa trên ngày
            normal_coefficient = attendance.work_shift.normal_day_coefficient
            rest_coefficient = attendance.work_shift.rest_day_coefficient

            # Kiểm tra ngày nghỉ (giả sử thứ 7, chủ nhật là ngày nghỉ)
            day_of_week = attendance.date.weekday()  # 0: Thứ 2, ..., 5: Thứ 7, 6: Chủ nhật
            is_rest_day = day_of_week >= 5  # Thứ 7 hoặc Chủ nhật

            # Tính công ngày thường và công ngày nghỉ
            if attendance.attendance_status != "unpermitted_absence":
                if is_rest_day:
                    rest_work_days += attendance.actual_work_days * rest_coefficient
                else:
                    normal_work_days += attendance.actual_work_days * normal_coefficient

            # Tính công nghỉ chế độ
            if attendance.attendance_status == "regime_absence":
                regime_work_days += attendance.actual_work_days

            # Tính số phút đi muộn/về sớm
            if attendance.check_in_time and attendance.work_shift.check_in_end:
                check_in_time_total = attendance.check_in_time.hour * 3600 + attendance.check_in_time.minute * 60 + attendance.check_in_time.second
                check_in_end_total = attendance.work_shift.check_in_end.hour * 3600 + attendance.work_shift.check_in_end.minute * 60 + attendance.work_shift.check_in_end.second
                if check_in_time_total > check_in_end_total:
                    late_minutes = (check_in_time_total - check_in_end_total) // 60
                    late_early_minutes += late_minutes

            if attendance.check_out_time and attendance.work_shift.check_out_start:
                check_out_time_total = attendance.check_out_time.hour * 3600 + attendance.check_out_time.minute * 60 + attendance.check_out_time.second
                check_out_start_total = attendance.work_shift.check_out_start.hour * 3600 + attendance.work_shift.check_out_start.minute * 60 + attendance.work_shift.check_out_start.second
                if check_out_time_total < check_out_start_total:
                    early_minutes = (check_out_start_total - check_out_time_total) // 60
                    late_early_minutes += early_minutes

        employee_data.append({
            'employee': employee,
            'standard_work_days': standard_work_days,
            'normal_work_days': normal_work_days,
            'rest_work_days': rest_work_days,
            'regime_work_days': regime_work_days,
            'late_early_minutes': late_early_minutes,
        })

    return render(request, 'attendance/attendance_summary_view.html', {
        'attendance_summary': attendance_summary,
        'employee_data': employee_data,
    })

def attendance_summary_delete(request, id):
    attendance_summary = get_object_or_404(AttendanceSummary, id=id)
    attendance_summary.delete()
    messages.success(request, "Đã xóa bảng chấm công tổng hợp thành công!")
    return redirect('attendance_summary')

def transfer_to_payroll(request, id):
    if request.method == 'POST':
        attendance_summary = get_object_or_404(AttendanceSummary, id=id)
        # Logic xử lý chuyển tính lương (giả lập ở đây)
        return JsonResponse({'status': 'success', 'message': 'Đã chuyển tính lương thành công!'})
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ!'})

def send_confirmation(request, id):
    if request.method == 'POST':
        attendance_summary = get_object_or_404(AttendanceSummary, id=id)
        # Logic xử lý gửi xác nhận (giả lập ở đây)
        return JsonResponse({'status': 'success', 'message': 'Đã gửi xác nhận thành công!'})
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ!'})