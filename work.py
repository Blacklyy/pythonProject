import math

# 初始种子
const_seed = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

# 从切片内取值位置
dataPos = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12],
    [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2],
    [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
]

# 循环左移偏移量
move_amounts = [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]

# pow(2, 32)*abs(sin(i)) 整数部分
statics = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xffffffff for i in range(64)]

'''
Convert input to stander
'''


def convertToWordArray(string):

    # 将string转换为byte方便数据处理
    message = bytearray(string, encoding='utf-8')

    # message bits数量,若长度超过pow(2,64),取低64位， 既&0xffffffffffffffff
    len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    # 第一位填充为 1
    # 由于数据存储方式为小端，故将 0x01翻转为0x80
    message.append(0x80)
    # 其余位填充为 0
    # message长度应满足 (len(message)*8)%512 = 448
    # 化简后既为 len(message)%512 = 56
    while len(message) % 64 != 56:
        message.append(0)
    # 预留的8bytes空间用于存储数据长度
    message += len_in_bits.to_bytes(8, byteorder='little')
    array = []
    # Convert to Array
    # 将数据分组 每一组为64bytes 既 64 * 8 = 512bits
    # 数据预处理完成
    for offset in range(0, len(message), 64):
        array.append(message[offset: offset + 64])
    return array


def F(x, y, z):
    return (x & y) | (~x & z)


def G(x, y, z):
    return (x & z) | (y & ~z)


def H(x, y, z):
    return x ^ y ^ z


def I(x, y, z):
    return y ^ (x | ~z)


functions = [F, G, H, I]


def leftMove(x, n):
    # if x is too long
    x &= 0xffffffff
    # 循环左移
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def md5Hash(message):
    x = convertToWordArray(message)
    # 初始化hashPart
    # 最终Hash值将由hashPart组合而成
    hash_part = const_seed[:]

    # 对每一组数据进行计算
    for i in range(0, len(x)):
        # 初始化a b c d
        a, b, c, d = hash_part
        # 将每一大组 (512bit/64byte) 分为16个小组(32bit/4byte)
        pieces = []
        for offset in range(0, 16):
            pieces.append(x[i][offset * 4:(offset + 1) * 4])

        # 开始运算
        cnt = 0  # 运算计数
        # 64次循环 每16次分别使用 F G H I 函数
        for i in range(0, 4):
            for j in range(0, 16):
                tempr = a + functions[i](b, c, d) + statics[cnt] + int.from_bytes(pieces[dataPos[i][j]], "little")

                tempr = leftMove(tempr, move_amounts[i][j % 4])
                updateB = (b + tempr) & 0xffffffff
                # 为a b c d重新赋值，实现a b c d循环右移
                a, b, c, d = d, updateB, b, c
                cnt += 1
        # 一轮运算后 赋值hashPart
        # old a/b/c/d add new a/b/c/d
        templist = [a, b, c, d]
        for i in range(0, 4):
            hash_part[i] += templist[i]
            hash_part[i] &= 0xffffffff
    # 运算结束 组合hash_part
    ans = int.to_bytes(hash_part[3], 4, byteorder="big") + int.to_bytes(hash_part[2], 4, byteorder="big") + \
          int.to_bytes(hash_part[1], 4, byteorder="big") + int.to_bytes(hash_part[0], 4, byteorder="big")

    # 此时ans为bytes
    # 将其转换为16进制
    # hex(int.from_bytes(ans, byteorder="little"))

    return hex(int.from_bytes(ans, byteorder="little"))


if __name__ == "__main__":
    print(md5Hash(""))
    print(md5Hash("ab"))
    print(md5Hash("d41d8cd98f00b204e9800998ecf8427e"))
