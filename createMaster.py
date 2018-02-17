import xml.etree.cElementTree as ET
import sys

def getIndexString(number):
    if number == 0:
        return ""
    else:
        return str(number)

try:
    if len(sys.argv) < 2:
        raise ValueError("Need one argument for amount of vehicles.")

    launch = ET.Element("launch")
    ET.SubElement(launch, "arg", name="visual", default="true")
    ET.SubElement(launch, "arg", name="sim", default="true")
    ET.SubElement(launch, "arg", name="rpi", default="false")
    ET.SubElement(launch, "arg", name="obstacles", default="true")
    ET.SubElement(launch, "arg", name="path_planning", default="true")
    ET.SubElement(launch, "arg", name="auto_master", default="true")

    ET.SubElement(launch, "arg", name="hw_api", default="false")

    ET.SubElement(launch, "arg", name="gamepad", default="true")
    ET.SubElement(launch, "arg", name="gamepad_rate", default="50.0")
    ET.SubElement(launch, "arg", name="gamepad_type", default="xbox")
    ET.SubElement(launch, "arg", name="gamepad_input", default="/dev/input/js0")
    ET.SubElement(launch, "arg", name="gulliview", default="true")

    groupSim = ET.SubElement(launch, "group")
    groupSim.set("if", "$(arg sim)")
    for i in range(0, int(sys.argv[1])):
        ET.SubElement(groupSim, "node", name="sim" + getIndexString(i), pkg="truck_automatic_ctrl", type="sim.py")

    groupUSim = ET.SubElement(launch, "group", unless="$(arg sim)")
    gulliview_node = ET.SubElement(groupUSim, "node", name= "gulliview", pkg= "gulliview_server", type="gulliview")
    gulliview_node.set("if", "$(arg gulliview)")
    groupHW = ET.SubElement(groupUSim, "group")
    groupHW.set("if", "$(arg hw_api)")
    for i in range(0, int(sys.argv[1])):
        ET.SubElement(groupHW, "node", name="cmd_node" + getIndexString(i), pkg="truck_hw_api", type="cmd_node.py")
        ET.SubElement(groupHW, "node", name="trailersensor" + getIndexString(i), pkg="truck_hw_api", type="trailersensor.py")

    ET.SubElement(groupUSim, "node", name="master", pkg="truck_master", type="master.py")

    groupGPSim = ET.SubElement(groupUSim, "group")
    groupGPSim.set("if", "$(arg gamepad)")
    for i in range(0, int(sys.argv[1])):
        joy_node = ET.SubElement(groupGPSim, "node", name="joy_node" + getIndexString(i), pkg="joy", type="joy_node")
        ET.SubElement(joy_node, "param", name="autorepeat_rate" + getIndexString(i), type="double", value="$(arg gamepad_rate)")
        ET.SubElement(joy_node, "param", name="coalesce_rate" + getIndexString(i), type="double", value="$(eval 1.0 / arg('gamepad_rate'))")
        ET.SubElement(joy_node, "param", name="dev" + getIndexString(i), type="string", value="$(arg gamepad_input)")
        gamepad = ET.SubElement(groupGPSim, "node", name="gamepad" + getIndexString(i), pkg="truck_manual_ctrl", type="gamepad.py")
        ET.SubElement(gamepad, "param", name="rate"+ getIndexString(i), type="double", value="$(arg gamepad_rate)")
        ET.SubElement(gamepad, "param", name="type"+ getIndexString(i), type="string", value="$(arg gamepad_type)")

    groupVisual = ET.SubElement(launch, "group")
    groupVisual.set("if", "$(arg visual)")
    ET.SubElement(groupVisual, "node", name= "visualization", pkg= "truck_visualization", type="visualization.py")
    ET.SubElement(groupVisual, "node", name="rviz", pkg="rviz", type="rviz", args="-d $(find truck_visualization)/config.rviz")
    for i in range(0, int(sys.argv[1])):
        node_path_planning = ET.SubElement(launch, "node", name="path_planning" + getIndexString(i), pkg= "path_planning", type="path_planning_node.py")
        node_path_planning.set("if", "$(arg path_planning)")
        ET.SubElement(node_path_planning, "param", name="rpi" + getIndexString(i), type="boolean", value="$(arg rpi)")

        node_auto_master = ET.SubElement(launch, "node", name= "auto_master" + getIndexString(i), pkg= "truck_automatic_ctrl", type="auto_master.py")
        node_auto_master.set("if", "$(arg auto_master)")
        ET.SubElement(node_auto_master, "param", name="sim"+getIndexString(i), type="boolean", value="$(arg sim)")

    obstacle_node = ET.SubElement(launch, "node", name="obstacle_node", pkg="truck_map", type="obstacle_node.py")
    obstacle_node.set("if", "$(arg obstacles)")

    tree = ET.ElementTree(launch)
    tree.write("master.launch")
except ValueError as e:
    print str(e)
