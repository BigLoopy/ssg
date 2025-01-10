import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_empty_line(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_emtpy_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "")
        node2 = TextNode("This is a text node", TextType.BOLD, "")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a different text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://notgoogle.com")
        self.assertNotEqual(node, node2)

    def test_textnode_to_html_invlalid_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a text node", "invalid", "https://google.com")
            node.text_node_to_html_node()
 
    def test_textnode_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        leaf = LeafNode("b",node.text)
        self.assertEqual(node.text_node_to_html_node(),leaf)

    def test_textnode_to_html_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf = LeafNode(None,node.text)
        self.assertEqual(node.text_node_to_html_node(),leaf)

    def test_textnode_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        leaf = LeafNode("i",node.text)
        self.assertEqual(node.text_node_to_html_node(),leaf)

    def test_textnode_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        leaf = LeafNode("code",node.text)
        self.assertEqual(node.text_node_to_html_node(),leaf)

    def test_textnode_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK,"https://www.google.com")
        leaf = LeafNode("a",node.text,{"href": "https://www.google.com"})
        self.assertEqual(node.text_node_to_html_node(),leaf)

    def test_textnode_to_html_image(self):
        node = TextNode("This is a text node", TextType.IMAGE,"https://www.google.com")
        leaf = LeafNode("img","",{"src": "https://www.google.com", "alt": node.text})
        self.assertEqual(node.text_node_to_html_node(),leaf)
    #     self.assertEqual(node.text_node_to_html_node(),'<mg src="https://www.google.com>This is a text node</img>')

    def test_textnode_to_html_link_no_link(self):
        node = TextNode("This is a text node", TextType.LINK,"")
        leaf = LeafNode("a",node.text,{"href": ""})
        self.assertEqual(node.text_node_to_html_node(),leaf)
    #     self.assertEqual(node.text_node_to_html_node(),'<a href="https://www.google.com">This is a text node</a>')

    def test_textnode_to_html_image_no_image(self):
        node = TextNode("This is a text node", TextType.IMAGE,"")
        leaf = LeafNode("img","",{"src": "", "alt": node.text})
        self.assertEqual(node.text_node_to_html_node(),leaf)
    
    if __name__ == "__main__":
        unittest.main()
