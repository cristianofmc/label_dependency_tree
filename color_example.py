from source import Item, Tree, DependencyGraph

tree = Tree('soft')
item1 = Item('blue', ['blue'], [])
item2 = Item('yellow', ['yellow'], [])
item3 = Item('red', ['red'], [])
item4 = Item('green', ['green'], ['blue', 'yellow'])
item5 = Item('orange', ['orange'], ['red', 'yellow'])
item6 = Item('violet', ['violet'], ['blue', 'red'])
item7 = Item('russet', ['russet'], ['orange', 'violet'])
items = [item1,item2,item3,item4,item5,item6,item7]

for item in list(items):
    tree.add_item(item)
    
graph = DependencyGraph(tree)
image_name = 'color_example'
graph.process_tree()
graph.draw(image_name)
