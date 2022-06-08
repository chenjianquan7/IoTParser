from front_analysise.modules.parser.baseparse import BaseParser
import xml.etree.ElementTree as ET

class DlinkHNAPXMLParser(BaseParser):
    def analysise(self):
        level = 1  
        try:
            tree = ET.parse(self.fpath)
            
            root = tree.getroot()
            self.walkData(root, level)
        except Exception as e:  
            self.log.error("parse {} fail!".format(self.fpath))
    
    def walkData(self, root_node, level):
        """
        实现从xml文件中读取数据
        """
        if level == 3:
            index = root_node.tag.find("}")
            if index > 0:
                str = root_node.tag[index+1:]
            
            else:
                str = root_node.tag
            
            self._get_function(str, check=0)
        elif level > 3:
            index = root_node.tag.find("}")
            if index > 0:
                str = root_node.tag[index+1:]
            
            else:
                str = root_node.tag
            
            self._get_keyword(str, check=0)
        
        children_node = list(root_node)
        if len(children_node) == 0:
            return
        for child in children_node:
            self.walkData(child, level+1)
        return
