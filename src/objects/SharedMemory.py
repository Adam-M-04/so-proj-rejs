import mmap
import struct

def create_shared_memory(size, fmt='i'):
    return mmap.mmap(-1, size * struct.calcsize(fmt), access=mmap.ACCESS_WRITE)

def write_to_shared_memory(shm, offset, value, fmt='i'):
    shm.seek(offset)
    shm.write(struct.pack(fmt, value))

def read_from_shared_memory(shm, fmt='i', offset=0):
    shm.seek(offset)
    return struct.unpack(fmt, shm.read(struct.calcsize(fmt)))[0]

def is_passenger_in_shared_memory(shared_memory, pass_id, fmt='i'):
    element_size = struct.calcsize(fmt)
    for i in range(0, len(shared_memory), element_size):
        if read_from_shared_memory(shared_memory, fmt, i) == pass_id:
            return True
    return False

def append_to_shared_memory(shared_memory, value, fmt='i'):
    element_size = struct.calcsize(fmt)
    for i in range(0, len(shared_memory), element_size):
        shared_memory.seek(i)
        if shared_memory.read(element_size) == b'\x00' * element_size:
            shared_memory.seek(i)
            shared_memory.write(struct.pack(fmt, value))
            return
    raise ValueError("No space left in shared memory to append the value.")

def count_passengers_in_shared_memory(shm, fmt='i'):
    """
    Counts the number of non-zero entries in the shared memory array.

    :param shm: The shared memory object.
    :param length: The number of elements in the array.
    :param fmt: The format of each element (default is 'i' for integer).
    :return: The count of non-zero entries.
    """
    try:
        count = 0
        length = len(shm)
        element_size = struct.calcsize(fmt)
        for i in range(length//4):
            offset = i * element_size
            shm.seek(offset)
            value = struct.unpack(fmt, shm.read(element_size))[0]
            if value != 0:
                count += 1
        return count
    except:
        return 0

def remove_from_shared_memory(shared_memory, pass_id, fmt='i'):
    element_size = struct.calcsize(fmt)
    for i in range(0, len(shared_memory), element_size):
        if read_from_shared_memory(shared_memory, fmt, i) == pass_id:
            write_to_shared_memory(shared_memory, i, 0, fmt)


def shared_memory_to_array(shared_memory, fmt='i'):
    element_size = struct.calcsize(fmt)
    values = []
    for i in range(0, len(shared_memory), element_size):
        val = read_from_shared_memory(shared_memory, fmt, i)
        if val:
            values.append(val)

    return values