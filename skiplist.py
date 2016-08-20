import random

class SkipList:
    def __init__(self):
        self.layers = [LayerList(None)]

    def __len__(self):
        return len(self.layers[0])

    def __iter__(self):
        for node in self.layers[0]:
            yield node

    def __repr__(self):
        return str(self.layers[0])

    # TODO: Prevent insertion of already present data
    def insert(self, data):
        """
        Inserts a SkipNode with the supplied data into the lowest layer. Then,
        recursively inserts that node into the next layer with probability 0.5.
        """
        prev = None
        tails = False
        layer_ind = 0

        while not tails:
            # If a layer does not not exist for the current insertion, create
            # it. Additionally, connect the prehead node for the new layer to
            # the prehead node of the layer directly below.
            if len(self.layers) - 1 < layer_ind:
                lower_prehead = self.layers[layer_ind - 1].prehead
                self.layers.append(LayerList(lower_prehead))
            current_layer = self.layers[layer_ind]

            # Set the reference to the previous layer
            inserted_node = current_layer.insert(data)
            inserted_node.down = prev

            prev = inserted_node
            layer_ind += 1
            tails = random.random() >= 0.5

    # FIXME: This is horrendously slow. layer.remove(data) takes O(n)
    def remove(self, data):
        """
        Remove the SkipNode with the supplied data from the SkipList. The node
        is removed from all layers.
        """
        for layer in self.layers:
            layer.remove(data)

    def __contains__(self, data):
        """
        Returns True if a SkipNode with the supplied data is in the SkipList
        and False otherwise.
        """
        if data is None:
            return False

        node = self.layers[-1].prehead
        while node is not None:
            if node.data == data:
                return True
            try:
                # If the data that we are looking for is greater than the data
                # at the current node, keep traversing the current layer.
                if data >= node.next.data:
                    node = node.next
                    continue
            except AttributeError:
                # If we try to go past the end of a layer, the value is larger
                # than anything in that layer.
                pass
            # If going to the next node in the layer would go 'past' the node
            # that we're looking for, go down a layer and repeat the process.
            node = node.down

        return False

class SkipNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.down = None

    def __repr__(self):
        return 'SkipNode({0})'.format(str(self.data))


# Pretty much a linked list that maintains sortedness. Prehead node exists
# because containment can't be checked without the ability to enter every layer
# at the beginning.
class LayerList:
    def __init__(self, lower_prehead):
        self.size = 0
        self.head = None
        self.prehead = SkipNode(None)
        self.prehead.next = self.head
        self.prehead.down = lower_prehead

    def __len__(self):
        """
        Returns the number of nodes currently in the LayerList.
        """
        return self.size

    def __iter__(self):
        """
        Iterates over every non-None node in the LayerList.
        """
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        """
        Pretty-prints a LayerList. 
        """
        s = '['
        for i, node in enumerate(self.__iter__()):
            s += str(node.data)
            if i < self.size - 1:
                s += ', '
        s += ']'

        return s

    def __contains__(self, data):
        """
        Returns True if the LayerList contains a SkipNode with the supplied data and
        False otherwise.
        """
        for node in self.__iter__():
            if node.data == data:
                return True

        return False
    
    def insert(self, data):
        """
        Inserts a new SkipNode with the supplied data as its data field. This method
        preserves sortedness of the LayerList
        """
        if self.size is 0 or self.head.data > data:
            # Base case where nothing precedes the node that we will be
            # inserting.
            self.prehead.next = SkipNode(data)
            self.prehead.next.next = self.head
            self.head = self.prehead.next
            node = self.head
        else:
            # Move pointer to the node that will be immediately before the
            # newly inserted node.
            node = self.head
            while node.next is not None and node.next.data < data:
                node = node.next

            # Our insertion will be in between this node and the next node, so
            # preserve the next node, connect the current node to a new node,
            # and that new node to the next node.
            old_next = node.next
            node.next = SkipNode(data)
            node.next.next = old_next
            node = node.next

        # Return a reference to the inserted node so down-pointers in SkipList
        # can be maintained.
        self.size += 1
        return node

    def remove(self, data):
        """
        If a SkipNode with the supplied data is in the LayerList, remove it.
        Otherwise, do nothing.
        """
        prev = self.prehead
        node = self.head
        while node is not None:
            if node.data == data:
                if node is self.head:
                    self.head = node.next
                prev.next = node.next
                self.size -= 1
                break
            prev = node
            node = node.next
