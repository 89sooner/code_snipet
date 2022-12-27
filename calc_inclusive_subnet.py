import ipaddress
import sys
import pymysql
import struct
from socket import inet_aton
from collections import defaultdict

def calc_inclusive_subnet(ip_list):

    ip_list = [ _ip[0] for _ip in ip_list]
    sorted_list = sorted(ip_list, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

    split_list = [ '.'.join(_ip.split('.')[0:3]) for _ip in sorted_list ]
    elim_dup_list = list(dict.fromkeys(split_list))

    buckets_obj = defaultdict(list)
    for sorted_ip in sorted_list:
        for index, bucket_ip in enumerate(elim_dup_list):
            if bucket_ip in sorted_ip:
                buckets_obj[bucket_ip].append(ipaddress.IPv4Address(sorted_ip))

    net = []
    for _bucket in buckets_obj.values():
        min_ip = min(_bucket)
        max_ip = max(_bucket)
        distance = int(max_ip)-int(min_ip)
        ip_range=0

        while 2**ip_range < distance:
            ip_range += 1

        net.append(ipaddress.IPv4Network(str(min_ip) + '/' +str(32-ip_range), strict=False))

    '''
        if max_ip not in net:
        # i.e. if the distance implies one size network, but IPs span 2
            ip_range+=1
            net = ipaddress.IPv4Network(str(min_ip) + '/' +str(32-ip_range), strict=False)
    '''

    return net


if __name__ == '__main__':

    srcIP = sys.argv[1]
    conn = pymysql.connect(host='', user='', port=, password='',db='')
    curs = conn.cursor()

    sql = """
    SELECT DISTINCT dstIP
      FROM ??
     WHERE 1=1
       AND srcIP = '%s';
    """%srcIP

    curs.execute(sql)
    list=curs.fetchall()

    net = calc_inclusive_subnet(list)
    print(net)
