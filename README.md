# AI CV Review Platform

AI CV Review Platform là hệ thống đánh giá và chấm điểm CV tự động dựa trên Trí tuệ Nhân tạo. Hệ thống giúp phân tích CV theo các tiêu chí chuẩn hóa, so khớp với yêu cầu công việc (Job Description) và đề xuất các giải pháp cải thiện cụ thể, đồng thời hỗ trợ lưu trữ và xem lại lịch sử đánh giá trực quan.

---

## 🌟 Tính năng chính
*   **Đánh giá E2E CV & JD**: Phân tích nội dung CV dựa trên 5 danh mục tiêu chí chuẩn hóa (mỗi tiêu chí tối đa 20 điểm, tổng điểm 100):
    *   **Structure**: Bố cục, định dạng và tính rõ ràng.
    *   **Skills**: Sự phù hợp của kỹ năng kỹ thuật & kỹ năng mềm.
    *   **Experience**: Kinh nghiệm làm việc, từ khóa hành động và số liệu lượng hóa.
    *   **Projects**: Dự án cá nhân/thực tế và liên kết kiểm chứng.
    *   **ATS**: Mức độ tối ưu hóa cho hệ thống lọc hồ sơ tự động.
*   **Lưu trữ cơ sở dữ liệu quan hệ (4 bảng)**: Lưu trữ lịch sử chuẩn hóa dữ liệu thông qua TypeORM và PostgreSQL:
    *   `users`: Thông tin tài khoản người dùng (tự động seed tài khoản test khi khởi động).
    *   `cvs`: Nội dung CV và JD tương ứng của lượt gửi.
    *   `reviews`: Kết quả đánh giá chung (điểm tổng, tóm tắt và độ tương thích JD).
    *   `review_feedbacks`: Điểm số chi tiết và danh sách điểm mạnh/điểm yếu/đề xuất nâng cấp cho từng tiêu chí.
*   **Lịch sử trực quan (Sidebar History)**: Tải và hiển thị danh sách các lượt chấm cũ trực tiếp từ database lên giao diện người dùng. Người dùng có thể nhấp chọn để xem chi tiết báo cáo cũ ngay lập tức.
*   **Health Check Động**: Kiểm tra trạng thái máy chủ và kết nối cơ sở dữ liệu thực tế tại endpoint `/api/health`.

---

## 📂 Cấu trúc dự án
Dự án được thiết kế theo mô hình Monorepo gồm các phân hệ sau:
*   `frontend/`: Ứng dụng client viết bằng **Next.js** (React, TypeScript).
*   `backend/`: Hệ thống API chính viết bằng **NestJS** quản lý nghiệp vụ và kết nối PostgreSQL qua **TypeORM**.
*   `ai-service/`: Dịch vụ phân tích trí tuệ nhân tạo viết bằng **FastAPI** (Python), hỗ trợ cả chế độ Heuristic cục bộ và tích hợp OpenAI GPT.
*   `shared/`: Chứa các kiểu dữ liệu (types), hằng số và tiện ích dùng chung giữa frontend và backend.
*   `docker-compose.yml`: Cấu hình Docker để khởi chạy nhanh cơ sở dữ liệu PostgreSQL.

---

## 🛠️ Công nghệ sử dụng
*   **Frontend**: Next.js 15, React, TypeScript, Vanilla CSS.
*   **Backend**: NestJS, TypeORM, PostgreSQL.
*   **AI Service**: FastAPI, Python 3.13, Uvicorn, Pydantic, OpenAI API.
*   **Database**: PostgreSQL 17 (chạy trực tiếp trên Windows hoặc qua Docker).

---

## 🚀 Hướng dẫn cài đặt & Chạy ứng dụng

### 1. Yêu cầu chuẩn bị
*   Đã cài đặt **Node.js** (phiên bản 18+).
*   Đã cài đặt **Python** (phiên bản 3.10+).
*   Đã cài đặt **PostgreSQL** đang chạy trên cổng `5432` (hoặc cài đặt Docker Desktop).

---

### 2. Thiết lập Database
Hệ thống sử dụng database có tên `review_cv_ai` với tài khoản `postgres`/`123456`.
Bạn có thể tạo nhanh cơ sở dữ liệu bằng cách:
*   Nếu dùng Postgres cục bộ trên Windows: Hãy tạo database có tên `review_cv_ai` qua pgAdmin/DBeaver.
*   Nếu dùng Docker:
    ```bash
    docker-compose up -d
    ```

---

### 3. Cấu hình & Chạy Backend (NestJS)
1.  Di chuyển vào thư mục backend:
    ```bash
    cd backend
    ```
2.  Cài đặt các thư viện phụ thuộc:
    ```bash
    npm install
    ```
3.  Tạo file cấu hình môi trường `.env` từ file ví dụ:
    *   Sao chép `.env.example` thành `.env`.
    *   Đảm bảo cấu hình kết nối database chính xác (mật khẩu và tên database):
        ```env
        DATABASE_HOST=localhost
        DATABASE_PORT=5432
        DATABASE_USER=postgres
        DATABASE_PASSWORD=123456
        DATABASE_NAME=review_cv_ai
        DATABASE_SYNCHRONIZE=true
        ```
4.  Biên dịch và chạy backend:
    ```bash
    npm run build
    npm run start:dev
    # hoặc chạy file build trực tiếp: node dist/main.js
    ```
    *API Backend sẽ lắng nghe tại cổng `http://localhost:4000`.*

---

### 4. Cấu hình & Chạy AI Service (FastAPI)
1.  Di chuyển vào thư mục AI:
    ```bash
    cd ai-service
    ```
2.  Tạo môi trường ảo Python và kích hoạt:
    *   **Windows**:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```
3.  Cài đặt các gói thư viện:
    ```bash
    pip install -r requirements.txt
    ```
4.  Tạo file `.env` bằng cách copy từ `.env.example`:
    ```bash
    cp .env.example .env
    ```
    *Mặc định `LLM_PROVIDER=heuristic` sẽ chạy thuật toán chấm điểm cục bộ mà không cần API Key.*
5.  Khởi chạy dịch vụ uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
    *Dịch vụ AI sẽ lắng nghe tại cổng `http://localhost:8000`.*

---

### 5. Khởi chạy Frontend (Next.js)
1.  Di chuyển vào thư mục frontend:
    ```bash
    cd frontend
    ```
2.  Cài đặt các thư viện:
    ```bash
    npm install
    ```
3.  Khởi chạy máy chủ phát triển:
    ```bash
    npm run dev
    ```
    *Giao diện người dùng sẽ sẵn sàng tại `http://localhost:3000`.*

---

## 📈 Danh sách các API chính

### Backend (`http://localhost:4000`)
*   `GET /api/health`: Kiểm tra trạng thái máy chủ và kết nối database.
*   `POST /api/review-cv`: Gửi CV và JD lên để thực hiện chấm điểm và lưu vào cơ sở dữ liệu.
*   `GET /api/review-cv/history`: Lấy toàn bộ danh sách lịch sử các CV đã đánh giá kèm điểm số chi tiết từ database.

### AI Service (`http://localhost:8000`)
*   `GET /health`: Kiểm tra trạng thái hoạt động dịch vụ AI.
*   `POST /api/v1/review-cv`: API cốt lõi xử lý thuật toán chấm điểm CV.
