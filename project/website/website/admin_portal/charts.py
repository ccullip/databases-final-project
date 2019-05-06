import pygal

class PieChart():
    def __init__(self, title, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = title

    def generate(self, data):
        # Add data to chart
        chart_data = data
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)

class HorizontalBarGraph():
    def __init__(self, title, **kwargs):
        self.chart = pygal.HorizontalBar(**kwargs)
        self.chart.title = title

    def generate(self, data):
        # Add data to chart
        chart_data = data
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
