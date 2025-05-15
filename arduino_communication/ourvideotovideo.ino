// 定义编码器引脚
#define ENCODER1_CLK 7
#define ENCODER1_DT 8
#define ENCODER2_CLK 9
#define ENCODER2_DT 10

// 状态变量
volatile int encoder1Count = 0;  // 时间轴编码器
volatile int encoder2Count = 0;  // 文化选择编码器

int lastEncoder2Region = 0;      // 上一次文化区域
unsigned long lastEncoder1Move = 0;
unsigned long lastEncoder2Move = 0;
const unsigned long STOP_THRESHOLD = 2000; // 2秒

// 编码器1的中断处理函数（时间轴）
void IRAM_ATTR handleEncoder1() {
  if (digitalRead(ENCODER1_CLK) == digitalRead(ENCODER1_DT)) {
    encoder1Count++;
  } else {
    encoder1Count--;
  }
  lastEncoder1Move = millis();
}

// 编码器2的中断处理函数（文化选择）
void IRAM_ATTR handleEncoder2() {
  if (digitalRead(ENCODER2_CLK) == digitalRead(ENCODER2_DT)) {
    encoder2Count++;
  } else {
    encoder2Count--;
  }
  lastEncoder2Move = millis();
}

void setup() {
  Serial.begin(115200);

  pinMode(ENCODER1_CLK, INPUT_PULLUP);
  pinMode(ENCODER1_DT, INPUT_PULLUP);
  pinMode(ENCODER2_CLK, INPUT_PULLUP);
  pinMode(ENCODER2_DT, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCODER1_CLK), handleEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER2_CLK), handleEncoder2, CHANGE);
}

void loop() {
  unsigned long currentTime = millis();

  // 处理文化选择编码器（每4格为一个区域，0~4）
  int region = ((encoder2Count % 20) + 20) % 20 / 4;
  if (region != lastEncoder2Region && (currentTime - lastEncoder2Move > STOP_THRESHOLD)) {
    Serial.println(region);
    lastEncoder2Region = region;
  }

  // 处理时间轴编码器
  static int lastEncoder1Count = 0;
  if (currentTime - lastEncoder1Move > STOP_THRESHOLD) {
    int diff = encoder1Count - lastEncoder1Count;
    if (diff != 0) {
      int num = abs(diff) / 2; // 每2格输出1个a/d
      if (num > 0) {
        for (int i = 0; i < num; i++) {
          Serial.print(diff > 0 ? "d" : "a");
        }
        Serial.println();
        lastEncoder1Count += (diff > 0 ? num * 2 : -num * 2); // 只消耗已输出的格数
      }
    }
  }

  delay(10);
}