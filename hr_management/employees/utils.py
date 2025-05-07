import xlwt
from django.http import HttpResponse
from datetime import datetime


def export_contracts_to_excel(contracts, filename='danh_sach_hop_dong'):
    response = HttpResponse(content_type='application/ms-excel')
    response[
        'Content-Disposition'] = f'attachment; filename="{filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Danh sách hợp đồng')

    # Định dạng
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Tiêu đề cột
    columns = [
        'STT', 'Số hợp đồng', 'Nhân viên', 'Mã NV', 'Vị trí công việc',
        # Xóa 'Đơn vị' khỏi danh sách cột
        'Loại hợp đồng', 'Ngày bắt đầu', 'Ngày kết thúc', 'Lương cơ bản', 'Trạng thái'
    ]

    # Ghi tiêu đề
    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    # Định dạng dữ liệu
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    # Ghi dữ liệu
    row_num = 1
    for i, contract in enumerate(contracts):
        ws.write(row_num, 0, i + 1, font_style)  # STT
        ws.write(row_num, 1, contract.contract_number, font_style)
        ws.write(row_num, 2, contract.employee.full_name, font_style)
        ws.write(row_num, 3, contract.employee.code, font_style)
        ws.write(row_num, 4, contract.position.name if contract.position else '', font_style)
        # Xóa dòng hiển thị đơn vị
        ws.write(row_num, 5, contract.get_contract_type_display(), font_style)
        ws.write(row_num, 6, contract.start_date, date_format)
        ws.write(row_num, 7, contract.end_date if contract.end_date else 'Không xác định', font_style)
        ws.write(row_num, 8, float(contract.basic_salary), font_style)
        ws.write(row_num, 9, 'Đang hiệu lực' if contract.is_active else 'Hết hiệu lực', font_style)
        row_num += 1

    wb.save(response)
    return response