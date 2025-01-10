import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode


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
        self.assertEqual(' href="https://www.google.com"',result)

    def test_htmlnode_props_to_html_multiple(self):
        hrefprop = {
           "href": "https://www.google.com",
           "target": "_blank",
           "id":  "txtBox",
        }

        node = HTMLNode("tag","value","children",hrefprop)
        result = node.props_to_html()
        self.assertEqual(' href="https://www.google.com" target="_blank" id="txtBox"',result)


    def test_htmlnode_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode("tag","value","children","props")
            node.to_html()

    def test_leafnode_to_html_valueerror(self):
        node = LeafNode(None,None)
        with self.assertRaises(ValueError):
            output = node.to_html()
        
    def test_leafnode_to_html_no_tag(self):
        node = LeafNode(None,"tagless text here")
        output = node.to_html()
        self.assertEqual("tagless text here",output)

    def test_leafnode_to_html_empty_tag(self):
        node = LeafNode("","tagless text here")
        output = node.to_html()
        self.assertEqual("tagless text here",output)

    def test_leafnode_to_html_with_tag(self):
        node = LeafNode("p","tagged text here")
        output = node.to_html()
        self.assertEqual("<p>tagged text here</p>",output)

    def test_leafnode_to_html_with_props(self):
        props = {
            "class": "paragraph"
        }
        node = LeafNode("p","tagged text here", props)
        output = node.to_html()
        self.assertEqual('<p class="paragraph">tagged text here</p>',output)

    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_to_html_nested_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                    LeafNode("b", "Bold text"),
                    ],
                ) 
            ],
        )
        
        self.assertEqual(node.to_html(),"<p><b>Bold text</b><p><b>Bold text</b></p></p>")

    def test_parentnode_to_html_double_nested_parent(self):
        node = ParentNode("p",[LeafNode("b", "Bold text"),ParentNode("p",[ParentNode("p",[LeafNode("b", "Bold text"),],),LeafNode("b", "Bold text"),],)],)
        
        self.assertEqual(node.to_html(),"<p><b>Bold text</b><p><p><b>Bold text</b></p><b>Bold text</b></p></p>")

    def test_parentnode_to_html_no_kids(self):
        node = ParentNode("p",[])
        
        self.assertEqual(node.to_html(),"<p></p>")

    def test_parentnode_to_html_none_kids(self):
        node = ParentNode("p",None)
        with self.assertRaises(ValueError):
            self.assertEqual(node.to_html(),"<p></p>")

    def test_parentnode_to_html_emtpy_tag(self):
        node = ParentNode("",[])
        with self.assertRaises(ValueError):
            self.assertEqual(node.to_html(),"<p></p>")

    def test_parentnode_to_html_none_tag(self):
        node = ParentNode(None,[])
        with self.assertRaises(ValueError):
            self.assertEqual(node.to_html(),"<p></p>")


if __name__ == "__main__":
    unittest.main()
