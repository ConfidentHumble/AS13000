lines = []
with open("totals.html", 'r') as f:
    lines = f.readlines()
    size = len(lines)
    for i in range(size):
        print('%d %s'%(i, lines[i]))
metrics_list = lines[17].split()
print(metrics_list)
Metrics_Name = [
    'ReqstdOps_rate',
    'ReqstdOps_resp',
    'Pct_read',
    'IOPS_read_rate',
    'IOPS_read_resp',
    'IOPS_write_rate',
    'IOPS_write_resp',
    'MbSec_read',
    'MbSec_write',
    'MbSec_total'
]
Metrics_Name[0] = metrics_list[2]
Metrics_Name[1] = metrics_list[3]
Metrics_Name[2] = metrics_list[6]
Metrics_Name[3] = metrics_list[7]
Metrics_Name[4] = metrics_list[8]
Metrics_Name[5] = metrics_list[9]
Metrics_Name[6] = metrics_list[10]
Metrics_Name[7] = metrics_list[11]
Metrics_Name[8] = metrics_list[12]
Metrics_Name[9] = metrics_list[13]
# print('ReqstOps_rate:' + ReqstdOps_rate)
# print('ReqstOps_reps:' + ReqstdOps_resp)
# print('Pct_read:' + Pct_read)
# print('IOPS_read_rate:' + IOPS_read_rate)
# print('IOPS_read_reps:' + IOPS_read_resp)
# print('IOPS_write_rate:' + IOPS_write_rate)
# print('IOPS_write_resp:' + IOPS_write_resp)
# print('MbSec_read:' + MbSec_read)
# print('MbSec_write:' + MbSec_write)
# print('MbSec_total:' + MbSec_total)





