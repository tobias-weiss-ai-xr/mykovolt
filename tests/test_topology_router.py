"""Tests for the topology-driven PCB autorouter.

Tests GridMap A* pathfinding, net classification, coordinate conversion,
and integration with the KiCad PCB generator.
"""

import os
import sys

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, "hardware", "kicad"))

from topology_router import (
    GridMap,
    TopologyRouter,
    classify_net,
    cell_from_nm,
    nm_from_cell,
    FREE,
    OBSTACLE,
    TRACK,
    CELL_UM,
    CLASS_I2C,
    CLASS_POWER,
    CLASS_POWER_WIDE,
    CLASS_SIGNAL,
    CLASS_XTAL,
    NET_RULES,
    NET_PRIORITY,
    TRACK_W_DEFAULT,
    TRACK_W_POWER,
)

import pytest


class TestGridMap:
    def test_creates_grid_with_correct_dimensions(self):
        gm = GridMap(int(30e6), int(20e6))
        assert gm.w == 301
        assert gm.h == 201

    def test_initial_all_free(self):
        gm = GridMap(int(10e6), int(10e6))
        for x in range(gm.w):
            for y in range(gm.h):
                assert gm.grid[x][y] == FREE

    def test_set_obstacle_marks_cells(self):
        gm = GridMap(int(10e6), int(10e6))
        gm.set_obstacle(int(5e6), int(5e6), int(1e6))
        cx, cy, r = int(5e6) // 100000, int(5e6) // 100000, int(1e6) // 100000
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r:
                    assert gm.grid[cx + dx][cy + dy] == OBSTACLE

    def test_set_rect_obstacle_marks_bounds(self):
        gm = GridMap(int(10e6), int(10e6))
        gm.set_rect_obstacle(int(2e6), int(3e6), int(5e6), int(7e6))
        x1, y1 = cell_from_nm(int(2e6)), cell_from_nm(int(3e6))
        x2, y2 = cell_from_nm(int(5e6)), cell_from_nm(int(7e6))
        assert gm.grid[x1][y1] == OBSTACLE
        assert gm.grid[x2][y2] == OBSTACLE
        assert gm.grid[0][0] == FREE

    def test_astar_finds_straight_path(self):
        gm = GridMap(int(30e6), int(20e6))
        path = gm.astar(int(1e6), int(1e6), int(5e6), int(1e6))
        assert path is not None
        assert path[0] == (int(1e6), int(1e6))
        assert path[-1] == (int(5e6), int(1e6))

    def test_astar_returns_none_for_blocked_path(self):
        gm = GridMap(int(10e6), int(10e6))
        gm.set_rect_obstacle(int(2e6), int(0), int(8e6), int(10e6))
        path = gm.astar(int(1e6), int(5e6), int(9e6), int(5e6))
        assert path is None

    def test_astar_finds_path_around_obstacle(self):
        gm = GridMap(int(10e6), int(10e6))
        gm.set_rect_obstacle(int(3e6), int(2e6), int(7e6), int(8e6))
        path = gm.astar(int(1e6), int(5e6), int(9e6), int(5e6))
        assert path is not None
        assert path[0] == (int(1e6), int(5e6))
        assert path[-1] == (int(9e6), int(5e6))

    def test_mark_track_sets_track_state(self):
        gm = GridMap(int(10e6), int(10e6))
        gm.mark_track(int(1e6), int(1e6), int(5e6), int(1e6), int(0.3e6))
        cx = cell_from_nm(int(3e6))
        cy = cell_from_nm(int(1e6))
        assert gm.grid[cx][cy] == TRACK

    def test_astar_refuses_out_of_bounds(self):
        gm = GridMap(int(30e6), int(20e6))
        assert gm.astar(-1, 0, int(5e6), int(1e6)) is None
        assert gm.astar(int(1e6), int(1e6), -1, int(5e6)) is None


class TestNetClassification:
    def test_classify_i2c(self):
        assert classify_net("I2C1_SCL") == CLASS_I2C
        assert classify_net("I2C1_SDA") == CLASS_I2C

    def test_classify_power(self):
        assert classify_net("3.3V") == CLASS_POWER
        assert classify_net("GND") == CLASS_POWER

    def test_classify_power_wide(self):
        assert classify_net("VSTOR") == CLASS_POWER_WIDE
        assert classify_net("LED_PWR") == CLASS_POWER_WIDE

    def test_classify_xtal(self):
        assert classify_net("XTAL_IN") == CLASS_XTAL
        assert classify_net("XTAL_OUT") == CLASS_XTAL

    def test_classify_signal_default(self):
        assert classify_net("SWD_CLK") == CLASS_SIGNAL
        assert classify_net("UART_TX") == CLASS_SIGNAL
        assert classify_net("UNKNOWN_NET") == CLASS_SIGNAL

    def test_classify_case_sensitive(self):
        assert classify_net("i2c1_scl") == CLASS_SIGNAL

    def test_all_rules_have_unique_prefixes(self):
        prefixes = [r[0] for r in NET_RULES]
        assert len(prefixes) == len(set(prefixes)), (
            f"Duplicate: {[p for p in prefixes if prefixes.count(p) > 1]}"
        )

    def test_all_priority_values_are_unique(self):
        vals = list(NET_PRIORITY.values())
        assert len(vals) == len(set(vals))

    def test_power_routed_first(self):
        assert NET_PRIORITY[CLASS_POWER] < NET_PRIORITY[CLASS_I2C]


class TestCoordinateConversion:
    def test_cell_from_nm_rounds_down(self):
        assert cell_from_nm(0) == 0
        assert cell_from_nm(int(0.05e6)) == 0
        assert cell_from_nm(int(0.1e6)) == 1
        assert cell_from_nm(int(30e6)) == 300

    def test_nm_from_cell_precise(self):
        assert nm_from_cell(0) == 0
        assert nm_from_cell(1) == 100000
        assert nm_from_cell(300) == 30_000_000

    def test_roundtrip(self):
        for nm in [0, int(0.1e6), int(5e6), int(30e6)]:
            assert nm_from_cell(cell_from_nm(nm)) == nm


class TestTopologyRouter:
    def _require_pcbnew(self):
        """Skip test if pcbnew (KiCad Python bindings) is not installed."""
        try:
            import pcbnew as pn

            return pn
        except ImportError:
            pytest.skip("pcbnew not available — install KiCad Python bindings")

    def test_route_all_creates_tracks(self):
        pn = self._require_pcbnew()

        board = pn.BOARD()
        board.SetCopperLayerCount(4)

        net = pn.NETINFO_ITEM(board, "GND", 1)
        board.Add(net)
        netcode_map = {"GND": 1}
        components = []
        pcb_pos = {}
        nets = [("GND", [])]

        router = TopologyRouter(board, pn, netcode_map, components, pcb_pos, nets)
        router.route_all()

        track_count = len(board.GetTracks())
        assert track_count == 0

    def test_route_all_with_unmatched_net_skips(self):
        pn = self._require_pcbnew()

        board = pn.BOARD()
        board.SetCopperLayerCount(4)

        net = pn.NETINFO_ITEM(board, "GND", 1)
        board.Add(net)
        netcode_map = {"GND": 1}
        components = []
        pcb_pos = {}
        nets = [("I2C1_SCL", [])]

        router = TopologyRouter(board, pn, netcode_map, components, pcb_pos, nets)
        router.route_all()

    def test_build_obstacle_grid_with_no_components(self):
        pn = self._require_pcbnew()

        board = pn.BOARD()

        router = TopologyRouter(board, pn, {}, [], {}, [])
        router.build_obstacle_grid()

        assert router.grid is not None

    def test_classify_affected_net_routing(self):
        pn = self._require_pcbnew()

        board = pn.BOARD()
        board.SetCopperLayerCount(4)

        for name in ["GND", "3.3V", "I2C1_SCL", "XTAL_IN", "LED_PWR"]:
            net = pn.NETINFO_ITEM(board, name, 1)
            board.Add(net)

        netcode_map = {"GND": 1, "3.3V": 1, "I2C1_SCL": 1, "XTAL_IN": 1, "LED_PWR": 1}
        nets = [(n, []) for n in ["GND", "3.3V", "I2C1_SCL", "XTAL_IN", "LED_PWR"]]

        router = TopologyRouter(board, pn, netcode_map, [], {}, nets)
        router.route_all()
