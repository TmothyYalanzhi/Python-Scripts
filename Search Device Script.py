from netmiko import ConnectHandler
import getpass

#Script created by Timothy Yalanzhi

def get_devices():
    devices = []
    print("Enter Cisco devices. Type 'no' when you're done.")
    while True:
        ip_address = input("Enter device: ")
        if ip_address.lower() == "no":
            break
        devices.append(ip_address)
    return devices

def get_show_commands():
    show_commands = []
    print("Enter show commands to execute. Type 'no' when you're done.")
    while True:
        command = input("Enter a show command: ")
        if command.lower() == "no":
            break
        show_commands.append(command)
    return show_commands

def connect_and_show(ip_address, username, password, commands):
    try:
        # Define device parameters
        device = {
            "device_type": "cisco_ios",
            "host": ip_address,
            "username": username,
            "password": password,
        }
        
        # Connect to the device
        with ConnectHandler(**device) as ssh:
            print(f"Connected to {ip_address}")
            
            # Execute show commands
            outputs = {}
            for command in commands:
                outputs[command] = ssh.send_command(command)
                
            return outputs
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    devices = get_devices()
    show_commands = get_show_commands()
    
 
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    # Connect to each device and execute show commands
    for device_ip in devices:
        print(f"\nConnecting to {device_ip}...")
        outputs = connect_and_show(device_ip, username, password, show_commands)
        
        # print(f"\n--- Output from {device_ip} ---")
        # for command, output in outputs.items():
        #     print(f"\nCommand: {command}")
        #     print(f"Output:\n{output}\n")
        
        print(f"\n--- Output from {device_ip} ---")
        with open ("CDP_report.csv", "a") as CDPreport:
            for command, output in outputs.items():
                print(f"\nCommand: {command}")
                CDPreport.write(f"{command}\n")
                print(f"Output:\n{output}\n")
                CDPreport.write(f"{output}\n")
