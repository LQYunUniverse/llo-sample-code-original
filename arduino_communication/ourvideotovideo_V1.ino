// 定义编码器引脚
#define ENCODER1_CLK 7
#define ENCODER1_DT 8
#define ENCODER2_CLK 9
#define ENCODER2_DT 10

// 编码器状态变量
volatile int encoder1Count = 0;  // 这个值表示相对于原点的步数
volatile int encoder2Count = 0;  // 编码器2的计数值
int lastEncoder1Count = 0;
int lastEncoder2Count = 0;      // 编码器2的上一个计数值
int lastEncoder1Direction = 0;  // 1表示右转，-1表示左转

// 时间相关变量
unsigned long lastEncoder1Move = 0;
unsigned long lastEncoder2Move = 0;  // 编码器2的最后移动时间
const unsigned long STOP_THRESHOLD = 2000; // 2秒

// 编码器1的中断处理函数
void IRAM_ATTR handleEncoder1() {
  if (digitalRead(ENCODER1_CLK) == digitalRead(ENCODER1_DT)) {
    encoder1Count++;  // 右转增加，表示向未来
    lastEncoder1Direction = 1; // 右转
  } else {
    encoder1Count--;  // 左转减少，表示向过去
    lastEncoder1Direction = -1; // 左转
  }
  lastEncoder1Move = millis();
}

// 编码器2的中断处理函数
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
  
  // 设置编码器引脚
  pinMode(ENCODER1_CLK, INPUT_PULLUP);
  pinMode(ENCODER1_DT, INPUT_PULLUP);
  pinMode(ENCODER2_CLK, INPUT_PULLUP);
  pinMode(ENCODER2_DT, INPUT_PULLUP);
  
  // 设置中断
  attachInterrupt(digitalPinToInterrupt(ENCODER1_CLK), handleEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER2_CLK), handleEncoder2, CHANGE);
  
  // 初始位置是 Present
  Serial.println("Present");
}

void loop() {
  unsigned long currentTime = millis();
  
  // 处理编码器1
  if (currentTime - lastEncoder1Move > STOP_THRESHOLD) {
    if (encoder1Count != lastEncoder1Count) {
      int steps = encoder1Count;  // 直接使用计数值，表示相对于原点的位置
      int years = ((abs(steps) - 1) / 4 + 1) * 200;  // 每4格200年，确保最小是200年
      
      if (steps == 0) {
        Serial.println("Present");
      } else if (steps > 0) { // 未来
        Serial.print(years);
        Serial.println(" years in the future");
      } else { // 过去
        Serial.print(years);
        Serial.println(" years ago");
      }
      
      lastEncoder1Count = encoder1Count;
    }
  }
  
  // 处理编码器2
  if (currentTime - lastEncoder2Move > STOP_THRESHOLD) {
    if (encoder2Count != lastEncoder2Count) {
      // 将编码器2的计数值映射到0-5的范围
      int position = (encoder2Count % 6 + 6) % 6;
      
      switch(position) {
        case 0:
          Serial.println("Ancient Greece");
          break;
        case 1:
          Serial.println("Ancient China");
          break;
        case 2:
          Serial.println("Ancient Egypt");
          break;
        case 3:
          Serial.println("Ancient India");
          break;
        case 4:
          Serial.println("Renaissance Europe");
          break;
        case 5:
          Serial.println("Ancient Japan");
          break;
      }
      lastEncoder2Count = encoder2Count;
    }
  }
  
  delay(10); // 小延迟以减少CPU使用
}