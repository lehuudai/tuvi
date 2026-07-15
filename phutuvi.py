# phutuvi.py - Hệ thống kiểm tra Phú Tử Vi chuyên nghiệp (Bản nâng cấp Hội Chiếu)

# Mảng tuần hoàn 12 Địa Chi dùng để tính toán vị trí xung chiếu, tam hợp
DIA_CHI_VONG = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Bản đồ các cặp cung Nhị Hợp cố định trong Tử Vi
NHI_HOP_MAP = {
    "Tý": "Sửu", "Sửu": "Tý",
    "Dần": "Hợi", "Hợi": "Dần",
    "Mão": "Tuất", "Tuất": "Mão",
    "Thìn": "Dậu", "Dậu": "Thìn",
    "Tỵ": "Thân", "Thân": "Tỵ",
    "Ngọ": "Mùi", "Mùi": "Ngọ"
}

PHU_DATA = [
    # ================= CÁC CÁCH CỤC TẠI BẢN CUNG (DỮ LIỆU CŨ CỦA BẠN - GIỮ NGUYÊN) =================
    {
        "id": "tu_vi_ngo",
        "cau_phu": "Tử vi cư Ngọ vô sát tấu, vị chí công khanh.",
        "giai_nghia": "Tử Vi ở Ngọ (Cực Hướng Ly Minh), không gặp sát tinh thì làm quan lớn, đại quý.",
        "cung_ap_dung": ["Ngọ"],
        "ten_cung_yeu_cau": ["MỆNH", "QUAN LỘC"],
        "sao_yeu_cau": ["Tử Vi"],
        "sao_ky": ["Kình Dương", "Đà La", "Địa Không", "Địa Kiếp", "Hỏa Tinh", "Linh Tinh", "Tuần", "Triệt"]
    },
    {
        "id": "tu_phu_dong_cung",
        "cau_phu": "Tử Phủ đồng cung, chung thân phúc hậu.",
        "giai_nghia": "Tử Vi, Thiên Phủ đồng cung ở Dần Thân, cả đời phúc lộc dồi dào, ít tai họa.",
        "cung_ap_dung": ["Dần", "Thân"],
        "ten_cung_yeu_cau": [],
        "sao_yeu_cau": ["Tử Vi", "Thiên Phủ"],
        "sao_ky": ["Tuần", "Triệt", "Địa Không", "Địa Kiếp"]
    },
    {
        "id": "tu_sat_ti_hoi",
        "cau_phu": "Tử Vi Thất Sát hóa quyền bính, sát nhân mãn doanh.",
        "giai_nghia": "Tử Vi và Thất Sát đồng cung ở Tỵ Hợi, mang quyền uy lớn, có thể làm tướng súy uy dũng.",
        "cung_ap_dung": ["Tỵ", "Hợi"],
        "ten_cung_yeu_cau": ["MỆNH", "QUAN LỘC"],
        "sao_yeu_cau": ["Tử Vi", "Thất Sát"],
        "sao_ky": ["Tuần", "Triệt"]
    },
    {
        "id": "menh_vo_chinh_dieu",
        "cau_phu": "Mệnh vô chính diệu, hoan ngộ tam không, hựu Song Lộc, phú quí khả kỳ.",
        "giai_nghia": "Mệnh Vô Chính Diệu gặp Tuần/Triệt/Thiên Không/Địa Không, hội Lộc thì cực giàu, nương nhờ ngoại cảnh mà phát.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": ["Vô Chính Diệu"],
        "sao_ky": []
    },
    {
        "id": "cu_nhat_dan_than",
        "cau_phu": "Cự Nhật Dần Thân, quan phong tam đại.",
        "giai_nghia": "Cự Môn, Thái Dương đồng cung ở Dần hoặc Thân. Đắc cách thì vinh hiển, làm quan ba đời.",
        "cung_ap_dung": ["Dần", "Thân"],
        "ten_cung_yeu_cau": ["MỆNH", "QUAN LỘC"],
        "sao_yeu_cau": ["Cự Môn", "Thái Dương"],
        "sao_ky": ["Tuần", "Triệt", "Hóa Kỵ"]
    },

    # ================= CÁC CÁCH CỤC NÂNG CẤP: HỘI CHIẾU (TAM PHƯƠNG TỨ CHÍNH / NHỊ HỢP) =================
    {
        "id": "co_nguyet_dong_luong",
        "cau_phu": "Cơ Nguyệt Đồng Lương tác lại nhân.",
        "giai_nghia": "Mệnh hội đủ bộ sao Thiên Cơ, Thái Âm, Thiên Đồng, Thiên Lương ở Tam phương Tứ chính chủ về làm công chức, mưu sĩ, có tiếng tăm.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": [],  # Không bắt buộc tụ tại bản cung
        "sao_tam_phuong": ["Thiên Cơ", "Thái Âm", "Thiên Đồng", "Thiên Lương"],  # Hội tụ đủ trong bộ 4 cung
        "sao_ky": ["Tuần", "Triệt"]
    },
    {
        "id": "nhat_nguyet_chieu_menh",
        "cau_phu": "Nhật Nguyệt tịnh minh, tá trợ ly minh.",
        "giai_nghia": "Mệnh lập ở Sửu/Mùi hoặc Vô Chính Diệu được Thái Dương, Thái Âm đắc địa từ cung xung chiếu hoặc tam hợp chiếu về cực đẹp, công danh sáng lạn.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": [],
        "sao_tam_phuong": ["Thái Dương", "Thái Âm"],
        "sao_ky": ["Hóa Kỵ", "Kình Dương"]
    },
    {
        "id": "vcd_nhat_nguyet_xung_chieu",
        "cau_phu": "Mệnh Vô Chính Diệu, Nhật Nguyệt xung chiếu, cực diệu công danh.",
        "giai_nghia": "Mệnh Vô Chính Diệu rất cần Thái Dương và Thái Âm từ cung đối diện (xung chiếu) thẳng vào để làm sáng cung Mệnh.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": ["Vô Chính Diệu"],
        "sao_xung_chieu": ["Thái Dương", "Thái Âm"],  # Bắt buộc phải nằm ở cung xung chiếu
        "sao_ky": ["Triệt"]
    },
    {
        "id": "tu_phu_vu_tuong",
        "cau_phu": "Tử Phủ Vũ Tướng hội Mệnh, đại phú đại quý, uy chấn thiên hạ.",
        "giai_nghia": "Mệnh hội đủ bộ cách Tử Vi, Thiên Phủ, Vũ Khúc, Thiên Tướng trong Tam phương Tứ chính, là cách cục của bậc lãnh đạo, đại gia.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": [],
        "sao_tam_phuong": ["Tử Vi", "Thiên Phủ", "Vũ Khúc", "Thiên Tướng"],
        "sao_ky": ["Địa Không", "Địa Kiếp", "Tuần", "Triệt"]
    },
    {
        "id": "nhi_hop_phu_quy",
        "cau_phu": "Sinh phùng hiển địa, hựu đắc minh châu nhị hợp chiếu.",
        "giai_nghia": "Cung Mệnh tốt lại được cung Nhị hợp có cát tinh quý hiển (như Hóa Lộc, Lộc Tồn) ngầm hỗ trợ, giúp cuộc đời may mắn, có quý nhân ngầm giúp đỡ.",
        "cung_ap_dung": [],
        "ten_cung_yeu_cau": ["MỆNH"],
        "sao_yeu_cau": [],
        "sao_nhi_hop": ["Hóa Lộc"],  # Bắt buộc phải tìm thấy Hóa Lộc ở cung nhị hợp
        "sao_ky": []
    }
]

def lay_phu_tu_vi_cho_cung(ten_dia_chi, ten_chuc_nang_cung, danh_sach_sao, toan_bo_la_so=None):
    """
    Hàm kiểm tra điều kiện phú tử vi nâng cao:
    1. ten_dia_chi: Tý, Sửu, Dần...
    2. ten_chuc_nang_cung: MỆNH, TÀI BẠCH, QUAN LỘC...
    3. danh_sach_sao: List các sao trong cung hiện tại.
    4. toan_bo_la_so: (Tùy chọn) Dict chứa sao của cả 12 cung dạng {"Tý": [...], "Sửu": [...]} để xét hội chiếu.
    """
    ket_qua_phu = []
    
    # Hàm con hỗ trợ chuẩn hóa danh sách sao nhanh chóng
    def _chuan_hoa(danh_sach):
        if not danh_sach:
            return []
        return [s.split(" (")[0].strip() for s in danh_sach]
        
    # Chuẩn hóa danh sách sao của bản cung hiện tại
    sao_sach = _chuan_hoa(danh_sach_sao)
    
    # Nếu có truyền vào dữ liệu toàn bộ lá số, ta tính toán trước các nhóm sao hội chiếu
    sao_xung_chieu = []
    sao_tam_hop = []
    sao_nhi_hop = []
    sao_tam_phuong_tu_chinh = []
    
    if toan_bo_la_so and ten_dia_chi in DIA_CHI_VONG:
        idx_hien_tai = DIA_CHI_VONG.index(ten_dia_chi)
        
        # 1. Tính toán cung Xung Chiếu (cách 6 cung)
        cung_xc = DIA_CHI_VONG[(idx_hien_tai + 6) % 12]
        sao_xung_chieu = _chuan_hoa(toan_bo_la_so.get(cung_xc, []))
        
        # 2. Tính toán 2 cung Tam Hợp (cách 4 cung và 8 cung)
        cung_th1 = DIA_CHI_VONG[(idx_hien_tai + 4) % 12]
        cung_th2 = DIA_CHI_VONG[(idx_hien_tai + 8) % 12]
        sao_th1 = _chuan_hoa(toan_bo_la_so.get(cung_th1, []))
        sao_th2 = _chuan_hoa(toan_bo_la_so.get(cung_th2, []))
        sao_tam_hop = sao_th1 + sao_th2
        
        # 3. Tính toán cung Nhị Hợp
        cung_nh = NHI_HOP_MAP.get(ten_dia_chi, "")
        sao_nhi_hop = _chuan_hoa(toan_bo_la_so.get(cung_nh, []))
        
        # 4. Gộp nhóm Tam Phương Tứ Chính (Bản cung + Xung Chiếu + Tam Hợp)
        sao_tam_phuong_tu_chinh = sao_sach + sao_xung_chieu + sao_tam_hop

    # Vòng lặp duyệt qua các câu phú
    for phu in PHU_DATA:
        # --- LOGIC KIỂM TRA ĐIỀU KIỆN CƠ BẢN ---
        
        # 1. Kiểm tra Địa Chi
        if phu["cung_ap_dung"] and ten_dia_chi not in phu["cung_ap_dung"]:
            continue
            
        # 2. Kiểm tra Chức năng cung
        if phu["ten_cung_yeu_cau"] and ten_chuc_nang_cung not in phu["ten_cung_yeu_cau"]:
            continue
            
        # 3. Kiểm tra Sao yêu cầu tại Bản cung (Nếu có)
        if phu["sao_yeu_cau"]:
            is_match = True
            for sao in phu["sao_yeu_cau"]:
                if sao not in sao_sach:
                    is_match = False
                    break
            if not is_match:
                continue
                
        # 4. Kiểm tra Sao kỵ tại Bản cung (Gặp sát tinh kỵ là loại cách cục)
        if phu["sao_ky"]:
            has_sao_ky = False
            for sao in phu["sao_ky"]:
                if sao in sao_sach:
                    has_sao_ky = True
                    break
            if has_sao_ky:
                continue

        # --- LOGIC KIỂM TRA ĐIỀU KIỆN NÂNG CAO (HỘI CHIẾU) ---
        # Kiểm tra xem câu phú này có yêu cầu hội chiếu hay không
        yeu_cau_hoi_chieu = any(k in phu for k in ["sao_xung_chieu", "sao_tam_hop", "sao_nhi_hop", "sao_tam_phuong"])
        
        if yeu_cau_hoi_chieu:
            # Nếu câu phú đòi hỏi hội chiếu mà người dùng không truyền `toan_bo_la_so` -> bỏ qua câu phú này
            if not toan_bo_la_so:
                continue
                
            # Kiểm tra sao ở cung Xung Chiếu
            if "sao_xung_chieu" in phu and phu["sao_xung_chieu"]:
                if not all(sao in sao_xung_chieu for sao in phu["sao_xung_chieu"]):
                    continue
                    
            # Kiểm tra sao ở các cung Tam Hợp
            if "sao_tam_hop" in phu and phu["sao_tam_hop"]:
                if not all(sao in sao_tam_hop for sao in phu["sao_tam_hop"]):
                    continue
                    
            # Kiểm tra sao ở cung Nhị Hợp
            if "sao_nhi_hop" in phu and phu["sao_nhi_hop"]:
                if not all(sao in sao_nhi_hop for sao in phu["sao_nhi_hop"]):
                    continue
                    
            # Kiểm tra bộ sao hội tụ trong toàn bộ Tam Phương Tứ Chính
            if "sao_tam_phuong" in phu and phu["sao_tam_phuong"]:
                if not all(sao in sao_tam_phuong_tu_chinh for sao in phu["sao_tam_phuong"]):
                    continue

        # Nếu đi qua hết các lớp bảo vệ mà không bị loại -> Đạt cách cục phú
        ket_qua_phu.append({
            "cau_phu": phu["cau_phu"],
            "giai_nghia": phu["giai_nghia"]
        })
        
    return ket_qua_phu