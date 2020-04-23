import socket,time

'''全局变量'''
file_path = "./TcpRev/"
file_size = 0
Addr = ("192.119.91.125",2000)#127.0.0.1
Transfered = 0
Buf = 11000

'''自定义函数'''
def ProgressBar(precent,length=50,end_str=""):
    count = round(precent*length)
    progress_bar = "%4.1f"%(precent*100)+'%'+'['+'='*count+'>'+'-'*(length-count)+']'+end_str;
    print('\r'+progress_bar,end='',flush=True)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(Addr)
    data = s.recv(50)
    file_size = int( (data.decode("utf-8")).split('|')[0] )
    file_path = file_path + (data.decode("utf-8")).split('|')[1]
    if file_size != 0:
        s.send(b"ok")
        print("Prepare to receive '%s' from %s,file size is %.2fMB!"%(file_path,Addr[0],file_size/1024/1024))
        with open(file_path,"wb") as f:
            time_start = time.time()
            while True:
                if Transfered >= file_size:
                    s.sendall(b'ok')
                    print("\n传输完成，耗时%.2fs！关闭sock连接！"%(time.time()-time_start))
                    s.close()
                    break
                data = s.recv(Buf)
                Transfered = Transfered + len(data)
                ProgressBar(Transfered/file_size,end_str="file_name:%s,file_size:%.2fMB!"%(file_path,file_size/1024/1024))
                f.write(data)
    else:
        print("File size is 0,failed to transfer file!!!")
        s.close()

    input("Enter ENTER key to quit!!!")


