# BÁO CÁO BENCHMARK: Multi-Memory AI Agent (Dự án Microservices)

Báo cáo này đánh giá hiệu năng của Agent trong việc hỗ trợ dự án nghiên cứu Microservices của người dùng Việt Anh. Các thử nghiệm tập trung vào khả năng nhớ ngữ cảnh chuyên môn và cá nhân hóa phản hồi.

## Tổng Quan Kết Quả

| # | Kịch bản | No-memory result | With-memory result | Pass? |
|---|----------|------------------|---------------------|-------|
| 1 | Nhận diện người dùng và mục tiêu | Chào bạn. | Chào Việt Anh! Rất vui được hỗ trợ đồ án Microservices của bạn. | Pass |
| 2 | Áp dụng sở thích định dạng (Code) | Trả lời dạng văn bản. | Luôn kèm ví dụ code Python minh họa. | Pass |
| 3 | Ghi nhớ thói quen (Cafe) | Không biết thói quen. | Nhớ bạn thích Cafe sữa đá. | Pass |
| 4 | Xử lý xung đột & Sức khỏe | Vẫn gợi ý Cafe hoặc nhầm lẫn. | Nhận diện lệnh kiêng Cafein, xóa bỏ fact Cafe cũ. | Pass |
| 5 | Truy xuất thông tin đã cập nhật | Gợi ý Cafe/Trà chung chung. | Gợi ý đồ uống không Cafein (Trà thảo mộc, nước ép). | Pass |
| 6 | Truy xuất kiến thức chuyên môn | Giải thích sơ sài. | Giải thích Circuit Breaker chi tiết kèm Semantic hits. | Pass |
| 7 | Ghi nhớ sự kiện quan trọng (Episodic) | Không biết gRPC là gì. | Lưu lại quyết định dùng gRPC cho giao tiếp nội bộ. | Pass |
| 8 | Nhớ lại quyết định quá khứ | Không nhớ lịch sử thảo luận. | Nhớ chính xác gRPC đã được chọn thay vì REST. | Pass |
| 9 | Tổng hợp thông tin Profile | Không biết Việt Anh là ai. | Xác nhận Việt Anh đang nghiên cứu về kiến trúc Microservices. | Pass |
| 10 | Lưu trữ kết quả giai đoạn | Kết thúc bình thường. | Lưu episodic log: "Hoàn thành giai đoạn 1 dự án Microservices". | Pass |

---

## Phân Tích Theo Loại Bộ Nhớ

### 1. Long-term Profile (Nhân vật: Việt Anh)
- **Dữ liệu**: Tên (Việt Anh), Dự án (Microservices), Sức khỏe (Kiêng hoàn toàn Cafein), Preference (Không gợi ý Cafe).
- **Hiệu quả**: Giúp Agent xưng hô thân thiện và ghi nhớ các ràng buộc sức khỏe quan trọng của người dùng.

### 2. Conflict Handling (Xử lý mâu thuẫn)
- **Tình huống**: Thay đổi từ "Thích Cafe" sang "Kiêng Cafein hoàn toàn vì sức khỏe".
- **Kết quả**: Hệ thống đã cập nhật key `health` và không còn đưa ra gợi ý gây hại cho sức khỏe người dùng.

### 3. Episodic Memory (Nhật ký dự án)
- **Tình huống**: Nhớ lại việc chọn giao thức gRPC cho giao tiếp nội bộ.
- **Kết quả**: Agent giúp duy trì tính nhất quán cho thiết kế hệ thống của dự án Microservices qua nhiều phiên làm việc.

### 4. Semantic Memory (Kiến thức Microservices)
- **Tình huống**: Giải thích Circuit Breaker, gRPC, Saga Pattern.
- **Kết quả**: Dữ liệu từ ChromaDB giúp Agent trả lời chính xác các thuật ngữ chuyên ngành thay vì chỉ dựa vào kiến thức tổng quát của LLM.

---

## Reflection: Phân Tích Rủi Ro & Giới Hạn

1.  **Memory hữu ích nhất**: **Episodic Memory** cực kỳ quan trọng cho các dự án dài hơi (như đồ án của Việt Anh) vì nó lưu lại các quyết định thiết kế đã chốt.
2.  **Rủi ro Privacy**: Nếu thông tin về kiến trúc hệ thống bí mật của Việt Anh bị rò rỉ qua Semantic Memory cho user khác, đó sẽ là một thảm họa bảo mật.
3.  **Cách xóa dữ liệu**: Sử dụng lệnh xóa đồng bộ tại các file trong thư mục `data/` và collection trong ChromaDB.
4.  **Giới hạn khi Scale**: Khi dự án Microservices có hàng nghìn episode, việc tìm kiếm (search) episodic memory có thể bị chậm hoặc lấy ra các episode không liên quan nếu không có cơ chế ranking tốt.
