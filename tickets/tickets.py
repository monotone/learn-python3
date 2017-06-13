# -*- coding: utf-8 -*-

"""命令行火车票查看器

Usage:
    tickets [-gdctkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -c          城际
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

init()

class TrainsCollection:
    header = '车次 出发站/到达站 出发时间/到达时间 历时 商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其他 备注'.split()

    def __init__(self, available_trains, code_2_name, options):
        """查询到的火车班次集合

        :param avaliable_trains: 一个列表，包含可获得的火车班次，每个火车班次是一个用|分割的字符串。

        :param options： 查询的选项，如高铁，动车，etc...
        """

        self.avaliable_trains = available_trains
        self.code_2_name = code_2_name
        self.options = options

    @property
    def trains(self):
        for raw_train in self.avaliable_trains:
            params = raw_train.split('|')
            if not self.options or params[3][0].lower() in self.options:
                train = [
                    params[3],
                    '/'.join([Fore.GREEN + self.code_2_name[params[6]] + Fore.RESET, Fore.RED + self.code_2_name[params[7]] + Fore.RESET]),
                    '/'.join([Fore.GREEN + params[8] + Fore.RESET, Fore.RED + params[9] + Fore.RESET]),
                    params[10],
                    params[-3] or "-", # 商务座
                    params[-10] or "-", # 特等座
                    params[-4] or "-", # 一等座
                    params[-5] or "-", # 二等座
                    "-",     # 高级软卧
                    params[-12] or "-",     # 软卧
                    params[-7] or "-",     # 硬卧
                    params[-8] or "-",     # 软座
                    params[-6] or "-",     # 硬座
                    params[-9] or "-", # 无座
                    "-",       # 其他
                    params[1],     # 备注
                    ]

                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)



def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    # 构建url
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
    # print(arguments)

    # 获取参数
    options = ''.join([
            key for key, value in arguments.items() if value is True
        ])

    r = requests.get(url, verify = False)
    result_array = r.json()['data']['result']
    code_2_name = r.json()['data']['map']
    TrainsCollection(result_array, code_2_name, options).pretty_print()

    # print(result_array)
    # print (code_2_name)

if __name__ == '__main__':
    cli()
