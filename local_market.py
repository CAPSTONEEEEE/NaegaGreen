# 📌 로컬 특산물 판매 데모 (게시물 관리 + 리뷰 + 인증 + 되돌아가기 포함)
import pandas as pd

# 데이터 저장소
sellers = []
products = []
reviews = {}

# 판매자 등록
def register_seller(name, address, business_id, manager, phone):
    if any(s["name"] == name and s["business_id"] == business_id for s in sellers):
        return f"⚠️ 이미 등록된 판매자입니다: {name}"
    sellers.append({
        "name": name,
        "address": address,
        "business_id": business_id,
        "manager": manager,
        "phone": phone
    })
    return f"✅ 판매자 등록 완료: {name} ({business_id})"

# 판매자 인증
def authenticate_seller(name, business_id):
    return any(s["name"] == name and s["business_id"] == business_id for s in sellers)

# 제품 등록
def register_product(seller_name, product_name, price, description):
    product = {
        "판매자": seller_name,
        "상품명": product_name,
        "가격": price,
        "설명": description,
        "상태": "판매중"
    }
    products.append(product)
    return f"✅ 상품 '{product_name}' 등록 완료!"

# 제품 보기
def view_products():
    if not products:
        print("🔍 등록된 상품이 없습니다.")
        return
    df = pd.DataFrame(products).reset_index().rename(columns={"index": "번호"})
    print(df[["번호", "상품명", "판매자", "가격", "상태"]])
    selection_input = input("상세히 볼 상품 번호를 선택하세요 (또는 'b' 입력 시 이전으로): ").strip()
    if selection_input.lower() == 'b':
        return
    try:
        selection = int(selection_input)
        if 0 <= selection < len(products):
            product = products[selection]
            print("\n📦 상품 상세 정보:")
            for k, v in product.items():
                print(f"{k}: {v}")
            # 리뷰 출력
            product_key = product["상품명"]
            product_reviews = reviews.get(product_key, [])
            print("\n📝 리뷰:")
            if product_reviews:
                for idx, r in enumerate(product_reviews):
                    print(f"{idx+1}. {r}")
            else:
                print("등록된 리뷰가 없습니다.")
            # 채팅 여부
            chat = input("🤝 판매자와 채팅하시겠습니까? (y/n): ").strip().lower()
            if chat == "y":
                seller_info = next(s for s in sellers if s["name"] == product["판매자"])
                print(f"📞 연결 완료! {seller_info['manager']}님에게 연락하세요: {seller_info['phone']}")
            else:
                print("❌ 채팅을 취소했습니다.")
        else:
            print("❗유효하지 않은 번호입니다.")
    except:
        print("❗잘못된 입력입니다.")

# 리뷰 쓰기
def write_review():
    keyword = input("리뷰를 남길 상품명을 입력하세요 (또는 'b' 입력 시 이전으로): ").strip()
    if keyword.lower() == 'b':
        return
    matches = [p for p in products if keyword in p["상품명"]]
    if not matches:
        print("❌ 해당 상품을 찾을 수 없습니다.")
        return
    print("\n🔍 검색 결과:")
    for idx, m in enumerate(matches):
        print(f"{idx}: {m['상품명']} (판매자: {m['판매자']})")
    selection_input = input("리뷰를 남길 상품 번호를 선택하세요: ").strip()
    try:
        idx = int(selection_input)
        selected_product = matches[idx]
        content = input("✍ 리뷰를 작성해주세요: ")
        key = selected_product["상품명"]
        if key not in reviews:
            reviews[key] = []
        reviews[key].append(content)
        print("✅ 리뷰가 저장되었습니다.")
    except:
        print("❗잘못된 입력입니다.")

# 게시물 관리
def manage_posts():
    print("\n🔐 게시물 관리를 위해 판매자 인증이 필요합니다.")
    name = input("상호명: ")
    if name.lower() == 'b': return
    business_id = input("사업자등록번호: ")
    if business_id.lower() == 'b': return
    if not authenticate_seller(name, business_id):
        print("❌ 판매자 인증 실패")
        return
    my_products = [p for p in products if p["판매자"] == name]
    if not my_products:
        print("📭 등록한 상품이 없습니다.")
        return
    print("\n📋 나의 등록 상품 목록:")
    for idx, p in enumerate(my_products):
        print(f"{idx}: {p['상품명']} / 상태: {p['상태']} / 가격: {p['가격']}")
    sel_input = input("수정/삭제할 상품 번호 선택 (또는 'b' 입력 시 이전으로): ").strip()
    if sel_input.lower() == 'b': return
    try:
        sel_idx = int(sel_input)
        selected = my_products[sel_idx]
        print("\n1. 상품 정보 수정")
        print("2. 판매 상태 변경")
        print("3. 상품 삭제")
        action = input("수행할 작업 번호 선택: ").strip()
        if action == '1':
            new_name = input(f"새 상품명 입력 (Enter=변경 없음): ").strip()
            new_price = input(f"새 가격 입력 (Enter=변경 없음): ").strip()
            new_desc = input(f"새 설명 입력 (Enter=변경 없음): ").strip()
            if new_name: selected["상품명"] = new_name
            if new_price: selected["가격"] = int(new_price)
            if new_desc: selected["설명"] = new_desc
            print("✅ 상품 정보가 수정되었습니다.")
        elif action == '2':
            print("선택 가능한 상태: 판매중 / 품절 / 예약중")
            new_state = input("새 판매 상태 입력: ").strip()
            if new_state in ["판매중", "품절", "예약중"]:
                selected["상태"] = new_state
                print(f"✅ 상태가 '{new_state}'(으)로 변경되었습니다.")
            else:
                print("❌ 유효하지 않은 상태입니다.")
        elif action == '3':
            products.remove(selected)
            print("🗑️ 상품이 삭제되었습니다.")
        else:
            print("❗잘못된 입력입니다.")
    except:
        print("❗입력 오류입니다.")

# 메인 루프
while True:
    print("\n🛍️ 무엇을 하시겠습니까?")
    print("1: 판매자 등록")
    print("2: 제품 등록")
    print("3: 제품 보기")
    print("4: 리뷰 쓰기")
    print("5: 게시물 관리")
    print("0: 종료")
    choice = input("번호 입력: ").strip()

    if choice == "1":
        print("\n👤 판매자 등록 (이전: 'b')")
        name = input("상호명: ")
        if name.lower() == 'b': continue
        address = input("주소: ")
        if address.lower() == 'b': continue
        business_id = input("사업자등록번호: ")
        if business_id.lower() == 'b': continue
        manager = input("담당자 이름: ")
        if manager.lower() == 'b': continue
        phone = input("가게 연락처: ")
        if phone.lower() == 'b': continue
        print(register_seller(name, address, business_id, manager, phone))

    elif choice == "2":
        print("\n📦 제품 등록 - 판매자 인증 (이전: 'b')")
        name = input("상호명: ")
        if name.lower() == 'b': continue
        business_id = input("사업자등록번호: ")
        if business_id.lower() == 'b': continue
        if authenticate_seller(name, business_id):
            product_name = input("상품명: ")
            if product_name.lower() == 'b': continue
            price_input = input("가격 (숫자): ")
            if price_input.lower() == 'b': continue
            try:
                price = int(price_input)
            except:
                print("❗유효한 숫자가 아닙니다.")
                continue
            description = input("상품 설명: ")
            if description.lower() == 'b': continue
            print(register_product(name, product_name, price, description))
        else:
            print("❌ 판매자 인증 실패. 등록된 판매자만 제품을 등록할 수 있습니다.")

    elif choice == "3":
        print("\n📋 등록된 제품 보기")
        view_products()

    elif choice == "4":
        print("\n✍ 리뷰 작성")
        write_review()

    elif choice == "5":
        print("\n🛠️ 게시물 관리")
        manage_posts()

    elif choice == "0":
        print("👋 종료합니다.")
        break

    else:
        print("❗잘못된 입력입니다. 다시 시도해주세요.")
