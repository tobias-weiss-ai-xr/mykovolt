#!/usr/bin/env python3
"""Topology-driven grid autorouter for MykoVolt DevKit PCB.

Replaces hardcoded _route_critical_nets() with:
  1. Obstacle grid (0.1mm resolution) built from component footprints
  2. Net-class routing strategies (I2C daisy-chain, power wide, signal A*)
  3. A* maze router for point-to-point nets
  4. Priority-ordered routing (power → I2C → critical signals → remaining)

Usage:
    router = TopologyRouter(board, pn_module, netcode_map, component_list)
    router.route_all()
"""

import heapq
from collections import defaultdict

# Grid resolution
CELL_UM = 100  # 0.1mm per cell
CELL_MM = 0.1

# Clearance in cells
CLR_COPPER = 3  # 0.3mm
CLR_EDGE = 5  # 0.5mm

# Cell states
FREE = 0
OBSTACLE = 1
TRACK = 2
VIA = 3

# Net class routing strategies
CLASS_I2C = "i2c"
CLASS_POWER = "power"
CLASS_POWER_WIDE = "power_wide"
CLASS_SIGNAL = "signal"
CLASS_XTAL = "xtal"

# Net classification rules: (prefix, class)
NET_RULES = [
    ("I2C1_", CLASS_I2C),
    ("VSTOR", CLASS_POWER_WIDE),
    ("LBOOST", CLASS_POWER_WIDE),
    ("LBUCK", CLASS_POWER_WIDE),
    ("V_PRESSLING", CLASS_POWER_WIDE),
    ("GND", CLASS_POWER),
    ("3.3V", CLASS_POWER),
    ("VOC_SAMP", CLASS_SIGNAL),
    ("VREF_SAMP", CLASS_SIGNAL),
    ("OK_PROG", CLASS_SIGNAL),
    ("OK_HYST", CLASS_SIGNAL),
    ("VRDIV", CLASS_SIGNAL),
    ("VOUT_SET", CLASS_SIGNAL),
    ("LED_PWR", CLASS_POWER_WIDE),
    ("V_SENSE", CLASS_SIGNAL),
    ("XTAL_", CLASS_XTAL),
]


TRACK_W_DEFAULT = int(0.3e6)
TRACK_W_POWER = int(0.5e6)

# Routing order for nets (lower = routed first)
NET_PRIORITY = {
    CLASS_POWER: 0,
    CLASS_POWER_WIDE: 1,
    CLASS_I2C: 2,
    CLASS_XTAL: 3,
    CLASS_SIGNAL: 4,
}


def classify_net(name):
    for prefix, cls in NET_RULES:
        if name.startswith(prefix):
            return cls
    return CLASS_SIGNAL


def cell_from_nm(nm_val):
    return int(nm_val / 1000 // CELL_UM)


def nm_from_cell(cell_val):
    return cell_val * CELL_UM * 1000


class GridMap:
    """2D obstacle grid at CELL_UM resolution."""

    def __init__(self, width_nm, height_nm):
        self.w = cell_from_nm(width_nm) + 1
        self.h = cell_from_nm(height_nm) + 1
        self.grid = [[FREE] * self.h for _ in range(self.w)]

    def _cells(self, x_nm, y_nm, radius_nm):
        cx = cell_from_nm(x_nm)
        cy = cell_from_nm(y_nm)
        r = max(1, int(radius_nm / 1000 // CELL_UM))
        return cx, cy, r

    def set_obstacle(self, x_nm, y_nm, radius_nm=300000):
        cx, cy, r = self._cells(x_nm, y_nm, radius_nm)
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                ix, iy = cx + dx, cy + dy
                if 0 <= ix < self.w and 0 <= iy < self.h:
                    self.grid[ix][iy] = OBSTACLE

    def set_rect_obstacle(self, x1_nm, y1_nm, x2_nm, y2_nm):
        c1x = max(0, cell_from_nm(x1_nm))
        c1y = max(0, cell_from_nm(y1_nm))
        c2x = min(self.w - 1, cell_from_nm(x2_nm))
        c2y = min(self.h - 1, cell_from_nm(y2_nm))
        for ix in range(c1x, c2x + 1):
            for iy in range(c1y, c2y + 1):
                self.grid[ix][iy] = OBSTACLE

    def mark_track(self, x1_nm, y1_nm, x2_nm, y2_nm, width_nm=300000):
        c1x, c1y, _ = self._cells(x1_nm, y1_nm, 0)
        c2x, c2y, _ = self._cells(x2_nm, y2_nm, 0)
        r = max(1, int(width_nm / 1000 // CELL_UM // 2))
        self._line(c1x, c1y, c2x, c2y, TRACK, r)

    def is_free(self, x_nm, y_nm):
        cx, cy, _ = self._cells(x_nm, y_nm, 0)
        if 0 <= cx < self.w and 0 <= cy < self.h:
            return self.grid[cx][cy] == FREE
        return False

    def _line(self, x0, y0, x1, y1, state, radius):
        cells = set()
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        cx, cy = x0, y0
        while True:
            for drx in range(-radius, radius + 1):
                for dry in range(-radius, radius + 1):
                    nx, ny = cx + drx, cy + dry
                    if 0 <= nx < self.w and 0 <= ny < self.h:
                        self.grid[nx][ny] = state
                        cells.add((nx, ny))
            if cx == x1 and cy == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                cx += sx
            if e2 <= dx:
                err += dx
                cy += sy

    def astar(self, x1_nm, y1_nm, x2_nm, y2_nm, max_steps=50000):
        sx, sy = cell_from_nm(x1_nm), cell_from_nm(y1_nm)
        ex, ey = cell_from_nm(x2_nm), cell_from_nm(y2_nm)

        if not (0 <= sx < self.w and 0 <= sy < self.h):
            return None
        if not (0 <= ex < self.w and 0 <= ey < self.h):
            return None
        if self.grid[sx][sy] != FREE and (sx, sy) != (ex, ey):
            self.grid[sx][sy] = FREE
        if self.grid[ex][ey] != FREE:
            self.grid[ex][ey] = FREE

        margin = max(abs(ex - sx), abs(ey - sy), 20) // 2 + 20
        bx1 = max(0, min(sx, ex) - margin)
        bx2 = min(self.w - 1, max(sx, ex) + margin)
        by1 = max(0, min(sy, ey) - margin)
        by2 = min(self.h - 1, max(sy, ey) + margin)

        def heuristic(ax, ay):
            return abs(ax - ex) + abs(ay - ey)

        open_set = [(heuristic(sx, sy), 0, sx, sy)]
        came_from = {}
        g_score = {(sx, sy): 0}

        while open_set:
            _, g, cx, cy = heapq.heappop(open_set)

            if (cx, cy) == (ex, ey):
                path = [(cx, cy)]
                while (cx, cy) in came_from:
                    cx, cy = came_from[(cx, cy)]
                    path.append((cx, cy))
                path.reverse()
                return [(nm_from_cell(x), nm_from_cell(y)) for x, y in path]

            if g > max_steps:
                continue

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if nx < bx1 or nx > bx2 or ny < by1 or ny > by2:
                    continue
                if self.grid[nx][ny] != FREE and (nx, ny) != (ex, ey):
                    continue
                ng = g + 1
                key = (nx, ny)
                if key not in g_score or ng < g_score[key]:
                    g_score[key] = ng
                    f = ng + heuristic(nx, ny)
                    heapq.heappush(open_set, (f, ng, nx, ny))
                    came_from[key] = (cx, cy)

        return None

    def has_clear_line(self, x1_nm, y1_nm, x2_nm, y2_nm):
        sx, sy = cell_from_nm(x1_nm), cell_from_nm(y1_nm)
        ex, ey = cell_from_nm(x2_nm), cell_from_nm(y2_nm)
        dx = abs(ex - sx)
        dy = -abs(ey - sy)
        step_x = 1 if sx < ex else -1
        step_y = 1 if sy < ey else -1
        err = dx + dy
        cx, cy = sx, sy
        while True:
            if self.grid[cx][cy] != FREE:
                return False
            if cx == ex and cy == ey:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                cx += step_x
            if e2 <= dx:
                err += dx
                cy += step_y
        return True


class TopologyRouter:
    """Topology-driven PCB autorouter for the MykoVolt DevKit."""

    def __init__(self, board, pn, netcode_map, components, pcb_pos, nets):
        self.board = board
        self.pn = pn
        self.netcode_map = netcode_map
        self.components = components
        self.pcb_pos = pcb_pos
        self.nets = nets

        self.grid = GridMap(int(30e6), int(20e6))
        self._routed_nets = set()
        self._fp_cache = {}
        self._tracks = []

    def build_obstacle_grid(self):
        self.grid = GridMap(int(30e6), int(20e6))

        for ref, value, footprint, _, _ in self.components:
            if ref not in self.pcb_pos:
                continue
            x_nm, y_nm = self.pcb_pos[ref]

            fp = self._load_footprint(footprint)
            if fp:
                bb = self._footprint_bbox(fp)
                if bb:
                    x1, y1, x2, y2 = bb
                    ox1 = x_nm + x1 - int(0.3e6)
                    oy1 = y_nm + y1 - int(0.3e6)
                    ox2 = x_nm + x2 + int(0.3e6)
                    oy2 = y_nm + y2 + int(0.3e6)
                    self.grid.set_rect_obstacle(ox1, oy1, ox2, oy2)
                else:
                    self.grid.set_obstacle(x_nm, y_nm, int(2e6))
            else:
                self.grid.set_obstacle(x_nm, y_nm, int(2e6))

        self.grid.set_rect_obstacle(0, 0, int(0.5e6), int(20e6))
        self.grid.set_rect_obstacle(int(29.5e6), 0, int(30e6), int(20e6))
        self.grid.set_rect_obstacle(0, 0, int(30e6), int(0.5e6))
        self.grid.set_rect_obstacle(0, int(19.5e6), int(30e6), int(20e6))

    def _load_footprint(self, footprint):
        if footprint in self._fp_cache:
            return self._fp_cache[footprint]
        if ":" not in footprint:
            self._fp_cache[footprint] = None
            return None
        lib, fp_name = footprint.split(":", 1)
        fp_path = "/usr/share/kicad/footprints"
        fp = self.pn.FootprintLoad(f"{fp_path}/{lib}.pretty", fp_name)
        self._fp_cache[footprint] = fp
        return fp

    def _footprint_bbox(self, fp):
        try:
            pads = fp.GetPads()
            if not pads:
                return None
            xs = [p.GetPosition().x for p in pads]
            ys = [p.GetPosition().y for p in pads]
            return (min(xs), min(ys), max(xs), max(ys))
        except Exception:
            return None

    def _pad_positions(self, ref):
        if ref not in self.pcb_pos:
            return {}
        cx, cy = self.pcb_pos[ref]

        comp = None
        fp_str = None
        for c in self.components:
            if c[0] == ref:
                comp = c
                fp_str = c[2]
                break
        if not comp or not fp_str:
            return {}

        fp = self._load_footprint(fp_str)
        if fp:
            positions = {}
            for pad in fp.Pads():
                p = pad.GetPosition()
                positions[pad.GetNumber()] = (cx + p.x, cy + p.y)
            return positions

        return {}

    def _add_track(self, x1, y1, x2, y2, width, layer, netcode=0):
        self._tracks.append(
            (int(x1), int(y1), int(x2), int(y2), int(width), layer, int(netcode))
        )

    def apply(self, board):
        for x1, y1, x2, y2, width, layer, netcode in self._tracks:
            track = self.pn.PCB_TRACK(board)
            if hasattr(self.pn, "VECTOR2I"):
                track.SetStart(self.pn.VECTOR2I(x1, y1))
                track.SetEnd(self.pn.VECTOR2I(x2, y2))
            else:
                track.SetStart(self.pn.wxPoint(x1, y1))
                track.SetEnd(self.pn.wxPoint(x2, y2))
            track.SetWidth(width)
            track.SetLayer(layer)
            if netcode > 0:
                track.SetNetCode(netcode)
            board.Add(track)

    def save(self, path):
        import json

        data = [
            {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "w": w, "l": l, "n": n}
            for x1, y1, x2, y2, w, l, n in self._tracks
        ]
        with open(path, "w") as f:
            json.dump(data, f)

    def load(self, path):
        import json

        with open(path) as f:
            data = json.load(f)
        self._tracks = [
            (d["x1"], d["y1"], d["x2"], d["y2"], d["w"], d["l"], d["n"]) for d in data
        ]

    def _get_net_pins(self, net_name):
        for n, conns in self.nets:
            if n == net_name:
                return conns
        return []

    def route_all(self):
        self.build_obstacle_grid()

        ordered = []
        for net_name, _ in self.nets:
            cls = classify_net(net_name)
            priority = NET_PRIORITY.get(cls, 5)
            ordered.append((priority, net_name, cls))

        ordered.sort()

        for priority, net_name, cls in ordered:
            if net_name in self._routed_nets:
                continue
            ncode = self.netcode_map.get(net_name, 0)
            if ncode == 0:
                continue

            if cls == CLASS_I2C:
                self._route_i2c(net_name, ncode)
            elif cls == CLASS_POWER_WIDE:
                self._route_power_wide(net_name, ncode)
            elif cls == CLASS_XTAL:
                self._route_signal(net_name, ncode, TRACK_W_DEFAULT, critical=True)
            else:
                self._route_signal(net_name, ncode, TRACK_W_DEFAULT)
            self._routed_nets.add(net_name)

    def _route_i2c(self, net_name, ncode):
        pins = self._get_net_pins(net_name)
        if len(pins) < 2:
            return

        stops = []
        for ref, pin in pins:
            pad_positions = self._pad_positions(ref)
            if pin in pad_positions:
                px, py = pad_positions[pin]
            elif ref in self.pcb_pos:
                px, py = self.pcb_pos[ref]
            else:
                continue
            stops.append((ref, pin, px, py))

        if len(stops) < 2:
            return

        trunk_y = int(sum(py for _, _, _, py in stops) / len(stops))
        x_vals = [px for _, _, px, _ in stops]
        x_min, x_max = min(x_vals), max(x_vals)

        trunk_y = (trunk_y // 100000) * 100000

        self._add_track(
            x_min - int(1e6),
            trunk_y,
            x_max + int(1e6),
            trunk_y,
            TRACK_W_DEFAULT,
            self.pn.F_Cu,
            ncode,
        )
        self.grid.mark_track(x_min - int(1e6), trunk_y, x_max + int(1e6), trunk_y)

        for ref, pin, px, py in stops:
            if py != trunk_y:
                self._add_track(
                    px, py, px, trunk_y, TRACK_W_DEFAULT, self.pn.F_Cu, ncode
                )
                self.grid.mark_track(px, py, px, trunk_y)

    def _route_power_wide(self, net_name, ncode):
        self._route_signal(net_name, ncode, TRACK_W_POWER)

    def _route_signal(self, net_name, ncode, width=TRACK_W_DEFAULT, critical=False):
        pins = self._get_net_pins(net_name)
        if len(pins) < 2:
            return

        points = []
        for ref, pin in pins:
            pad_positions = self._pad_positions(ref)
            if pin in pad_positions:
                px, py = pad_positions[pin]
                points.append((px, py))
            elif ref in self.pcb_pos:
                px, py = self.pcb_pos[ref]
                pin_i = int(pin) if pin.isdigit() else 0
                offset_x = -int(1.5e6) if pin_i % 2 == 1 else int(1.5e6)
                offset_y = int(0.5e6) * (pin_i // 2 - 1)
                points.append((px + offset_x, py + offset_y))

        if len(points) < 2:
            return

        routed_segments = []

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            if self.grid.has_clear_line(x1, y1, x2, y2):
                path = [(x1, y1), (x2, y2)]
            else:
                path = self.grid.astar(x1, y1, x2, y2)
                if path is None:
                    path = [
                        (x1, y1),
                        ((x1 + x2) // 2, y1),
                        ((x1 + x2) // 2, y2),
                        (x2, y2),
                    ]

            compressed = self._compress_waypoints(path)
            for j in range(len(compressed) - 1):
                cx1, cy1 = compressed[j]
                cx2, cy2 = compressed[j + 1]
                self._add_track(cx1, cy1, cx2, cy2, width, self.pn.F_Cu, ncode)
                self.grid.mark_track(cx1, cy1, cx2, cy2, width)
                routed_segments.append(((cx1, cy1), (cx2, cy2)))

    def _compress_waypoints(self, waypoints):
        if not waypoints or len(waypoints) < 3:
            return waypoints
        compressed = [waypoints[0]]
        for i in range(1, len(waypoints) - 1):
            x0, y0 = waypoints[i - 1]
            x1, y1 = waypoints[i]
            x2, y2 = waypoints[i + 1]
            dx1, dy1 = x1 - x0, y1 - y0
            dx2, dy2 = x2 - x1, y2 - y1
            if dx1 * dy2 == dy1 * dx2:
                continue
            compressed.append((x1, y1))
        compressed.append(waypoints[-1])
        return compressed
