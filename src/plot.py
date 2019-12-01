import holoviews as hv
from bokeh.embed import autoload_static
from bokeh.resources import CDN

hv.extension("bokeh")


PLOT_FOLDER = "../plot/"
SCRIPT_FOLDER = "script/"
ELEMENT_FOLDER = "element/"


def save_plot(plot, name, print_element=True):
    """Saves a holoviews plot to be used for the data story."""

    renderer = hv.renderer("bokeh")
    plot_state = renderer.get_plot(plot).state

    script_path = SCRIPT_FOLDER + name + ".js"
    script, element = autoload_static(plot_state, CDN, script_path)

    with open(PLOT_FOLDER + SCRIPT_FOLDER + name + ".js", "w+") as file:
        file.write(script)

    with open(PLOT_FOLDER + ELEMENT_FOLDER + name + ".html", "w+") as file:
        file.write(element)

    if print_element:
        print(element.strip())

    return script, element
