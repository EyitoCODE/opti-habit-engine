"""
Opti-Habit Engine: Optical Proof-of-Work Verifier

Uses OpenCV to open an electro-optic sensor feed, filter noise,
apply Canny edge detection, and calculate structural contour area
to verify physical proof-of-work before confirming habit execution.
"""
import time
import cv2

class HardwareVerifier:
    def __init__(self, camera_index: int = 0, area_threshold: int = 15000):
        """
        camera_index: Hardware device index (0 is typically the integrated camera).
        area_threshold: Minimum contour pixel area required to authenticate object presence.
        """
        self.camera_index = camera_index
        self.area_threshold = area_threshold

    def verify_physical_task(self, scan_duration: int = 10) -> bool:
        """
        Streams frames from the optical sensor, performing real-time edge analysis.
        Returns True once an object matching the physical size threshold is detected.
        """
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            return False

        start_time = time.time()
        verified = False

        while (time.time() - start_time) < scan_duration:
            ret, frame = cap.read()
            if not ret:
                break

            # 1. Grayscale transformation simplifies 3D channel matrices into 1D intensity values.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 2. Gaussian blur filters out high-frequency sensor noise.
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 3. Canny edge detector calculates spatial gradient magnitudes via hysteresis thresholding.
            edges = cv2.Canny(blurred, 50, 150)
            
            # 4. Extract external geometric boundaries from the binary edge map.
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.area_threshold:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(
                        frame, 
                        "HARDWARE VERIFIED", 
                        (x, max(y - 10, 20)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, 
                        (0, 255, 0), 
                        2
                    )
                    verified = True

            cv2.imshow("Opti-Habit Hardware Verification", frame)
            
            # Allow manual exit via 'q' key.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if verified:
                # Retain bounding box on screen for 1.5 seconds for visual confirmation.
                cv2.waitKey(1500)
                break

        cap.release()
        cv2.destroyAllWindows()
        return verified