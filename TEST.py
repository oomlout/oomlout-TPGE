import re


str = "http://sds.01/create/http/capital/870745800/create/period_1_1364871116_438861511.ssa"

m = re.match(r"period_1_(.*)\.ssa", str)
print m