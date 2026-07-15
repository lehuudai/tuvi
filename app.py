import math
from flask import Flask, request, jsonify, render_template
from lunar_python import Lunar, Solar

# IMPORT FILE THƯ VIỆN PHÚ TỬ VI (Đã nâng cấp)
from phutuvi import lay_phu_tu_vi_cho_cung

app = Flask(__name__, template_folder='templates', static_folder='static')

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CUNG_NAMES = ["CUNG_TI", "CUNG_SUU", "CUNG_DAN", "CUNG_MAO", "CUNG_THIN", "CUNG_TY", 
              "CUNG_NGO", "CUNG_MUI", "CUNG_THAN", "CUNG_DAU", "CUNG_TUAT", "CUNG_HOI"]

def get_ngu_hanh_nap_am(can_idx, chi_idx):
    v_can = (can_idx // 2) + 1
    v_chi = (chi_idx // 2) % 3
    tong = v_can + v_chi
    if tong > 5: tong -= 5
    ngu_hanh_map = {1: "Kim", 2: "Thủy", 3: "Hỏa", 4: "Thổ", 5: "Mộc"}
    return ngu_hanh_map[tong], tong

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lap-la-so', methods=['POST'])
def lap_la_so():
    data = request.form
    ho_ten = data.get('ho_ten', 'Khách Hàng')
    gioi_tinh = data.get('gioi_tinh', 'nam')
    loai_lich = data.get('loai_lich', '1')
    
    ngay = int(data.get('ngay', 18))
    thang = int(data.get('thang', 10))
    nam = int(data.get('nam', 1986))
    gio_sinh_idx = int(data.get('gio_sinh', 10)) // 2 
    nam_xem = int(data.get('nam_xem', 2026))
    
    # 1. ĐỔI LỊCH VÀ XÁC ĐỊNH NGÀY THÁNG ÂM DƯƠNG
    if loai_lich == '1':
        solar = Solar.fromYmd(nam, thang, ngay)
        lunar = solar.getLunar()
        nam_am, thang_am_raw, ngay_am = lunar.getYear(), lunar.getMonth(), lunar.getDay()
        thang_am = abs(thang_am_raw)
        ngay_duong_str = f"{ngay:02d}/{thang:02d}/{nam}"
        ngay_am_str = f"{ngay_am:02d}/{thang_am:02d}/{nam_am}{' (Nhuận)' if thang_am_raw < 0 else ''}"
    else:
        nam_am, thang_am, ngay_am = nam, thang, ngay
        lunar = Lunar.fromYmd(nam, thang, ngay)
        solar = lunar.getSolar()
        ngay_duong_str = f"{solar.getDay():02d}/{solar.getMonth():02d}/{solar.getYear()}"
        ngay_am_str = f"{ngay_am:02d}/{thang_am:02d}/{nam_am}"

    # 2. CAN CHI, BẢN MỆNH VÀ CỤC
    can_nam_idx = (nam_am - 4) % 10
    chi_nam_idx = (nam_am - 4) % 12
    nam_can_chi = f"{CAN[can_nam_idx]} {CHI[chi_nam_idx]}"
    
    is_duong_nam = (can_nam_idx % 2 == 0)
    am_duong = ("Dương " if is_duong_nam else "Âm ") + ("Nam" if gioi_tinh == 'nam' else "Nữ")
    is_thuan_ly = (can_nam_idx % 2 == 0 and gioi_tinh == 'nam') or (can_nam_idx % 2 != 0 and gioi_tinh == 'nu')
    
    ten_hanh_menh, id_hanh_menh = get_ngu_hanh_nap_am(can_nam_idx, chi_nam_idx)

    menh_idx = (2 + (thang_am - 1) - gio_sinh_idx) % 12
    than_idx = (2 + (thang_am - 1) + gio_sinh_idx) % 12

    can_dan_idx = ((can_nam_idx % 5) * 2 + 2) % 10
    can_menh_idx = (can_dan_idx + (menh_idx - 2) % 12) % 10
    
    _, id_hanh_cuc = get_ngu_hanh_nap_am(can_menh_idx, menh_idx)
    cuc_map_val = {1: 4, 2: 2, 3: 6, 4: 5, 5: 3}
    cuc_so = cuc_map_val[id_hanh_cuc]
    ten_cuc = {2: "Thủy Nhị Cục", 3: "Mộc Tam Cục", 4: "Kim Tứ Cục", 5: "Thổ Ngũ Cục", 6: "Hỏa Lục Cục"}[cuc_so]

    ad_nl = "Âm Dương Thuận Lý" if (can_nam_idx % 2 == menh_idx % 2) else "Âm Dương Nghịch Lý"
    if cuc_so == 4 and id_hanh_menh == 1: mc_desc = "Cục Mệnh Bình Hòa"
    elif id_hanh_menh == id_hanh_cuc: mc_desc = "Cục Mệnh Bình Hòa"
    elif (id_hanh_cuc==2 and id_hanh_menh==5) or (id_hanh_cuc==5 and id_hanh_menh==3) or (id_hanh_cuc==3 and id_hanh_menh==4) or (id_hanh_cuc==4 and id_hanh_menh==1) or (id_hanh_cuc==1 and id_hanh_menh==2): mc_desc = "Cục Sinh Mệnh"
    elif (id_hanh_menh==2 and id_hanh_cuc==5) or (id_hanh_menh==5 and id_hanh_cuc==3) or (id_hanh_menh==3 and id_hanh_cuc==4) or (id_hanh_menh==4 and id_hanh_cuc==1) or (id_hanh_menh==1 and id_hanh_cuc==2): mc_desc = "Mệnh Sinh Cục"
    elif (id_hanh_cuc==2 and id_hanh_menh==3) or (id_hanh_cuc==3 and id_hanh_menh==1) or (id_hanh_cuc==1 and id_hanh_menh==5) or (id_hanh_cuc==5 and id_hanh_menh==4) or (id_hanh_cuc==4 and id_hanh_menh==2): mc_desc = "Cục Khắc Mệnh"
    else: mc_desc = "Mệnh Khắc Cục"

    # 3. AN CHÍNH TINH (TỬ VI - THIÊN PHỦ)
    X = math.ceil(ngay_am / cuc_so)
    diff = (X * cuc_so) - ngay_am
    tv_idx = (2 + X - 1) % 12
    tv_idx = (tv_idx + diff) % 12 if diff % 2 == 0 else (tv_idx - diff) % 12
    tp_idx = (16 - tv_idx) % 12

    cung_data = {i: {"chinh": [], "tot": [], "xau": [], "luu": []} for i in range(12)}
    def add_sao(idx, name, type_sao): cung_data[idx % 12][type_sao].append(name)

    add_sao(tv_idx, "Tử Vi (M)", "chinh")
    add_sao(tv_idx - 1, "Thiên Cơ (Đ)", "chinh")
    add_sao(tv_idx - 3, "Thái Dương (M)", "chinh")
    add_sao(tv_idx - 4, "Vũ Khúc (M)", "chinh")
    add_sao(tv_idx - 5, "Thiên Đồng (Đ)", "chinh")
    add_sao(tv_idx - 8, "Liêm Trinh (V)", "chinh")

    add_sao(tp_idx, "Thiên Phủ (M)", "chinh")
    add_sao(tp_idx + 1, "Thái Âm (M)", "chinh")
    add_sao(tp_idx + 2, "Tham Lang (V)", "chinh")
    add_sao(tp_idx + 3, "Cự Môn (Đ)", "chinh")
    add_sao(tp_idx + 4, "Thiên Tướng (V)", "chinh")
    add_sao(tp_idx + 5, "Thiên Lương (Đ)", "chinh")
    add_sao(tp_idx + 6, "Thất Sát (M)", "chinh")
    add_sao(tp_idx + 10, "Phá Quân (M)", "chinh")

    # 4. AN PHỤ TINH
    tu_hoa_map = {
        0: {"Lộc": "Liêm Trinh", "Quyền": "Phá Quân", "Khoa": "Vũ Khúc", "Kỵ": "Thái Dương"},
        1: {"Lộc": "Thiên Cơ", "Quyền": "Thiên Lương", "Khoa": "Tử Vi", "Kỵ": "Thái Âm"},
        2: {"Lộc": "Thiên Đồng", "Quyền": "Thiên Cơ", "Khoa": "Văn Xương", "Kỵ": "Liêm Trinh"},
        3: {"Lộc": "Thái Âm", "Quyền": "Thiên Đồng", "Khoa": "Thiên Cơ", "Kỵ": "Cự Môn"},
        4: {"Lộc": "Tham Lang", "Quyền": "Thái Âm", "Khoa": "Hữu Bật", "Kỵ": "Thiên Cơ"},
        5: {"Lộc": "Vũ Khúc", "Quyền": "Tham Lang", "Khoa": "Thiên Lương", "Kỵ": "Văn Khúc"},
        6: {"Lộc": "Thái Dương", "Quyền": "Vũ Khúc", "Khoa": "Thái Âm", "Kỵ": "Thiên Đồng"},
        7: {"Lộc": "Cự Môn", "Quyền": "Thiên Lương", "Khoa": "Văn Khúc", "Kỵ": "Văn Xương"},
        8: {"Lộc": "Thiên Lương", "Quyền": "Tử Vi", "Khoa": "Tả Phụ", "Kỵ": "Vũ Khúc"},
        9: {"Lộc": "Phá Quân", "Quyền": "Cự Môn", "Khoa": "Thái Âm", "Kỵ": "Tham Lang"}
    }
    
    lt_map = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]
    lt_idx = lt_map[can_nam_idx]
    add_sao(lt_idx, "Lộc Tồn", "tot")
    add_sao(lt_idx + 1, "Kình Dương (H)", "xau")
    add_sao(lt_idx - 1, "Đà La (Đ)", "xau")

    bs_sao = ["Bác Sĩ", "Lực Sĩ", "Thanh Long", "Tiểu Hao (Đ)", "Tướng Quân", "Tấu Thư", "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao (Đ)", "Phục Binh", "Quan Phù"]
    for i in range(12):
        vitri = (lt_idx + i) % 12 if is_thuan_ly else (lt_idx - i) % 12
        add_sao(vitri, bs_sao[i], "tot" if i not in [3, 6, 8, 9, 10, 11] else "xau")

    tt_sao = ["Thái Tuế", "Thiếu Dương", "Tang Môn (H)", "Thiếu Âm", "Quan Phù", "Tử Phù", "Tuế Phá", "Long Đức", "Bạch Hổ (H)", "Phúc Đức", "Điếu Khách", "Trực Phù"]
    for i in range(12):
        add_sao((chi_nam_idx + i) % 12, tt_sao[i], "tot" if i in [1, 3, 7, 9] else "xau")

    add_sao(11 - gio_sinh_idx, "Địa Không (H)", "xau")
    add_sao(11 + gio_sinh_idx, "Địa Kiếp (H)", "xau")

    hoa_map = {0: 2, 1: 3, 2: 1, 3: 9}
    linh_map = {0: 10, 1: 10, 2: 3, 3: 10}
    nhom_chi = chi_nam_idx % 4
    if is_thuan_ly:
        add_sao(hoa_map[nhom_chi] + gio_sinh_idx, "Hỏa Tinh (Đ)", "xau")
        add_sao(linh_map[nhom_chi] - gio_sinh_idx, "Linh Tinh (H)", "xau")
    else:
        add_sao(hoa_map[nhom_chi] - gio_sinh_idx, "Hỏa Tinh (Đ)", "xau")
        add_sao(linh_map[nhom_chi] + gio_sinh_idx, "Linh Tinh (H)", "xau")

    ta_phu = (4 + thang_am - 1) % 12
    huu_bat = (10 - thang_am + 1) % 12
    add_sao(ta_phu, "Tả Phụ", "tot")
    add_sao(huu_bat, "Hữu Bật", "tot")
    add_sao((9 + thang_am - 1) % 12, "Thiên Hình", "xau")
    add_sao((1 + thang_am - 1) % 12, "Thiên Diêu", "xau")
    add_sao((1 + thang_am - 1) % 12, "Thiên Y", "tot")
    
    vx_idx = (10 - gio_sinh_idx) % 12
    vk_idx = (4 + gio_sinh_idx) % 12
    add_sao(vx_idx, "Văn Xương (Đ)", "tot")
    add_sao(vk_idx, "Văn Khúc (Đ)", "tot")
    add_sao(vk_idx + 2, "Thai Phụ", "tot")
    add_sao(vk_idx - 2, "Phong Cáo", "tot")

    kv_map = [{0:1,1:7}, {0:0,1:8}, {0:11,1:9}, {0:11,1:9}, {0:1,1:7}, {0:0,1:8}, {0:6,1:2}, {0:6,1:2}, {0:3,1:5}, {0:3,1:5}]
    add_sao(kv_map[can_nam_idx][0], "Thiên Khôi", "tot")
    add_sao(kv_map[can_nam_idx][1], "Thiên Việt", "tot")
    
    qf_map = [{0:7,1:9}, {0:4,1:8}, {0:5,1:0}, {0:2,1:11}, {0:3,1:3}, {0:9,1:2}, {0:11,1:6}, {0:9,1:5}, {0:10,1:6}, {0:6,1:5}]
    add_sao(qf_map[can_nam_idx][0], "Thiên Quan", "tot")
    add_sao(qf_map[can_nam_idx][1], "Thiên Phúc", "tot")
    
    lh_map = [9, 10, 7, 4, 5, 6, 8, 3, 11, 2]
    add_sao(lh_map[can_nam_idx], "Lưu Hà", "xau")
    
    co_map = {0:2, 1:5, 2:8, 3:11}
    qua_map = {0:10, 1:1, 2:4, 3:7}
    add_sao(co_map[chi_nam_idx//3], "Cô Thần", "xau")
    add_sao(qua_map[chi_nam_idx//3], "Quả Tú", "xau")
    
    dao_map = {0:9, 1:6, 2:3, 3:0}
    add_sao(dao_map[nhom_chi], "Đào Hoa", "tot")
    hl_idx = (3 - chi_nam_idx) % 12
    add_sao(hl_idx, "Hồng Loan", "tot")
    add_sao(hl_idx + 6, "Thiên Hỷ", "tot")

    add_sao((lt_idx + 8) % 12, "Quốc Ấn", "tot")
    add_sao((lt_idx - 7) % 12, "Đường Phù", "tot")
    add_sao((4 + chi_nam_idx) % 12, "Long Trì", "tot")
    add_sao((10 - chi_nam_idx) % 12, "Phượng Các", "tot")
    add_sao((10 - chi_nam_idx) % 12, "Giải Thần", "tot")
    add_sao((vx_idx + ngay_am - 2) % 12, "Ân Quang", "tot")
    add_sao((vk_idx - ngay_am + 2) % 12, "Thiên Quý", "tot")
    add_sao((ta_phu + ngay_am - 1) % 12, "Tam Thai", "tot")
    add_sao((huu_bat - ngay_am + 1) % 12, "Bát Tọa", "tot")
    add_sao((6 - chi_nam_idx) % 12, "Thiên Khốc", "xau")
    add_sao((6 + chi_nam_idx) % 12, "Thiên Hư", "xau")
    add_sao((menh_idx + chi_nam_idx) % 12, "Thiên Tài", "tot")
    add_sao((than_idx + chi_nam_idx) % 12, "Thiên Thọ", "tot")
    add_sao(4, "Thiên La", "xau")
    add_sao(10, "Địa Võng", "xau")
    add_sao((menh_idx + 5) % 12, "Thiên Thương", "xau")
    add_sao((menh_idx + 7) % 12, "Thiên Sứ", "xau")
    
    pt_map = {0:5, 1:9, 2:1}
    add_sao(pt_map[chi_nam_idx%3], "Phá Toái", "xau")
    ks_map = {0:5, 1:2, 2:11, 3:8}
    add_sao(ks_map[nhom_chi], "Kiếp Sát", "xau")
    hc_map = {0:4, 1:1, 2:10, 3:7}
    add_sao(hc_map[nhom_chi], "Hoa Cái", "tot")
    
    add_sao((8 + thang_am - 1) % 12, "Thiên Giải", "tot")
    add_sao((7 + thang_am - 1) % 12, "Địa Giải", "tot")
    add_sao((9 + chi_nam_idx) % 12, "Thiên Đức", "tot")
    add_sao((5 + chi_nam_idx) % 12, "Nguyệt Đức", "tot")
    
    hoa_khi = tu_hoa_map[can_nam_idx]
    for i in range(12):
        for c in cung_data[i]["chinh"]:
            for k, v in hoa_khi.items():
                if v in c: add_sao(i, f"Hóa {k}", "tot" if k != "Kỵ" else "xau")
        for p in cung_data[i]["tot"]:
            for k, v in hoa_khi.items():
                if v in p: add_sao(i, f"Hóa {k}", "tot" if k != "Kỵ" else "xau")

    # VÒNG LƯU NIÊN DỰA THEO NĂM XEM
    can_xem_idx = (nam_xem - 4) % 10 
    chi_xem_idx = (nam_xem - 4) % 12 
    nam_xem_can_chi = f"{CAN[can_xem_idx]} {CHI[chi_xem_idx]}"
    
    llt_idx = lt_map[can_xem_idx]
    add_sao(llt_idx, "Lưu Lộc Tồn", "luu")
    add_sao(llt_idx + 1, "Lưu Kình Dương", "luu")
    add_sao(llt_idx - 1, "Lưu Đà La", "luu")
    add_sao(chi_xem_idx, "Lưu Thái Tuế", "luu")
    add_sao((chi_xem_idx + 2) % 12, "Lưu Tang Môn", "luu")
    add_sao((chi_xem_idx + 6) % 12, "Lưu Bạch Hổ", "luu")
    add_sao((12 + 6 - chi_xem_idx) % 12, "Lưu Thiên Khốc", "luu")
    add_sao((6 + chi_xem_idx) % 12, "Lưu Thiên Hư", "luu")
    lm_map = {0:2, 1:11, 2:8, 3:5}
    add_sao(lm_map[chi_xem_idx % 4], "Lưu Thiên Mã", "luu")
    
    add_sao((10 - gio_sinh_idx) % 12, "LN Văn Tinh", "tot")
    add_sao((2 - thang_am + gio_sinh_idx) % 12, "Đẩu Quân", "xau")

    # TUẦN - TRIỆT
    triet_idx = {0:8, 1:6, 2:4, 3:2, 4:0, 5:8, 6:6, 7:4, 8:2, 9:0}[can_nam_idx]
    tuan_idx = (chi_nam_idx - can_nam_idx) % 12
    triet_cung = [triet_idx, triet_idx + 1]
    tuan_cung = [(tuan_idx - 1) % 12, (tuan_idx - 2) % 12]

    # KHỞI TẠO VÒNG TRÀNG SINH
    vong_trang_sinh = {}
    ts_start = {2: 8, 3: 11, 4: 5, 5: 8, 6: 2}[cuc_so]
    ts_sao = ["Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
    for i in range(12):
        vitri = (ts_start + i) % 12 if is_thuan_ly else (ts_start - i) % 12
        vong_trang_sinh[vitri] = ts_sao[i]

    # THUẬT TOÁN XÁC ĐỊNH CUNG TIỂU HẠN
    start_cung_map = {
        0: 10, 4: 10, 8: 10,  # Thân, Tý, Thìn -> Khởi tại Tuất (vị trí 10)
        2: 4, 6: 4, 10: 4,    # Dần, Ngọ, Tuất -> Khởi tại Thìn (vị trí 4)
        11: 1, 3: 1, 7: 1,    # Hợi, Mão, Mùi -> Khởi tại Sửu (vị trí 1)
        5: 7, 9: 7, 1: 7      # Tỵ, Dậu, Sửu -> Khởi tại Mùi (vị trí 7)
    }
    start_cung = start_cung_map[chi_nam_idx]
    diff = (chi_xem_idx - chi_nam_idx) % 12
    if gioi_tinh == 'nam':
        tieu_han_cung = (start_cung + diff) % 12
    else:
        tieu_han_cung = (start_cung - diff) % 12

    # THUẬT TOÁN LƯU NGUYỆT (TÍNH THÁNG 1 THEO LƯU ĐẨU QUÂN)
    thang_1_idx = (chi_nam_idx - (thang_am - 1) + gio_sinh_idx + chi_xem_idx) % 12

    # CHUẨN BỊ DỮ LIỆU JSON TRẢ VỀ
    la_so_data = {
        "status": "success",
        "THIEN_BAN": {
            "ho_ten": ho_ten,
            "nam_xem": nam_xem,
            "nam_xem_str": f"{nam_xem} ({nam_xem_can_chi})",
            "tuoi_am": nam_xem - nam_am + 1,
            "ngay_duong_str": ngay_duong_str,
            "ngay_am_str": f"{ngay_am_str} - năm {nam_can_chi}",
            "gio_am": f"Giờ {CHI[gio_sinh_idx]}",
            "am_duong": am_duong,
            "cuc": ten_cuc, 
            "menh_cuc": f"{ad_nl} - {mc_desc}",
            "hanh_menh": f"Mệnh: {ten_hanh_menh}",
        }
    }

    chuoi_chuc_nang = ["MỆNH", "PHỤ MẪU", "PHÚC ĐỨC", "ĐIỀN TRẠCH", "QUAN LỘC", "NÔ BỘC", 
                       "THIÊN DI", "TẬT ÁCH", "TÀI BẠCH", "TỬ TỨC", "PHU THÊ", "HUYNH ĐỆ"]

    # ==============================================================================
    # BƯỚC MỚI: XÂY DỰNG TOÀN BỘ BẢN ĐỒ LÁ SỐ (12 CUNG) TRƯỚC ĐỂ LUẬN HỘI CHIẾU
    # ==============================================================================
    toan_bo_la_so = {}
    for i in range(12):
        # Gom các sao của cung i
        all_stars_temp = cung_data[i]["chinh"] + cung_data[i]["tot"] + cung_data[i]["xau"]
        if i in tuan_cung: all_stars_temp.append("Tuần")
        if i in triet_cung: all_stars_temp.append("Triệt")
        
        # Đánh dấu Vô Chính Diệu
        if len(cung_data[i]["chinh"]) == 0:
            all_stars_temp.append("Vô Chính Diệu")
            
        # Gán vào dict theo chìa khóa tên Địa Chi (VD: "Tý", "Sửu"...)
        toan_bo_la_so[CHI[i]] = all_stars_temp
    # ==============================================================================

    for i in range(12):
        cung_name = CUNG_NAMES[i]
        kc_cung = (i - menh_idx) % 12 
        is_than = "<Thân>" if i == than_idx else ""
        kc_daihan = (i - menh_idx) % 12 if is_thuan_ly else (menh_idx - i) % 12
        dai_han = cuc_so + (kc_daihan * 10)
        
        t_str = []
        if i in tuan_cung: t_str.append("Tuần")
        if i in triet_cung: t_str.append("Triệt")
        
        # 1. Lấy danh sách sao đã gom sẵn ở bước xây dựng trên
        all_stars_in_cung = toan_bo_la_so[CHI[i]]
            
        # 2. Lấy tên chức năng của cung (MỆNH, TÀI BẠCH, QUAN LỘC...)
        ten_chuc_nang_cung = chuoi_chuc_nang[kc_cung]
        
        # 3. TRUYỀN THÊM THAM SỐ TOÀN BỘ LÁ SỐ ĐỂ KIỂM TRA PHÚ HỘI CHIẾU
        phu_tu_vi_list = lay_phu_tu_vi_cho_cung(
            ten_dia_chi=CHI[i], 
            ten_chuc_nang_cung=ten_chuc_nang_cung, 
            danh_sach_sao=all_stars_in_cung,
            toan_bo_la_so=toan_bo_la_so # <--- Đây là điểm kết nối siêu quan trọng
        )
        
        la_so_data[cung_name] = {
            "TEN_CUNG": f"{ten_chuc_nang_cung} {is_than}",
            "THIEN_CAN_CUNG": f"{CAN[(can_dan_idx + (i - 2) % 12) % 10]}.{CHI[i]}", 
            "CHINH_TINH": cung_data[i]["chinh"],
            "PHU_TINH_TOT": cung_data[i]["tot"],  
            "PHU_TINH_XAU": cung_data[i]["xau"],  
            "SAO_LUU": cung_data[i]["luu"],  
            "DAT": vong_trang_sinh[i], 
            "NAM_DAI_VAN": str(dai_han),
            "TUAN_TRIET": " - ".join(t_str),
            "IS_TIEU_HAN": bool(i == tieu_han_cung),
            "THANG_LUU_NIEN": (i - thang_1_idx) % 12 + 1,
            "PHU_TU_VI": phu_tu_vi_list  # Kết quả Phú Tử Vi sau khi check chéo các cung
        }

    return jsonify(la_so_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)