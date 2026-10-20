// TT gear motor on an L298N, driven by an ESP32 over USB serial.
//
// Wiring (see ../../connections.txt):
//   GPIO2  -> L298N IN1   (channel A, OUT1/OUT2)
//   GPIO14 -> L298N IN2
//   GPIO15 -> L298N IN3   (channel B, OUT3/OUT4)
//   GPIO13 -> L298N IN4
//   GND    -> GND
// ENA and ENB keep their jumpers on: speed is set by PWM on the IN pins.
//
// Serial, 115200 baud, one command per line:
//   S <-100..100>   speed in % duty; the sign is the direction (+ = top of the roller moves forward)
//   C <A|B>         which L298N channel the motor is on (default A)
//   X               stop now (coast, no ramp)
//   R <%/s>         ramp rate (default 200 %/s, 0 = no ramp)
//   K <ms>          kick: full duty for this long when starting from standstill (default 60 ms)
//   ?               print the status
// Every command, also an empty line, feeds the watchdog: with no line for 1.5 s the motor stops,
// so it stops when the PC program closes or the cable comes out.
// Status line, every 100 ms:  T <target %> <actual %> <channel> <kick 0/1>

const int PIN_IN1 = 2;
const int PIN_IN2 = 14;
const int PIN_IN3 = 15;
const int PIN_IN4 = 13;

const uint32_t PWM_FREQ = 1000;     // Hz; low frequency keeps torque at low duty on an L298N
const uint8_t PWM_BITS = 10;
const int PWM_MAX = (1 << PWM_BITS) - 1;
const uint32_t WATCHDOG_MS = 1500;
const uint32_t STATUS_MS = 100;

float target = 0;        // %
float actual = 0;        // %
float rampRate = 200;    // %/s
uint32_t kickMs = 60;
char channel = 'A';

uint32_t lastCmd = 0;
uint32_t lastStep = 0;
uint32_t lastStatus = 0;
uint32_t kickUntil = 0;
String line;

void writePins(float pct) {
  int duty = (int)(fabsf(pct) / 100.0f * PWM_MAX + 0.5f);
  if (duty > PWM_MAX) duty = PWM_MAX;
  int fwd = pct > 0 ? duty : 0;
  int rev = pct < 0 ? duty : 0;
  // sign-magnitude: one input PWM, the other low; the unused channel stays off
  ledcWrite(PIN_IN1, channel == 'A' ? fwd : 0);
  ledcWrite(PIN_IN2, channel == 'A' ? rev : 0);
  ledcWrite(PIN_IN3, channel == 'B' ? fwd : 0);
  ledcWrite(PIN_IN4, channel == 'B' ? rev : 0);
}

void stopNow() {
  target = 0;
  actual = 0;
  kickUntil = 0;
  writePins(0);
}

void printStatus() {
  Serial.printf("T %.1f %.1f %c %d\n", target, actual, channel, millis() < kickUntil ? 1 : 0);
}

void handle(String cmd) {
  cmd.trim();
  lastCmd = millis();
  if (cmd.length() == 0) return;
  char c = toupper(cmd[0]);
  String arg = cmd.substring(1);
  arg.trim();
  switch (c) {
    case 'S': {
      float v = constrain(arg.toFloat(), -100.0f, 100.0f);
      if (actual == 0 && v != 0 && kickMs > 0) kickUntil = millis() + kickMs;
      target = v;
      break;
    }
    case 'C': {
      char ch = toupper(arg.length() ? arg[0] : 'A');
      if (ch == 'A' || ch == 'B') {
        stopNow();
        channel = ch;
      }
      break;
    }
    case 'X': stopNow(); break;
    case 'R': rampRate = max(0.0f, arg.toFloat()); break;
    case 'K': kickMs = (uint32_t)max(0L, arg.toInt()); break;
    case '?': break;
    default: Serial.printf("E unknown command '%s'\n", cmd.c_str()); return;
  }
  printStatus();
}

void setup() {
  Serial.begin(115200);
  for (int pin : {PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4}) {
    ledcAttach(pin, PWM_FREQ, PWM_BITS);
    ledcWrite(pin, 0);
  }
  lastCmd = lastStep = millis();
  Serial.println("I tt_motor ready");
}

void loop() {
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      handle(line);
      line = "";
    } else if (ch != '\r' && line.length() < 64) {
      line += ch;
    }
  }

  uint32_t now = millis();
  if (now - lastCmd > WATCHDOG_MS && (target != 0 || actual != 0)) {
    stopNow();
    Serial.println("I watchdog stop");
  }

  // ramp actual towards target
  float dt = (now - lastStep) / 1000.0f;
  lastStep = now;
  if (rampRate <= 0) {
    actual = target;
  } else {
    float step = rampRate * dt;
    if (fabsf(target - actual) <= step) actual = target;
    else actual += (target > actual ? step : -step);
  }

  if (now < kickUntil && target != 0) writePins(target > 0 ? 100 : -100);
  else writePins(actual);

  if (now - lastStatus >= STATUS_MS) {
    lastStatus = now;
    printStatus();
  }
}
