import cv2

# カメラの選択 (通常は0がデフォルトのカメラ)
cap = cv2.VideoCapture(0)

# カメラが正しく開けたか確認
if not cap.isOpened():
    print("カメラが開けません。")
else:
    print("カメラが正常に検出されました。")

    # カメラからフレームをキャプチャし、ウィンドウに表示
    while True:
        # フレームをキャプチャ
        ret, frame = cap.read()

        # フレームのキャプチャが成功したかどうかを確認
        if not ret:
            print("フレームをキャプチャできません。終了します。")
            break

        # ウィンドウにフレームを表示
        cv2.imshow('Camera Test', frame)

        # 'q'キーが押されるとループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # カメラデバイスを解放
    cap.release()

# すべてのウィンドウを破棄
cv2.destroyAllWindows()
