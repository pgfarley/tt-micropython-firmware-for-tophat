'''
Created on Nov 8, 2025

@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com


    low-level machine related methods.
    @note: Register magic is based on "3.1.11. List of registers" 
    from the rp2350-datasheet.pdf
    
    Have some read_ and write_ for in/bidir/out ports
    NOTE: [mappings] that these rely on GPIO pin mappings specific
    to the demoboard layout
    
    The read_ will only return bits for GPIO that are set 
    as INPUTs
    The write_ will write values to all GPIO but these will only
    impact GPIO that are setup as OUTPUTs.  For input gpio, this 
    value will be remembered and apply should the pin be turned
    into an output.
    
    
    The machine native stuff below uses 
    direct access to mem32 to go fastfastfast
    but this is pretty opaque.  For ref, here are 
    relevant registers from 2.3.1.7. List of Registers
        0x004 GPIO_IN Input value for GPIO pins 0..31
        0x008 GPIO_IN HI Input value for GPIO pins 32..47
        
        0x010 GPIO_OUT GPIO output value 0..31
        0x014 GPIO_OUT HI GPIO output value 32..47
        
        0x018 GPIO_OUT_SET GPIO output value set 0..31
        0x01C GPIO_OUT_SET HI GPIO output value set 32..47
        
        
        0x020 GPIO_OUT_CLR 0..31
        0x024 GPIO_OUT_CLR HI 32..47
        
        
        0x028 GPIO_OUT_XOR 0..32
        0x02C GPIO_OUT_XOR HI 32..47
        
        0x030 GPIO_OE GPIO output enable
        0x034 GPIO_OE HI
        
        0x038 GPIO_OE_SET
        0x03C GPIO_OE_SET HI
        
        
        0x040 GPIO_OE_CLR GPIO output enable clear
        0x044 GPIO_OE_CLR HI
        
        0x048 GPIO_OE_XOR GPIO output enable XOR
        0x04C GPIO_OE_XOR HI
    
    
'''
import rp2
import machine 

@micropython.native
def write_ui_in_byte(val):
    # move the value bits to GPIO spots
    # inputs start on GPIO12
    val = val << 12
    # xor with current GPIO values, and mask to keep only input bits
    # 0x1E1E00 == 0b111100001111000000000 so GPIO 9-12 and 17-20
    val = (machine.mem32[0xd0000010] ^ val) & (0xff << 12)
    # val is now be all the input bits that have CHANGED:
    # writing to GPIO_OUT_XOR will flip any GPIO where a 1 is found
    machine.mem32[0xd0000028] = val
    
@micropython.native
def read_ui_in_byte():
    return ( (machine.mem32[0xd0000004] & (0xff << 12)) >> 12)


@micropython.native
def write_uio_byte(val):
    # dump_portset('uio', val)
    # low level machine stuff
    # move the value bits to GPIO spots
    # for bidir, all uio bits are in a line starting 
    # at GPIO 21
    val = (val << 22)
    val = (machine.mem32[0xd0000010] ^ val) & (0xff << 22)
    # val is now be all the bits that have CHANGED:
    # writing to 0xd000001c will flip any GPIO where a 1 is found,
    # only applies immediately to pins set as output 
    machine.mem32[0xd0000028] = val
    
    
@micropython.native
def read_uio_byte():
    return (machine.mem32[0xd0000004] & (0xff << 22)) >> 22

@micropython.native
def read_uio_outputenable():
    # GPIO_OE register, masked for our bidir pins
    return (machine.mem32[0xd0000030] & (0xff << 22)) >> 22
    
    
@micropython.native
def write_uio_outputenable(val):
    # dump_portset('uio_oe', val)
    # GPIO_OE register, clearing bidir pins and setting any enabled
    val = (val << 22)
    machine.mem32[0xd0000030] = (machine.mem32[0xd0000030] & ((1 << 22) - 1)) | val
    
@micropython.native
def write_uo_out_byte(val):
    # dump_portset('uo_out', val)
    # low level machine stuff
    # move the value bits to GPIO spots
    
    valL = (val & 0x3) << 30
    valH = (val & 0xfc) >> 2
    
    valL = (machine.mem32[0xd0000010] ^ valL) & (0x3 << 30)
    
    valH = (machine.mem32[0xd0000014] ^ valH)
    # val is now be all the bits that have CHANGED:
    # flip any GPIO where a 1 is found,
    # only applies immediately to pins set as output 
    machine.mem32[0xd0000028] = valL
    machine.mem32[0xd000002C] = valH

@micropython.native
def read_uo_out_byte():
    return ((machine.mem32[0xd0000004] & (0x3 << 30)) >> 30) | (
            (machine.mem32[0xd0000008] & 0x3F) << 2)

@micropython.native
def read_clock():
    # clock is on GPIO21
    return ((machine.mem32[0xd0000010] & (1 << 21)) >> 21)
   
@micropython.native
def write_clock(val):
    # not a huge optimization, as this is a single bit, 
    # but 5% or so counts when using the microcotb tests
    if val:
        machine.mem32[0xd0000038] = (1 << 21) 
    else:
        machine.mem32[0xd0000040] = (1 << 21)
    
