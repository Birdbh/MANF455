
class ComsManager():
    def direct_communication(self, com_type, nodeId, new_value):
        #TODO: Need to ideat and define the other com_types and their respective functions, probably in a switch statement
        if com_type == 'Downtime':
            self.add_downtime_event(new_value)

    def add_downtime_event(new_value):
        #this will need to set a new downtime event in the database
        pass
    