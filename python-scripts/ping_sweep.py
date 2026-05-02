
"""Ping sweep: discover live hosts on a subnet using ICMP."""
import argparse
import ipaddress
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping(host: str, timeout: int = 1) -> tuple[str, bool]:
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), str(host)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return str(host), result.returncode == 0


def sweep(network: str, workers: int = 100, timeout: int = 1) -> list[str]:
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        print(f"[!] Invalid network: {e}", file=sys.stderr)
        sys.exit(1)

    hosts = list(net.hosts())
    if not hosts:
        print("[!] No usable hosts in that range.", file=sys.stderr)
        sys.exit(1)

    live = []
    print(f"[*] Sweeping {len(hosts)} hosts on {net} ...")

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(ping, h, timeout): h for h in hosts}
        for future in as_completed(futures):
            host, is_up = future.result()
            if is_up:
                print(f"  [+] {host} is UP")
                live.append(host)

    return sorted(live, key=lambda ip: ipaddress.ip_address(ip))


def main():
    parser = argparse.ArgumentParser(
        description="Ping sweep a subnet to find live hosts."
    )
    parser.add_argument(
        "network",
        help="Target network in CIDR notation, e.g. 192.168.1.0/24",
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Number of concurrent ping threads (default: 100)",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds per host (default: 1)",
    )
    args = parser.parse_args()

    live_hosts = sweep(args.network, args.workers, args.timeout)

    print(f"\n[*] Sweep complete. {len(live_hosts)} host(s) up.")
    if live_hosts:
        print("\nLive hosts:")
        for h in live_hosts:
            print(f"  {h}")


if __name__ == "__main__":
    main()


