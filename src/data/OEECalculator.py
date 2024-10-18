from data.Order import OrderTable
from data.Downtime import DowntimeTable

TOTAL_RUN_TIME_HOURS_IN_ONE_DAY = 8
PARTS_PRODUCED_PER_HOUR = 40

class OEECalculator:
    def calculate_oee(self):
        oee = self.calculate_availability() * self.calculate_performance() * self.calculate_quality()
        return oee
    
    def calculate_availability(self):
        actual_availability = self.total_run_time() - self.total_down_time()
        planned_production_time = self.total_run_time()
        availability = actual_availability / planned_production_time
        return availability
    
    def total_run_time(self):
        return TOTAL_RUN_TIME_HOURS_IN_ONE_DAY
    
    def total_down_time(self):
        #TODO: querty the downtime database to get the sum of all the downtime for the current day
        downtime_db = DowntimeTable()
        total_downtime = downtime_db.get_total_downtime_today()
        #convert the total_downtime to hours
        total_downtime = total_downtime.total_seconds() / 3600
        return total_downtime
    
    def calculate_performance(self):
        actual_part_producted = self.total_part_produced()
        max_possible_parts_produced = self.max_parts_produced()
        performance = actual_part_producted / max_possible_parts_produced
        return performance
    
    def max_parts_produced(self):
        return self.total_run_time() * PARTS_PRODUCED_PER_HOUR
    
    def total_part_produced(self):
        #TODO: querty the Order database to get the sum of all the parts produced for the current day
        order_db = OrderTable()
        total_parts_produced = order_db.get_total_parts_produced_today()
        return total_parts_produced
    
    def calculate_quality(self):
        good_parts_produced = self.total_good_parts_produced()
        total_parts_produced = self.total_part_produced()
        try:
            quality = good_parts_produced / total_parts_produced
        except:
            quality = 0
        return quality
    
    def total_good_parts_produced (self):
        #TODO: querty the Order database to get the sum of all the good parts produced for the current day
        order_db = OrderTable()
        total_good_parts_produced = order_db.get_total_good_parts_produced_today()
        return total_good_parts_produced
