import unittest
from processor import split_nodes_image
from textnode import TextType, TextNode

class TestImages(unittest.TestCase):


################################################
    def test_split_nodes_image_none_nodes_returns_empty_list(self):
        old_nodes = None
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, list())

    def test_split_nodes_image_bad_type_raises_valueerror(self):
        old_nodes = TextType.TEXT
        with self.assertRaises(ValueError):
            split_nodes_image(old_nodes)

    def test_split_nodes_image_valueerror_list_of_bad_type(self):
        old_nodes = [TextType.TEXT]
        with self.assertRaises(ValueError):
            split_nodes_image(old_nodes)

    def test_split_nodes_image_delimeter_only_the_thing(self):
            old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)]
            new_nodes = split_nodes_image(old_nodes)
            expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_delimeter_only_the_thing_multiple(self):
            old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)]
            new_nodes = split_nodes_image(old_nodes)
            expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_delimeter_only_the_thing_multiple_with_space(self):
            old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) ![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)]
            new_nodes = split_nodes_image(old_nodes)
            expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        TextNode(" ", TextType.TEXT),
                        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_delimeter_start(self):
            old_nodes = [TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) some additional **stuff**",TextType.TEXT)]
            new_nodes = split_nodes_image(old_nodes)
            expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        TextNode(" some additional **stuff**", TextType.TEXT),
            ]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_before_and_after_text(self):
        singleNode = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif).",TextType.TEXT)
        new_nodes = split_nodes_image(singleNode)
        expected =  [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                    TextNode(".", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_image_delimeter_not_in_text(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        expected = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_image_delimeter_end(self):
            old_nodes = [TextNode("some additional **stuff** ![rick roll](https://i.imgur.com/aKaOqIh.gif)",TextType.TEXT)]
            new_nodes = split_nodes_image(old_nodes)
            expected = [TextNode("some additional **stuff** ", TextType.TEXT),
                        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                        
            ]
            self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
