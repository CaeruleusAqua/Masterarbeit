import json

from objects import *


class JsonHandler():
    def __init__(self):
        pass

    def lane_2_dict(self, lane):
        obj = dict()
        obj['points'] = lane.points
        obj['anchor'] = lane.anchor.id
        nodes = [node.id for node in lane.nodes]
        obj['nodes'] = nodes
        return obj

    def node_2_dict(self, node):
        obj = dict()
        obj['pos'] = node.pos
        lanes = [lane.id for lane in node.lanes]
        obj['lanes'] = lanes
        return obj

    def serialize(self, graph):
        obj = dict()
        nodes = dict()
        lanes = dict()
        nodes = {node.id: self.node_2_dict(node) for node in graph.nodes}
        lanes = {lane.id: self.lane_2_dict(lane) for lane in graph.lanes}
        obj['lane_counter'] = graph.lane_counter
        obj['node_counter'] = graph.node_counter
        obj['nodes'] = nodes
        obj['lanes'] = lanes
        return json.dumps(obj, indent=2, ensure_ascii=True)

    def deserialize(self, obj):
        obj = json.loads(obj)
        nodes = obj['nodes']
        lanes = obj['lanes']
        node_dict = dict()
        lane_dict = dict()
        for key, value in nodes.iteritems():
            node = Node(value['pos'])
            node.id = int(key)
            node.lanes = value['lanes']
            node_dict[int(key)] = node

        for key, value in lanes.iteritems():
            lane = Lane()
            lane.id = int(key)
            lane.points = value['points']
            lane.anchor = node_dict[value['anchor']]
            lane.nodes = [node_dict[id] for id in value['nodes']]
            lane_dict[int(key)] = lane

        for key, value in node_dict.iteritems():
            value.lanes = [lane_dict[id] for id in value.lanes]

        graph = Graph()
        graph.lanes = [x for x in lane_dict.itervalues()]
        graph.nodes = [x for x in node_dict.itervalues()]
        graph.lane_counter = obj['lane_counter']
        graph.node_counter = obj['node_counter']
        return graph
