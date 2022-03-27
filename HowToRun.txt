- Chạy file test.py để hoạt động, train-face để train.

- Sử dụng hình ảnh một số người nổi tiếng và mặt sinh viên.

- Vẫn có lỗi ko nhận hoặc nhận ra người khác -> Độ chính xác không cao.

- Khi register import ảnh, terminal bị đứng chưa khắc phục được, 
phải kill trước khi chạy tiếp.

- Các hình ảnh cũng như thông tin được lưu trong images_check sau khi đăng kí.

- Sau khi register xong, phải chạy train-face.py để train các faces 
đã đăng ký trước khi cho vào hoạt động.

- Khi Login, xuất hiện cửa sổ Cam để bắt camera thì ta nhìn xuống terminal xem có load student id của người đã đăng kí không.
Nếu có tức chương trình đang nhận diện đúng, nhấn x để đóng cửa sổ Cam và hoàn tất check in.

- Bởi vì Login sử dụng camera, để đăng nhập được nên em chụp hình các file trong images rồi đưa điện thoại để nhận diện.
Xem ảnh test_cam_login.jpg để biết thêm chi tiết.