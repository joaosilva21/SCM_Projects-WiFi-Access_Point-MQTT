
from connect_mqtt import MQTT
import signal, sys, time

manage = MQTT()
working = 0

def signal_handler(sig, frame):
    print("\nClosing app...")
    manage.shutdown() 
    sys.exit(0) 

def main():    
    parameters = ""

    print("\nBefore starting configure the default values:")
    print(" With human presence: ")
    parameters += input("  Min temperature: ") + ";"
    parameters += input("  Max temperature: ") + ";"

    print(" Without human presence: ")
    parameters += input("  Min temperature: ") + ";"
    parameters += input("  Max temperature: ") + ";"

    parameters += input(" Safe CO2: ") + ";"
    parameters += input(" Max CO2: ") + ";"
    parameters += input(" Light threshold: ")

    manage.set_parameters(parameters)
    print("\nValues configured!")

    manage.start()
    while(not manage.get_connect()):
        time.sleep(1)

    while(True):
        command = input("SCM@manage-application:~$ ")
        commands = command.split(" ")

        # condition [room name]
        if(commands[0] == "condition" and len(commands) == 2):
            manage.get_condition(commands[1])
        # config [room name] [1-7 -> limiar to change] [value]
        elif(commands[0] == "config" and len(commands) == 4):
            manage.publish_config(commands[1], commands[2], commands[3])
        # update [room name]
        elif(commands[0] == "update" and len(commands) == 2):
            manage.publish_update(commands[1])
        # light [room name] [on/off]
        elif(commands[0] == "light" and len(commands) == 3):
            manage.publish_light(commands[1], commands[2])
        # help
        elif(commands[0] == "help"):
            print("Commands:")
            print(" condition - see the condition of a specific room")
            print(" config - configure a specific room")
            print(" update - update a specific sensor")
            print(" lights - manage the light system")
            print(" help - to see every command\n")
        else:
            print("Invalid command '" + command + "'.\nType 'help' to see the list of commands.\n")
        
        time.sleep(1)

if __name__ == '__main__':    
    signal.signal(signal.SIGINT, signal_handler)
    main()
