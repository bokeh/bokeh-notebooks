from collections import OrderedDict
import pandas as pd
import numpy as np

from jinja2 import Template

from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource, Plot, Circle, Range1d,
    LinearAxis, HoverTool, Text,
    SingleIntervalTicker, Slider, CustomJS
)
from bokeh.palettes import Spectral6
from bokeh.plotting import vplot
from bokeh.resources import CDN
from bokeh.templates import JS_RESOURCES


def _process_gapminder_data():
    from bokeh.sampledata.gapminder import fertility, life_expectancy, population, regions

    # Make the column names ints not strings for handling
    columns = list(fertility.columns)
    years = list(range(int(columns[0]), int(columns[-1])))
    rename_dict = dict(zip(columns, years))

    fertility = fertility.rename(columns=rename_dict)
    life_expectancy = life_expectancy.rename(columns=rename_dict)
    population = population.rename(columns=rename_dict)
    regions = regions.rename(columns=rename_dict)

    # Turn population into bubble sizes. Use min_size and factor to tweak.
    scale_factor = 200
    population_size = np.sqrt(population / np.pi) / scale_factor
    min_size = 3
    population_size = population_size.where(population_size >= min_size).fillna(min_size)

    # Use pandas categories and categorize & color the regions
    regions.Group = regions.Group.astype('category')
    regions_list = list(regions.Group.cat.categories)

    def get_color(r):
        return Spectral6[regions_list.index(r.Group)]
    regions['region_color'] = regions.apply(get_color, axis=1)

    return fertility, life_expectancy, population_size, regions, years, regions_list


def get_gapminder_plot():
    fertility_df, life_expectancy_df, population_df_size, regions_df, years, regions = _process_gapminder_data()

    sources = {}

    region_color = regions_df['region_color']
    region_color.name = 'region_color'

    for year in years:
        fertility = fertility_df[year]
        fertility.name = 'fertility'
        life = life_expectancy_df[year]
        life.name = 'life'
        population = population_df_size[year]
        population.name = 'population'
        new_df = pd.concat([fertility, life, population, region_color], axis=1)
        sources['_' + str(year)] = ColumnDataSource(new_df)

    dictionary_of_sources = dict(zip([x for x in years], ['_%s' % x for x in years]))
    js_source_array = str(dictionary_of_sources).replace("'", "")

    xdr = Range1d(1, 9)
    ydr = Range1d(20, 100)
    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=800,
        plot_height=400,
        outline_line_color=None,
        toolbar_location=None,
        responsive=True,
    )
    AXIS_FORMATS = dict(
        minor_tick_in=None,
        minor_tick_out=None,
        major_tick_in=None,
        major_label_text_font_size="10pt",
        major_label_text_font_style="normal",
        axis_label_text_font_size="10pt",

        axis_line_color='#AAAAAA',
        major_tick_line_color='#AAAAAA',
        major_label_text_color='#666666',

        major_tick_line_cap="round",
        axis_line_cap="round",
        axis_line_width=1,
        major_tick_line_width=1,
    )

    xaxis = LinearAxis(SingleIntervalTicker(interval=1), axis_label="Children per woman (total fertility)", **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=20), axis_label="Life expectancy at birth (years)", **AXIS_FORMATS)
    plot.add_layout(xaxis, 'below')
    plot.add_layout(yaxis, 'left')

    # ### Add the background year text
    # We add this first so it is below all the other glyphs
    text_source = ColumnDataSource({'year': ['%s' % years[0]]})
    text = Text(x=2, y=35, text='year', text_font_size='150pt', text_color='#EEEEEE')
    plot.add_glyph(text_source, text)

    # Add the circle
    renderer_source = sources['_%s' % years[0]]
    circle_glyph = Circle(
        x='fertility', y='life', size='population',
        fill_color='region_color', fill_alpha=0.8,
        line_color='#7c7e71', line_width=0.5, line_alpha=0.5)
    circle_renderer = plot.add_glyph(renderer_source, circle_glyph)

    # Add the hover (only against the circle and not other plot elements)
    tooltips = "@index"
    plot.add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))

    # Add the legend
    text_x = 7
    text_y = 95
    for i, region in enumerate(regions):
        plot.add_glyph(Text(x=text_x, y=text_y, text=[region], text_font_size='10pt', text_color='#666666'))
        plot.add_glyph(Circle(x=text_x - 0.1, y=text_y + 2, fill_color=Spectral6[i], size=10, line_color=None, fill_alpha=0.8))
        text_y = text_y - 5

    # Add the slider
    code = """
        var year = slider.get('value'),
            sources = %s,
            new_source_data = sources[year].get('data');
        renderer_source.set('data', new_source_data);
        text_source.set('data', {'year': [String(year)]});
    """ % js_source_array

    callback = CustomJS(args=sources, code=code)
    slider = Slider(start=years[0], end=years[-1], value=1, step=1, title="Year", callback=callback, name='testy')
    callback.args["renderer_source"] = renderer_source
    callback.args["slider"] = slider
    callback.args["text_source"] = text_source

    # Lay it out
    return vplot(plot, slider)


def get_gapminder_html():
    layout = get_gapminder_plot()
    with open('assets/gapminder_template.jinja', 'r') as f:
        template = Template(f.read())
    script, div = components(layout)
    html = template.render(
        title="Bokeh - Gapminder demo",
        bokeh_js=JS_RESOURCES.render(js_raw=CDN.js_raw, js_files=CDN.js_files),
        plot_script=script,
        plot_div=div,
    )
    return html


def get_gapminder_1964_data():
    fertility_df, life_expectancy_df, population_df_size, regions_df, years, regions = _process_gapminder_data()
    year = 1964
    region_color = regions_df['region_color']
    region_color.name = 'region_color'
    fertility = fertility_df[year]
    fertility.name = 'fertility'
    life = life_expectancy_df[year]
    life.name = 'life'
    population = population_df_size[year]
    population.name = 'population'
    new_df = pd.concat([fertility, life, population, region_color], axis=1)
    return new_df


def get_gapminder_1964_scatter_data():
    fertility_df, life_expectancy_df, population_df_size, regions_df, years, regions = _process_gapminder_data()
    xyvalues = OrderedDict()
    xyvalues['1964'] = list(
        zip(
            fertility_df[1964].dropna().values,
            life_expectancy_df[1964].dropna().values
        )
    )
    return xyvalues


def get_medal_data():
    from bokeh.sampledata.olympics2014 import data as olympics2014

    data = []
    for item in olympics2014['data']:
        if item['medals']['total'] == 0:
            # Don't use countries with no medals
            continue
        new_item = {}
        new_item['country'] = item['abbr']
        new_item['name'] = item['name']
        new_item['medals'] = [
            {'medal': 'bronze', 'count': item['medals']['bronze']},
            {'medal': 'silver', 'count': item['medals']['silver']},
            {'medal': 'gold', 'count': item['medals']['gold']}
        ]
        data.append(new_item)
    medals = pd.io.json.json_normalize(data, 'medals', ['name', 'country'])
    return medals

def get_custom_hover():
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.models import HoverTool

    source = ColumnDataSource(
            data=dict(
                x=[1, 2, 3, 4, 5],
                y=[2, 5, 8, 2, 7],
                desc=['A', 'b', 'C', 'd', 'E'],
                imgs = [
                    'http://bokeh.pydata.org/static/snake.jpg',
                    'http://bokeh.pydata.org/static/snake2.png',
                    'http://bokeh.pydata.org/static/snake3D.png',
                    'http://bokeh.pydata.org/static/snake4_TheRevenge.png',
                    'http://bokeh.pydata.org/static/snakebite.jpg'
                ]
            )
        )

    hover = HoverTool(
            tooltips="""
            <div>
                <div>
                    <img
                        src="@imgs" height="42" alt="@imgs" width="42"
                        style="float: left; margin: 0px 15px 15px 0px;"
                        border="2"
                    ></img>
                </div>
                <div>
                    <span style="font-size: 17px; font-weight: bold;">@desc</span>
                    <span style="font-size: 15px; color: #966;">[$index]</span>
                </div>
                <div>
                    <span style="font-size: 15px;">Location</span>
                    <span style="font-size: 10px; color: #696;">($x, $y)</span>
                </div>
            </div>
            """
        )

    p = figure(plot_width=300, plot_height=300, tools=[hover],
            title="Mouse over the dots")

    p.circle('x', 'y', size=20, source=source)
    return p
