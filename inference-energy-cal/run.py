import subprocess


def print_sata_sim_banner():
    banner = r"""
   _____      _______                   _____ _____ __  __ 
  / ____|  /\|__   __|/\               / ____|_   _|  \/  |
 | (___   /  \  | |  /  \     ______  | (___   | | | \  / |
  \___ \ / /\ \ | | / /\ \   |______|  \___ \  | | | |\/| |
  ____) / ____ \| |/ ____ \            ____) |_| |_| |  | |
 |_____/_/    \_\_/_/    \_\          |_____/|_____|_|  |_|
                                                                                                               
    """
    print(banner)

if __name__ == "__main__":


    print_sata_sim_banner()
    subprocess.run('python3 comp-utils.py', shell=True)
    subprocess.run('python3 mem-utils.py', shell=True)
    subprocess.run('python3 cycle-utils.py', shell=True)
    subprocess.run('python3 energy-cal.py', shell=True)
