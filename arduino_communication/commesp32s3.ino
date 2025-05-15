void setup() {
	Serial.begin(115200);
}

void loop() {
	
	Serial.println("Hello from XIAO ESP32S3!");

	if (Serial.available() > 0) {
		String receivedString = Serial.readStringUntil('\n');
		// Process the received string
	}

	delay(1000);
}