import csv
import json
import os

# Ánh xạ mã số tỉnh/thành phố thành tên đầy đủ
province_mapping = {
    "01": "THÀNH PHỐ HÀ NỘI",
    "02": "THÀNH PHỐ HỒ CHÍ MINH",
    "03": "THÀNH PHỐ HẢI PHÒNG",
    "04": "THÀNH PHỐ ĐÀ NẴNG",
    "05": "TỈNH HÀ GIANG",
    "06": "TỈNH CAO BẰNG",
    "07": "TỈNH LAI CHÂU",
    "08": "TỈNH LÀO CAI",
    "09": "TỈNH TUYÊN QUANG",
    "10": "TỈNH LẠNG SƠN",
    "11": "TỈNH BẮC KẠN",
    "12": "TỈNH THÁI NGUYÊN",
    "13": "TỈNH YÊN BÁI",
    "14": "TỈNH SƠN LA",
    "15": "TỈNH PHÚ THỌ",
    "16": "TỈNH VĨNH PHÚC",
    "17": "TỈNH QUẢNG NINH",
    "18": "TỈNH BẮC GIANG",
    "19": "TỈNH BẮC NINH",
    "21": "TỈNH HẢI DƯƠNG",
    "22": "TỈNH HƯNG YÊN",
    "23": "TỈNH HÒA BÌNH",
    "24": "TỈNH HÀ NAM",
    "25": "TỈNH NAM ĐỊNH",
    "26": "TỈNH THÁI BÌNH",
    "27": "TỈNH NINH BÌNH",
    "28": "TỈNH THANH HÓA",
    "29": "TỈNH NGHỆ AN",
    "30": "TỈNH HÀ TĨNH",
    "31": "TỈNH QUẢNG BÌNH",
    "32": "TỈNH QUẢNG TRỊ",
    "33": "TỈNH THỪA THIÊN - HUẾ",
    "34": "TỈNH QUẢNG NAM",
    "35": "TỈNH QUẢNG NGÃI",
    "36": "TỈNH KON TUM",
    "37": "TỈNH BÌNH ĐỊNH",
    "38": "TỈNH GIA LAI",
    "39": "TỈNH PHÚ YÊN",
    "40": "TỈNH ĐẮK LẮK",
    "41": "TỈNH KHÁNH HÒA",
    "42": "TỈNH LÂM ĐỒNG",
    "43": "TỈNH BÌNH PHƯỚC",
    "44": "TỈNH BÌNH DƯƠNG",
    "45": "TỈNH NINH THUẬN",
    "46": "TỈNH TÂY NINH",
    "47": "TỈNH BÌNH THUẬN",
    "48": "TỈNH ĐỒNG NAI",
    "49": "TỈNH LONG AN",
    "50": "TỈNH ĐỒNG THÁP",
    "51": "TỈNH AN GIANG",
    "52": "TỈNH BÀ RỊA – VŨNG TÀU",
    "53": "TỈNH TIỀN GIANG",
    "54": "TỈNH KIÊN GIANG",
    "55": "THÀNH PHỐ CẦN THƠ",
    "56": "TỈNH BẾN TRE",
    "57": "TỈNH VĨNH LONG",
    "58": "TỈNH TRÀ VINH",
    "59": "TỈNH SÓC TRĂNG",
    "60": "TỈNH BẠC LIÊU",
    "61": "TỈNH CÀ MAU",
    "62": "TỈNH ĐIỆN BIÊN",
    "63": "TỈNH ĐĂK NÔNG",
    "64": "TỈNH HẬU GIANG"
}

# Đọc dữ liệu từ file CSV
def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Chuyển đổi sbd thành 8 chữ số
def format_sbd(sbd):
    return sbd.zfill(8)

# Chuyển đổi giá trị rỗng thành null và các giá trị không phải ma_ngoai_ngu thành số
def process_row(row):
    processed_row = {}
    for key, value in row.items():
        if key == 'ma_ngoai_ngu':
            processed_row[key] = value
        else:
            try:
                processed_row[key] = float(value) if value else None
            except ValueError:
                processed_row[key] = value
    return processed_row

# Thêm tên tỉnh/thành phố vào dữ liệu
def add_province_names(data):
    for row in data:
        sbd = format_sbd(row['sbd'])
        prefix = sbd[:2]
        row['tinh_thanh'] = province_mapping.get(prefix, "UNKNOWN")
    return data

# Lưu mỗi sbd vào một file JSON riêng biệt
def save_each_sbd_to_json(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for row in data:
        sbd = format_sbd(row['sbd'])
        file_name = os.path.join(output_dir, f'{sbd}.json')
        processed_row = process_row(row)
        processed_row['sbd'] = sbd
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(processed_row, file, indent=4, ensure_ascii=False)

# Đường dẫn đến file CSV
csv_file_path = 'diem_thi_thpt_2024.csv'
# Đường dẫn đến thư mục đầu ra
output_dir = 'data'

# Thực hiện các bước
data = read_csv(csv_file_path)
data_with_provinces = add_province_names(data)
save_each_sbd_to_json(data_with_provinces, output_dir)

print("Đã hoàn tất việc xử lý và lưu dữ liệu vào các file JSON.")
