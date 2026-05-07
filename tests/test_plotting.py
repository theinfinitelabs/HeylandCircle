import matplotlib

# Use non-interactive backend for testing
matplotlib.use("Agg")

from heylandcircle.circle_diagram import CircleDiagram
from heylandcircle.data_structures import CircleDiagramConfig


# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------

def test_plot_runs(diagram):
    fig, ax = diagram.plot()

    assert fig is not None
    assert ax is not None


def test_plot_save(tmp_path, diagram):
    output_file = tmp_path / "circle_diagram.png"

    fig, ax = diagram.plot(save_path=str(output_file))

    assert output_file.exists()


# ------------------------------------------------------------------
# Configuration behavior
# ------------------------------------------------------------------

def test_plot_without_optional_scales(sample_data):
    config = CircleDiagramConfig(
        power_scale=1.0,
        current_scale=1.0,
        show_eff_scale=False,
        show_slip_scale=False,
        show_pf_curve=False,
        show_full_circle=False,
        show_grid=False,
    )

    diagram = CircleDiagram(config, sample_data)

    fig, ax = diagram.plot()

    assert fig is not None
    assert ax is not None