import subprocess
import re
import time
import statistics
import platform
from datetime import datetime


def ping_host(host, count=4):
    """Ping a host and return RTT values in ms."""
    system = platform.system().lower()
    
    if system == "windows":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout
    except subprocess.TimeoutExpired:
        return None, "Timeout: host unreachable"
    except FileNotFoundError:
        return None, "ping command not found"
    
    rtt_values = re.findall(r'time[=<](\d+\.?\d*)\s*ms', output, re.IGNORECASE)
    rtt_values = [float(v) for v in rtt_values]
    
    if not rtt_values:
        return None, f"No response from {host}"
    
    return rtt_values, None


def analyze_delay(rtt_values):
    """Compute delay statistics from a list of RTT values."""
    if not rtt_values:
        return {}
    return {
        "min":    round(min(rtt_values), 2),
        "max":    round(max(rtt_values), 2),
        "avg":    round(statistics.mean(rtt_values), 2),
        "stddev": round(statistics.stdev(rtt_values), 2) if len(rtt_values) > 1 else 0.0,
        "count":  len(rtt_values),
    }


def classify_latency(avg_ms):
    """Return a human-readable quality label based on average RTT."""
    if avg_ms < 20:
        return "Excellent"
    elif avg_ms < 60:
        return "Good"
    elif avg_ms < 150:
        return "Acceptable"
    else:
        return "Poor"


def measure_hosts(hosts, count=4):
    """
    Measure and compare latency across multiple hosts.
    
    Args:
        hosts  : list of hostnames or IPs to ping
        count  : number of ping packets per host
    
    Returns:
        list of result dicts, one per host
    """
    results = []
    
    for host in hosts:
        print(f"  Pinging {host} ({count} packets)...", end=" ", flush=True)
        rtt_values, error = ping_host(host, count)
        
        if error:
            print(f"FAILED \u2014 {error}")
            results.append({
                "host":  host,
                "error": error,
                "stats": None,
            })
        else:
            stats = analyze_delay(rtt_values)
            label = classify_latency(stats["avg"])
            print(f"avg={stats['avg']} ms  [{label}]")
            results.append({
                "host":       host,
                "error":      None,
                "rtt_values": rtt_values,
                "stats":      stats,
                "quality":    label,
            })
    
    return results


def compare_paths(results):
    """Print a side-by-side comparison table of all measured hosts."""
    header = f"{'Host':<25} {'Min':>8} {'Avg':>8} {'Max':>8} {'Stddev':>8} {'Quality':<12}"
    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))
    
    for r in results:
        if r["error"]:
            print(f"{r['host']:<25} {'ERROR \u2014 ' + r['error']}")
        else:
            s = r["stats"]
            print(
                f"{r['host']:<25}"
                f"{s['min']:>7.1f}ms"
                f"{s['avg']:>7.1f}ms"
                f"{s['max']:>7.1f}ms"
                f"{s['stddev']:>7.1f}ms"
                f"  {r['quality']:<12}"
            )
    
    print("=" * len(header))
    
    successful = [r for r in results if not r["error"]]
    if successful:
        best = min(successful, key=lambda r: r["stats"]["avg"])
        print(f"\n  Lowest latency path: {best['host']}  ({best['stats']['avg']} ms avg)\n")


def run_tool(hosts=None, count=4, repeat=1, interval=5):
    """
    Main entry point for the Network Delay Measurement Tool.
    
    Args:
        hosts    : list of hosts to measure (defaults to common public DNS servers)
        count    : ping packets per host per round
        repeat   : how many measurement rounds to run
        interval : seconds to wait between rounds
    """
    if hosts is None:
        hosts = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
    
    print("\n========================================")
    print("   Network Delay Measurement Tool")
    print("========================================")
    print(f"  Hosts   : {', '.join(hosts)}")
    print(f"  Packets : {count} per host")
    print(f"  Rounds  : {repeat}")
    print("========================================\n")
    
    all_rounds = []
    
    for round_num in range(1, repeat + 1):
        if repeat > 1:
            print(f"Round {round_num} of {repeat}  [{datetime.now().strftime('%H:%M:%S')}]")
        
        results = measure_hosts(hosts, count)
        compare_paths(results)
        all_rounds.append(results)
        
        if round_num < repeat:
            print(f"  Waiting {interval}s before next round...\n")
            time.sleep(interval)
    
    if repeat > 1:
        print("\n=== Aggregate Summary (all rounds) ===")
        for host in hosts:
            host_avgs = []
            for round_results in all_rounds:
                for r in round_results:
                    if r["host"] == host and r["stats"]:
                        host_avgs.append(r["stats"]["avg"])
            if host_avgs:
                overall_avg = round(statistics.mean(host_avgs), 2)
                print(f"  {host:<25} overall avg = {overall_avg} ms")
        print()


if __name__ == "__main__":
    run_tool(
        hosts=["8.8.8.8", "1.1.1.1", "google.com", "cloudflare.com"],
        count=4,
        repeat=1,
    )
