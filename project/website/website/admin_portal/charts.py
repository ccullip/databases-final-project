import pygal

class PieChart():
    def __init__(self, title, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = title

    def generate(self):
        # Add data to chart
        chart_data = {'apples': 9, 'oranges': 21, 'pears': 50}
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
