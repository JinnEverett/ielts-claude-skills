# Hướng dẫn sử dụng IELTS Claude Skills

> Cập nhật: 2026-09-21

---

## 1. Tổng quan

**IELTS Claude Skills** là một bộ 8 Claude Code Skill biến Claude thành một AI coach luyện thi IELTS toàn diện. Khác với chat tự do thông thường, bộ skill này:

- **Lưu dữ liệu lâu dài** giữa các buổi chat (điểm số, lỗi sai, từ vựng...) tại `~/.ielts/`
- **Có trí nhớ coaching** — tự ghi lại điểm yếu, sở thích học tập, chiến lược đã đưa ra để không lặp lại lời khuyên
- **Chấm điểm và phân tích có cấu trúc** theo đúng 4 tiêu chí chấm thi IELTS thật
- **Có dashboard trực quan** để xem tiến độ theo thời gian

### 8 skill trong bộ

| Lệnh | Chức năng |
|---|---|
| `/ielts` | Cổng vào chính — hỏi mục tiêu điểm/ngày thi, điều hướng sang skill phù hợp |
| `/ielts-writing` | Chấm bài viết 4 tiêu chí (TR/CC/LR/GRA), viết lại mẫu điểm cao |
| `/ielts-reading` | Phân tích lỗi đọc, tách câu hỏi T/F/NG, xây kho từ đồng nghĩa |
| `/ielts-speaking` | Soạn "universal story" cho Part 2, dự đoán câu hỏi Part 3 |
| `/ielts-listening` | Phân tích lỗi nghe, phân loại nguyên nhân sai, gợi ý luyện nghe kỹ |
| `/ielts-vocab` | Ôn từ vựng theo spaced repetition (thuật toán SM-2) |
| `/ielts-diagnosis` | Đọc toàn bộ lịch sử → chẩn đoán điểm yếu → lập kế hoạch học |
| `/ielts-dashboard` | Xuất trang HTML biểu đồ tiến độ, radar 4 kỹ năng, bản đồ lỗi |

**Lưu ý quan trọng:** đây không phải công cụ dạy tiếng Anh từ đầu — nó giúp bạn tối ưu điểm số trong luật chơi của bài thi IELTS. Toàn bộ dữ liệu lưu local trên máy bạn, không có cloud.

---

## 2. Cài đặt và nơi lưu dữ liệu

### Đã cài ở đâu

- Mã nguồn skill (bản gốc, đã dịch sang tiếng Anh): `D:\Ielts\`
- Bản Claude Code thực sự dùng: `~/.claude/skills/` (tức `C:\Users\jinne\.claude\skills\`), gồm 10 thư mục: `ielts`, `ielts-writing`, `ielts-reading`, `ielts-speaking`, `ielts-listening`, `ielts-vocab`, `ielts-diagnosis`, `ielts-dashboard`, `shared` (chứa `ielts_cli.py`), `dashboard` (chứa template HTML)

### Dữ liệu học tập lưu ở đâu

Tất cả nằm trong `~/.ielts/` (tức `C:\Users\jinne\.ielts\`):

| File/thư mục | Nội dung |
|---|---|
| `config.json` | Mục tiêu điểm, ngày thi, trình độ từng kỹ năng |
| `writing/` | Lịch sử các bài viết đã chấm |
| `reading/` | Lịch sử các bài đọc đã phân tích |
| `listening/` | Lịch sử các bài nghe đã phân tích |
| `speaking/` | Lịch sử luyện nói |
| `errors.json` | Sổ tay lỗi sai, tự gộp theo tần suất |
| `synonyms.json` | Kho từ đồng nghĩa tích lũy |
| `progress.json` | Xu hướng điểm theo thời gian |
| `vocab.json` | Từ vựng + dữ liệu ôn tập spaced repetition |
| `memories.json` | Trí nhớ coaching (sở thích/điểm yếu/chiến lược) |
| `dashboard.html` | Dashboard đã tạo ra |

Vì dữ liệu là local nên **nếu đổi máy, phải backup/restore thủ công** (xem mục 6).

---

## 3. Bắt đầu: lệnh `/ielts`

Gõ `/ielts` trong Claude Code để vào cổng chính. Lần đầu tiên (hồ sơ trống), hệ thống sẽ hỏi lần lượt 3 câu:

1. **Mục tiêu điểm là bao nhiêu? Thi ngày nào?**
2. **Trình độ hiện tại khoảng bao nhiêu? Đã thi thử chưa — nếu có, 4 kỹ năng được bao nhiêu?**
3. **Hôm nay muốn làm gì?** (chọn A–G, xem bảng dưới)

| Chọn | Điều hướng đến | Ghi chú |
|---|---|---|
| A | `/ielts-writing` | Chấm bài viết / phân tích đề / viết lại |
| B | `/ielts-reading` | Luyện đọc chuyên sâu |
| C | `/ielts-speaking` | Soạn tài liệu nói |
| D | `/ielts-listening` | Phân tích lỗi nghe / luyện nghe kỹ |
| E | `/ielts-vocab` | Ôn từ vựng / luyện đồng nghĩa |
| F | `/ielts-diagnosis` | Chẩn đoán dữ liệu + lập kế hoạch |
| G | `/ielts-dashboard` | Tạo và mở dashboard |

Từ lần thứ 2 trở đi, `/ielts` sẽ hiện tóm tắt tiến độ (điểm gần nhất mỗi kỹ năng, số từ cần ôn, lỗi hay gặp nhất) rồi hỏi luôn muốn làm gì hôm nay — không hỏi lại từ đầu.

**Mẹo:** không nhất thiết phải gõ `/ielts` trước — nếu bạn dán thẳng một bài viết, một bài đọc, hoặc nói "luyện nghe", hệ thống sẽ tự nhận diện và điều hướng đúng skill.

---

## 4. Chi tiết từng skill con

### `/ielts-writing` — Chấm bài viết

Dán đề bài + bài viết của bạn. Nhận lại:
- Điểm 4 tiêu chí: Task Response (TR), Coherence & Cohesion (CC), Lexical Resource (LR), Grammatical Range & Accuracy (GRA)
- Đánh dấu lỗi ở từng câu
- Bản viết lại đạt mức điểm mục tiêu
- Danh sách ưu tiên cần sửa trước
- Tự động lưu lịch sử vào `~/.ielts/writing/`

### `/ielts-reading` — Phân tích đọc

Dán bài đọc + câu hỏi + đáp án của bạn + đáp án đúng. Nhận lại:
- Phân tích nguyên nhân sai từng câu
- Bảng từ đồng nghĩa được trích ra → tự thêm vào kho
- Phân tích logic loại câu True/False/Not Given

### `/ielts-speaking` — Tài liệu nói

Hỏi về chủ đề nói hoặc Part 2. Nhận lại:
- Câu chuyện "vạn năng" dùng được cho nhiều chủ đề Part 2 khác nhau
- Dự đoán câu hỏi Part 3 liên quan
- Từ/cụm từ điểm cao theo chủ đề

### `/ielts-listening` — Phân tích nghe

Dán câu hỏi + đáp án của bạn + đáp án đúng. Nhận lại:
- Phân tích điểm theo từng Section
- Phân loại lỗi (chính tả / số liệu / không nghe kịp / bẫy gây nhiễu)
- Bài tập luyện nghe kỹ (intensive listening) được đề xuất

### `/ielts-vocab` — Ôn từ vựng

4 chế độ:
- **Ôn theo spaced repetition** (nói "ôn từ vựng") — đẩy các từ đến hạn, cập nhật theo thuật toán SM-2
- **Thêm từ mới** — bạn cho một từ, hệ thống tự thêm định nghĩa + ví dụ + từ đồng nghĩa liên quan
- **Luyện đồng nghĩa** (nói "luyện đồng nghĩa") — kéo từ trong kho ra để ghép cặp/thay thế
- **Gói từ theo chủ đề** (nói "từ vựng chủ đề giáo dục"...) — 25–40 từ mỗi chủ đề: Education, Environment, Technology, Health, Society & Culture, Work & Economy, Travel & Tourism, Food & Lifestyle

**Lưu ý:** kho từ ban đầu trống — phải chủ động thêm từ (thủ công, từ bài chấm/đọc, hoặc lấy gói từ chủ đề) thì mới có gì để ôn.

### `/ielts-diagnosis` — Chẩn đoán + kế hoạch

Đọc toàn bộ dữ liệu lịch sử (điểm, lỗi, tiến độ), xuất ra:
- Báo cáo chẩn đoán điểm yếu
- Kế hoạch luyện tập theo ngày/tuần

Cần có dữ liệu từ các skill khác trước thì chẩn đoán mới có ý nghĩa.

### `/ielts-dashboard` — Dashboard trực quan

Tạo file HTML tại `~/.ielts/dashboard.html` và tự mở trong trình duyệt, gồm:
- Biểu đồ xu hướng điểm viết (10 bài gần nhất)
- Radar chart 4 kỹ năng (hiện tại vs mục tiêu)
- Top 10 lỗi thường gặp
- Thống kê kho từ đồng nghĩa và tổng quan ôn từ vựng
- Số ngày còn lại đến kỳ thi

---

## 5. Chiến lược học và cách tính điểm

### Công thức tính điểm tổng

Điểm tổng = trung bình 4 kỹ năng, làm tròn đến 0.5 gần nhất. **Lưu ý: .25 và .75 làm tròn lên** (VD: 7.25→7.5, 6.75→7.0).

Ví dụ:
- Mục tiêu 7.5 = Nghe 8 + Đọc 8 + Viết 6.5 + Nói 6.5 (29 ÷ 4 = 7.25 → 7.5)
- Mục tiêu 7.0 = Nghe 7.5 + Đọc 7.5 + Viết 6 + Nói 6 (27 ÷ 4 = 6.75 → 7.0)

**Chiến lược đề xuất: dành 80% thời gian cho Nghe + Đọc, 20% cho Viết + Nói** — vì Nghe/Đọc dễ nâng điểm nhanh hơn bằng luyện tập có hệ thống, còn Viết/Nói cần thời gian tích lũy dài hơn.

### Bảng quy đổi điểm gần đúng (Academic)

**Nghe (Listening):**

| Số câu đúng (/40) | Band |
|---|---|
| 39-40 | 9.0 |
| 37-38 | 8.5 |
| 35-36 | 8.0 |
| 32-34 | 7.5 |
| 30-31 | 7.0 |
| 26-29 | 6.5 |
| 23-25 | 6.0 |
| 18-22 | 5.5 |
| 16-17 | 5.0 |

**Đọc (Academic Reading):**

| Số câu đúng (/40) | Band |
|---|---|
| 39-40 | 9.0 |
| 37-38 | 8.5 |
| 35-36 | 8.0 |
| 33-34 | 7.5 |
| 30-32 | 7.0 |
| 27-29 | 6.5 |
| 23-26 | 6.0 |
| 19-22 | 5.5 |
| 15-18 | 5.0 |

### Phân công công cụ AI theo kỹ năng

| Kỹ năng | Công cụ | Mức độ hữu ích |
|---|---|---|
| Nghe | Tự luyện đề Cambridge + nghe kỹ (intensive listening) | ★★★☆☆ |
| Đọc | `/ielts-reading` | ★★★☆☆ |
| Viết | `/ielts-writing` | ★★★★★ |
| Nói | Gemini Live / ChatGPT Voice + `/ielts-speaking` (soạn tài liệu) | ★★★☆☆ |

---

## 6. Sao lưu và khôi phục dữ liệu

Vì dữ liệu chỉ lưu local, nên backup định kỳ, đặc biệt trước khi đổi máy:

```bash
python ~/.claude/skills/shared/ielts_cli.py backup
```

Lệnh này tạo file `~/ielts-backup-YYYY-MM-DD.zip`.

Khi chuyển sang máy khác, khôi phục bằng:

```bash
python ~/.claude/skills/shared/ielts_cli.py restore --file ~/ielts-backup-YYYY-MM-DD.zip
```

> Trên Windows dùng lệnh `python`, không phải `python3`.

---

## 7. Mẹo sử dụng, câu hỏi thường gặp và giới hạn

**Q: Dùng skill nào trước khi có dữ liệu gì cả?**
Nên bắt đầu từ `/ielts-writing`, `/ielts-reading`, `/ielts-listening`, hoặc lấy một gói từ vựng theo chủ đề qua `/ielts-vocab` — đây là những skill tạo ra dữ liệu đầu tiên. `/ielts-diagnosis` và `/ielts-dashboard` cần có dữ liệu sẵn mới phát huy tác dụng.

**Q: Vì sao vào `/ielts-vocab` mà không có từ nào để ôn?**
Vì kho từ ban đầu trống. Cần chủ động thêm từ (nói tên một từ, lấy gói từ chủ đề, hoặc để nó tự trích từ bài chấm/bài đọc) trước khi có gì để ôn theo spaced repetition.

**Q: Sửa/thêm tính năng cho skill thì làm sao?**
Sửa file `.md`/`.py` trong `D:\Ielts\` (bản nguồn), sau đó copy đè sang `~/.claude/skills/` để Claude Code dùng bản mới — xem `CLAUDE.md` trong repo để biết quy trình đầy đủ.

**Giới hạn của hệ thống:**
- Không dạy tiếng Anh từ đầu — chỉ tối ưu điểm số theo luật chấm IELTS
- Không thay thế việc thi thử thật hoặc luyện nghe/nói thực tế
- Dữ liệu thuần local — mất máy hoặc quên backup sẽ mất lịch sử
- Các gói từ vựng chủ đề do AI soạn tại chỗ, không phải danh sách cố định có sẵn

---

## 8. Repo và liên kết

- Mã nguồn: [github.com/JinnEverett/ielts-claude-skills](https://github.com/JinnEverett/ielts-claude-skills) (public)
- File hướng dẫn cho AI (không phải cho người dùng): `CLAUDE.md` trong repo — mô tả quy trình dev/sync sang `~/.claude/skills/`
