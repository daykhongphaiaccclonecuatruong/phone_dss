1. Tải code

Vào link GitHub mình gửi → bấm Code → Download ZIP → giải nén file ZIP ra.

2. Mở project

Mở VS Code → File → Open Folder → chọn thư mục phone_dss vừa giải nén.

3. Mở Terminal trong VS Code

Chọn Terminal → New Terminal.

4. Tạo môi trường ảo

python -m venv .venv

5. Kích hoạt môi trường ảo

Nếu dùng PowerShell:

.\.venv\Scripts\Activate.ps1

Khi thành công sẽ thấy:

(.venv) PS C:\...\phone_dss>

6. Cài thư viện cần thiết

pip install -r requirements.txt

Project hiện cần pandas, nên bước này rất quan trọng.

7. Chạy chương trình

python main.py

Nếu chương trình chạy ra kết quả thì cài đặt thành công.
