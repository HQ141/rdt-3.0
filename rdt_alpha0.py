import socket
import struct
class pkt:
    def __init__(self):
        self.seq=False
        self.data=""
        self.checksum=0

    def corrupt(self,data,checksum):
        ch=self.gen_checksum(data)
        if(ch!=checksum):
            return True
        return False


    def gen_checksum(self,msg):
        for i in msg:
            sum+=ord(i)
        while (len(bin(sum)))-2>8:
            print(pow(2,(len(bin(sum)))-3))
            tmp=int(sum / pow(2,(len(bin(sum)))-3))
            sum=sum % pow(2,(len(bin(sum)))-3)
            print(sum)
            print(tmp)
            sum=sum+tmp
        return sum


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
            self.data=var[1].decode()
            self.checksum=var[2]
            return self.seq,self.data,self.checksum
        except Exception as ex:
            raise(ex)


    def isACK(self):
        if(self.data=="ACK0"):
            return True
        return False


    def isNACK(self):
        if(self.data=="ACK1"):
            return True
        return False

class rdt:
    def __init__(self,sc_port,ds_ip,ds_port):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(('localhost',9898))
        self.socket.settimeout(20)
        self.ds_ip=ds_ip
        self.seq=False
        self.ds_port=ds_port



    def corrupt(self,data,checksum):
        ch=self.gen_checksum(data)
        if(ch!=checksum):
            return True
        return False


    def gen_checksum(self,msg):
        for i in msg:
            sum+=ord(i)
        while (len(bin(sum)))-2>8:
            print(pow(2,(len(bin(sum)))-3))
            tmp=int(sum / pow(2,(len(bin(sum)))-3))
            sum=sum % pow(2,(len(bin(sum)))-3)
            print(sum)
            print(tmp)
            sum=sum+tmp
        return sum



    def rdt_recv(self):
        self.socket.settimeout(30)
        try:
            data,addr=self.socket.recvfrom(4096)
            packet=pkt()
            seq,msg,cs=packet.decode(data)
            if(self.corrupt(msg,cs)):
                raise Exception("Resend")
            if(packet.isNACK()):
                raise Exception("Resend")
        except:
            return None



    def send_data(self,tmp_msg):
        for i in tmp_msg:
            while True:
                packet=pkt(self.seq,i,self.gen_checksum(i))
                self.udt_send(packet.encode())
                tmp=self.rdt_recv()
                if(tmp != None):
                    self.seq= not self.seq
                    break


    def udt_send(self,pkt):
            self.socket.sendto(pkt,(self.ds_ip,self.ds_port))



    def rdt_send(self,msg):
        tmp_msg=[]
        while len(msg)>5:
            tmp_msg.append(msg[0:5])
            msg=msg[5:len(msg)]
        tmp_msg.append(msg)
        self.send_data(tmp_msg)
    
