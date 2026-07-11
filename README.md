<div align="center">

# `allan-abraham`

**Embedded Systems &bull; Cloud Infrastructure &bull; Computer Vision**

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=2000&pause=1000&color=58A6FF&center=true&vCenter=true&width=450&lines=I2C+%2F+SPI+%2F+UART;AWS+Architecture;Quantized+ML+Inference;Kalman+Filter+Sensor+Fusion)](https://git.io/typing-svg)

[`portfolio`](https://allan-portfolio-five.vercel.app) &nbsp;&bull;&nbsp; [`linkedin`](https://www.linkedin.com/in/abrahamallan)

</div>

---

### 🧑‍💻 about me

I am a Software Engineer based in Bangalore, India. I specialize in building at the intersection of hardware and software—developing custom embedded firmware, configuring cloud infrastructure, and deploying machine learning models to edge devices. 

I enjoy taking things apart to understand what happens beneath the abstraction layer. Whether it's optimization of low-level ISR latencies, soldering upgraded GDDR6 memory dies onto PCBs, or debugging memory drift on microcontrollers, I build systems by understanding their limits.

---

### 💻 technology stack

* **Languages:** `C` &bull; `C++` &bull; `Python` &bull; `Java` &bull; `Assembly (ARM/AVR)` &bull; `SQL` &bull; `TypeScript`
* **Hardware & Systems:** `STM32` &bull; `Arduino` &bull; `GPIO` &bull; `I2C` &bull; `SPI` &bull; `UART` &bull; `Linux Shell`
* **Cloud & DevOps:** `AWS (EC2, S3, SQS, Lambda)` &bull; `Docker` &bull; `Kubernetes` &bull; `CI/CD Pipelines`
* **AI & Machine Learning:** `PyTorch` &bull; `OpenCV` &bull; `TensorFlow` &bull; `Quantization` &bull; `Kalman Filters`

---

### 🛠️ featured systems

<details open>
<summary><b>1. Autonomous Navigation Bot (C++ / Arduino)</b></summary>
<blockquote>
Built a two-wheeled crawling robot on Arduino Uno that uses ultrasonic and IR sensors to navigate around obstacles. The bot maps a room incrementally and makes turn decisions in real time without any pre-programmed routes.
<br/><br/>
<b>Challenge:</b> IR sensors turned completely unreliable near dark surfaces or under fluorescent lighting — readings would swing by 30–40% with no physical change in distance. This caused the bot to spin randomly in corners.
<br/>
<b>Solution:</b> Added a 5-sample moving average per sensor and cross-validated readings between the ultrasonic and IR before making any turn decision. Noisy input stopped causing actual movement errors after that.
<br/><br/>
<code>1,240 LOC</code> &bull; <code>16 MHz clock</code> &bull; <code>1.8 KB SRAM</code>
</blockquote>
</details>

<details>
<summary><b>2. Multi-Sensor Embedded Framework (C / STM32)</b></summary>
<blockquote>
Wrote a lightweight sensor abstraction layer for STM32 microcontrollers that handles multiple I2C and SPI devices sharing the same bus. The framework manages interrupt priorities, debounces digital inputs, and exposes a clean API so sensor reads don't block the main loop.
<br/><br/>
<b>Challenge:</b> When two sensors triggered interrupts within microseconds of each other, the ISR for the slower one would get preempted repeatedly and never complete — effectively starving it.
<br/>
<b>Solution:</b> Implemented a priority-tagged volatile flag register system. ISRs now only set a flag and return immediately. The main loop reads flags and dispatches handlers in sequence, which eliminated the starvation entirely.
<br/><br/>
<code>2,800 LOC</code> &bull; <code>ISR latency < 8µs</code> &bull; <code>STM32 + HAL</code>
</blockquote>
</details>

<details>
<summary><b>3. ML Model Deployment Pipeline (Python / AWS)</b></summary>
<blockquote>
Set up an end-to-end pipeline that takes a trained PyTorch model, packages it, and deploys it to AWS for inference. Users submit images through an API, jobs get queued via SQS, and a worker on EC2 runs inference and writes results back. The Lambda just handles the API layer — it doesn't touch the model.
<br/><br/>
<b>Challenge:</b> First version had Lambda trying to load the model and run inference directly. Cold starts alone were taking 18–22 seconds, and anything above a batch size of 4 hit the timeout wall.
<br/>
<b>Solution:</b> Separated concerns completely — Lambda only validates the request and pushes a job to SQS. An EC2 worker with the model already warm in memory picks it up and returns results asynchronously. Latency dropped to under 3 seconds for standard requests.
<br/><br/>
<code>3,400 LOC</code> &bull; <code>p95 latency < 3s</code> &bull; <code>EC2 + SQS + S3</code>
</blockquote>
</details>

<details>
<summary><b>4. Edge Pothole Detection (Edge CV / PyTorch / Pi)</b></summary>
<blockquote>
Mounted a camera and GPS module on a vehicle and built a pipeline that detects potholes from the live feed, classifies severity (shallow / deep / edge-damage), and logs the GPS coordinates with each detection.
<br/><br/>
<b>Challenge:</b> MobileNetV2 was still too slow on the Pi's ARM CPU — we were getting around 4–5 FPS, which meant detections were being missed between frames at normal driving speed.
<br/>
<b>Solution:</b> Switched to a quantized INT8 model and offloaded post-processing to a separate thread. Got to ~14 FPS, which is workable. Also added overlap detection between frames to catch anything the model missed on a single pass.
<br/><br/>
<code>INT8 Quantized Model</code> &bull; <code>14 FPS on Pi 4</code> &bull; <code>AWS S3 Integration</code>
</blockquote>
</details>

---

### ⚠️ hardware incident report: INCIDENT-404

```
[SYSTEM ALERT]: Thermal runaway detected on VRM.
[ROOT CAUSE]: GPU VRAM hardware upgrade (GDDR6 desoldering/resoldering) combined with a custom BIOS voltage override pushing power draw 40% past design limits.
[IMPACT]: motherboard scorched, VRM MOSFETs backfed unregulated spike into CPU socket. The CPU did not survive.
[RESOLUTION]: Validating power phases using current sensing, testing VCore modifications in 10mV increments under a thermal camera. 'It might just work' is no longer an engineering methodology.
```

---

### 📊 activity & contribution telemetry

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=allanabtech&theme=github-compact" width="100%" alt="Contribution Graph" />

&nbsp;

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/allanabtech/allanabtech/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/allanabtech/allanabtech/output/github-snake.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/allanabtech/allanabtech/output/github-snake.svg" width="100%" />
</picture>

&nbsp;

<!-- STREAK_LINE_START -->
**total contributions: 25 &nbsp;·&nbsp; current streak: 1 &nbsp;·&nbsp; longest streak: 2**
<!-- STREAK_LINE_END -->

&nbsp;

<img src="https://komarev.com/ghpvc/?username=allanabtech&style=flat-square&color=58a6ff" alt="Profile Views" />

</div>
