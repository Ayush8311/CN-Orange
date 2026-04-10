# CN-Orange
# 🔥 SDN Firewall using Mininet & POX Controller

## 📌 Problem Statement

Traditional networks use static rules for traffic control, making them inflexible and difficult to manage.
The goal of this project is to implement a **Software Defined Networking (SDN) based firewall** using Mininet and the POX controller that:

* Demonstrates controller–switch interaction
* Uses OpenFlow match–action rules
* Controls network traffic dynamically

---

## 🎯 Objective

To design a firewall that:

* Blocks traffic from a specific host (h1)
* Allows communication between other hosts
* Demonstrates SDN-based access control

---

## 🏗️ Network Topology

* 1 Switch (s1)
* 3 Hosts (h1, h2, h3)
* Remote POX Controller

---

## ⚙️ Implementation

### 🔹 Controller Logic

* Uses POX controller
* Handles:

  * `ConnectionUp` → installs firewall rules
  * `PacketIn` → handles forwarding

### 🔹 Firewall Rule

* Block traffic from:

  * MAC: `00:00:00:00:00:01` (h1)

### 🔹 Flow Rules

* Match: Source MAC address
* Action: DROP (no action)

---

## 🚀 How to Run

### 1. Start Controller

```bash
./pox.py firewall
```

### 2. Start Mininet

```bash
sudo mn --topo single,3 --controller remote
```

---

## 🧪 Test Cases

### ❌ Blocked Traffic

```bash
h1 ping h2
```

Expected: Packet loss / unreachable

---

### ✅ Allowed Traffic

```bash
h2 ping h3
```

Expected: Successful ping

---

## 📊 Results

| Test Case | Result    |
| --------- | --------- |
| h1 → h2   | ❌ Blocked |
| h2 → h3   | ✅ Allowed |

---

## 📸 Proof of Execution

### 🔴 Blocked Traffic

![Blocked](screenshots/blocked.png)

### 🟢 Allowed Traffic

![Allowed](screenshots/allowed.png)

### ⚙️ Controller Output

![Controller](screenshots/controller.png)

---

## 📈 Performance Observation

* Latency measured using ping
* Flow rules dynamically installed
* Packet forwarding controlled by controller

---

## 🧠 Conclusion

This project demonstrates how SDN enables **centralized and dynamic traffic control**.
The firewall successfully blocks unauthorized hosts while allowing normal communication.

---

## 📚 References

* Mininet Documentation
* POX Controller Documentation
* OpenFlow Protocol
