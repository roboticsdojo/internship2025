import serial

# Open serial port to Arduino
ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

print("Listening for encoder data from Arduino...")

while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line.startswith("E"):
            # Line format: E1234,5678
            data = line[1:]  # Remove the "E"
            try:
                left, right = map(int, data.split(","))
                print(f"Left Encoder: {left}, Right Encoder: {right}")
            except ValueError:
                print("Malformed encoder data:", line)
        else:
            print("Ignored line:", line)

    except KeyboardInterrupt:
        print("Stopped by user")
        break
    except Exception as e:
        print("Error:", e)
