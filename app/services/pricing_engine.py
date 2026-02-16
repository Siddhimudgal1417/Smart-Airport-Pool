class PricingEngine:

    def calculate(self, base_fare, distance_km, demand_ratio):
        surge = max(1, demand_ratio)
        pooling_discount = 0.2

        fare = (base_fare + distance_km * 10) * surge
        return fare * (1 - pooling_discount)
