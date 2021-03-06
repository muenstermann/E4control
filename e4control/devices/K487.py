# -*- coding: utf-8 -*-

from time import sleep

from .device import Device


class K487(Device):
    rampSpeed_step = 5
    rampSpeed_delay = 1  # s

    def __init__(self, connection_type, host, port):
        super(K487, self).__init__(connection_type=connection_type, host=host, port=port)

    def userCmd(self, cmd):
        print('user cmd: %s' % cmd)
        return self.ask(cmd)

    def initialize(self, iChannel=-1):
        self.write('G0O0C1X')
        # self.write('L4X')

    def setVoltage(self, fsetValVolts, iChannel=-1):
        self.write('V%.3f,1,1X' % fsetValVolts)

    def enableOutput(self, bEnable, iChannel=-1):
        if bEnable:
            self.write('O1X')
        else:
            self.write('O0X')

    def getVoltage(self, iChannel=-1):
        sV = self.ask('U8X')
        fV = float(sV[sV.find('=')+1:sV.find('E')])*10**float(sV[sV.find('E')+1:sV.find('E')+4])
        return fV

    def getCurrent(self, iChannel=-1):
        sI = self.ask('U6X')
        fI = float(sI[sI.find('=')+1:sI.find('E')])*10**float(sI[sI.find('E')+1:sI.find('E')+4])
        return fI

    def setRange(self, sRange, iChannel=-1):
        if (sRange == 'R0'):
            self.write('R0X')
            self.write('C2X')
        elif (sRange == 'R1'):
            self.write('R1X')
            self.write('C2X')
        elif (sRange == 'R2'):
            self.write('R2X')
            self.write('C2X')
        elif (sRange == 'R3'):
            self.write('R3X')
            self.write('C2X')
        elif (sRange == 'R4'):
            self.write('R4X')
            self.write('C2X')
        elif (sRange == 'R5'):
            self.write('R5X')
            self.write('C2X')
        elif (sRange == 'R6'):
            self.write('R6X')
            self.write('C2X')
        elif (sRange == 'R7'):
            self.write('R7X')
            self.write('C2X')
        else:
            print('No new range set!')

    def setTrigger(self, sTrigger, iChannel=-1):
        pass

    def setFilterMode(self, sFilter, iChannel=-1):
        if (sFilter == 'P0'):
            self.write('P0X')
        elif (sFilter == 'P1'):
            self.write('P1X')
        elif (sFilter == 'P2'):
            self.write('P2X')
        elif (sFilter == 'P3'):
            self.write('P3X')
        else:
            print('No new filter set!')

    def setRampSpeed(self, iRampSpeed, iDelay):
        if iRampSpeed < 1 or iRampSpeed > 255:
            print('Set RampSpeed size is out off range!')
        else:
            self.rampSpeed_step = iRampSpeed
        if iDelay < 0:
            print('No negativ Delay is possible!')
        else:
            self.rampSpeed_delay = iDelay

    def getRampSpeed(self):
        return([int(self.rampSpeed_step), int(self.rampSpeed_delay)])

    def rampVoltage(self, fVnew, iChannel=-1):
        V = self.getVoltage(iChannel)
        V = round(V, 4)
        if abs(fVnew-V) <= self.rampSpeed_step:
            self.setVoltage(fVnew, iChannel)
            print('Voltage reached: %.2f V' % fVnew)
            return
        else:
            self.setVoltage(V+self.rampSpeed_step*(fVnew-V)/abs(fVnew-V))
            print('Ramp Voltage: %.2f V' % (V+self.rampSpeed_step*(fVnew-V)/abs(fVnew-V)))
            sleep(self.rampSpeed_delay)
            self.rampVoltage(fVnew, iChannel)

    def reset(self):
        self.write('L0X')

    def output(self,  show=True):
        bPower = self.getEnableOutput()
        if show:
            print('K487:')
            if bPower == '1':
                print('Output \033[32m ON \033[0m')
            else:
                print('Output \033[31m OFF \033[0m')
        if bPower == '1':
            fVoltage = self.getVoltage()
            fCurrent = self.getCurrent() * 1E6
            if show:
                print('Voltage = %0.1f V' % fVoltage)
                print('Current = %0.3f uA' % fCurrent)
        else:
            if show:
                print('Voltage = ---- V')
                print('Current = ---- uA')
            fVoltage = 0
            fCurrent = 0
        return([['Output', 'U[V]', 'I[uA]'], [str(bPower), str(fVoltage), str(fCurrent)]])

    def interaction(self):
        print('1: enable Output')
        print('2: set Voltage')
        x = raw_input('Number? \n')
        while x != '1' and x != '2':
            x = raw_input('Possible Inputs: 1 or 2! \n')
        if x == '1':
            bO = raw_input('Please enter ON or OFF! \n')
            if bO == 'ON' or bO == 'on':
                self.enableOutput(True)
            else:
                self.rampVoltage(0)
                self.enableOutput(False)
        elif x == '2':
            fV = raw_input('Please enter new Voltage in V \n')
            self.rampVoltage(float(fV))
