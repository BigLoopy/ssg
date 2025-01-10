class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if (self.props == "" or self.props == None):
            return ""
        stringprops = map(lambda key: f' {key}="{self.props[key]}"',self.props.copy())
        return ("".join(stringprops))
    
    def __repr__(self):
        return f"-->tag={self.tag}\n-->value={self.value}\n-->children={self.children}\n-->props={self.props}"
    
    def __eq__(self, value):
        if self.tag != value.tag:
            return False
        elif self.value != value.value:
            return False
        elif self.children != value.children:
            return False
        elif self.props != value.props:
            return False
        return True
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        
        if self.value == None:
            raise ValueError("Value is required")
        elif self.value == "":
            return f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        if self.tag == None or self.tag == "":
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("tag is required")
        if (self.children == None):
            raise ValueError("parents must have children")
        
        results = ""
        for child in self.children:
            results += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{results}</{self.tag}>"
        
