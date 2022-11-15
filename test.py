
import struct
tmp_pkt=[]
seq=1
data='hello'
checksum=10
var=struct.pack('?5si',seq,bytes(data, encoding='utf8'),checksum)
print(var)
tup = struct.unpack('?5si', var)
print(tup)