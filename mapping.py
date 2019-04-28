
def main():
    print("----------------")
    print("1. CONTIGUOUS ALLOCATION")
    print("2. MODIFY CONTIGUOUS ALLOCATION(EXTENT-BASE)")
    print("3. LINKED ALLOCATION")
    print("4. INDEXED ALLOCATION")
    print("5. TWO-LEVEL INDEXED ALLOCATION")
    print("6. INODE")
    print("7. LINKED INDEXED")
    print("0. EXIT")
    print("----------------")

    mapping_type = input("Mapping Type: ")

    if mapping_type == "1":
        print("-->CONTIGUOUS ALLOCATION")
        logical_address = input("Logical Address: ")
        block_size      = input("Block Size: ")

        contiguous_allocation(convert_to_bytes(logical_address), convert_to_bytes(block_size))
        return True
    elif mapping_type == "2":
        print("-->MODIFY CONTIGUOUS ALLOCATION")
        extent_blocks   = input("Extent Blocks: ")
        logical_address = input("Logical Adress: ")
        block_size      = input("Block Size: ")
        
        modify_contiguous_allocation(int(extent_blocks), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    elif mapping_type == "3":
        print("-->LINKED ALLOCATION")
        pointer_size    = input("Pointer Size: ")
        logical_address = input("Logical Adress: ")
        block_size      = input("Block Size: ")

        linked_allocation(convert_to_bytes(pointer_size), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    elif mapping_type == "4":
        print("-->INDEXED ALLOCATION")
        pointer_size    = input("Pointer Size: ")
        logical_address = input("Logical Adress: ")
        block_size      = input("Block Size: ")

        indexed_allocation(convert_to_bytes(pointer_size), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    elif mapping_type == "5":
        print("-->TWO-LEVEL INDEXED ALLOCATION")
        pointer_size    = input("Pointer Size: ")
        logical_address = input("Logical Adress: ")
        block_size      = input("Block Size: ")

        twolevel_indexed_allocation(convert_to_bytes(pointer_size), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    elif mapping_type == "6":
        print("-->INDEX NODE")
        pointer_size    = input("Pointer Size: ")
        block_size      = input("Block Size: ")
        logical_address = input("Logical Address: ")

        inode(convert_to_bytes(pointer_size), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    elif mapping_type == "7":
        print("-->LINKED INDEX")
        pointer_size    = input("Pointer Size: ")
        block_size      = input("Block Size: ")
        logical_address = input("Logical Address: ")

        linked_index(convert_to_bytes(pointer_size), convert_to_bytes(block_size), convert_to_bytes(logical_address))
        return True
    else:
        return False
        

def convert_to_bytes(string):
    length = len(string)
    # number = 0
    if string[length-2:] == "KB" or string[length-2:] == "kb":
        number = float(string[:length-2]) * 1024
    elif string[length-2:] == "MB" or string[length-2:] == "mb":
        number = float(string[:length-2]) * 1024 * 1024
    elif string[length-2:] == "GB" or string[length-2:] == "gb":
        number = float(string[:length-2]) * 1024 * 1024 * 1024
    else:
        number = float(string)
    return number

def contiguous_allocation(logical_address, block_size):
    block_number = logical_address // block_size
    offset       = logical_address % block_size
    print("-->Block Number: ", block_number)
    print("-->Offset:       ", offset)

def modify_contiguous_allocation(extent_blocks, block_size, logical_address):
    extent       = logical_address // (extent_blocks * block_size)
    block_number = ( logical_address % (extent_blocks * block_size) ) // block_size
    offset       = logical_address % block_size
    print("-->Extent:       ", extent)
    print("-->Block Number: ", block_number)
    print("-->Offset:       ", offset)

def linked_allocation(pointer_size, block_size, logical_address):
    data_part_size = block_size - pointer_size
    block_number   = logical_address // data_part_size
    offset         = logical_address % data_part_size + pointer_size
    print("-->Data Part Size: ", data_part_size)
    print("-->Block Number:   ", block_number)
    print("-->Offset:         ", offset)

def indexed_allocation(pointer_size, block_size, logical_address):
    sum_pointer       = block_size / pointer_size
    maximum_file_size = sum_pointer * block_size
    block_number      = logical_address // block_size
    offset            = logical_address % block_size

    print("-->Block Number: ", block_number)
    print("-->Offset:       ", offset)
    print("Maximum File Size: ", maximum_file_size)

def twolevel_indexed_allocation(pointer_size, block_size, logical_address):
    sum_pointer  = block_size / pointer_size
    index_table  = logical_address // (sum_pointer * block_size)
    block_number = ( logical_address % (sum_pointer * block_size) ) // block_size
    offset       = logical_address % block_size

    print("-->Index Table:  ", int(index_table))
    print("-->Block Number: ", int(block_number))
    print("-->Offset:       ", offset)

def inode(pointer_size, block_size, logical_address):
    sum_of_pointer            = block_size / pointer_size
    max_direct_pointer        = 12
    max_SIP                   = sum_of_pointer + max_direct_pointer
    max_DIP                   = (sum_of_pointer ** 2) +  max_SIP
    max_TIP                   = (sum_of_pointer ** 3) + max_DIP

    block_number              = logical_address // block_size
    bn                        = block_number + 1

    print("-->Max Direct Pointer: ", max_direct_pointer)
    print("-->Max SIP: ", max_SIP)
    print("-->Max DIP: ", max_DIP)
    print("-->Max TIP: ", max_TIP)
    print("-->Sum Pointer: ", sum_of_pointer)
    print("-->Block Number: ", block_number)

    if bn > max_TIP:
        print("Invalid")
    elif bn > max_DIP:
        print("Triple Indirect Pointer")
        sum_of_block = block_number - max_DIP
        block1 = sum_of_block // sum_of_pointer ** 2
        block2 = (sum_of_block % sum_of_pointer ** 2) // sum_of_pointer
        block3 = (sum_of_block % sum_of_pointer ** 2) % sum_of_pointer
        offset = logical_address % block_size
        print("Sum of block: ", sum_of_block)
        print("Block 1: ", block1)
        print("Block 2: ", block2)
        print("Block 3: ", block3)
        print("Offset: ", offset)
    elif bn > max_SIP:
        print("Double Indirect Pointer")
        sum_of_block = block_number - max_SIP
        block1 = sum_of_block // sum_of_pointer
        block2 = sum_of_block % sum_of_pointer
        offset = logical_address % block_size
        print("Sum of block: ", sum_of_block)
        print("Block 1: ", block1)
        print("Block 2: ", block2)
        print("Offset: ", offset)
    elif bn > max_direct_pointer:
        sum_of_block = block_number - max_direct_pointer
        offset = logical_address % block_size
        print("Single Indirect Pointer")
        print("Sum of block: ", sum_of_block)
        print("Offset: ", offset)
    else:
        print("Direct Pointer")
    
def linked_index(pointer_size, block_size, logical_address):
    sum_of_pointer = block_size / pointer_size
    data_pointer   = sum_of_pointer - 1
    index_block    = logical_address // (data_pointer * block_size)
    block_number   = ( logical_address % (data_pointer * block_size) ) // block_size
    offset         = logical_address % block_size
    print("-->Sum of pointer: ", sum_of_pointer)
    print("-->Data Pointer: ", data_pointer)
    print("-->Index Block: ", index_block)
    print("-->Block Number: ", block_number)
    print("-->Offset: ", offset)


if __name__ == "__main__":
    while main():
        main()