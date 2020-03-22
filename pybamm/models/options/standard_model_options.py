#
# Standard model options.
#
import pybamm


operating_mode = pybamm.Option(
    "operating mode", "current", ["current", "voltage", "power", "FUNCTION"]
)

dimensionality = pybamm.Option("dimensionality", 0, [0, 1, 2])

surface_form = pybamm.Option(
    "surface form", False, [False, "differential", "algebriac"]
)

side_reactions = pybamm.Option("side reactions", [], [])

convection = pybamm.Option("convection", False, [False, True])

current_collector = pybamm.Option(
    "current collector", "uniform", ["uniform", "potential pair"]
)

particle = pybamm.Option(
    "particle", "Fickian diffusion", ["Fickian diffusion", "fast diffusion"]
)

thermal = pybamm.Option(
    "thermal",
    "isothermal",
    ["isothermal", "x-full", "x-lumped", "xyz-lumped", "lumped"],
)

thermal_cc = pybamm.Option("thermal current collector", False, [True, False])

external_submodels = pybamm.Option("external submodels", [], [])