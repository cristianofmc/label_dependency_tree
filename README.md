# Label Dependency Tree

This app created with python that provide a base to create a dependency tree, with a optional output draw of the tree.

![Screenshot](https://github.com/cristianofmc/label_dependency_tree/blob/main/color_example.png)

## Instalation
To run this project you need the python3 and the requirements instaled, please check the [requirements.txt](https://github.com/cristianofmc/label_dependency_tree/blob/main/requirements.txt)

## Usages
To use this project, you first need to call the Tree class, where you will create the basis for the interactions between the nodes of the tree. To add the nodes, you must send objects of type Item to the add_items method.
In case you want to export an image with the tree with the items and the connections between the items, you must send an instance of the Tree class to the DependencyGraph class.

A better understanding of the code can be obtained from the interpretation of the tests.

## Licence
This is a free software, and may be redistributed under the terms specified in the [LICENSE](https://github.com/cristianofmc/label_dependency_tree/blob/main/LICENCE) file.
