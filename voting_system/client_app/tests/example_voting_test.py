import time

from admin.test import run_setup as admin_run1


from voter1.test import run_final as run1
from voter2.test import run_final as run2
from voter3.test import run_final as run3
from voter4.test import run_final as run4
from example_voting_steps import get_final_voting_result

sc_address = admin_run1()
time.sleep(1)

run1(
    sc_address,
    "0x123",
    "0x4759d339ba129b0922f008577d3029dcd00aa9da40fa8d2f748ddd36ed71261",
    "0x6677fe62ee39c7b07401f754138502bab7fac99d2d3c5d37df7d1c6fab10819",
)
run2(
    sc_address,
    "0x234",
    "0x43efbb1923d35f4fff94f5a8236b811199b4d48eca1ffe7f0e6d4870733c5c0",
    "0x5b6b8189bb580f0df1e6d6bec509ff0d6c9be7365d10627e0cf222ec1b47a71",
)
run3(
    sc_address,
    "0x345",
    "0x485446a579888a25821e2cc8cb935121b58cc5f258d4b80c194fdb7dd82800",
    "0x4e0b838810cb1a355beb7b3d894ca0e98ee524309c3f8b7cccb15a48e6270e2",
)
run4(
    sc_address,
    "0x456",
    "0x54b9cf9cb757b344313db9554533d5a74ef0283d359741f03fcddc29e3764b8",
    "0x42b249d1633812d903f303d640a4261f58fead5aa24925a9efc1dd9d76fb555",
)

time.sleep(1)
final_results = get_final_voting_result(sc_address)

print("Expected result: [0x1, 0x3, 0x19, 0x4b]")

print(f"Actual results: {final_results}")

# if final_results.split(": ")[1] == "[0x1, 0x3, 0x19, 0x4b]":
#     print("Test passed")
# else:
#     print("Test failed")
