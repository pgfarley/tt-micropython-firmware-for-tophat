'''
Created on Nov 8, 2025

@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com
'''
from ttboard.pins.gpio_map import GPIOMapBase

class GPIOMapTTDBv3(GPIOMapBase):
    RP_PROJCLK = 21
    PROJECT_nRST = 20
    CTRL_SEL_nRST = 1
    CTRL_SEL_INC = 2
    CTRL_SEL_ENA = 0
    UO_OUT0 = 30
    UO_OUT1 = 31
    UO_OUT2 = 32
    UO_OUT3 = 33
    UO_OUT4 = 34
    UO_OUT5 = 35
    UO_OUT6 = 36 
    UO_OUT7 = 37
    UI_IN0 = 12
    UI_IN1 = 13
    UI_IN2 = 14
    UI_IN3 = 15
    UI_IN4  = 16
    UI_IN5  = 17
    UI_IN6  = 18
    UI_IN7  = 19
    UIO0 = 22
    UIO1 = 23
    UIO2 = 24
    UIO3 = 25
    UIO4 = 26
    UIO5 = 27
    UIO6 = 28
    UIO7 = 29
    RP_LED = 11

    # Enable a workaround for a PCB error in TT07 carrier board, which swapped the ctrl_sel_inc and ctrl_sel_nrst lines:
    tt07_cb_fix = False
    
    @classmethod 
    def project_clock(cls):
        return cls.RP_PROJCLK
    
    @classmethod 
    def project_reset(cls):
        return cls.PROJECT_nRST
    
    
    @classmethod 
    def ctrl_increment(cls):
        return cls.CTRL_SEL_INC
    
    @classmethod 
    def ctrl_enable(cls):
        return cls.CTRL_SEL_ENA
    
    @classmethod 
    def ctrl_reset(cls):
        return cls.CTRL_SEL_nRST
    
    @classmethod 
    def always_outputs(cls):
        return [
            'cinc',
            'cena',
            'ncrst'
        ]
    @classmethod 
    def all(cls):
        retDict = cls.all_common()

        retDict.update({
            'nprojectrst': cls.PROJECT_nRST,
            'cinc': cls.CTRL_SEL_INC,
            'cena': cls.CTRL_SEL_ENA,
            'ncrst': cls.CTRL_SEL_nRST,
            'uo_out0': cls.UO_OUT0,
            'uo_out1': cls.UO_OUT1,
            'uo_out2': cls.UO_OUT2,
            'uo_out3': cls.UO_OUT3
        })

        return retDict
