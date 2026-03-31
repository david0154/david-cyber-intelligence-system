#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
CLI Entry Point — Works on Windows, macOS, Linux
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

console = Console()

BANNER = """
██████╗  █████╗ ██╗   ██╗██╗██████╗      ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██║   ██║██║██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║  ██║███████║██║   ██║██║██║  ██║    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║  ██║██╔══██║╚██╗ ██╔╝██║██║  ██║    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
██████╔╝██║  ██║ ╚████╔╝ ██║██████╔╝    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝      ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝

            INTELLIGENCE SYSTEM v1.0 | Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

MENU = """
[1]  🦠  Malware Analysis
[2]  🌐  Network IDS
[3]  🕵️   OSINT Investigation
[4]  🧪  Pentest Engine
[5]  🛡️   Defense Engine
[6]  🧠  Threat Intelligence
[7]  ✈️   Flight Tracker
[8]  🚢  Ship Tracker
[9]  🛰️   Satellite Tracker
[10] 🗺️   Geo Intelligence
[11] 💬  AI Chat (LLM Brain)
[0]  🚪  Exit
"""

def print_banner():
    console.print(Panel(BANNER, style="bold cyan"))

def run_menu():
    from core.task_router import TaskRouter
    router = TaskRouter()

    while True:
        console.print(Panel(MENU, title="[bold green]DAVID CYBER INTELLIGENCE SYSTEM[/bold green]", style="green"))
        choice = Prompt.ask("[bold yellow]Select Module[/bold yellow]")

        if choice == "0":
            console.print("[bold red]Exiting... Stay Secure! 🛡️[/bold red]")
            sys.exit(0)
        elif choice == "1":
            path = Prompt.ask("[cyan]Enter file path for malware analysis[/cyan]")
            result = router.route("malware", {"file_path": path})
            console.print(Panel(str(result), title="🦠 Malware Result", style="red"))
        elif choice == "2":
            iface = Prompt.ask("[cyan]Enter network interface (e.g. eth0)[/cyan]")
            result = router.route("network", {"interface": iface})
            console.print(Panel(str(result), title="🌐 Network IDS Result", style="blue"))
        elif choice == "3":
            target = Prompt.ask("[cyan]Enter target IP/Domain/Email[/cyan]")
            result = router.route("osint", {"target": target})
            console.print(Panel(str(result), title="🕵️ OSINT Result", style="magenta"))
        elif choice == "4":
            target = Prompt.ask("[cyan]Enter target IP/Host[/cyan]")
            result = router.route("pentest", {"target": target})
            console.print(Panel(str(result), title="🧪 Pentest Result", style="yellow"))
        elif choice == "5":
            result = router.route("defense", {})
            console.print(Panel(str(result), title="🛡️ Defense Engine", style="green"))
        elif choice == "6":
            ioc = Prompt.ask("[cyan]Enter IOC (IP/Hash/Domain)[/cyan]")
            result = router.route("intel", {"ioc": ioc})
            console.print(Panel(str(result), title="🧠 Threat Intel", style="cyan"))
        elif choice == "7":
            callsign = Prompt.ask("[cyan]Enter ICAO24 or flight callsign[/cyan]")
            result = router.route("flight", {"callsign": callsign})
            console.print(Panel(str(result), title="✈️ Flight Tracker", style="blue"))
        elif choice == "8":
            mmsi = Prompt.ask("[cyan]Enter vessel MMSI number[/cyan]")
            result = router.route("ship", {"mmsi": mmsi})
            console.print(Panel(str(result), title="🚢 Ship Tracker", style="cyan"))
        elif choice == "9":
            sat_id = Prompt.ask("[cyan]Enter NORAD satellite ID[/cyan]")
            result = router.route("satellite", {"sat_id": sat_id})
            console.print(Panel(str(result), title="🛰️ Satellite Tracker", style="magenta"))
        elif choice == "10":
            ip = Prompt.ask("[cyan]Enter IP for geo mapping[/cyan]")
            result = router.route("geo", {"ip": ip})
            console.print(Panel(str(result), title="🗺️ Geo Intelligence", style="green"))
        elif choice == "11":
            query = Prompt.ask("[cyan]Enter your query[/cyan]")
            result = router.route("chat", {"query": query})
            console.print(Panel(str(result), title="💬 LLM Response", style="white"))
        else:
            console.print("[red]Invalid choice. Try again.[/red]")

if __name__ == "__main__":
    print_banner()
    run_menu()
