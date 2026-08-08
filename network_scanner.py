from scapy.all import sniff, IP, TCP, UDP
import wifi  # 替换为纯 Python 的 wifi 库


# ================= 功能 1：局域网数据包抓包 =================
def start_packet_sniffer():
    def packet_callback(packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = "Unknown"
            port_info = ""

            if packet.haslayer(TCP):
                protocol = "TCP"
                port_info = f" (Port: {packet[TCP].sport} -> {packet[TCP].dport})"
            elif packet.haslayer(UDP):
                protocol = "UDP"
                port_info = f" (Port: {packet[UDP].sport} -> {packet[UDP].dport})"

            print(f"[{protocol}] {src_ip} --> {dst_ip}{port_info}")

    print("\n📡 正在监听局域网数据包，按 Ctrl+C 停止...")
    try:
        sniff(prn=packet_callback, store=0)
    except KeyboardInterrupt:
        print("\n🛑 抓包监听已停止。")


# ================= 功能 2：扫描附近 WiFi (使用新库) =================
def scan_nearby_wifi():
    print("\n📶 正在扫描附近的 WiFi，请稍候...")
    try:
        # 自动获取无线网卡并扫描所有可见的 WiFi 网络
        cells = wifi.Cell.all('wlan0')  # Windows 下通常默认即可，若报错可尝试不传参或传网卡名
    except Exception as e:
        print(f"❌ 扫描失败，请确保以管理员身份运行。错误信息: {e}")
        return

    if not cells:
        print("未发现任何 WiFi 网络。")
        return

    print(f"\n共发现 {len(cells)} 个 WiFi 网络：")
    print("-" * 60)
    print(f"{'WiFi名称 (SSID)':<30} {'信号强度':<10} {'加密方式'}")
    print("-" * 60)

    for cell in cells:
        ssid = cell.ssid if cell.ssid else "<隐藏网络>"
        signal = cell.signal
        security = cell.encryption  # 直接读取加密方式

        print(f"{ssid:<30} {signal:<10} {security}")


# ================= 主程序菜单 =================
if __name__ == "__main__":
    while True:
        print("\n" + "=" * 30)
        print("   🛠️ 网络探索小工具")
        print("=" * 30)
        print("1. 抓取局域网数据包")
        print("2. 扫描附近的 WiFi")
        print("0. 退出程序")

        choice = input("\n请输入你的选择 (0/1/2): ").strip()

        if choice == "1":
            start_packet_sniffer()
        elif choice == "2":
            scan_nearby_wifi()
        elif choice == "0":
            print("👋 拜拜，下次见！")
            break
        else:
            print("⚠️ 输入无效，请重新选择。")