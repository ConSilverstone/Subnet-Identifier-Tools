####The Mythical Gryphon / ConSilverstone####
####Initilise Variables####
from itertools import cycle #To help us cycle through lists of different lengths

classful_range = {"A": 126, "B": 191, "C": 223, "D": 239, "E": 255} #A dictonary containg the last usable address from the first octect to find the class type
ipv4_list = [] #The user will change this by entering a ipv4 address they are trying to find information on
mask_list = [] #The user will change this by entering a subnet mash they are trying to find informtaion on
class_type = "" #A blank string that will be used to display the class of network, used in conjunction with classful_range
binary_scale = [128, 64, 32, 16, 8, 4, 2, 1] #our binary scale which we will use to convert to and from binary and base 10
##Calculated variables in functions##
cidr_mask = 0
broadcast_address = [0,0,0,0]
network_address = [0,0,0,0]
first_address = [0,0,0,0]
last_address = [0,0,0,0]
total_hosts = 0

##Lets take input for the users IPv4 Address##
def ip_input (ipv4_list):
    ipv4_string = input()
    
    #Error Handling#
    if len(ipv4_string) > 16 or len(ipv4_string) < 8:
        print("Sorry but that was not a valid IPv4 address, a valid address should be between 8 and 16 characters in length (0.0.0.1 or 255.255.255.255) for example.")
        ip_input(ipv4_list)
    elif ipv4_string.count(".") != 3:
        print("Sorry but that was not a valid IPv4 address, a valid address should have 3 full stops, one after every octet (192.168.1.0 or 127.16.0.0) for example")
        ip_input(ipv4_list)
    else: #everything seems fine lets split the string into a list we can work with
        ipv4_string_cleaned = ipv4_string.split(".") ##Take the raw input and clean it up using the full stops
        for i in ipv4_string_cleaned:
            if i != ".": ##We want to discard the full stops for the list
                ipv4_list.append(int(i))
    return ipv4_list

##Lets take input for the users IPv4 Mask##
def mask_input (mask_list):

    mask_string = input()
    
    #Error Handling#
    if len(mask_string) > 16 or len(mask_string) < 8:
        print("Sorry but that was not a valid IPv4 mask, a valid mask should be between 8 and 16 characters in length (0.0.0.1 or 255.255.255.255) for example.")
        mask_input(mask_list)
    elif mask_string.count(".") != 3:
        print("Sorry but that was not a valid IPv4 mask, a valid mask should have 3 full stops, one after every 4 numbers (255.0.0.0 or 255.255.255.0) for example")
        mask_input(mask_list)
    else: #everything seems fine lets split the string into a list we can work with
        mask_string_cleaned = mask_string.split(".") ##Take the raw input and clean it up using the full stops
        for i in mask_string_cleaned:
            if i != ".": ##We want to discard the full stops for the list
                mask_list.append(int(i))
    return mask_list

#####Calculations####

def ip_class (class_type):
    
    #Lets create a local int containing the first octect of the user's ipv4 address so we can compare it to a class type
    local_int = ipv4_list[0]

    #Now to compare
    if local_int < classful_range.get("A", "No Class Given"):
        class_type = "A"
        
    elif local_int > classful_range.get("A", "No Class Given") and local_int < classful_range.get("B", "No Class Given") and local_int != 127:
        class_type = "B"
        
    elif local_int > classful_range.get("B", "No Class Given") and local_int < classful_range.get("C", "No Class Given"):
        class_type = "C"
        
    elif local_int > classful_range.get("C", "No Class Given") and local_int < classful_range.get("D", "No Class Given"):
        class_type = "This is a multicast address with class D, it is ill advised to use this for general subnetting."
        
    elif local_int > classful_range.get("D", "No Class Given") and local_int < classful_range.get("E", "No Class Given"):
        class_type = "This is a experemental address with class E, it is ill advised to use this for general subnetting."   
        
    elif local_int == 127:
        class_type = "This is the loopback address range for local address, however the class B 127.16.0.0 to 127.31.255.255 address range is still usable for local subnetting."   
    #If nothing above works then there is a fault with the user's input as it is likely out of range.
    else:
        print("There was a problem with presenting the IPv4 calculation, please ensure that the IPv4 address is within the ranges of 0 to 255 n each octect.")
        class_type = ""
    
    return class_type


def cidr_math (cidr_mask):
   #Local string for converting with
   local_string_cidr = ""
   
   #Now we need to cycle through the users base 10 input to create a binary string that we can show the cidr notation with.
   for i, elem in enumerate (mask_list):
       for j, elem in enumerate (binary_scale):          
           if mask_list[i] - binary_scale[j] > 0:
               local_string_cidr = local_string_cidr + "1"
           else:
               local_string_cidr = local_string_cidr + "0"          
    #Now take that local string and count for the cidr
   cidr_mask = local_string_cidr.count("1")
   
   return cidr_mask

######Everything above is working as intended######

def subnet_addresses_math (broadcast_address, network_address, first_address, last_address):

    #Lets create a local string to store the ipv4 info that our user has put in to keep that users input.
    local_string_ip = ""
    #Lets create a local ipv4_list that we can change the values in freely, need list() to copy the information not reference it
    local_ipv4_list = list(ipv4_list)
    
    #Now we need to cycle through the users base 10 input to create a binary string that we can subnet with.
    for i, elem in enumerate (local_ipv4_list):
        for j, elem in enumerate (binary_scale):
            
            if local_ipv4_list[i] - binary_scale[j] >= 0:
                local_string_ip = local_string_ip + "1"
                ##Now we need to update the value in local_ipv4_list
                local_ipv4_list[i] = local_ipv4_list[i] - binary_scale[j]
            elif local_ipv4_list[i] - binary_scale[j] < 0:
                local_string_ip = local_string_ip + "0"
                
            else: #A exception has happened and we need to notify of this.
                print("There was a fault when trying to calculate the subnet address and it may not display correctly.")
                
    #Lets make our local broadcast and network strings
    local_broadcast_string = local_string_ip[0: cidr_mask]
    local_network_string = local_string_ip[0: cidr_mask]
    remaining_bits = 32 - cidr_mask
    
    for i in range (0, remaining_bits):
        local_broadcast_string = local_broadcast_string + "1"
        local_network_string = local_network_string + "0"
    #Now we need to take our local_x_strings and turn them into lists of binary numbers to convert back into base 10
    broadcast_binary_list = []
    network_binary_list = []
    for x in local_broadcast_string:
        broadcast_binary_list.append(x)
    for x in local_network_string:
        network_binary_list.append(x)
    
    ##We need to set some things up, first we want to reset the binary scale after every 8 bits
    ##We need to start from 1 to make the binary scale work from 0 to 8 (i starts at 0)
    binary_scale_enumerator = 0
    start_from_1 = 1

    #First the broadcast address    
    for i, elem in enumerate (broadcast_binary_list):
        if start_from_1 <= 8:
            if broadcast_binary_list[i] == "1":
                broadcast_address[0] = broadcast_address[0] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 16 and start_from_1 > 8:
            if broadcast_binary_list[i] == "1":
                broadcast_address[1] = broadcast_address[1] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 24 and start_from_1 > 16:
            if broadcast_binary_list[i] == "1":
                broadcast_address[2] = broadcast_address[2] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 32 and start_from_1 > 24:
            if broadcast_binary_list[i] == "1":
                broadcast_address[3] = broadcast_address[3] + binary_scale[binary_scale_enumerator]
        if start_from_1 % 8 == 0:
           binary_scale_enumerator = -1
        binary_scale_enumerator = binary_scale_enumerator + 1
        start_from_1 = start_from_1 + 1
    
    #Reset the start_from_1 variable
    start_from_1 = 1
    #Second the network address
    for i, elem in enumerate (network_binary_list):
        if start_from_1 <= 8:
            if network_binary_list[i] == "1":
                network_address[0] = network_address[0] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 16 and start_from_1 > 8:
            if network_binary_list[i] == "1":
                network_address[1] = network_address[1] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 24 and start_from_1 > 16:
            if network_binary_list[i] == "1":
                network_address[2] = network_address[2] + binary_scale[binary_scale_enumerator]
        if start_from_1 <= 32 and start_from_1 > 24:
            if network_binary_list[i] == "1":
                network_address[3] = network_address[3] + binary_scale[binary_scale_enumerator]
        if start_from_1 % 8 == 0:
           binary_scale_enumerator = - 1
        binary_scale_enumerator = binary_scale_enumerator + 1
        start_from_1 = start_from_1 + 1

    #Now that the lists are correct let us add the correct values to the first and last address        
    first_address[0:3] = network_address[0:3]
    last_address[0:3] = broadcast_address[0:3]
    #The first three octets are gonna match the now accurate network and broadcast addresses, we just need to add or take away 1 respectively
    first_address[3] = network_address[3] + 1
    last_address[3] = broadcast_address[3] - 1
    
    return network_address
    return broadcast_address
    return first_address
    return last_address

#Last piece of math is to calculate the total usable addresses in this subnet
def total_hosts_math (total_hosts):
    
    #Lets create local ints to do the math with
    local_int = 32 - cidr_mask #Give us the power, bits on host side.
    local_base_two = 2 #as bits grow in powers of two (on, off)
    
    total_hosts = (local_base_two ** local_int) - 2 #-2 for network and broadcast addresses
    return total_hosts

##Call Functions##And notify the user of what function they are on##
##print next line here so it only prints once##
print("Thank you for using the Subnet Identifier Tool, please enter the IPv4 address you would like information on.")
ipv4_list = ip_input(ipv4_list)
print("Now please enter the subnet mask for the same network as the IPv4 address.")
mask_input = mask_input(mask_list)
class_type = ip_class(class_type) #Set the value outside the function to with =
cidr_mask = cidr_math(cidr_mask) #Set the value outside the function to with =
subnet_addresses_math(broadcast_address, network_address, first_address, last_address)
total_hosts = total_hosts_math(total_hosts)

####Finally we can display everything we have been working on!####
print() #Want an empty space#
print("Subnet Identification Information:")
print("IPv4 Address: " + str(ipv4_list[0]) + "." + str(ipv4_list[1]) + "." + str(ipv4_list[2]) + "." + str(ipv4_list[3]))
print("Mask: " + str(mask_list[0]) + "." + str(mask_list[1]) + "." + str(mask_list[2]) + "." + str(mask_list[3]))
print("Class Type: " + class_type)
print("Cidr Notation: /" + str(cidr_mask))
print("This IPv4 Network Address: " + str(network_address[0]) + "." + str(network_address[1]) + "." + str(network_address[2]) + "." + str(network_address[3]))
print("This IPv4 Broadcast Address: " + str(broadcast_address[0]) + "." + str(broadcast_address[1]) + "." + str(broadcast_address[2]) + "." + str(broadcast_address[3]))
print("Subnets first usable address: " + str(first_address[0]) + "." + str(first_address[1]) + "." + str(first_address[2]) + "." + str(first_address[3]))
print("Subnets last usable address: " + str(last_address[0]) + "." + str(last_address[1]) + "." + str(last_address[2]) + "." + str(last_address[3]))
print("Total hosts usable in subnet: " + str(total_hosts))
print()
print(input("Thank you for using the Subnet_Identifier_Tool, happy building!"))