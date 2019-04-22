
class StructureConnection:
    color_set = (0,0,0)
    id_num = 0
    ip_addr = ""
#    name_str = ""
    def __init__(self,num,ip_position):
        self.color_set = (0,255,0)
        self.id_num = num
        self.ip_addr = ip_position