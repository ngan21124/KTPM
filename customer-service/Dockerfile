# Sử dụng Python bản nhẹ
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file yêu cầu thư viện vào trước để cache
COPY requirements.txt .

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Lệnh chạy ứng dụng (thay app.py bằng file chính của bạn nếu khác tên)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
