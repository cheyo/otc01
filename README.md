# otc01
blacklist.Extend([device_2, device_3], reason='Reason for blacklisting')
```


## Where it is used.

The blacklist file path is passed directly to the following scripts in chromium:

  - [test\_runner.py](https://cs.chromium.org/chromium/src/build/android/test_runner.py)
  - [provision\_devices.py](https://cs.chromium.org/chromium/src/build/android/provision_devices.py)
  - [bb\_device\_status\_check.py](https://cs.chromium.org/chromium/src/build/android/buildbot/bb_device_status_check.py)

The blacklist is also used in the following scripts:

  - [device\_status.py](https://cs.chromium.org/chromium/src/third_party/catapult/devil/devil/android/tools/device_status.py)
  - [device\_recovery.py](https://cs.chromium.org/chromium/src/third_party/catapult/devil/devil/android/tools/device_recovery.py)

