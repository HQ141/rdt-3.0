import socket
import struct
class pkt:
    def __init__(self,seq,data,checksum):
        self.seq=seq
        self.data=data
        self.checksum=checksum
    def encode(self):
        var=struct.pack('?5si',self.seq,bytes(self.data, encoding='utf8'),self.checksum)
        return var
    def decode(self,pkt):
        try:
            var=struct.unpack('?5si',pkt)
            self.seq=var[0]
            self.data=var[1]
            self.checksum=var[2]
        except Exception as ex:
            raise(ex)


        
    
