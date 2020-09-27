import aios
import time
import threading
import numpy as np
import json

# Server_IP_list = ['192.168.1.112','192.168.1.164','192.168.1.190']
Server_IP_list = []
# Server_IP_list = ['192.168.1.169','192.168.1.125','192.168.1.141']
# Server_IP_list = ['192.168.8.156','192.168.8.157','192.168.8.163']
# Server_IP_list = ['192.168.1.102','192.168.1.104']
# Server_IP_list = ['192.168.1.120']
# Server_IP_list = ['39.97.214.191']
# Server_IP_list = ['123.57.14.125']
# Server_IP_list = ['192.168.1.190']

pos_list_1 = [1000, 2000, 3000, 5000, 2000, 6000, 10000, 0, 5000, -10000, 15000, 20000, 0]
delay_list_1 = [0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 1, 1, 1, 2, 2, 2, 2]

pos_list_2 = [1000, 2000, 3000, 4000, 0]
delay_list_2 = [0, 0, 0, 0, 1]


def main():

    Server_IP_list = aios.broadcast_func()
    if Server_IP_list:


        # for i in range(1000):
        #     start = time.time()
        #     for j in range(len(Server_IP_list)):
        #         aios.dum_func(Server_IP_list[j])
        #     for j in range(len(Server_IP_list)):
        #         aios.receive_func()
        #     print((time.time() - start)*1000)
        #     time.sleep(0.005)
        for i in range(5):
            for i in range(len(Server_IP_list)):
                cvp = aios.getCVP(Server_IP_list[i], 1)
                print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))

            time.sleep(0.02)
        print('\n')

        cali_flag = False
        for i in range(len(Server_IP_list)):
            if (not aios.encoderIsReady(Server_IP_list[i], 1)):
                # aios.encoderOffsetCalibration(Server_IP_list[i], 1)
                aios.encoderIndexSearch(Server_IP_list[i], 1)
                cali_flag = True


        print('\n')

        if cali_flag:
            time.sleep(10)
        else:
            for i in range(len(Server_IP_list)):
                aios.AIOSGetRoot(Server_IP_list[i])

            print('\n')

            for i in range(len(Server_IP_list)):
                aios.getMotionCtrlConfig(Server_IP_list[0], 1)
            print('\n')
            # aios.setTrapTraj(320000, 320000, 200000, Server_IP_list[0], 0)
            # aios.getTrapTraj(Server_IP_list[0], 0)

            # for i in range(len(Server_IP_list)):
            #     cvp = aios.getCVP(Server_IP_list[i], 1)
            #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
            #     cvp = aios.getCVP(Server_IP_list[i], 0)
            #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
            #     print('\n')
            #
            # str = input("Press Enter：")
            #
            # for i in range(len(Server_IP_list)):
            #     aios.setLinearCount(0, Server_IP_list[i], 1)
            #     aios.setLinearCount(0, Server_IP_list[i], 0)
            # print('\n')
            #
            # for i in range(len(Server_IP_list)):
            #     cvp = aios.getCVP(Server_IP_list[i], 1)
            #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
            #     cvp = aios.getCVP(Server_IP_list[i], 0)
            #     print("Position = %.2f, Velocity = %.0f, Current = %.4f" %(cvp[0], cvp[1], cvp[2]))
            #     print('\n')

            enableSuccess = True

            for i in range(len(Server_IP_list)):
                enableSuccess = aios.AIOSEnable(Server_IP_list[i], 1)
            print('\n')

            if enableSuccess:

                # aios.controlMode(3, Server_IP_list[0], 1)

                for i in range(len(Server_IP_list)):
                    aios.trapezoidalMove(0, True, Server_IP_list[i], 1)
                time.sleep( 2 )


                for i in range(len(pos_list_1)):
                    start = time.time()
                    for j in range(len(Server_IP_list)):
                        aios.trapezoidalMove(pos_list_1[i], True, Server_IP_list[j], 1)
                    print((time.time() - start)*1000)
                    time.sleep( delay_list_1[i] )


                for i in range(len(pos_list_2)):
                    start = time.time()
                    for j in range(len(Server_IP_list)):
                        aios.trapezoidalMove(pos_list_2[i], True, Server_IP_list[j], 1)
                        time.sleep( 0.2 )
                    print((time.time() - start)*1000)
                    time.sleep( delay_list_2[i] )

                # pos = 0
                for i in range(800):
                    start = time.time()
                    pos = np.sin(i*0.04*np.pi)*2000
                    # pos = pos + 10
                    print(pos)
                    for j in range(len(Server_IP_list)):
                        # aios.setPosition(pos, 0, 0, True, Server_IP_list[j], 1)
                        aios.trapezoidalMove(pos, False, Server_IP_list[j], 1)
                    print(time.time() - start)
                    time.sleep(0.01)


                for i in range(len(Server_IP_list)):
                    aios.trapezoidalMove(2000, True, Server_IP_list[i], 1)
                time.sleep( 1 )



                for i in range(len(Server_IP_list)):
                    aios.AIOSDisable(Server_IP_list[i], 1)



if __name__ == '__main__':
    main()