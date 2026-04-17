# 📡 Network Delay Measurement Tool

A Python-based tool to measure and analyze network latency (delay) between your system and multiple hosts using ICMP ping.

It collects round-trip time (RTT) data, computes statistics, and compares multiple network paths to help identify the fastest and most reliable connection.

---

## 🚀 Features

* ✅ Ping multiple hosts (IP or domain)
* 📊 Compute latency statistics:

  * Minimum delay
  * Maximum delay
  * Average delay
  * Standard deviation
* 🏷️ Classify network quality:

  * Excellent
  * Good
  * Acceptable
  * Poor
* 📈 Compare multiple hosts side-by-side
* 🔁 Run repeated measurements with intervals
* 🏆 Automatically detects the lowest latency path

---

## 🧠 How It Works

1. The tool sends ICMP ping packets to each host.
2. Extracts RTT (Round Trip Time) values from the response.
3. Computes statistical metrics using Python’s `statistics` module.
4. Classifies latency based on average delay.
5. Displays results in a formatted comparison table.

---

## 📂 Project Structure

```
network_delay_tool.py
README.md
```

---

## ⚙️ Requirements

* Python 3.x
* Internet connection
* OS with `ping` command available (Windows/Linux/macOS)

---

## ▶️ Usage

Run the script directly:

```bash
python network_delay_tool.py
```

---

## 🛠️ Example Configuration

You can modify the parameters in the `run_tool()` function:

```python
run_tool(
    hosts=["8.8.8.8", "1.1.1.1", "google.com", "cloudflare.com"],
    count=4,
    repeat=1,
)
```

### Parameters:

* `hosts` → List of servers to test
* `count` → Number of ping packets per host
* `repeat` → Number of measurement rounds
* `interval` → Time gap between rounds (seconds)

---

## 📊 Sample Output

```
Host                      Min     Avg     Max   Stddev   Quality
--------------------------------------------------------------
8.8.8.8                  10.2ms  12.5ms  15.1ms  1.8ms   Excellent
1.1.1.1                   9.8ms  11.3ms  13.7ms  1.5ms   Excellent
google.com               20.4ms  25.6ms  30.2ms  3.2ms   Good
cloudflare.com           18.2ms  22.1ms  27.5ms  2.9ms   Good
```

🏆 Lowest latency path is automatically highlighted.

---

## 🧩 Key Functions

* `ping_host()` → Sends ping and extracts RTT values
* `analyze_delay()` → Computes statistics
* `classify_latency()` → Labels network quality
* `measure_hosts()` → Runs tests for all hosts
* `compare_paths()` → Displays results in table
* `run_tool()` → Main controller function

---

## 🌐 Default Hosts

If no hosts are provided, the tool uses:

* Google DNS → `8.8.8.8`
* Cloudflare DNS → `1.1.1.1`
* Quad9 DNS → `9.9.9.9`

---

## 💡 Use Cases

* Network performance analysis
* Comparing ISPs or routes
* Debugging latency issues
* Academic / CN lab experiments

---

## 🔮 Future Improvements

* GUI dashboard 📊
* Export results to CSV
* Real-time plotting
* Packet loss analysis

---

## 👨‍💻 Author

Developed as a networking utility project for analyzing delay and performance across multiple hosts.

---

## 📜 License

This project is open-source and free to use for educational purposes.
