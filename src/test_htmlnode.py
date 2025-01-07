import unittest
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_htmlnode_nones(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_htmlnode_construction(self):
        node = HTMLNode("tag","value","children","props")
        self.assertEqual(node.tag, "tag" )
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, "children")
        self.assertEqual(node.props, "props")

    def test_htmlnode_props_to_html_empty(self):
        node = HTMLNode("tag","value","children","")
        result = node.props_to_html()
        self.assertEqual("",result)

    def test_htmlnode_props_to_html_none(self):
        node = HTMLNode("tag","value","children",None)
        result = node.props_to_html()
        self.assertEqual("",result)

    def test_htmlnode_props_to_html_single(self):
        hrefprop = {
           "href": "https://www.google.com", 
        }

        node = HTMLNode("tag","value","children",hrefprop)
        result = node.props_to_html()
        self.assertEqual('href="https://www.google.com"',result)

    def test_htmlnode_props_to_html_multiple(self):
        hrefprop = {
           "href": "https://www.google.com",
           "target": "_blank",
           "id":  "txtBox",
        }

        node = HTMLNode("tag","value","children",hrefprop)
        result = node.props_to_html()
        self.assertEqual('href="https://www.google.com" target="_blank" id="txtBox"',result)



    def test_htmlnode_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode("tag","value","children","props")
            node.to_html()

    

if __name__ == "__main__":
    unittest.main()
