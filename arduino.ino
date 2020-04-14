int greenLED = 6;
int redLED = 7;
int button = 8;

void setup() {
  // Set up Arduino components
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(button, INPUT);
  // Set up serial port
  Serial.begin(115200);
  // Check that both LEDs work
  blink(greenLED, 2);
  blink(redLED, 2);
  // Default LED state
  digitalWrite(redLED, LOW);
  digitalWrite(greenLED, LOW);
;}

void loop() {
  int buttonState = digitalRead(button);
  if (buttonState == HIGH) {
    String command = ("check");
    Serial.println(command);
    delay(500);
    // Read the result
    char result = 0;
    while (Serial.available() > 0) {
      // Placed in a while loop in case values stack up
      result = Serial.read();
    }
    if (result == 'a') {
      // Authorised
      digitalWrite(greenLED, HIGH);
      delay(1000);
      digitalWrite(greenLED, LOW);
    } else if (result == 'u') {
      // Unauthorised
      digitalWrite(redLED, HIGH);
      delay(1000);
      digitalWrite(redLED, LOW);
    }
  }
}

// ========== Helper Functions ========== //

void blink(int LEDport, byte numOfBlinks) {
  for (byte n = 0; n < numOfBlinks; n++) {
    digitalWrite(LEDport, HIGH);
    delay(200);
    digitalWrite(LEDport, LOW);
    delay(200);
  }
}

void flushSerial() {
  while (Serial.available() > 0) {
    char t = Serial.read();
  }
}
