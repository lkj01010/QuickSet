#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import time
import subprocess

kInterval = 2

kUnityPath = "/Applications/Unity/Unity.app/Contents/MacOS/Unity"


# 监视srcdir，如果有文件更新，就copy到destdir
def watch(srcdir, destdir):
    print 'start watch \nsrc  ---> ' + srcdir + '\ndest ---> ' + destdir
    while True:
        if os.path.isdir(srcdir):
            for filename in os.listdir(srcdir):

                filepath = os.path.join(srcdir, filename)
                if os.path.isfile(filepath):
                    # cmds.file(final_filename, force=True, save=True, options='v=1;p=17', type='mayaBinary')

                    modify_time = os.path.getmtime(filepath)
                    now = time.time()

                    passtime = now - modify_time

                    # print filename + ' pass ' + str(passtime)
                    if passtime < kInterval + 1:
                        shutil.copy(filepath, os.path.join(destdir, filename))
                        print 'copy ------> ' + filename + ' ---- passtime ' + str(passtime)

                        # dont do, 会多开
                        # subprocess.Popen([kUnityPath], shell=True)

        time.sleep(kInterval)


UNITY_FX = "/Users/Midstream/Documents/Cur/Moba2D/Assets/Textures/Fx"
WS_FX_SPRITE = "/Users/Midstream/Documents/Cur/Ws-Effect/O_Sprite"
WS_FX_AN = "/Users/Midstream/Documents/Cur/Ws-Effect/O_An"

if __name__ == "__main__":
    # watch(sys.argv[1], sys.argv[2])
    watch(WS_FX_SPRITE, UNITY_FX)
