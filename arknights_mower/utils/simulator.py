from os import system
import subprocess
from enum import Enum
from arknights_mower.utils.log import logger
import time
from arknights_mower.utils import config

class Simulator_Type(Enum):
    Nox = "夜神"
    MuMu12 = "MuMu12"
    Leidian9 = "雷电9"
    Waydroid = "Waydroid"


def restart_simulator(data, stop=True, start=True):
    index = data["index"]
    simulator_type = data["name"]
    cmd = ""

    if simulator_type in [
        Simulator_Type.Nox.value,
        Simulator_Type.MuMu12.value,
        Simulator_Type.Leidian9.value,
        Simulator_Type.Waydroid.value,
    ]:
        if simulator_type == Simulator_Type.Nox.value:
            cmd = "Nox.exe"
            if index >= 0:
                cmd += f' -clone:Nox_{data["index"]}'
            cmd += " -quit"
        elif simulator_type == Simulator_Type.MuMu12.value:
            cmd = "MuMuManager.exe api -v "
            if index >= 0:
                cmd += f'{data["index"]} '
            cmd += "shutdown_player"
        elif simulator_type == Simulator_Type.Waydroid.value:
            cmd = "waydroid session stop"
        elif simulator_type == Simulator_Type.Leidian9.value:
            cmd = "ldconsole.exe quit --index "
            if index >= 0:
                cmd += f'{data["index"]} '
            else:
                cmd += '0'
        if stop:
            exec_cmd(cmd, data["simulator_folder"])
            if data["name"] == 'MuMu12' and config.fix_mumu12_adb_disconnect:
                system('taskkill /f /t /im adb.exe')
            logger.info(f"关闭{simulator_type}模拟器")
            time.sleep(2)
        if simulator_type == Simulator_Type.Nox.value:
            cmd = cmd.replace(" -quit", "")
        elif simulator_type == Simulator_Type.MuMu12.value:
            cmd = cmd.replace(" shutdown_player", " launch_player")
        elif simulator_type == Simulator_Type.Waydroid.value:
            cmd = "waydroid show-full-ui"
        elif simulator_type == Simulator_Type.Leidian9.value:
            cmd = cmd.replace("quit", "launch")
        if start:
            exec_cmd(cmd, data["simulator_folder"])
            logger.info(f"开始启动{simulator_type}模拟器，等待25秒钟")
            time.sleep(25)
    else:
        logger.warning(f"尚未支持{simulator_type}重启/自动启动")


def exec_cmd(cmd, folder_path):
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=folder_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
