import launch
import launch_ros
from rclpy.logging import get_logger

logger = get_logger("launch2json")


def _make_entity_serializable(entity: launch.LaunchDescriptionEntity):
    import re

    d = {}
    d["type"] = entity.__class__.__name__
    if type(entity) is launch.actions.IncludeLaunchDescription:
        package_name_pattern = r".*/(\w+)/share/.*"
        d["package"] = re.match(package_name_pattern, entity._get_launch_file_directory())[1]
        d["file_name"] = entity._get_launch_file().split("/")[-1]

    if type(entity) is launch.actions.GroupAction:
        d["scoped"] = entity._GroupAction__scoped
        d["forwarding"] = entity._GroupAction__forwarding

    if type(entity) is launch_ros.actions.ComposableNodeContainer:
        d["package"] = entity.node_package
        d["executable"] = entity.node_executable
        d["namespace"] = entity._Node__expanded_node_namespace.replace(
            launch_ros.actions.Node.UNSPECIFIED_NODE_NAMESPACE, "/"
        )
        d["name"] = entity._Node__expanded_node_name

    if type(entity) is launch_ros.actions.LoadComposableNodes:
        d["target_container"] = entity._LoadComposableNodes__final_target_container_name

    if type(entity) is launch_ros.descriptions.ComposableNode:
        d["package"] = entity.package
        d["plugin"] = entity.node_plugin
        d["namespace"] = entity.node_namespace
        d["name"] = entity.node_name

    if type(entity) is launch_ros.actions.Node:
        d["package"] = entity.node_package
        d["executable"] = entity.node_executable
        d["namespace"] = entity._Node__expanded_node_namespace.replace(
            launch_ros.actions.Node.UNSPECIFIED_NODE_NAMESPACE, "/"
        )
        d["name"] = entity._Node__expanded_node_name

    if type(entity) is launch.actions.ExecuteProcess:
        d["name"] = entity.name

    return d


def make_entity_tree_serializable(tree: dict | object, context: launch.LaunchContext):
    if not isinstance(tree, dict):
        return _make_entity_serializable(tree)

    d = {}
    d["entity"] = _make_entity_serializable(tree["entity"])
    if isinstance(tree["children"], list):
        d["children"] = [
            make_entity_tree_serializable(child, context) for child in tree["children"]
        ]

    return d
