####Initilise Variables####
from pickle import APPEND #adding content on the end of lists/strings
from re import A

classful_range = {"A" : 126, "B" : 191, "C" : 223, "D" : 239, "E" : 255} #A library containg the last usable address from the first octect to find the class type
ipv4_list = () #The user will change this by entering a ipv4 address they are trying to find information on
mask_list = () #The user will change this by entering a subnet mash they are trying to find informtaion on
class_type = "" #A blank string that will be used to display the class of network, used in conjunction with classful_range
binary_scale = (128, 64, 32, 16, 8, 4, 2, 1) #our binary scale which we will use to convert to and from binary and base 10
##Calculated variables in functions##
cidr_mask = 0
broadcast_address = ()
network_address = ()
first_address = ()
last_address = ()
total_hosts = 0

def ip_input (ipv4_list):
    ipv4_string = input("Thank you for using the Subnet Identifier Tool, please enter the IPv4 address you would like information on.")
    
    #Error Handling#
    if ipv4_string.len() > 16 or ipv4_string.len() < 8:
        print("Sorry but that was not a valid IPv4 address, a valid address should be between 8 and 16 characters in length (0.0.0.1 or 255.255.255.255) for example.")
        ip_input()
    elif ipv4_string.count(".") != 4:
        print("Sorry but that was not a valid IPv4 address, a valid address should have 4 full stops, one after every 4 numbers (192.168.1.0 or 127.16.0.0) for example")
        ip_input()
    else: #everything seems fine lets split the string into a list we can work with
        ipv4_string.split(".")
        for i in ipv4_string:
            ipv4_list.append(i)
    return ipv4_list

def mask_input (mask_list):

    mask_string = input("Now please enter the subnet mask for the same network as the IPv4 address.")
    
    #Error Handling#
    if mask_string.len() > 16 or mask_string.len() < 8:
        print("Sorry but that was not a valid IPv4 mask, a valid mask should be between 8 and 16 characters in length (0.0.0.1 or 255.255.255.255) for example.")
        mask_input()
    elif mask_string.count(".") != 4:
        print("Sorry but that was not a valid IPv4 mask, a valid mask should have 4 full stops, one after every 4 numbers (255.0.0.0 or 255.255.255.0) for example")
        mask_input()
    else: #everything seems fine lets split the string into a list we can work with
        mask_string.split(".")
        for i in mask_string:
            mask_list.append(i)
    return mask_list

#####Calculations####

def ip_class (class_type):
    
    #Lets create a local int containing the first octect of the user's ipv4 address so we can compare it to a class type
    local_int = ipv4_list[0]
    
    #Now to compare
    if local_int < classful_range.value("A"):
        class_type = "A"
        
    elif local_int > classful_range.value("A") and local_int < classful_range.value("B") and local_int != 127:
        class_type = "B"
        
    elif local_int > classful_range.value("C") and local_int < classful_range.value("D"):
        class_type = "C"
        
    elif local_int > classful_range.value("D") and local_int < classful_range.value("E") and local_int != 127:
        class_type = "This is a multicast address with class D, it is ill advised to use this for general subnetting."
        
    elif local_int > classful_range.value("E") and local_int < 255:
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
    for i in local_broadcast_string [0 : 7]:
        if i == "1":
            broadcast_address[0] = broadcast_address[0] + binary_scale[i]
        