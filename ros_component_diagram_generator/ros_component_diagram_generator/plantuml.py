from ament_index_python.packages import get_package_share_path
from jinja2 import Template
from rclpy.logging import get_logger

logger = get_logger("launch2json")


def _get_all_entities(tree: dict):
    if tree.get("children"):
        entities = [tree["entity"]]
        for subtree in tree["children"]:
            entities.extend(_get_all_entities(subtree))
        return entities
    else:
        return [tree]


def get_component_kind(entity: dict):
    if entity["type"] == "IncludeLaunchDescription":
        return "folder"
    if entity["type"] == "GroupAction":
        return "folder"
    if entity["type"] == "ComposableNodeContainer":
        return "folder"
    if entity["type"] == "LoadComposableNodes":
        return "folder"
    if entity["type"] == "ComposableNode":
        return "node"
    if entity["type"] == "Node":
        return "node"
    if entity["type"] == "ExecuteProcess":
        return "node"
    return "card"


def get_component_id(entity: dict):
    if entity["type"] == "IncludeLaunchDescription":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "GroupAction":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "ComposableNodeContainer":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "LoadComposableNodes":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "ComposableNode":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "Node":
        return f'{entity["type"]}_{entity["id"]}'
    if entity["type"] == "ExecuteProcess":
        return f'{entity["type"]}_{entity["id"]}'
    return f'Unknown_{entity["type"]}_{entity["id"]}'


def get_component_style(entity: dict):
    if entity["type"] == "IncludeLaunchDescription":
        return "#LightGray"
    if entity["type"] == "GroupAction":
        return "#DarkGray;line:Black;"
    if entity["type"] == "ComposableNodeContainer":
        return "#DarkSeaGreen;line:Black;"
    if entity["type"] == "LoadComposableNodes":
        return "#GreenYellow;line:Black;"
    if entity["type"] == "ComposableNode":
        return "#LightSkyBlue;line:Black;"
    if entity["type"] == "Node":
        return "#DeepSkyBlue;line:Black;"
    if entity["type"] == "ExecuteProcess":
        return "#MediumSlateBlue;line:Black;"
    return "#Pink;line:Red;"


def create_entity_index_map(tree: dict):
    index_map = {}

    def update_index(tree):
        if tree.get("children"):
            index_map[str(tree["entity"])] = tree
            for subtree in tree["children"]:
                update_index(subtree)
        else:
            index_map[str(tree)] = tree

    update_index(tree)

    return index_map


def get_children(index_map: dict, entity: dict):
    index = index_map[str(entity)]
    if not index.get("children"):
        return []

    children = []
    for child in index["children"]:
        if child.get("children"):
            children.append(child["entity"])
        else:
            children.append(child)

    return children


def generate_plantuml(serializable_tree: dict):
    share = get_package_share_path("ros_component_diagram_generator")
    template_text = (share / "templates" / "launch_plantuml.jinja2").read_text()
    template = Template(template_text)

    entities = _get_all_entities(serializable_tree)
    for i, e in enumerate(entities):
        e["id"] = i

    index_map = create_entity_index_map(serializable_tree)

    return template.render(
        {
            "entities": entities,
            "index_map": index_map,
            "get_component_kind": get_component_kind,
            "get_component_id": get_component_id,
            "get_component_style": get_component_style,
            "get_children": get_children,
        }
    )
