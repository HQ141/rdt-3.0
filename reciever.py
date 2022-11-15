import rdt_alpha1
reciever=rdt_alpha1.rdt(9090,("127.0.0.1",9999))
print(reciever.recv_data())

