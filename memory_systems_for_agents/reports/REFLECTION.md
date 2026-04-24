# Reflection: Privacy Và Limitations

## 1. Phân Tích Ký Ức & Hiệu Quả
- **Memory hữu ích nhất**: **Short-term memory** hữu ích nhất cho chất lượng hội thoại tức thời vì giữ được ngữ cảnh gần nhất. **Long-term profile** hữu ích nhất cho việc cá nhân hóa (Personalization) qua nhiều phiên làm việc khác nhau.
- **Memory rủi ro privacy nhất**: **Long-term profile** rủi ro nhất vì chứa PII (Tên Việt Anh, Dự án Microservices, Sức khỏe). **Episodic memory** cũng nhạy cảm vì có thể lưu lại các bí mật thiết kế hệ thống hoặc sự kiện riêng tư trong quá trình làm việc.

## 2. Quản Lý Dữ Liệu Người Dùng
- **Cách xóa user data**: Để xóa dữ liệu, hệ thống cần thực hiện xóa ở cả 4 tầng:
    1. Reset biến state trong LangGraph (Short-term).
    2. Xóa dữ liệu trong `data/user_profile.json`.
    3. Xóa các bản ghi trong `data/episodes.json`.
    4. Xóa các document/vector liên quan trong `data/chroma_db`.
- **Đề xuất Production**: Trong môi trường thực tế, việc xóa phải được đồng bộ sang Redis, SQL, Vector DB và các hệ thống backup. Cần có cơ chế **Consent** (Chấp thuận) và **TTL** (Time-To-Live) để tự động xóa dữ liệu cũ.

## 3. Hạn Chế Của Hệ Thống (Limitations)
- **Hạn chế của Extractor**: Hiện tại bộ trích xuất thông tin là rule-based đơn giản, có thể bỏ sót các fact quan trọng hoặc phân tích sai các câu đính chính (correction) phức tạp.
- **Scaling Fail**: Hệ thống hiện tại dùng file JSON phẳng. Khi số lượng user tăng lên hàng triệu, việc đọc/ghi file sẽ gây nghẽn I/O. Cần chuyển sang hệ thống Database phân tán.
- **Context Window**: Việc inject quá nhiều ký ức vào prompt có thể làm vượt quá giới hạn token của LLM hoặc gây hiện tượng "lost in the middle" (mất thông tin ở giữa).
- **Security**: Việc lưu trữ API Key trong `.env` và PII trong JSON không mã hóa là những lỗ hổng bảo mật cần được khắc phục.

## 4. Các Trường Hợp Thất Bại (Failure Cases)
- **Conflict Extraction sai**: Không nhận diện được user đang sửa lại thông tin cũ, dẫn đến việc lưu hai thông tin mâu thuẫn.
- **Semantic Ranking sai**: Truy xuất các đoạn kiến thức không liên quan từ ChromaDB làm nhiễu câu trả lời của Agent.
- **Inject nhầm ký ức**: Rủi ro lớn nhất là khi hệ thống Multi-user inject nhầm profile của người dùng A vào prompt của người dùng B.

## 5. Tóm Lược Rủi Ro & Đề Xuất
- **PII risk**: Profile và Episodic memory có thể chứa tên (Việt Anh), mục tiêu dự án (Microservices), thói quen sức khỏe (kiêng Cafein) hoặc bí mật kiến trúc phần mềm.
- **TTL/deletion**: Production nên có retention policy riêng cho từng loại memory và tự động expire profile facts hoặc old episodes khi quá hạn.
- **Failure cases**: Conflict extraction sai, semantic chunk không liên quan, lưu quá nhiều episode, hoặc rủi ro nghiêm trọng nhất là inject nhầm private memory của người dùng này vào prompt của người dùng khác.
