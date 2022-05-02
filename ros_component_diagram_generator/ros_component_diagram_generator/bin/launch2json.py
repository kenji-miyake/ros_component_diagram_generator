from pathlib import Path

from rclpy.logging import get_logger

from ros_component_diagram_generator.filter import filter_entity_tree
from ros_component_diagram_generator.parser import create_entity_tree
from ros_component_diagram_generator.plantuml import generate_plantuml
from ros_component_diagram_generator.serialization import make_entity_tree_serializable

logger = get_logger("launch2json")


def _parse_args():
    import argparse

    import rclpy
    from rclpy.node import Node
    from rclpy.parameter import Parameter
    from ros2launch.command.launch import LaunchCommand

    rclpy.init()

    node = Node("launch2json")
    node.declare_parameter("launch_command", Parameter.Type.STRING)

    launch_command = node.get_parameter("launch_command")
    argv = launch_command.value.replace("ros2 launch ", "").split(" ")

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    LaunchCommand().add_arguments(parser, "ros2")

    rclpy.shutdown()

    return parser.parse_args(args=argv)


def _prepare(args):
    import launch
    from ros2launch.api.api import get_share_file_path_from_package
    from ros2launch.api.api import parse_launch_arguments

    launch_file_path = get_share_file_path_from_package(
        package_name=args.package_name, file_name=args.launch_file_name
    )

    parsed_launch_arguments = parse_launch_arguments(args.launch_arguments)

    root_entity = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.AnyLaunchDescriptionSource(launch_file_path),
        launch_arguments=parsed_launch_arguments,
    )

    launch_service = launch.LaunchService(
        argv=parsed_launch_arguments, noninteractive=args.noninteractive, debug=args.debug
    )

    return root_entity, launch_service


def main():
    import json

    args = _parse_args()
    root_entity, launch_service = _prepare(args)

    raw_tree = create_entity_tree(root_entity, launch_service)
    filtered_tree = filter_entity_tree(raw_tree.copy())
    serializable_tree = make_entity_tree_serializable(filtered_tree, launch_service.context)

    plantuml = generate_plantuml(serializable_tree)

    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "entity_tree.pu", "w") as f:
        f.write(plantuml)

    # tmp
    with open(output_dir / "entity_tree.json", "w") as f:
        json.dump(serializable_tree, f, indent=2)


if __name__ == "__main__":
    main()
