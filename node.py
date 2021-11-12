from collections import deque
import uuid

class Node:
    
    def __repr__(self):
        return str(self.id)
    
    def __eq__(self, o):
        return self.id == o.id
    
    def __init__(self, node_id, prop_speed, distance_from_adjacents=1000):
        self.id = node_id
        self.distance_from_adjacents = distance_from_adjacents
        self.prop_speed = prop_speed

        self.q = deque()
        self.left_node = None
        self.right_node = None
        self.num_collisions = 0
        self.prop_delay_lookup = {}
    
    def empty(self):
        # return self.q.count == 0
        return len(self.q) == 0
    
    def add_packet(self, packet):
        self.q.append(packet)
        
    def dequeue_packet(self):
        return self.q.popleft()
    
    def requeue_packet(self, packet):
        self.q.appendleft(packet)
    
    def apply_wait_to_packets(self, wait_time, override_arrival_time=None):
        collided_packet = self.q[0]
        collided_packet.arrival_time += wait_time
        if override_arrival_time:
                collided_packet.arrival_time = override_arrival_time + wait_time
        new_arrival_time = collided_packet.arrival_time 
        for i in range(1, len(self.q)):
            if self.q[i].arrival_time < new_arrival_time:
                self.q[i].arrival_time = new_arrival_time
    
    def init_prop_delay_lookup(self, left, right, level=1):
        if not left and not right:
            return
        if left:
            self.prop_delay_lookup[left.id] = self.distance_from_adjacents * level / self.prop_speed
        if right:
            self.prop_delay_lookup[right.id] = self.distance_from_adjacents * level / self.prop_speed
        next_left = None if not left else left.left_node
        next_right = None if not right else right.right_node
        self.init_prop_delay_lookup(next_left, next_right, level + 1)
    
        