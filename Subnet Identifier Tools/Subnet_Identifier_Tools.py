####The Mythical Gryphon / ConSilverstone####
####Initilise Variables####
from pickle import APPEND #adding content on the end of lists/strings
from re import A

classful_range = {"A": 126, "B": 191, "C": 223, "D": 239, "E": 255} #A dictonary containg the last usable address from the first octect to find the class type
ipv4_list = [] #The user will change this by entering a ipv4 address they are trying to find information on
mask_list = [] #The user will change this by entering a subnet mash they are trying to find informtaion on
class_type = "" #A blank string that will be used to display the class of network, used in conjunction with classful_range
binary_scale = [128, 64, 32, 16, 8, 4, 2, 1] #our binary scale which we will use to convert to and from binary and base 10
##Calculated variables in functions##
cidr_mask = 0
broadcast_address = []
network_address = []
first_address = []
last_address = []
total_hosts = 0

##Lets take input for the users IPv4 Address##
def ip_input (ipv4_list):
    ipv4_string = input()
    
    #Error Handling#
    if len(ipv4_string) > 16 or len(ipv4_string) < 8:
        print("Sorry but that was not a valid IPv4 address, a valid address should be between 8 and 16 characters in length (0.0.0.1 or 255.255.255.255) for example.")
        ip_input(ipv4_list)
    elif ipv4_string.count(".") != 3:
        print("Sorry but that was not a valid IPv4 address, a valid address should have 4 full stops, one after every octet (192.168.1.0 or 127.16.0.0) for example")
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
        print("Sorry but that was not a valid IPv4 mask, a valid mask should have 4 full stops, one after every 4 numbers (255.0.0.0 or 255.255.255.0) for example")
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
    print(type(local_int))
    print(local_int)
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
   
   for i in mask_list:
       for i in binary_scale:
           if mask_list[i] - binary_scale[i] > 0:
               local_string_cidr.append("1")
           elif mask_list[i] - binary_scale[i] < 0:
               local_string_cidr.append("0")
           else: #A exception has happened and we need to notify of this.
               print("There was a fault when trying to calculate the cidr notation and it may not display correctly.")
   
    #Now take that local string and count for the cidr
   cidr_mask = local_string_cidr.count("1")
   
   return cidr_mask


def subnet_addresses_math (broadcast_address, network_address, first_address, last_address):
    
    #Lets create a local string to store the ipv4 info that our user has put in to keep that users input.
    local_string_ip = ""
    
    #Now we need to cycle through the users base 10 input to create a binary string that we can subnet with.
    for i in binary_scale:
        if ipv4_list[i] - binary_scale[i] > 0:
            local_string_ip.append("1")
        elif ipv4_list[i] - binary_scale[i] < 0:
            local_string_ip.append("0")
        else: #A exception has happened and we need to notify of this.
            print("There was a fault when trying to calculate the subnet address and it may not display correctly.")
    
    local_broadcast_string = local_string_ip
    local_network_string = local_string_ip
    
    for i in local_broadcast_string[cidr_mask - 1 : 32]:
        local_broadcast_string[i] = "1"
        
    for i in local_network_string[cidr_mask -1 : 32]:
        local_network_string[i] = "0"
        
    #Now we need to take our cleaned local_x_strings and turn those binary values back into base 10
    #First the broadcast address    
    for i in local_broadcast_string [0 : 7]:
        if i == "1":
            broadcast_address[0] = broadcast_address[0] + binary_scale[i]
    for i in local_broadcast_string [8 : 15]:
        if i == "1":
            broadcast_address[1] = broadcast_address[1] + binary_scale[i]
    for i in local_broadcast_string [16 : 23]:
        if i == "1":
            broadcast_address[2] = broadcast_address[2] + binary_scale[i]
    for i in local_broadcast_string [24 : 31]:
        if i == "1":
            broadcast_address[3] = broadcast_address[3] + binary_scale[i]
    #Second the network address
    for i in local_network_string [0 : 7]:
        if i == "1":
            network_address[0] = network_address[0] + binary_scale[i]
    for i in local_network_string [8 : 15]:
        if i == "1":
            network_address[1] = network_address[1] + binary_scale[i]
    for i in local_network_string [16 : 23]:
        if i == "1":
            network_address[2] = network_address[2] + binary_scale[i]
    for i in local_network_string [24 : 31]:
        if i == "1":
            network_address[3] = network_address[3] + binary_scale[i]       
    
    #Now that the lists are correct let us add the correct values to the first and last address        
    first_address[0:2] == network_address[0:2]
    last_address[0:2] == network_address[0:2]
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
    local_int = 32 - cidr_mask
    local_base_two = 2 #as bits grow in powers of two (on, off)
    
    total_hosts = (local_base_two ** local_int) - 2 #-2 for network and broadcast addresses
    return total_hosts

##Call Functions##And notify the user of what function they are on##
##print next line here so it only prints once##
print("Thank you for using the Subnet Identifier Tool, please enter the IPv4 address you would like information on.")
ip_input(ipv4_list)
print("Now please enter the subnet mask for the same network as the IPv4 address.")
mask_input(mask_list)
ip_class(class_type)
cidr_math(cidr_mask)
subnet_addresses_math(broadcast_address, network_address, first_address, last_address)
total_hosts_math(total_hosts_math)

####Finally we can display everything we have been working on!####
print("Subnet Identification Information:")
print("IPv4 Address: " + ipv4_list[0] + "." + ipv4_list[1] + "." + ipv4_list[2] + "." + ipv4_list[3])
print("Mask: " + mask_list[0] + "." + mask_list[1] + "." + mask_list[2] + "." + mask_list[3])
print("Cidr Notation: /" + cidr_mask)
print("This IPv4 Network Address: " + network_address[0] + "." + network_address[1] + "." + network_address[2] + "." + network_address[3])
print("This IPv4 Broadcast Address: " + broadcast_address[0] + "." + broadcast_address[1] + "." + broadcast_address[2] + "." + broadcast_address[3])
print("Subnets first usable address: " + first_address[0] + "." + first_address[1] + "." + first_address[2] + "." + first_address[3])
print("Subnets last usable address: " + last_address[0] + "." + last_address[1] + "." + last_address[2] + "." + last_address[3])
print("Thank you for using the Subnet_Identifier_Tool, happy building!")