import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller

# Inisialisasi keyboard controller
keyboard = Controller()

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set lebar frame
cap.set(4, 720)   # Set tinggi frame

# Membuat objek HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=2)

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        self.color = (29, 26, 26, 100)  # Warna default (abu-abu dengan opacity 100)
        self.default_color = (29, 26, 26, 100)  # Tambah alpha di sini (misalnya 100)
        self.clicked_color = (0, 255, 0, 255)  # Warna saat diklik (hijau)
        self.clicked = False  # Status apakah tombol sudah diklik atau tidak

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        overlay = img.copy()
        cv2.rectangle(overlay, self.pos, (w + x, y + h), self.color, cv2.FILLED)
        img = cv2.addWeighted(overlay, self.color[3] / 255.0, img, 1 - self.color[3] / 255.0, 0)

        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, 4, 4)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        return img

# Daftar tombol
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        [" "]]

padding = 15
button_width = 85
button_height = 85
button_spacing_x = button_width + padding
button_spacing_y = button_height + padding

# Membuat daftar tombol berdasarkan keys
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        x = j * button_spacing_x + 50
        y = i * button_spacing_y + 50
        if key == " ":
            button_size = [button_width * 6 + padding * 5, button_height]
        else:
            button_size = [button_width, button_height]
        buttonList.append(Button([x, y], key, button_size))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hands, img = detector.findHands(frame)
    for button in buttonList:
        img = button.draw(img)
    
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
        else:
            lmList2 = None
        
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Reset warna tombol ke warna default
            button.color = button.default_color

            # Periksa jari telunjuk dan jari tengah dari tangan 1 (hand1)
            if lmList1:
                dist, _, _ = detector.findDistance(lmList1[8][:2], lmList1[12][:2])  # Jarak antara jari telunjuk dan jari tengah
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    if dist < 40:  # Jika jari telunjuk dan jari tengah berdekatan
                        button.color = button.clicked_color  # Ubah warna menjadi hijau
                        if not button.clicked:
                            keyboard.press(button.text)
                            keyboard.release(button.text)
                            print(f"Button {button.text} clicked")
                            button.clicked = True
                    else:
                        button.clicked = False

            # Periksa jari telunjuk dan jari tengah dari tangan 2 (hand2)
            if lmList2:
                dist, _, _ = detector.findDistance(lmList2[8][:2], lmList2[12][:2])  # Jarak antara jari telunjuk dan jari tengah
                if x < lmList2[8][0] < x + w and y < lmList2[8][1] < y + h:
                    if dist < 40:  # Jika jari telunjuk dan jari tengah berdekatan
                        button.color = button.clicked_color  # Ubah warna menjadi hijau
                        if not button.clicked:
                            keyboard.press(button.text)
                            keyboard.release(button.text)
                            print(f"Button {button.text} clicked")
                            button.clicked = True
                    else:
                        button.clicked = False

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()