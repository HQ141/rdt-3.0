def gen_checksum(msg):
        sum=0
        for i in msg:
            sum+=ord(i)
        while (len(bin(sum)))-2>8:
            tmp=int(sum / pow(2,(len(bin(sum)))-3))
            sum=sum % pow(2,(len(bin(sum)))-3)
            sum=sum+tmp
        return sum

print(gen_checksum('hello there'))