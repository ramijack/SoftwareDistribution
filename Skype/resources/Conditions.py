import psutil
import subprocess
import re

Memory = 0
DiskSpace = 1
PERCENTAGE_REG_EX = '\d{1,3}%'


def minimum_ram_required(memory_required, unit):
    """
    This function verifies the Memory(Ram) condition required for downloading/installing the Application is met.
    :param memory_required: This parameter specifies the size of Ram required for installing the Application.
    :param unit: This parameter defines the unit of Memory(RAM) Size specified, which is in Kilobytes(KB) or Megabytes(MB) or Gigabytes(GB).
    :return: True/False based on condition criteria.
    """
    return space_required(memory_required, unit, Memory)


def minimum_free_disk_space(disk_size, unit):
    """
    This function verifies the Diskspace condition required for downloading/installing the Application is met.
    :param disk_size: This parameter specifies the size of Diskspace available for downloding/installing the Application.
    :param unit: This parameter defines the unit of Memory(RAM) Size specified, which is in Kilobytes(KB) or Megabytes(MB) or Gigabytes(GB).
    :return: True/False based on condition criteria.
    """
    return space_required(disk_size, unit, DiskSpace)


def space_required(min_val, unit, type):
    """
    This function verifies the Diskspace/Memory condition required for downloading/installing the Application is met.
    :param min_val: This parameter specifies the size of Diskspace/Memory available for downloding/installing the Application.
    :param unit: This parameter defines the unit of Memory(RAM) Size specified, which is in Kilobytes(KB) or Megabytes(MB) or Gigabytes(GB).
    :param type: This parameter defines type of condition to verify, DiskSpace or Memory(RAM).
    :return: True/False based on condition criteria.
    """
    unit_val = 1
    if unit == "KB":
        unit_val = 1024
    elif unit == "MB":
        unit_val = 1024 * 1024
    elif unit == "GB":
        unit_val = 1024 * 1024 * 1024

    if type == Memory:
        memory = psutil.virtual_memory().total
    elif type == DiskSpace:
        # primaryPartitionName = psutil.disk_partitions()[0].device
        memory = psutil.disk_usage('/').free

    return (memory / unit_val) >= min_val


def is_power_on_adapter():
    """
    This function verifies if the device is on AC Power.
    :return: Returns True if Device is on AC Power otherwise False.
    """
    power_info = subprocess.check_output(["pmset", "-g", "batt"])
    return "AC Power" in power_info


def is_power_on_battery():
    # powerInfo = subprocess.check_output('pmset -g batt')
    """
    This function verifies if the device is on Battery Power.
    :return: Returns True if Device is on Battery Power otherwise False.
    """
    power_info = subprocess.check_output(["pmset", "-g", "batt"])
    return "Battery Power" in power_info


def check_min_battery_required(minimum_percentage):
    """
    This function verfies if Remaining Battery percentages meets provided battery percentage.
    :param minimum_percentage: Minimum Battery charge required.
    :return: True/False based on condition criteria.
    """
    if is_power_on_adapter():
        return True

    power_info = subprocess.check_output(["pmset", "-g", "batt"])
    current_battery_percent = re.search(PERCENTAGE_REG_EX, power_info).group(0)
    current_battery_percent = int(current_battery_percent[:-1])
    return current_battery_percent >= minimum_percentage


def execute_script(script_file):
    """
    This function executes the condition specified in script file.
    :param script_file: File Name of the script file.
    :return: True/False if the script file executes successfully.
    """
    return_val = 0
    if script_file.endswith("py"):
        return_val = subprocess.check_output(["python", "./conditions/download/" + script_file])
    if script_file.endswith("sh"):
        return_val = subprocess.check_output(["sh", "./conditions/download/" + script_file])
    return return_val == 1


def execute_command(cmd_args):
    """
    This function executes the command specified in script file.
    :param cmd_args: List of Command arguments, e.g ["pmset", "-g", "batt"]
    """
    subprocess.check_output(cmd_args)


#print minimum_ram_required(16, "GB")
