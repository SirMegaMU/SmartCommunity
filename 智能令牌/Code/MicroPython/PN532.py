from machine import UART 
import time
import struct
u1=UART(2,115200,rx=machine.Pin(16),tx=machine.Pin(17))
class Pn532(object):
    def __init__(self,uart):
        self.u1 = uart
        self.uid=b''#uid预付值
        self.awaken()
    def checks(self,verify):#取得校验和的后两位的补码并拼接到验证命令后面
        verify_list=struct.unpack('%db'%len(verify),verify) 
        check=struct.pack('bb',~sum(verify_list))
        verify=verify+check
        return verify
    def uart_send(self,data):
        self.u1.read()  #清空串口
        time.sleep_ms(10) #延时
        self.u1.write(data) #唤醒模块
        time.sleep_ms(80)
    def awaken(self):
        while 1:
            data=b'\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x03\xfd\xd4\x14\x01\x17\x00' #唤醒模块
            self.uart_send(data)
            if self.u1.any()>0:
                data1=self.u1.read(15) #读15个数

                if data1==b'\x00\x00\xff\x00\xff\x00\x00\x00\xff\x02\xfe\xd5\x15\x16\x00': #验证数据，正确就跳出
                    print('huanxing  ok',data1)
                    return 'ok'
    def find_card(self,piect):# 寻卡和验证，参数为正整数表示寻找第几块
        
        while 1:
            if self.u1.any()==0: # 确保串口空闲时发送
                data=b'\x00\x00\xff\x04\xfc\xd4\x4a\x02\x00\xe0\x00'  #寻卡指令
                self.uart_send(data)
                if self.u1.any()>0:
                    data=self.u1.read()
                    if len(data) >12: #甄别出有效数据一般应该大于12位
                        uid = data[-6:-2]  #取出获取到的UID
                        verify=b'\x00\x00\xff\x0f\xf1\xd4\x40\x01\x60%c\xff\xff\xff\xff\xff\xff'%piect+uid #把UID拼接到固定命令后
                        verify=self.checks(verify) #验证尾部校验合的函数
                        self.uart_send(verify)
                        date_verify=self.u1.read()
                        if date_verify[-4:-2]==b'\x41\x00':
                            return 'verify_ok'                          
                    time.sleep(0.2)
            else:
                self.u1.read()
    def read(self,piect):
        self.find_card(piect)
        self.u1.read()
        time.sleep_ms(20)
        if self.u1.any()==0:
            
            senddata=b'\x00\x00\xff\x05\xfb\xd4\x40\x01\x30%c'%piect
            senddata=self.checks(senddata)
            self.uart_send(senddata)
            if u1.any()>20:
                rec_data=self.u1.read()
                print(rec_data)
                if rec_data[12:14]==b'\x41\x00': #查看返回是否是正确码
                    return rec_data[-18:-2]
                else:
                    return ''
            else:
                self.u1.read()
                time.sleep_ms(80)
        else:
            self.u1.read()
    def write(self,piect,b_datas):#俩参数前边是块号，后面是16位二进制数格式为b'\x01\x02'这种共16个
        self.find_card(piect)
        self.u1.read()
        time.sleep_ms(20)
        if self.u1.any()==0:
            senddata=b'\x00\x00\xff\x15\xeb\xd4\x40\x01\xa0%c'%piect+b_datas #写入前面是写入命令里边拼接块号，后面再拼入数据 
            senddata=self.checks(senddata)
            self.uart_send(senddata)
            if u1.any()>12:
                rec_data=self.u1.read()
                if rec_data[-4:-2]==b'\x41\x00':
                    print('write ok==> ',rec_data)
                else:
                    print('write err')
            else:
                self.u1.read()
                time.sleep_ms(80)
        else:
            self.u1.read()

if __name__=='__main__':
    u1=UART(2,115200,rx=machine.Pin(16),tx=machine.Pin(17))
    a=Pn532(u1) #实例化，同时会执行唤醒模块操作
    read_data=a.read(5)  #读块命令，参数为块号,读取成功有返回值，返回为16位块数据，失败返回空
#   验证和读写进行了组合，读写命令都是阻塞等待模式，方便读写卡，可以先执行命令等一会再放卡
    data = b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x10\x01\x02\x03\x05\x01' #待写入数据共16位
#   a.write(5,data) #写块命令，前面参数是块号后面是写入的数据,无返回值，成功打印wirte ok ==> b'\x00\x....'


