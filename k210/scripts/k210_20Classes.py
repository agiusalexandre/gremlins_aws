import sensor,image,lcd,time
import KPU as kpu
################## oro
from Maix import GPIO
from fpioa_manager import fm
from machine import UART
################## oro
lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load(0x500000)
#task = kpu.load(“/sd/model/20class.kmodel”)
#task = kpu.load(0x300000)
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
########################## oro
#Unit V GPIO_UART
#fm.register(35, fm.fpioa.UART2_TX, force=True)
#fm.register(34, fm.fpioa.UART2_RX, force=True)
#uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
#UnitV ButtonA
fm.register(19, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
fm.register(18, fm.fpioa.GPIO2)
but_b=GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)
##########################
while(True):
    clock.tick()
    img = sensor.snapshot()
    a = lcd.display(img)
    ##print(clock.fps())
    if but_b.value() == 0:
        print("b pushed")
    if but_a.value() == 0:
        print("a pushed")
        code = kpu.run_yolo2(task, img)
        print(clock.fps())
        if code:
            for i in code:
                a=img.draw_rectangle(i.rect())
                a = lcd.display(img)
                print(code)
                for i in code:
                    ##lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
                    ##lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
                    ##lcd.draw_string(50, 50, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
                    print(classes[i.classid()])
        else:
            a = lcd.display(img)
a = kpu.deinit(task)