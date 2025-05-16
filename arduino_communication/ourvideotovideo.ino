#include <Encoder.h>

// Define the pins for the first encoder connected to Xiao ESP32 S3
#define ENCODER1_CLK 44  // CLK connected to D7 -> GPIO44
#define ENCODER1_DT 7    // DT connected to D8 -> GPIO7

// Define the pins for the second encoder connected to Xiao ESP32 S3
#define ENCODER2_CLK 8   // Assuming connected to GPIO8
#define ENCODER2_DT 9    // Assuming connected to GPIO9

// Create Encoder objects
Encoder encoder1(ENCODER1_DT, ENCODER1_CLK);
Encoder encoder2(ENCODER2_DT, ENCODER2_CLK);

// Define parameters for the first encoder
const int encoder1ResolutionCounts = 60; // Total counts for one revolution of the first encoder
const int encoder1Divisions = 5;         // Divide one revolution into 5 segments
const int countsPerDivision = encoder1ResolutionCounts / encoder1Divisions; // Counts per segment
long encoder1CurrentPosition = 0;
long encoder1LastPosition = 0;
int encoder1Output = 0;
unsigned long encoder1LastMoveTime = 0;

// Define parameters for the second encoder
long encoder2CurrentPosition = 0;
long encoder2LastPosition = 0;
unsigned long encoder2LastMoveTime = 0;
const unsigned long stopDelay = 2000; // Delay of 2 seconds of no movement to trigger output
long encoder2InitialPosition = 0;
bool outputSent = false; // Flag to indicate if the output has been sent

void setup() {
  Serial.begin(115200);
  Serial.println("Combined Dual Encoder Test");

  // Read the initial position of the second encoder
  encoder2InitialPosition = encoder2.read();
}

void loop() {
  // Read the change in the first encoder
  long newPosition1 = encoder1.read();
  if (newPosition1 != encoder1LastPosition) {
    encoder1CurrentPosition = newPosition1;
    // Ensure encoder1CurrentPosition is non-negative for cyclical output
    long positivePosition1 = encoder1CurrentPosition % encoder1ResolutionCounts;
    if (positivePosition1 < 0) {
      positivePosition1 += encoder1ResolutionCounts;
    }
    encoder1Output = (positivePosition1 / countsPerDivision) % encoder1Divisions;
    encoder1LastMoveTime = millis();
    encoder1LastPosition = newPosition1;
    outputSent = false; // Reset output flag on movement
  }

  // Read the change in the second encoder
  long newRawPosition2 = encoder2.read();
  if (newRawPosition2 != encoder2LastPosition) {
    encoder2CurrentPosition = newRawPosition2;
    encoder2LastMoveTime = millis();
    encoder2LastPosition = newRawPosition2;
    outputSent = false; // Reset output flag on movement
  }

  // Check if both encoders have stopped moving for the specified delay and output hasn't been sent
  if (millis() - encoder1LastMoveTime >= stopDelay && millis() - encoder2LastMoveTime >= stopDelay && !outputSent) {
    Serial.print(encoder1Output);

    // Calculate the relative position of the second encoder from its initial position
    long relativePosition2 = encoder2CurrentPosition - encoder2InitialPosition;
    if (relativePosition2 > 0) {
      // Rotating right, output 'a'
      for (int i = 0; i < relativePosition2 / 2; i++) {
        Serial.print('a');
      }
    } else if (relativePosition2 < 0) {
      // Rotating left, output 'd'
      for (int i = 0; i < abs(relativePosition2) / 2; i++) {
        Serial.print('d');
      }
    }
    Serial.println();
    outputSent = true; // Set output flag to prevent repeated sending
  }

  delay(10);
}