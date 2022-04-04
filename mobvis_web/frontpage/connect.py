from mobvis.preprocessing.parser import Parser as par

from mobvis.metrics.utils.Locations import Locations as loc
from mobvis.metrics.utils.HomeLocations import HomeLocations as hloc
from mobvis.metrics.utils.Contacts import Contacts as cnt

from mobvis.metrics.utils.MetricBuilder import MetricBuilder as mb

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *

def mobvis_connection(trace, configurations, metrics, plots):
    context = {}

    parsed_trace = par.parse(raw_trace=trace, raw_trace_cols=['timestamp', 'id', 'x', 'y'], is_ordered=True)

    [trace_loc, loc_centers] = loc.find_locations(trace=parsed_trace, max_d=0.014, pause_threshold=10, dist_type="euclidean")
    trace_homes = hloc.find_homes(trace_loc=trace_loc)
    trace_contacts = cnt.detect_contacts(df=parsed_trace, radius=0.13, dist_type="euclidean")

    trace_trvd = mb.build_metric('TRVD', trace_loc=trace_loc, dist_type="Euclidean").extract()
    trace_radg = mb.build_metric('RADG', trace=parsed_trace, trace_loc=trace_loc, sl_centers=loc_centers, homes=trace_homes, dist_type="Euclidean").extract()
    trace_viso = mb.build_metric('VISO', trace_loc=trace_loc).extract()
    trace_vist = mb.build_metric('VIST', trace_loc=trace_loc).extract()
    trace_trvt = mb.build_metric('TRVT', trace_loc=trace_loc).extract()
    trace_inco = mb.build_metric('INCO', contacts_df=trace_contacts).extract()

    context['tables'] = []

    context['tables'].append(trace_trvd.head(10).to_html(classes="tables_content", index=False))
    context['tables'].append(trace_radg.head(10).to_html(classes="tables_content", index=False))
    context['tables'].append(trace_viso.head(10).to_html(classes="tables_content", index=False))
    context['tables'].append(trace_vist.head(10).to_html(classes="tables_content", index=False))
    context['tables'].append(trace_trvt.head(10).to_html(classes="tables_content", index=False))
    context['tables'].append(trace_inco.head(10).to_html(classes="tables_content", index=False))

    fig1 = plot_trace(trace=trace, initial_id=1, number_of_nodes=5, show_y_label=False)
    fig2 = plot_trace3d(trace=trace, initial_id=1, nodes_list=[4, 5, 6], show_y_label=False)
    fig3 = plot_density(trace=trace, initial_id=1, number_of_nodes=50)
    fig4 = plot_visit_order(trace_viso=trace_viso, initial_id=1, number_of_nodes=1)

    fig5= plot_metric_histogram(
        trace_trvd,
        initial_id=1,
        metric_type='TRVD',
        differ_nodes=False,
        show_title=False,
        show_y_label=True,
        max_users=100
    )

    fig6 = plot_metric_histogram(
        trace_radg,
        initial_id=1,
        metric_type='RADG',
        differ_nodes=False,
        show_title=False,
        show_y_label=True,
        max_users=100
    )

    context['figures'] = []

    context['figures'].append(fig1.to_html())
    context['figures'].append(fig2.to_html())
    context['figures'].append(fig3.to_html())
    context['figures'].append(fig4.to_html())
    context['figures'].append(fig5.to_html())
    context['figures'].append(fig6.to_html())

    return context