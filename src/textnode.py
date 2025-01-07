from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode():
    def __init__(self,text, text_type, url = None):
        #print(f"-> Making a new TextNode")
        self.text = text
        self.text_type = text_type
        self.url = url
        #print(f"--->self.text = {text}")
        #print(f"--->self.text_type = {text_type}")
        #print(f"--->self.url = {url}")
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    