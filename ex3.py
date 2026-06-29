from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI(title="Product Management API")

# Dữ liệu danh sách sản phẩm mock ban đầu
products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(
    keyword: Optional[str] = Query(None, description="Tìm sản phẩm theo tên"),
    max_price: Optional[float] = Query(None, description="Lọc sản phẩm có giá nhỏ hơn hoặc bằng giá này")
):
    # 1. Xử lý bẫy dữ liệu: giá tối đa không được âm
    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=400, detail="max_price không được âm")
    
    # 2. Khởi tạo danh sách kết quả
    filtered_products = products
    
    # 3. Lọc theo keyword (không phân biệt chữ hoa, chữ thường)
    if keyword:
        filtered_products = [
            p for p in filtered_products 
            if keyword.lower() in p["name"].lower()
        ]
        
    # 4. Lọc theo giá tối đa max_price
    if max_price is not None:
        filtered_products = [
            p for p in filtered_products 
            if p["price"] <= max_price
        ]
        
    # 5. Trả về kết quả đúng định dạng
    return filtered_products