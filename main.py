#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM v2.0
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
CLI Entry Point - Windows | macOS | Linux
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

BANNER = """[bold cyan]
██████╗  █████╗ ██╗   ██╗██╗██████╗      ██████╗██╗ ██╗██████╗ ███████╗██████╗
██╔══██╗██╔══██╗██║   ██║██║██╔══██╗    ██╔════╝██║ ██║██╔══██╗██╔════╝██╔══██╗
██║  ██║███████║██║   ██║██║██║  ██║    ██║      ██████╔╝██████╔╝█████╗  ██████╔╝
██║  ██║██╔══██║╚██╗ ██╔╝██║██║  ██║    ██║      ██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
██████╔╝██║  ██║ ╚████╔╝ ██║██████╔╝    ╚██████╗██║  ██║██████╔╝███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚═════╝╚══════╝╚═╝  ╚═╝
     [/bold cyan][dim]INTELLIGENCE SYSTEM v2.0 | Devil Pvt Ltd & Nexuzy Tech Pvt Ltd[/dim]"""

MODULES = [
    ("1",  "🦠", "Malware Analysis",      "malware"),
    ("2",  "🌐", "Network IDS",           "network"),
    ("3",  "🕵️",  "OSINT Investigation",  "osint"),
    ("4",  "🧪", "Pentest Engine",        "pentest"),
    ("5",  "🛡️",  "Defense Engine",       "defense"),
    ("6",  "🧠", "Threat Intelligence",   "intel"),
    ("7",  "✈️",  "Flight Tracker",        "flight"),
    ("8",  "🚢", "Ship Tracker",          "ship"),
    ("9",  "🛰️",  "Satellite Tracker",    "satellite"),
    ("10", "🗺️",  "Geo Intelligence",     "geo"),
    ("11", "🔍", "OWASP ZAP Scan",        "zap"),
    ("12", "📊", "Wazuh Alerts",          "wazuh"),
    ("13", "🕳️", "OpenVAS CVE Scan",     "openvas"),
    ("14", "🔑", "Hydra Brute Test",      "hydra"),
    ("15", "☁️", "Cloudflare Stats",      "cloudflare"),
    ("16", "🤖", "DeepExploit (RL)",      "deepexploit"),
    ("17", "💬", "AI Brain Chat",         "chat"),
    ("18", "🌐", "API Dashboard",         "dashboard"),
    ("0",  "🚪", "Exit",                  "exit"),
]


def print_banner():
    console.print(Panel(BANNER, border_style="cyan", padding=(0, 2)))


def print_menu():
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim", width=4)
    table.add_column(width=3)
    table.add_column(style="bold green")
    for num, icon, name, _ in MODULES:
        table.add_row(f"[{num}]", icon, name)
    console.print(Panel(table, title="[bold green]SELECT MODULE[/bold green]", border_style="green"))


def run_dashboard():
    import uvicorn
    console.print("[cyan]Starting API + Dashboard on http://0.0.0.0:8000[/cyan]")
    console.print("[dim]Docs: http://localhost:8000/docs | Dashboard: http://localhost:8000[/dim]")
    uvicorn.run("core.api:app", host="0.0.0.0", port=8000, reload=False)


def main():
    from core.task_router import TaskRouter
    router = TaskRouter()

    print_banner()
    console.print(f"[dim]Loaded modules: {list(router._engines.keys())}[/dim]\n")

    while True:
        print_menu()
        choice = Prompt.ask("[bold yellow]>[/bold yellow]").strip()

        if choice == "0":
            console.print("[bold red]Stay Secure! 🛡️ Goodbye.[/bold red]")
            sys.exit(0)

        if choice == "18":
            run_dashboard()
            continue

        module_map = {m[0]: (m[2], m[3]) for m in MODULES}
        if choice not in module_map:
            console.print("[red]Invalid choice.[/red]")
            continue

        label, mod = module_map[choice]
        console.print(f"\n[cyan]=== {label} ===[/cyan]")

        try:
            params = {}
            if mod == "malware":
                params["file_path"] = Prompt.ask("File path")
            elif mod == "network":
                params["interface"] = Prompt.ask("Interface", default="eth0")
            elif mod in ("osint", "pentest", "openvas", "deepexploit"):
                params["target"] = Prompt.ask("Target IP/Domain")
            elif mod == "intel":
                params["ioc"] = Prompt.ask("IOC (IP/Hash/Domain)")
            elif mod == "flight":
                params["callsign"] = Prompt.ask("ICAO24/Callsign")
            elif mod == "ship":
                params["mmsi"] = Prompt.ask("Vessel MMSI")
            elif mod == "satellite":
                params["sat_id"] = Prompt.ask("NORAD ID")
            elif mod == "geo":
                params["ip"] = Prompt.ask("IP address")
            elif mod == "zap":
                params["url"] = Prompt.ask("Target URL")
            elif mod == "wazuh":
                params["limit"] = int(Prompt.ask("Alert limit", default="20"))
            elif mod == "hydra":
                params["target"] = Prompt.ask("Target host")
                params["service"] = Prompt.ask("Service", default="ssh")
            elif mod == "chat":
                params["query"] = Prompt.ask("Your query")
            elif mod == "cloudflare":
                params["zone_id"] = Prompt.ask("Zone ID (optional)", default="")
            elif mod == "defense":
                pass

            result = router.route(mod, params)
            console.print_json(data=result)

        except KeyboardInterrupt:
            console.print("\n[dim]Cancelled.[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
