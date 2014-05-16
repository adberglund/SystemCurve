''' A script that (will) take CSV input for pipes and pipe fittings
    (e.g., elbows, tees, valves, meters) and generates a
    system curve to match against a pump curve. 
'''

import math

class Pipe:
    '''One of n-possible pipes in a network'''
    def __init__(self, ID, length, diameter, equivalent_roughness, Reynolds):
        '''Keyword Arguments:
        ID - pipe identifier
        length -- length of pipe segment
        diameter -- diameter of pipe
        equivalent_roughness -- a value associated with pipe material 
        Reynolds -- Reynolds number for the particular pipe/flow
        '''
        self.ID = ID
        self.length = length
        self.diameter = diameter
        self.equivalent_roughness = equivalent_roughness
        self.Reynolds = Reynolds                
        
class Fitting:
    '''Fitting class represents anything contributing
    to the minor losses in the pipe system.
    '''
    def __init__(self, ID, diameter, k_factor):
        '''Keyword Arguments:
        ID -- fitting identifier
        diameter -- diameter of associated pipe
        k_factor -- minor loss coefficient
        '''
        self.ID = ID
        self.diameter = diameter
        self.k_factor = k_factor
        
class Curve:            
    '''Iterator that establishes total head at various flow rates.'''    
    def __init__(self, pipes, fittings, max_flow_rate, flow_increment):
        '''Keyword Arguments:
        pipes -- list/set of pipes
        fittings -- list/set of fittings
        max_flow_rate -- last point to evaulate the system curve
        flow_increment -- number of units to increase to evaulate a new point
        '''
        self.pipes = pipes 
        self.fittings = fittings
        self.max_flow_rate = max_flow_rate
        self.flow_increment = flow_increment

    def __iter__(self):
        self.flow_rate = 0        
        return self

    def next(self):
        total_head = (self.flow_rate, self.calculate())
        self.flow_rate += self.flow_increment
        if self.flow_rate > self.max_flow_rate:
            raise StopIteration

        return total_head
        
    def calculate(self):        
        '''Calculates the friction loss and minor loss for all
        considered pipes and fittings.
        '''
        g = 32.2 #gravity
        total_friction_loss =0
        minor_loss = 0

        for pipe in self.pipes:
            area = math.pi * pipe.diameter**2 / 4
            velocity = self.flow_rate / area
            velocity_head = velocity**2 / (2 * g)
            for friction_factor in ColebrookEquation(pipe):
                friction_loss = friction_factor * pipe.length / \
                                pipe.diameter * velocity_head
        total_friction_loss += friction_loss

        for fitting in self.fittings:
            area = math.pi * fitting.diameter**2 / 4
            velocity = self.flow_rate / area
            minor_loss += fitting.k_factor * velocity_head

        return total_friction_loss + minor_loss

            
class ColebrookEquation:
    '''Iterator that estimates a friction factor for a particular pipe'''
    self.precision = 1e-4
    
    def __init__(self, pipe):
        self.pipe = pipe
        
    def __iter__(self):    
        self.friction_guess = 1
        return self
        
    def next(self):
        friction_factor = -2.0 * math.log((self.pipe.equivalent_roughness / \
                          self.pipe.diameter) / 3.7 + 2.51 / \
                          (self.pipe.Reynolds * math.sqrt(self.friction_guess)), 10)
        
        if friction_factor - self.friction_guess < self.precision:            
            raise StopIteration
            
        self.friction_guess = friction_factor
        return self.friction_guess

if __name__ == '__main__':
    pipes = [Pipe(1, 100, 10, 0.0005, 10e5)]
    fittings = [Fitting(1, 10, 2.5)]    
    for head in Curve(pipes, fittings, 100, 1):
        #print head                