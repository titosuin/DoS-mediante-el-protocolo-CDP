# Laboratorio de Seguridad en Redes: Ataques de Capa 2 con Scapy

**Estudiante:** Martin Alexander Perez Moya  
**Matrícula:** 2024-2295  
**Asignatura:** Seguridad en Redes  
**Fecha:** Febrero 2026

**Link del video**: https://youtu.be/s6Emg7BInSg


---

 Descripción y Topología del Escenario

El laboratorio se ha desplegado en un entorno virtualizado utilizando **GNS3**, simulando una infraestructura de red corporativa vulnerada desde el interior.

### Detalles de la Topología
* **Segmentación de Red:** Se ha configurado la **VLAN 2295** (basada en los últimos 4 dígitos de la matrícula).
* **Direccionamiento IP:** Subred `10.22.95.0/24`.
* **Infraestructura:**
    * **Gateway (Router Cisco IOU L3):** Configurado como *Router-on-a-Stick* en la interfaz `e0/0.2295` con IP `10.22.95.1`.
    * **Switch (Cisco IOU L2):** Puertos de acceso configurados en la VLAN 2295.
* **Actores:**
    * **Atacante:** Kali Linux (IP asignada por DHCP: `10.22.95.4`).
    * **Víctima:** PC1 / VPCS (IP asignada por DHCP: `10.22.95.3`).

<img width="641" height="712" alt="image" src="https://github.com/user-attachments/assets/07ad4a81-ae2d-4e63-ad94-2061a26abefb" />

 Dispositivo   | Interfaz	|Dirección IP         |	Máscara de Subred 	|Gateway Predeterminado
 Router        | Gateway	|e0/0.2295	10.22.95.1|	255.255.255.0 (/24)	|N/A
 Switch L2	   | VLAN 2295	| 10.22.95.2 (Gestión)|	255.255.255.0 (/24)	|10.22.95.1
 Kali Linux    | Atacante  |	10.22.95.4	       |255.255.255.0 (/24)	|10.22.95.1
 PC1 (Víctima) |eth0 DHCP  | 10.22.95.3	       |255.255.255.0 (/24)	|10.22.95.1

---

 Requisitos Previos y Herramientas

Para la ejecución exitosa de estos scripts, se requiere el siguiente entorno:

* **Sistema Operativo:** Kali Linux o cualquier distribución Linux basada en Debian.
* **Lenguaje:** Python 3.x.
* **Librerías:** `Scapy` (Instalación: `sudo apt install python3-scapy`).
* **Privilegios:** Acceso **Root** (sudo) es obligatorio para la inyección de paquetes en crudo y la manipulación de interfaces de red.

---

 Ataque : DoS mediante Inundación CDP (CDP Flood)

### Objetivo del Script
El script `ataque_cdp2.py` tiene como objetivo saturar la tabla de vecinos CDP (Cisco Discovery Protocol) del switch objetivo, provocando una Denegación de Servicio en la capacidad de administración del equipo.

Debido a que los equipos Cisco descartan paquetes CDP mal formados, este script fue desarrollado utilizando **inyección de paquetes RAW**, construyendo manualmente la cabecera del protocolo y calculando el **Checksum (RFC 1071)** matemáticamente para evadir los filtros de integridad del switch.

### Parámetros Usados
* **Interfaz:** `eth0`
* **Dirección Destino:** Multicast Cisco `01:00:0c:cc:cc:cc`.
* **Campos Falsificados (TLVs):**
    * *Device ID:* Generado aleatoriamente (`Router_Hack_XXX`).
    * *Port ID:* Simulación de interfaces Ethernet (`Ethernet0/X`).
    * *Capabilities:* Flag `0x0001` (Simulación de rol de Router).

### Evidencia de Ejecución

<img width="520" height="106" alt="image" src="https://github.com/user-attachments/assets/cb6811b3-39d8-4bfd-a7bb-124bde2fd8a0" />



<img width="658" height="388" alt="image" src="https://github.com/user-attachments/assets/48b78c10-5d50-435d-95a7-0f3d5dbc086b" />


---

Medidas de Mitigación
Para proteger la infraestructura contra estos vectores de ataque, se recomiendan las siguientes configuraciones de endurecimiento (Hardening):

Contra CDP Flood
Deshabilitar CDP: En todas las interfaces que conectan a usuarios finales o zonas no confiables.
```bash
Switch(config-if)# no cdp run
```
Control de Versión: Utilizar CDPv2 con autenticación (si es soportado) o migrar a LLDP con medidas de seguridad.


  
