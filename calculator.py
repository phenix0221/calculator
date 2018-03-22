#!/usr/bin/env python3

# Author: phenix0221
# -*- coding: utf-8 -*-


# 使用sys模块来获取命令行参数
import sys
# 使用csv模块来保存程序输出结果
import csv
# 使用os模块来判断参数中的文件是否存在
import os


class Args(object):

    """
    处理命令行参数类
    1.获取命令行参数
    2.判断参数格式是否正确
    3.返回文件路径
    """

    # 私有属性__cmd_args，用于保存从命令行获取的参数列表
    __cmd_args = []
    # 私有属性__file_dict，用于保存从命令行获取的"选项: 文件路径"键值对
    __file_dict = {}
    # 私有属性__default_opt，用于定义默认的命令行选项
    # 第一个元祖用于判断命令行选项是否都存在，第二个元祖用于判断选项对应的文件是否存在
    # 输出文件由用户指定，默认是不存在的，不用判断是否存在
    __default_opt = [('-c', '-i', '-o'), ('-c', '-i')]

    # 初始化方法，从命令行获取参数列表__cmd_args
    def __init__(self):
        self.__cmd_args = sys.argv[1:]

    # 判断命令行参数合法性，并返回文件路径的方法
    def __get_file_path(self):
        # 命令行参数格式错误的提示信息
        usage = 'Usage: {} -c <config_file> -i <input_file> -o <output_file>'.format(sys.argv[0])
        # 判断参数的个数是否为6个
        if len(self.__cmd_args) != 6:
            print(usage)
            sys.exit(101)
        else:
            # 判断选项及参数是否合法
            # 这段代码能确保__cmd_args中同时存在'-c'，'-i'，'-o'三个选项
            for opt in self.__default_opt[0]:
                try:
                    # 判断选项'-c', '-i', '-o'是否都在命令行参数列表中
                    # opt_index用于判断并保存对应选项在__cmd_args中的索引值
                    opt_index = self.__cmd_args.index(opt)
                except:
                    print(usage)
                    sys.exit(101)
                try:
                    # 判断选项是否都有对应的参数，如果选项后面没有参数，则抛出异常
                    self.__cmd_args[opt_index + 1]
                except:
                    print(usage)
                    sys.exit(101)
            # 判断选项对应的文件路径是否存在，存在则添加至__file_dict，否则退出
            # 这段代码用于判断'-c'，'-i'两个选项对应的文件是否存在，输出文件由程序创建，因此不作判断
            for opt in self.__default_opt[1]:
                # opt_index用于保存选项在__cmd_args中的索引值
                opt_index = self.__cmd_args.index(opt)
                if os.path.exists(self.__cmd_args[opt_index + 1]):
                    # 如果文件存在，则在__file_dict中添加'opt: path'键值对
                    self.__file_dict[opt] = self.__cmd_args[opt_index + 1]
                else:
                    print('File "{}" not exist!'.format(self.__cmd_args[opt_index + 1]))
                    sys.exit(102)
            # 单独添加输出文件的路径至__file_dict
            self.__file_dict['-o'] = self.__cmd_args[self.__cmd_args.index('-o') + 1]
        # 如果命令行参数正确，且对应文件存在，则返回文件路径字典__file_dict
        return self.__file_dict

    # 定义装饰器，用于返回文件路径字典__file_dict
    @property
    def get_file_path(self):
        return self.__get_file_path()


class Config(object):

    """
    获取配置文件信息类
    1.读取配置文件信息
    2.判断配置文件格式
    3.返回配置信息字典
    """

    # 私有属性__config_dict，用于保存配置文件信息
    __config_dict = {}
    # 私有属性__config_file，用于保存配置文件路径
    __config_file = ''

    # 初始化方法，从Args()中获取配置文件路径，即'-c'选项对应的文件路径
    def __init__(self):
        # 将Args()实例化为get_file_path
        file_path = Args()
        # 将路径信息保存在私有属性__config_file中
        self.__config_file = file_path.get_file_path['-c']

    # 定义判断配置文件内容合法性的方法，并返回配置信息
    def __get_config(self):
        with open(self.__config_file) as f:
            for line in f:
                try:
                    # 逐行处理文件内容，去掉空格和换行符，以'='为分隔符进行切分
                    # 将配置信息保存至__config_dict
                    self.__config_dict[line.replace(' ', '').split('=')[0]] = \
                        float('%.3f' % float(line.replace(' ', '').strip('\n').split('=')[1]))
                except:
                    print('Config file error!')
                    sys.exit(103)
        # 文件处理完成后，返回配置信息字典__config_dict
        return self.__config_dict

    # 定义装饰器，用于返回配置文件信息字典__config_dict
    @property
    def get_config(self):
        return self.__get_config()


class UserData(object):

    """
    获取用户信息类
    1.读取用户信息
    2.判断用户信息格式
    3.返回用户信息字典
    """

    # 私有属性__user_data_dict，用于保存用户信息
    __user_data_dict = {}
    # 私有属性__user_data_file，用于保存用户信息文件路径
    __user_data_file = ''

    # 初始化方法，从Args()中获取用户信息文件路径，即'-i'选项对应的文件路径
    def __init__(self):
        file_path = Args()
        self.__user_data_file = file_path.get_file_path['-i']

    # 定义判断用户信息文件内容合法性的方法，并返回用户信息
    def __get_users_data(self):
        with open(self.__user_data_file) as f:
            for line in f:
                try:
                    self.__user_data_dict[line.replace(' ', '').split(',')[0]] = \
                        float('%.2f' % float(line.replace(' ', '').strip('\n').split(',')[1]))
                except:
                    print('User data file error!')
                    sys.exit(104)
        return self.__user_data_dict

    # 定义装饰器，用于返回用户信息字典__user_data_dict
    @property
    def get_user_data(self):
        return self.__get_users_data()


class WagesCalculator(object):

    """
    工资计算类
    1.返回从UserData()中获取的用户ID
    2.返回从UserData()中获取的税前工资
    3.返回从Config()中获取的费种
    4.返回从Config()中获取的费率
    5.计算缴费金额
    6.定义个税起征点
    7.计算个人所得税金额
    8.计算税后工资
    """

    # 配置信息字典
    __config_dict = {}
    # 用户信息字典
    __user_data_dict = {}
    # 费种，费率信息字典
    __fee_config_dict = ()
    # 用户ID
    __user_id = []
    # 税前工资
    __wages_before_tax = []
    # 费种
    __fee_type = []
    # 费率
    __fee_rate = []
    # 缴费金额
    __fee_sum = []
    # 个税起征点
    __tax_threshold = 3500
    # 个人所得税
    __personal_tax = []
    # 税后工资
    __wages_after_tax = []
    # 工资详情
    __wages_detail = []

    # 初始化方法，从Config()中获取配置信息，从UserData()中获取用户信息
    def __init__(self):
        get_config = Config()
        self.__config_dict = get_config.get_config
        self.__fee_config_dict = self.__config_dict.copy()
        del self.__fee_config_dict['JiShuL']
        del self.__fee_config_dict['JiShuH']
        get_user_data = UserData()
        self.__user_data_dict = get_user_data.get_user_data

    # 获取用户ID列表__user_id的方法
    def __get_user_id(self):
        self.__user_id = list(self.__user_data_dict.keys())
        return self.__user_id

    # 访问用户ID列表__user_id的方法
    @property
    def get_user_id(self):
        return self.__get_user_id()

    # 获取税前工资列表__wages_before_tax的方法
    def __get_wages_before_tax(self):
        self.__wages_before_tax = list(self.__user_data_dict.values())
        return self.__wages_before_tax

    # 访问税前工资列表__wages_before_tax的方法
    @property
    def get_wages_before_tax(self):
        return self.__get_wages_before_tax()

    # 获取费种列表__fee_type的方法
    def __get_fee_type(self):
        self.__fee_type = list(self.__fee_config_dict.keys())
        return self.__fee_type

    # 访问费种列表__fee_type的方法
    @property
    def get_fee_type(self):
        return self.__get_fee_type()

    # 获取费率列表__fee_rate的方法
    def __get_fee_rate(self):
        self.__fee_rate = list(self.__fee_config_dict.values())
        return self.__fee_rate

    # 访问费率列表__fee_rate的方法
    @property
    def get_fee_rate(self):
        return self.__get_fee_rate()

    # 计算缴费金额，生成缴费金额列表__fee_sum的方法
    def __cal_fee_sum(self):
        sum_fee_rate = sum(self.get_fee_rate)
        for wages_before_tax in self.get_wages_before_tax:
            if wages_before_tax <= self.__config_dict['JiShuL']:
                fee = self.__config_dict['JiShuL'] * sum_fee_rate
            elif wages_before_tax >= self.__config_dict['JiShuH']:
                fee = self.__config_dict['JiShuH'] * sum_fee_rate
            else:
                fee = wages_before_tax * sum_fee_rate
            self.__fee_sum.append(fee)
        return self.__fee_sum

    # 访问缴费金额列表__fee_sum的方法
    @property
    def get_fee_sum(self):
        return self.__cal_fee_sum()

    # 计算个人所得税金额，生成列表__personal_tax的方法
    def __cal_personal_tax(self):
        for i in range(len(self.get_user_id)):
            tax_income = self.get_wages_before_tax[i] - self.get_fee_sum[i] - self.__tax_threshold
            if tax_income <= 0:
                tax = 0
            elif 0 < tax_income <= 1500:
                tax = tax_income * 0.03 - 0
            elif 1500 < tax_income <= 4500:
                tax = tax_income * 0.1 - 105
            elif 4500 < tax_income <= 9000:
                tax = tax_income * 0.2 - 555
            elif 9000 < tax_income <= 35000:
                tax = tax_income * 0.25 - 1005
            elif 35000 < tax_income <= 55000:
                tax = tax_income * 0.3 - 2755
            elif 55000 < tax_income <= 80000:
                tax = tax_income * 0.35 - 5505
            else:
                tax = tax_income * 0.45 - 13505
            self.__personal_tax.append(tax)
        return self.__personal_tax

    # 访问个人所得税金额列表__personal_tax的方法
    @property
    def get_personal_tax(self):
        return self.__cal_personal_tax()

    # 计算税后工资，生成税后工资列表__wages_after_tax的方法
    def __cal_wages_after_tax(self):
        for i in range(len(self.get_user_id)):
            wages_after_tax = self.get_wages_before_tax[i] - \
                              self.get_fee_sum[i] - self.get_personal_tax[i]
            self.__wages_after_tax.append(wages_after_tax)
        return self.__wages_after_tax

    # 访问税后工资列表__wages_after_tax的方法
    @property
    def get_wages_after_tax(self):
        return self.__cal_wages_after_tax()

    # 生成工资详情列表__wages_detail
    def __set_wages_detail(self):
        for i in range(len(self.get_user_id)):
            tmp_list = list()
            tmp_list.append(self.get_user_id[i])
            tmp_list.append(self.get_wages_before_tax[i])
            tmp_list.append(format(self.get_fee_sum[i], '.2f'))
            tmp_list.append(format(self.get_personal_tax[i], '.2f'))
            tmp_list.append(format(self.get_wages_after_tax[i], '.2f'))
            self.__wages_detail.append(tmp_list)
        return self.__wages_detail

    # 访问工资详情列表__wages_detail的方法
    @property
    def get_wages_detail(self):
        return self.__set_wages_detail()


if __name__ == '__main__':

    wages = WagesCalculator()
    wages_detail = wages.get_wages_detail

    file = Args()
    output_file = file.get_file_path['-o']
    with open(output_file, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(wages_detail)
