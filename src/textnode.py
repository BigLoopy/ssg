from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
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
        if (value == None):
            return False
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(text_node):
        match text_node.text_type:
           case TextType.TEXT:
                return LeafNode(None,text_node.text)
           case TextType.BOLD:
                return LeafNode("b",text_node.text)
           case TextType.ITALIC:
                return LeafNode("i",text_node.text)
           case TextType.CODE:
                return LeafNode("code",text_node.text)
           case TextType.LINK:
                props = {
                    "href": text_node.url
                }
                return LeafNode("a",text_node.text, props)
           case TextType.IMAGE:
                props = {
                    "src": text_node.url,
                    "alt" : text_node.text
                }
                return LeafNode("img","", props)
           case  _:
                raise ValueError("invalide text type")

