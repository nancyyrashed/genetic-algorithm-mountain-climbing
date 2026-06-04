# In creature.py
import genome 
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np
import math

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor:
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
            self.motor_type = MotorType.SINE
        self.amp = control_amp
        self.freq = control_freq
        #self.amp = 5
        #self.freq = 5
        self.phase = 0

    def get_output(self):
        self.phase = (self.phase + self.freq) % (np.pi * 2)
        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = self.amp
            else:
                output = -self.amp
        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)
        return output 
    
class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.beginning_location = None
        self.final_location = None
        self.locations = []
        self.prior_proximity_to_the_origin = None
        self.score_for_fitness = 0

    def get_flat_links(self):
        if self.flat_links == None:
            gdicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        self.get_flat_links()
        if self.exp_links is not None:
            return self.exp_links
        
        exp_links = [self.flat_links[0]]
        genome.Genome.expandLinks(self.flat_links[0], 
                                self.flat_links[0].name, 
                                self.flat_links, 
                                exp_links)
        self.exp_links = exp_links
        return self.exp_links

    def to_xml(self):
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_element(adom))
        first = True
        for link in self.exp_links:
            if first:# skip the root node! 
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))
        robot_tag.setAttribute("name", "pepe") #  choose a name!
        return '<?xml version="1.0"?>' + robot_tag.toprettyxml()

    def get_motors(self):
        self.get_expanded_links()
        if self.motors == None:
            motors = []
            for i in range(1, len(self.exp_links)):
                l = self.exp_links[i]
                m = Motor(l.control_waveform, l.control_amp,  l.control_freq)
                motors.append(m)
            self.motors = motors 
        return self.motors 

    def update_position(self, loc):
        if self.beginning_location is None:
            self.beginning_location = loc
        else:
            self.final_location = loc
        self.locations.append(loc)  # fixed: always append to self.locations

        current_proximity_to_origin = self.attain_current_proximity_to_origin()
        if self.prior_proximity_to_the_origin is not None:
            # Reward getting closer
            if current_proximity_to_origin < self.prior_proximity_to_the_origin:
                self.score_for_fitness += 1
            else:
                self.score_for_fitness -= 0.5  # mild penalty for drifting away
        self.prior_proximity_to_the_origin = current_proximity_to_origin

    def attain_distance_travelled(self):
        if self.beginning_location is None or self.final_location is None:
            return 0
        p1 = np.asarray(self.beginning_location)
        p2 = np.asarray(self.final_location)
        dist = np.linalg.norm(p1-p2)
        return dist 

    def attain_the_reached_altitude(self):
        if self.locations:
            altitudes = [loc[2] for loc in self.locations]
            return max(altitudes)
        return 0

    # Calculate the consistency based on the variations from the initial location
    def attain_consistency(self):
        # If there are fewer than 2 locations, consistency is undefined
        if len(self.locations) < 2:
            return 0
        
        # Calculate the variations in the x and y directions for all locations
        variations = []
        for loc in self.locations:
            delta_x = loc[0] - self.beginning_location[0]
            delta_y = loc[1] - self.beginning_location[1]
            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
            variations.append(distance)

        # Return consistency as the reciprocal of the fluctuations of these variations
        consistency = 1 / (1 + np.var(variations))  
        return consistency

    def attain_current_proximity_to_origin(self):
        if not self.locations:
            return float('inf') 
        final_location = self.locations[-1]
        center_origin = np.array([0, 0, 0]) 
        return np.linalg.norm(np.array(final_location) - center_origin)

    def attain_fitness_score(self):
        if not self.locations or len(self.locations) < 2:
            return -1e6  # big penalty for not moving

        start_x, start_y, _ = self.locations[0]
        end_x, end_y, end_z = self.locations[-1]

        start_dist = np.linalg.norm([start_x, start_y])
        end_dist = np.linalg.norm([end_x, end_y])

        # Reward net progress toward the center
        progress_reward = (start_dist - end_dist) * 1000  # Strong incentive to reduce distance
        progress_reward = max(progress_reward, 0)  # Don't reward moving away

        # Extra reward for being very close to center
        proximity_bonus = 0
        if end_dist < 2.0:
            proximity_bonus = 1000 / (end_dist + 0.1)

        # Reward climbing if close to center
        altitude_reward = 0
        if end_dist < 6:
            altitude_reward = max(0, end_z) * 500

        # Slight reward for total distance moved to encourage exploration
        movement_reward = self.attain_distance_travelled() * 10

        return progress_reward + proximity_bonus + altitude_reward + movement_reward



    def clear_position_data(self):
        self.beginning_location = None
        self.final_location = None
        self.locations = []
        self.prior_proximity_to_the_origin = None
        self.score_for_fitness = 0

    def update_dna(self, dna):
        self.dna = dna
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.beginning_location = None
        self.final_location = None
        self.locations = []
        self.prior_proximity_to_the_origin = None
        self.score_for_fitness = 0