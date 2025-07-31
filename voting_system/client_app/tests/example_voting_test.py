import time

from admin.test import run_setup as admin_run1
from admin.test import run_final as admin_run2

from voter1.test import run_setup as run1
from voter2.test import run_setup as run2
from voter3.test import run_setup as run3
from voter4.test import run_setup as run4

from voter1.test import run_final as run5
from voter2.test import run_final as run6
from voter3.test import run_final as run7
from voter4.test import run_final as run8
from example_voting_steps import get_final_voting_result

sc_address = admin_run1()
time.sleep(1)
run1(sc_address)
run2(sc_address)
run3(sc_address)
run4(sc_address)
time.sleep(1)

admin_run2(sc_address)
time.sleep(1)
run5(sc_address)
run6(sc_address)
run7(sc_address)
run8(sc_address)

time.sleep(1)
print(get_final_voting_result(sc_address))
print("Expected result: [0x1, 0x3, 0x19, 0x4b]")