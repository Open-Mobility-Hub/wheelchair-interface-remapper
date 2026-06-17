
#!/bin/bash
set -e

# Create gadget
mkdir /sys/kernel/config/usb_gadget/wir
cd /sys/kernel/config/usb_gadget/wir

echo 0x0100 > bcdDevice # Version 1.0.0
echo 0x0200 > bcdUSB # USB 2.0
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceProtocol
echo 0x00 > bDeviceSubClass
echo 0x08 > bMaxPacketSize0
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x1d6b > idVendor # Linux Foundation

mkdir strings/0x409

echo "Open Mobility Hub" > strings/0x409/manufacturer
echo "WIR" > strings/0x409/product
echo "01" > strings/0x409/serialnumber

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 10 > functions/hid.usb0/report_length
echo 1 > functions/hid.usb0/subclass

cat "$(dirname "$0")/hid_desc.bin" > functions/hid.usb0/report_desc

mkdir configs/c.1
mkdir configs/c.1/strings/0x409

echo 0x80 > configs/c.1/bmAttributes
echo 200 > configs/c.1/MaxPower # 200 mA
echo "WIR Configuration" > configs/c.1/strings/0x409/configuration

ln -s functions/hid.usb0 configs/c.1/

# Enable gadget
ls /sys/class/udc > UDC
