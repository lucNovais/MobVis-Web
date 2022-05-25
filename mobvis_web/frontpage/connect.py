from mobvis.preprocessing.parser import Parser as par

from mobvis.metrics.utils.Locations import Locations as loc
from mobvis.metrics.utils.HomeLocations import HomeLocations as hloc
from mobvis.metrics.utils.Contacts import Contacts as cnt

from mobvis.metrics.utils.MetricBuilder import MetricBuilder as mb

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *

NEED_LOCATIONS = [
    'TRVD',
    'RADG',
    'VISO',
    'AVSP',
    'TRVT',
    'VIST'
]

NEED_HOMES = [
    'RADG'
]

NEED_CONTACTS = [
    'INCO',
    'CODU'
]

def mobvis_connection(trace, configurations, metrics, plots):
    context = {}
    context['tables'] = []
    context['figures'] = []

    parsed_trace = par.parse(raw_trace=trace, is_ordered=True)

    if metrics:
        requirements = get_metrics_prerequirements(parsed_trace, metrics, configurations)
        metrics_data = {}
        for metric in metrics:
            metrics_data[metric] = build_and_extract_metric(metric=metric, req_dict=requirements)
        
            context['tables'].append(metrics_data[metric].head(10).to_html())

    if plots:
        figures = {}
        if metrics and 'statistical' in plots:
            for metric, data in metrics_data.items():
                figures[metric] = generate_statistical_plot(data, metric)
                context['figures'].append(figures[metric][0].to_html())
                context['figures'].append(figures[metric][1].to_html())
                context['figures'].append(figures[metric][2].to_html())
        else:
            print("ATTENTION: Can't generate statistical plots without any metric!")

    return context

def get_metrics_prerequirements(trace, metrics, configurations):
    requirements = {}

    dist_type = configurations[3]
    requirements['dist_type'] = dist_type

    if [metric for metric in metrics if metric in NEED_LOCATIONS]:
        max_d = float(configurations[0])
        pause_t = float(configurations[1])

        [trace_loc, sl_centers] = loc.find_locations(
            trace=trace,
            max_d=max_d,
            pause_threshold=pause_t,
            dist_type=dist_type
        )

        requirements['max_d'] = max_d
        requirements['pause_t'] = pause_t
        requirements['trace_loc'] = trace_loc
        requirements['loc_centers'] = sl_centers

        if [metric for metric in metrics if metric in NEED_HOMES]:
            requirements['trace'] = trace
            trace_homes = hloc.find_homes(trace_loc)
            requirements['homes'] = trace_homes

    if [metric for metric in metrics if metric in NEED_CONTACTS]:
        contact_r = float(configurations[2])

        contacts = cnt.detect_contacts(trace, contact_r, dist_type)

        requirements['contacts_df'] = contacts

    return requirements

def build_and_extract_metric(metric, req_dict):
    metric_data = mb.build_metric(metric, **req_dict).extract()

    return metric_data

def generate_statistical_plot(data, metric, configs=None):
    if not configs:
        configs = [
            False,
            len(data.id.unique()),
            True
        ]

    hist = plot_metric_histogram(
        metric_df=data,
        metric_name=metric,
        differ_nodes=configs[0],
        users_to_display=configs[1],
        show_y_label=configs[2]
    )

    box = boxplot_metric(
        metric_df=data,
        metric_name=metric,
        differ_nodes=configs[0],
        users_to_display=configs[1],
        show_y_label=configs[2]
    )

    dist = plot_metric_dist(
        metric_df=data,
        metric_name=metric,
        differ_nodes=configs[0],
        users_to_display=configs[1],
        show_y_label=configs[2]
    )

    return [hist, box, dist]
