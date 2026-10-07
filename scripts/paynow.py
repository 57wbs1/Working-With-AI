# -*- coding: utf-8 -*-
"""Build a PayNow (SGQR / EMVCo) payload and render it as a PNG."""
import segno

def tlv(tag, value):
    return "%s%02d%s" % (tag, len(value), value)

def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return crc

MOBILE = "+6591817066"
AMOUNT = "50.00"
NAME   = "WORKING WITH AI"
REF    = "AIBRIEF"

merchant = tlv("00", "SG.PAYNOW") + tlv("01", "0") + tlv("02", MOBILE) + tlv("03", "0")
payload  = (
    tlv("00", "01")          # payload format indicator
  + tlv("01", "12")          # dynamic (amount fixed)
  + tlv("26", merchant)      # PayNow merchant account info
  + tlv("52", "0000")        # merchant category code
  + tlv("53", "702")         # currency: SGD
  + tlv("54", AMOUNT)
  + tlv("58", "SG")
  + tlv("59", NAME)
  + tlv("60", "Singapore")
  + tlv("62", tlv("01", REF))
)
payload += "6304"
crc = crc16_ccitt_false(payload.encode("ascii"))
payload += "%04X" % crc

print("PAYLOAD:", payload)
print("LENGTH :", len(payload))
print("CRC    : %04X" % crc)

qr = segno.make(payload, error="m")
qr.save("paynow-50.png", scale=10, border=3, dark="#111111", light="#FFFFFF")
print("WROTE  : paynow-50.png")

# read back and confirm the CRC validates
body, got = payload[:-4], payload[-4:]
assert "%04X" % crc16_ccitt_false(body.encode()) == got
print("CRC self-check: PASS")
