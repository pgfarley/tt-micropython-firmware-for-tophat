
RP2040SystemClockDefaultHz = 125000000

import microcotb.platform
IsRP2040 = microcotb.platform.IsRP2040

if IsRP2040:
    # TODO:FIXME hardcoded rp2350
    from .rp2 import *
    from .rp2350 import *
else:
    from .desktop import *
    