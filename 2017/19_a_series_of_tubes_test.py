import importlib

module = importlib.import_module("19_a_series_of_tubes")
walker = module.walker


def test_example():
    example = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
    """.split("\n")

    result = walker(example, (0, 5))

    assert result == "ABCDEF"
