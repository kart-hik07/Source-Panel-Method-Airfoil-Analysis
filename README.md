# Source Panel Method for 2D Airfoil Analysis

A Python implementation of the source panel method to compute the surface pressure
distribution (Cp) over a non-lifting 2D body — here, a NACA0012 airfoil at zero
angle of attack.

## What this does

The source panel method models potential flow over a body by distributing source
singularities along its surface. Each panel gets a constant source strength, solved
for by enforcing flow tangency (zero normal velocity) at each panel's control point.
Because sources are non-circulatory, this method captures thickness effects but
cannot produce lift — that's what the vortex panel method is for (separate repo,
coming soon).

## Files

- `source_panel_method.py` — main script: builds the influence coefficient matrix,
  solves for source strengths, computes surface velocity and Cp
- `generate_naca0012.py` — generates NACA0012 coordinates using the standard NACA
  4-digit thickness equation (cosine-spaced for better leading-edge resolution)
- `naca0012.dat` — pre-generated airfoil coordinates (x, y pairs)

## Running it

```bash
python generate_naca0012.py   # only needed if naca0012.dat isn't present
python source_panel_method.py
```

This produces `cp_distribution.png` and prints a validation check to the console.

## Validation

For a symmetric airfoil at zero angle of attack, the stagnation point sits right at
the leading edge, where Cp should be very close to 1.0. Running this script gives:

```
Max Cp: 0.9987  (expected close to 1.0 at the stagnation point)
```

This confirms the panel method is correctly enforcing the no-penetration boundary
condition at the surface.

## Method summary

1. Discretize the airfoil surface into N flat panels
2. Place a constant-strength source on each panel
3. Build an N x N influence coefficient matrix from panel geometry
4. Solve for source strengths that satisfy zero normal flow at each control point
5. Recover tangential velocity and surface Cp from the source strengths

## Limitations

- Non-lifting only — no circulation, so this cannot predict lift or model angle of
  attack effects on a cambered airfoil correctly
- Inviscid — no boundary layer, so no drag or separation prediction
- Panel count is fixed at generation time; a convergence study (Cp vs. N) would be
  a natural next step

## Related work

A vortex panel method (adds circulation via the Kutta condition, enabling lift
prediction) is in progress as a companion repo.
