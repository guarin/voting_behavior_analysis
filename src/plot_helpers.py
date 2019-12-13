from matplotlib import pyplot as plt
import holoviews as hv


def by_legislature(plot_fctn, vals):
    """
    Create a plot per legislature, using the specified plot_function 
    """
    plt.figure(figsize=(16,4))
    for i, v in enumerate(vals):
        plt.subplot(1,3,i+1)
        plot_fctn(v)
        plt.title('Legislature ' + str(i+1))
        

        
def hv_by_legislature(plot_fctn, vals):
    """
    Create a Hollowviews plot per legislature
    """
    plots = []
    for i, v in enumerate(vals):
        plt = plot_fctn(v)
        plt = plt.opts(frame_height=300)
        plt = plt.opts(frame_width=250)
        plots.append(plt.relabel('Legislature ' + str(i+1)))
    layout = hv.Layout(plots).opts(shared_axes=False)
    return layout
