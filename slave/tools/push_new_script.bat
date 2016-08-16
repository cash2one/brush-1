adb shell rm -r /sdcard/com.hipipal.qpyplus/scripts3/slave/*

adb push D:\py\brush\slave  /sdcard/com.hipipal.qpyplus/scripts3/slave/
adb push D:\py\brush\slave  /sdcard/com.hipipal.qpyplus/projects3/slave/

adb shell rm -r /sdcard/com.hipipal.qpyplus/scripts3/slave/*.pyc
adb shell rm -r /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/*.pyc

pause