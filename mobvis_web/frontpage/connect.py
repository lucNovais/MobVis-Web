from mobvis.preprocessing.parser import Parser as par

from mobvis.metrics.utils.Locations import Locations as loc
from mobvis.metrics.utils.HomeLocations import HomeLocations as hloc
from mobvis.metrics.utils.Contacts import Contacts as cnt

from mobvis.metrics.utils.MetricBuilder import MetricBuilder as mb

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *

def mobvis_connection(trace, configurations, metrics, plots):
    context = {}
    context['tables'] = []
    context['figures'] = []

    parsed_trace = par.parse(raw_trace=trace, is_ordered=True)

    # TODO: Redo all of these procedures with more elegance

    [trace_loc, loc_centers] = loc.find_locations(
        trace=parsed_trace,
        max_d=float(configurations[0]),
        pause_threshold=float(configurations[1]),
        dist_type=configurations[3]
    )

    trace_homes = hloc.find_homes(trace_loc=trace_loc)

    for metric in metrics:
        if metric == 'TRVD':
            trvd = mb.build_metric('TRVD', trace_loc=trace_loc, dist_type=configurations[3]).extract()
            context['tables'].append(trvd.head(10).to_html(classes='tables_content', index=False))

            if 'statistical' in plots:
                fig = plot_metric_histogram(
                    trvd,
                    metric_name=metric,
                    differ_nodes=False,
                    show_title=True,
                    show_y_label=True,
                    nbins=30
                )
                context['figures'].append(fig.to_html())

        if metric == 'RADG':
            radg = mb.build_metric('RADG', trace=parsed_trace, trace_loc=trace_loc, sl_centers=loc_centers, homes=trace_homes, dist_type=configurations[3]).extract()
            context['tables'].append(radg.head(10).to_html(classes='tables_content', index=False))

            if 'statistical' in plots:
                fig = plot_metric_histogram(
                    radg,
                    metric_name=metric,
                    differ_nodes=False,
                    show_title=True,
                    show_y_label=True,
                    nbins=30
                )
                context['figures'].append(fig.to_html())

        if metric == 'TRVT':
            trvt = mb.build_metric('TRVT', trace_loc=trace_loc).extract()
            context['tables'].append(trvt.head(10).to_html(classes='tables_content', index=False))

            if 'statistical' in plots:
                fig = plot_metric_histogram(
                    trvt,
                    metric_name=metric,
                    differ_nodes=False,
                    show_title=True,
                    show_y_label=True,
                    nbins=30
                )
                context['figures'].append(fig.to_html())

        if metric == 'VIST':
            vist = mb.build_metric('VIST', trace_loc=trace_loc).extract()
            context['tables'].append(vist.head(10).to_html(classes='tables_content', index=False))

            if 'statistical' in plots:
                fig = plot_metric_histogram(
                    vist,
                    metric_name=metric,
                    differ_nodes=False,
                    show_title=True,
                    show_y_label=True,
                    nbins=30
                )
                context['figures'].append(fig.to_html())

        if metric == 'VISO':
            viso = mb.build_metric('VISO', trace_loc=trace_loc).extract()
            context['tables'].append(viso.head(10).to_html(classes='tables_content', index=False))

            fig = plot_visit_order(
                trace_viso=viso,
                specific_users=[2]
            )
            context['figures'].append(fig.to_html())

        if metric == 'INCO':
            pass

    return context
