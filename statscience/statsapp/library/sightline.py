from statsapp.library.database import database
from scipy.stats import linregress
import math  # Oh good, my nightmares in a python package :3


class Sightline:
    """
    Sightline is an engine designed for calculating the current condition of a stat, its future condition,
    and what you need to do to improve the condition of the statistic by using mathematics.
    """
    def __init__(self, statistic_name: str):
        self.stat_name = statistic_name
        self.stat_data = database.fetch_statistic_data(statistic_name)
        self.stat_details = database.fetch_statistic_details(statistic_name)

    valid_trends = ['up', 'down', 'level']
    valid_conditions = [
        'non-existence',
        'non-existence-NPF',  # See ./docs/nonexistence.md for more data.
        'danger',
        'emergency',
        'normal',
        'affluence',
        'power'  # TODO: Research condition of Power. Find out what it is and how to identify it.
    ]

    @staticmethod
    def get_data_average(data: list[int]) -> float:
        """
        From a set of numbers, calculates the average.
        """
        if not data:
            raise ValueError("Empty data list.")
        return sum(data) / len(data)

    def find_stat_direction(self, min_points: int = None, threshold: float = 0.05, log_history=True) -> tuple[str, float]:
        """
        Uses linear regression to determine if a statistic is trending 'up', 'down', or is 'level'.
        Also returns a numeric indicator of trend strength: 0.5 is level, >0.5 is up, <0.5 is down.

        Automatically chooses minimum required data points based on the statistic's type.

        :param min_points: Override for a minimum number of points. If None, it's set based on the stat type.
        :param threshold: Minimum slope relative to average value to be considered a real trend.
        :param log_history: Whether to log the trend history in the database.
        :return: Tuple ('up' | 'down' | 'level', strength: float)
        """
        data = self.stat_data['data']['values']
        stat_type = self.stat_details.get('type', 'unknown').lower()

        # Automatically assign min_points based on the stat type, if not explicitly provided
        if min_points is None:
            if stat_type == 'daily':
                min_points = 4
            elif stat_type == 'weekly':
                min_points = 2
            else:
                min_points = 2  # fallback default

        if len(data) < min_points:
            return 'Insufficient Data', -1

        x = list(range(len(data)))
        y = data

        slope, intercept, r_value, p_value, std_err = linregress(x, y)

        avg_y = self.get_data_average(y)
        epsilon = 1e-9

        if abs(avg_y) < epsilon:
            return 'level', 0.5

        normalized_slope = slope / abs(avg_y)

        slope_strength = math.tanh(normalized_slope * 10)
        strength_indicator = 0.5 + 0.5 * slope_strength

        if normalized_slope > threshold:
            trend = 'up'
        elif normalized_slope < -threshold:
            trend = 'down'
        else:
            trend = 'level'
            strength_indicator = 0.5

        if log_history:
            database.log_trend_history(self.stat_name, trend)

        return trend, round(strength_indicator, 5)

    def find_stat_condition(self):
        trend, trend_strength = self.find_stat_direction()
        if trend not in self.valid_trends:
            return "N/A"

        # TODO: Expand this. Identifying conditions is more intricate than this
        if trend == 'up':
            if trend_strength > 0.8:
                condition = 'affluence'
            else: # Trend strength must be >0.5 to be 'up'. All 'normal' requires is a SLIGHT up.
                condition = 'normal'
        elif trend == 'down':
            if trend_strength <= 0.3:
                condition = 'danger'
            elif trend_strength <= 0.4:
                condition = 'emergency'
            else:
                # Not <=0.4. Likely normal
                condition = 'normal'
        elif trend == 'level':
            if 0.4 <= trend_strength <= 0.5:
                condition = 'emergency'
            elif trend_strength == 0.0:
                condition = 'Non-Existence'
            else:
                condition = 'emergency'
        else:
            raise ValueError(f"Invalid trend: {trend}")

        return condition