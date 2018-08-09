#!/usr/bin/env python3
import sys
import subprocess
import asyncio
from asyncio.subprocess import PIPE, STDOUT

@asyncio.coroutine
def fetch_data_points(metric, shell_command):
    p = yield from asyncio.create_subprocess_shell(shell_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    return (metric, (yield from p.communicate())[0].splitlines())

if __name__ == '__main__':
    path = sys.argv[1]
    metric_paths = subprocess.check_output('find {} -type f'.format(path), shell=True).split()
    metric_paths = [path.decode("utf-8") for path in metric_paths]
    loop = asyncio.get_event_loop()
    coros = [fetch_data_points(metric, 'whisper-fetch.py --from=$(date +%s -d "-2 min") {}'.format(metric)) for metric in metric_paths]

    try:
        output = loop.run_until_complete(asyncio.gather(*coros))
    finally:
        loop.close()

    for i in output:
        print("{},{},{}".format(i[0],i[1][0].decode("utf-8").split()[1],i[1][1].decode("utf-8").split()[1]))
