import os
from PIL import Image, ImageSequence

list_size = []
list_max_value = 0


def init(file_name_all, key=1, image_size=(70, 70)):
    if file_name_all.split(".")[1] == "gif":
        def try_path(path):
            """检查目录，没有就创建"""
            if not os.path.exists(path):
                print(f'创建目录{path}')
                os.makedirs(path)

        def parseGIF(gifname, key=1):
            """    
            将gif解析为图片\n
            gifname: 文件名\n
            key：是否抽帧，key默认为1,改为其他值则按比例抽帧
            """
            global list_max_value

            # 读取GIF
            im = Image.open(gifname)
            # GIF图片流的迭代器
            iter = ImageSequence.Iterator(im)
            # 获取文件名
            file_name = gifname.split(".")[0]
            index = 0
            # 判断目录是否存在
            save_path = f"imgs/{file_name}/"
            try_path(save_path)

            # 遍历图片流的每一帧并保存为JPG
            for _key, _frame in enumerate(iter):
                if _key % key == 0:
                    print(f"遍历帧数：{_key}")
                    _frame_resize = _frame.resize((70, 70))
                    _frame_save = _frame_resize.convert('RGB')
                    _frame_save.save(
                        f"{save_path}/{file_name}_{index}.jpg", quality=60, subsampling=0)
                    index += 1
                    list_max_value += 1

        def write_to_h(path, file_name):
            """    
            将JPG文件的数据流写入.h文件\n
            输入：
                path: 路径\n
                file_name：输入的文件名
            """
            def _10to16(int_value: int) -> str:
                """
                [转换十进制为十六进制并格式化]\n
                只支持16以内的十进制转换\n
                返回格式为形如 0xFF 的字符串\n
                输入:
                    int_value (int): [需要转换的十进制]\n
                返回:
                    str: [转换并格式化的十六进制]
                """
                num_list = ["0", "1", "2", "3", "4", "5", "6",
                            "7", "8", "9", "A", "B", "C", "D", "E", "F"]
                str_16 = ''
                # 取余
                int_value, mod = divmod(int_value, 16)
                # 拼接
                str_16 = str(num_list[mod]) + str_16
                # 格式化
                if int_value == 0:
                    str_16 = "0" + str_16
                else:
                    int_value, mod = divmod(int_value, 16)
                    str_16 = str(num_list[mod]) + str_16

                return "0x" + str_16 + ","

            def write_to_h_one(path: str, file_name: str) -> list:
                """
                [在.h里写入一个变量的声明和赋值]\n
                一次写入一个声明和\n
                输入:
                    path (str): [jpg文件所存的路径]\n
                    file_name (str): [输入图片的文件名]\n
                返回:
                    list: [组合好的全部声明文本,声明的数组的大小]
                """
                file = path + file_name + ".jpg"
                num = 0
                re_str = "const uint8_t " + \
                    f"{file_name}[] PROGMEM = " + "{\n\t"
                binfile = open(file, 'rb')  # 打开二进制文件
                size = os.path.getsize(file)  # 获得文件大小
                re_str_size = 0
                for _ in range(size):
                    data = binfile.read(1)  # 每次输出一个字节
                    re_str = re_str + _10to16(data[0])
                    num += 1
                    if num == 16:
                        # break
                        re_str = re_str + "\n\t"
                        num = 0
                    re_str_size += 1
                binfile.close()
                re_str = re_str + "\n};\n"
                return [re_str, re_str_size]

            os_list = os.listdir(path)

            os_list.sort(key=lambda x: int(
                x.split('.')[0].split('_')[1]), reverse=False)

            with open(f"{file_name}.h", 'w') as a:
                # 写入数组声明
                a.write("#include <pgmspace.h> \n")
                for i in os_list:
                    _file_name = i.split('.')[0]
                    write_value, size = write_to_h_one(path, _file_name)
                    a.write(write_value)
                    # 记录数组名称
                    list_size.append(size)

                # 写入数组头指针数组的声明
                a.write("\n\nconst uint8_t *" + file_name +
                        f"[{list_max_value}]" + " PROGMEM {")
                for i in range(list_max_value):
                    a.write(f"{file_name}_{i},")
                a.write("};\n")

                # 写入数组头指针所指向的数组的大小的声明
                a.write("\nconst uint32_t " + file_name +
                        "_size" + f"[{list_max_value}]"+" PROGMEM {")
                for i in list_size:
                    a.write(f"{i},")

                # 收尾
                a.write("};\n")

        # 提取无后缀文件名
        file_name = file_name_all.split(".")[0]
        # 设定工作目录
        path = f"./imgs/{file_name}/"
        print("文件名", file_name)

        # 将GIF转化为JPG
        parseGIF(file_name_all, key)
        # 将JPG文件的数据流写入.h文件
        write_to_h(path, file_name)
    else:
        exit("格式错误，请检查是否为GIF")


if __name__ == "__main__":
    # 把GIF放到py文件旁边。默认只支持正方形的图片，不是正方形的自己改图片大小
    # 第一个参数为文件名，需带后缀
    # 第二个参数是是否抽帧，适用于GIF帧率较高的时候，按比例抽帧(2就是每2帧取1帧) 默认为1
    # 第三个参数为生产的图片尺寸(默认为70,70),如需更改请配合修改对应的坐标参数

    # 如果看不懂这里在什么，请使用默认参数！
    # 如果看不懂这里在什么，请使用默认参数！
    # 如果看不懂这里在什么，请使用默认参数！

    file_name = "hutao.gif"
    init(file_name)
