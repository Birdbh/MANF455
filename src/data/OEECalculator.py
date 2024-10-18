from data.Order import OrderTable
from data.Downtime import DowntimeTable
import pandas as pd

TOTAL_RUN_TIME_HOURS_IN_ONE_DAY = 8
PARTS_PRODUCED_PER_HOUR = 40

class OEECalculator:
    def get_past_week_of_oee(self):
        dates_from_past_week = pd.date_range(end=pd.Timestamp.today(), periods=7).date
        oee_from_past_week = []

        print(dates_from_past_week)
        for date in dates_from_past_week:
            oee = self.calculate_oee(date)
            oee_from_past_week.append(oee)

        return dates_from_past_week, oee_from_past_week

    def calculate_oee(self, date):
        oee = self.calculate_availability(date) * self.calculate_performance(date) * self.calculate_quality(date)
        return oee
    
    def calculate_availability(self, date):
        actual_availability = self.total_run_time(date) - self.total_down_time(date)
        planned_production_time = self.total_run_time(date)
        availability = actual_availability / planned_production_time
        return availability
    
    def total_run_time(self, date):
        return TOTAL_RUN_TIME_HOURS_IN_ONE_DAY
    
    def total_down_time(self, date):
        #TODO: querty the downtime database to get the sum of all the downtime for the current day
        downtime_db = DowntimeTable()
        total_downtime = downtime_db.get_total_downtime_for_date(date)
        #convert the total_downtime to hours
        total_downtime = total_downtime.total_seconds() / 3600
        return total_downtime
    
    def calculate_performance(self, date):
        actual_part_producted = self.total_part_produced(date)
        max_possible_parts_produced = self.max_parts_produced(date)
        performance = actual_part_producted / max_possible_parts_produced
        return performance
    
    def max_parts_produced(self, date):
        return self.total_run_time(date) * PARTS_PRODUCED_PER_HOUR
    
    def total_part_produced(self, date):
        #TODO: querty the Order database to get the sum of all the parts produced for the current day
        order_db = OrderTable()
        total_parts_produced = order_db.get_total_parts_produced_for_date(date)
        return total_parts_produced
    
    def calculate_quality(self, date):
        good_parts_produced = self.total_good_parts_produced(date)
        total_parts_produced = self.total_part_produced(date)
        try:
            quality = good_parts_produced / total_parts_produced
        except:
            quality = 0
        return quality
    
    def total_good_parts_produced(self, date):
        #TODO: querty the Order database to get the sum of all the good parts produced for the current day
        order_db = OrderTable()
        total_good_parts_produced = order_db.get_total_good_parts_produced_today(date)
        return total_good_parts_produced
