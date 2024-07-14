import streamlit as st
import sqlite3
import pandas as pd
import io
import base64
import qrcode

# SQLite setup
conn = sqlite3.connect('scanprods.db')
c = conn.cursor()

# Function to generate QR code with specified size and product ID
def generate_qr_code(product_id, product_name, barcode, expiry_date, status):
    qr_data = f"PRODAPP: {product_id}\nProduct Name: {product_name}\nBarcode: {barcode}\nExpiry Date: {expiry_date}\nStatus: {status}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    return qr_img

def main():
    st.title('View Products')
    c.execute('SELECT id, product_name, barcode, expiry_date, status FROM products ORDER BY id ASC')
    products = c.fetchall()

    if products:
        product_data = []
        for product in products:
            product_id, product_name, barcode, expiry_date, status = product
            qr_img = generate_qr_code(product_id, product_name, barcode, expiry_date, status)
            img_byte_arr = io.BytesIO()
            qr_img.save(img_byte_arr, format='PNG')
            qr_image_bytes = img_byte_arr.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')
            qr_image_html = f'<img src="data:image/png;base64,{qr_image_base64}" alt="QR Code" width="100">'
            
            product_data.append((product_id, product_name, barcode, expiry_date, status, qr_image_html))
        
        df = pd.DataFrame(product_data, columns=['Product ID', 'Product Name', 'Barcode', 'Expiry Date', 'Status', 'QR Code'])
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.write("No products found.")

if __name__ == '__main__':
    main()
