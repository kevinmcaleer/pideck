# Quick and Dirty YAML Parser
# Kevin McAleer
# February 2021


class YAML():
    """ A Quick and dirty YAML Parser """
    list = []
    def __init__(self):
        """ nothing to see here, yet """
        pass

    def remove_comments(self, text:str):
        return text.sub(r'(?m)^ *#.*\n','', text)

    @staticmethod
    def is_block(text):
        text = text.lstrip()
        if len(text) > 2:
            if text[0] == '-' and text[1] == ' ':
                return True
            else:
                return False
        else:
            return False
        
    def is_comment(self, text):
        if text in ['#']:
            return True

    def is_scalar(self, text):
        # if text
        return True
    
    @staticmethod
    def split_mapping(text):
        """ Converts a line of text in to a key value pair """ 
        mapping = text.split(':')
        key = mapping[0].strip()
        key = key.lstrip('-').strip()
        value = mapping[1].strip()
        new_list = {key: value}
        
        print('new_list is:',new_list)
        return new_list

    @staticmethod
    def is_mapping(text:str):
        """ Check if the yaml text line contains the semicolon character, or not 
            Returns True or False
        """
        if ':' in text:
            return True
        else:
            return False
    
    @staticmethod
    def count_indentation(text):
        """ Counts the number of spaces at the start of the line """
        leading_spaces = len(text) - len(text.lstrip())
        return leading_spaces

    def load(self, file)->list:
        """ loads the file and returns a list """
        within_block = False 
        block_list = []
        level = 0
        node = 0
        for line in file:
            # count indentation level 
            current_level = self.count_indentation(line)
            if current_level == level and YAML.is_block(line) and node > 0:
                self.list.append(block_list)
                block_list = []
                
                new_line = YAML.split_mapping(line)
                block_list.append(new_line)
                self.list.append(block_list)
                block_list = []
                level = self.count_indentation(line)
            else:
                # just the first node
                if node == 0:
                    new_line = YAML.split_mapping(line)
                    block_list.append(new_line)
                    node += 1
                else:
                    if YAML.is_mapping(line):
                        # split string at mapping and remove whitespace
                        new_line = YAML.split_mapping(line)
                        block_list.append(new_line)
                        # self.list.append(new_line)
 
        return self.list

    def pretty_print(self):
        for item in self.list:
            print(item)