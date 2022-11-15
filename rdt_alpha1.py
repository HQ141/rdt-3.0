import socket
import struct
import time
class pkt:
    def corrupt(self,data,checksum):
        ch=pkt.gen_checksum(data)
        if(ch!=checksum):
            return True
        return False

    def mk_ack_pkt(seq):
        var=struct.pack('?5si',seq,bytes('ACK',encoding='utf8'),pkt.gen_checksum('ACK'))
        return var

    def gen_checksum(msg):
        sum=0
        for i in msg:
            sum+=ord(i)
        while (len(bin(sum)))-2>8:
            tmp=int(sum / pow(2,(len(bin(sum)))-3))
            sum=sum % pow(2,(len(bin(sum)))-3)
            sum=sum+tmp
        return sum


    def __init__(self,seq=False,data=""):
        self.seq=seq
        self.data=data
        self.checksum=pkt.gen_checksum(data)


    def encode(self):
        var=struct.pack('?5si',self.seq,bytes(self.data, encoding='utf8'),self.checksum)
        return var


    def decode(self,pkt):
        try:
            var=struct.unpack('?5si',pkt)
            self.seq=var[0]
            self.data=var[1].decode()
            self.checksum=var[2]
            return self.seq,self.data,self.checksum
        except Exception as ex:
            raise(ex)

#rdt3.0
class rdt:
    def __init__(self,sc_port,ds_addr):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(('localhost',sc_port))
        self.ds_addr=ds_addr
        self.seq=False
        self.buffer=""

    def send_data(self,tmp_msg):
        for i in tmp_msg:
            while True:
                packet=pkt(self.seq,i)
                print(packet.encode())
                self.udt_send(packet.encode())
                try:
                    self.socket.settimeout(30)
                    seq,data,checksum=self.rdt_recv()
                    if(seq != self.seq):
                        self.seq=seq
                        break
                except:
                    pass
        
    def rdt_send(self,msg):
        tmp_msg=[]
        while len(msg)>5:
            tmp_msg.append(msg[0:5])
            msg=msg[5:len(msg)]
        tmp_msg.append(msg)
        self.send_data(tmp_msg)

    def udt_send(self,pkt):
        self.socket.sendto(pkt,self.ds_addr)

    def recv_data(self):
        self.buffer=""
        while True:
            print(self.buffer)
            print(self.seq)
            try:
                while True:
                    tmp=self.rdt_recv()
                    if(tmp):
                        try:
                            self.udt_send(pkt.mk_ack_pkt( not self.seq))
                            self.seq= not self.seq
                            break
                        except Exception as e:
                            print(e)
                    else:
                        try:
                            self.udt_send(pkt.mk_ack_pkt(self.seq))
                            break
                        except Exception as e:
                            print(e) 
            except:
                pass


    def rdt_recv(self):
        data,addr=self.socket.recvfrom(4096)
        self.ds_addr=addr
        return(self.extract(data))

    def extract(self,data):
        packet=pkt()
        seq,data,checksum=packet.decode(data)
        if(packet.corrupt(data,checksum)):
            return None
        self.buffer=self.buffer+data
        return seq,data,checksum
