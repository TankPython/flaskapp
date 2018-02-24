

import re

a = re.match(r"1[34578]\d{9}", "18979907572")
print a.group()
print a