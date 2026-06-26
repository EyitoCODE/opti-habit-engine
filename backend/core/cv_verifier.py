import cv2
import time

class HardwareVerifier:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def verify_physical_task(self, scan_duration=10) -> bool:
        """
        Opens the electro-optic sensor (webcam) and scans for physical objects 
        using contour and edge detection. Returns True if verified.
        """
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("Error: Could not initialize camera interface.")
            return False

        start_time = time.time()
        verified = False

        while (time.time() - start_time) < scan_duration:
            ret, frame = cap.read()
            if not ret:
                break

            # Signal Processing: Grayscale conversion and Gaussian Blur for noise reduction
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Feature Extraction: Apply Canny Edge Detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Isolate geometric structures (contours)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                # Area threshold to verify a significant object is close to the lens
                if area > 15000:
                    x, y, w, h = cv2.boundingRect(contour)
                    # Draw telemetry on the frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "SYSTEM VERIFIED", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    verified = True
            
            cv2.imshow("Opti-Habit Hardware Verification", frame)
            
            # Manual override (Press 'q' to quit early)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if verified:
                # Hold the verified frame on screen for 1.5 seconds for visual feedback
                cv2.waitKey(1500)
                break

        cap.release()
        cv2.destroyAllWindows()
        return verified