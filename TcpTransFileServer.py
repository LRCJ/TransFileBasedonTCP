import socket,time,os,sys

'''全局变量'''
file_path = sys.argv[1]
if not os.path.isfile(file_path):
    raise Exception("'%s' is not file!!!"%file_path)
file_size = os.path.getsize(file_path)
Transfered = 0
Buf = 10240
Addr = ("0.0.0.0",2000)

'''自定义函数'''
def ProgressBar(precent,length=50,end_str=""):
    count = round(precent*length)
    progress_bar = "%4.1f"%(precent*100)+'%'+'['+'='*count+'>'+'-'*(length-count)+']'+end_str;
    print('\r'+progress_bar,end='',flush=True)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(Addr)
    s.listen()
    print("Waiting !!!")
    sock,addr = s.accept()
    print('Accept new connection from %s:%s...' % addr)

    sock.send(("%d|%s"%(file_size,file_path.split('/')[-1])).encode("utf-8"))
    data = sock.recv(50)
    if data == b"ok":
        print("Start transfer '%s' to %s,file size is %.2fMB!!!"%(file_path,addr[0],file_size/1024/1024))
        time_start = time.time()
        with open(file_path,"rb") as f:
            while True:
                data = f.read(Buf)
                if data == b'':
                    print("\n传输完成，耗时%fs！"%(time.time()-time_start))
                    data = sock.recv(20)
                    print("关闭socket连接！")
                    sock.close()
                    break
                sock.sendall(data)
                Transfered = Transfered + Buf
                ProgressBar(Transfered/file_size,end_str="file_name:%s,file_size:%.2fMB!"%(file_path,file_size/1024/1024))
        s.close()
    else:
        print(data.decode("utf-8"))
        print("Refused to transfer file!!!")
        sock.close()
        s.close()

    input("Enter ENTER key to quit!!!")

