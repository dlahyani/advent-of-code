from dataclasses import dataclass, field
from regex import match
from typing import Dict, Iterable, Optional, Set


@dataclass
class Node:
    # Key of this node.
    color_name: str

    # Directed edges of from this node to other nodes.
    # There are 2 relations that connects a node to another:
    # 1. Contains relation - Colors contained by this node. These edges are weighted.
    # 2. Contained by relation - Colors that contain this node.
    contained_colors: Optional[Dict[str, int]] = None
    contained_by_colors: Set[str] = field(default_factory=set)

    @property
    def total_contained_bags(self):
        """
        Returns the total number of bags directly contained in this bag
        """
        return sum(self.contained_colors.values()) if self.contained_colors else 0

    @staticmethod
    def from_rule_str(rule_str: str) -> 'Node':
        EMPTY_BAG_PATTERN = "^(\w+ \w+) bags contain no other bags\.$"
        NON_EMPTY_BAG_PATTERN = (
            "^(\w+ \w+) bags contain ((\d+) (\w+ \w+) bags?, )*((\d+) (\w+ \w+) bags?\.)$"
        )
        
        # Assuming either one this would match.
        m = match(EMPTY_BAG_PATTERN, rule_str) or match(NON_EMPTY_BAG_PATTERN, rule_str)

        groups = m.groups()
        color_name = groups[0]
        contained_colors = None
        if m.re.pattern == NON_EMPTY_BAG_PATTERN:
            contained_colors = {
                color: int(count) for color, count in zip(m.captures(4), m.captures(3))
            }
            contained_colors[groups[6]] = int(groups[5])
        
        return Node(color_name=color_name, contained_colors=contained_colors)


@dataclass
class Graph:
    """
    A directed graph representing bag colors containment rules. Each node in the graph represents
    a bag-color and it has 2 sets of directed edges connecting it to other bag-colors (nodes).
        1. Contained colors - Set of outgoing edges connecting the node to bag-colors that are 
           contained by the bag-color the node represents. These edges are weighted, the edge weight
           represents the number of bags of the specified color contained by the node's bag color.
        2. Contained by colors - Set of incoming edges connecting the nodes to bag-colors that 
           contain at least one bag of the color the node represents.
    """

    nodes: Dict[str, Node] = field(default_factory=dict)

    def __post_init__(self):
        self._update_contained_by_relations()

    def _update_contained_by_relations(self):
        for color, node in self.nodes.items():
            if node.contained_colors:
                for contained_color in node.contained_colors:
                    self.nodes[contained_color].contained_by_colors.add(color)

    def get_colors_containing_color(self, color: str) -> Set[str]:
        """
        Find all bag-colors that contain, directly or indirectly, a bag of the given `color`.
        Assuming no circles in the graph the run-time complexity is O(V*E)
        """
        node = self.nodes[color]        
        containing_colors = set(node.contained_by_colors)
        for color in node.contained_by_colors:
            containing_colors.update(self.get_colors_containing_color(color))

        return containing_colors

    def get_total_bag_count_for_color(self, color: str) -> int:
        """
        Count the number of bags that are, directly or indirectly, contained in a bag of the given
        `color`.
        """
        node = self.nodes[color]
        if not node.contained_colors:
            return 0

        total_bags_required = node.total_contained_bags
        for color, count in node.contained_colors.items():
            total_bags_required += self.get_total_bag_count_for_color(color) * count

        return total_bags_required        

    @staticmethod
    def from_rules(rules: Iterable[str]) -> 'Graph':
        """
        Builds a graph from string rules. Run-time complexity O(V*E).
        """
        nodes = [Node.from_rule_str(rule_str) for rule_str in rules]
        return Graph({node.color_name: node for node in nodes})


if __name__ == "__main__":
    graph = Graph.from_rules(open("2020/07/input.txt", "r").readlines())

    # Part 1
    containing_colors = graph.get_colors_containing_color("shiny gold")
    print(f"Number of bag-colors that contain at least one shiny gold bag: {len(containing_colors)}")

    # Part 2
    total_bags_required = graph.get_total_bag_count_for_color("shiny gold")
    print(f"Individual bags required inside a single shiny gold bag: {total_bags_required}")
