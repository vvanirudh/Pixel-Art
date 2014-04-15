# Change optimization step to remove the need of harmonic maps

This change boils down to treat sets of points that share the same position as a
single point, then there will be no displacements on the final output. e.g. if
you change the position of one node, you must change the position of all nodes
that lies on the old position to the new position.

I didn't test this algorithm, but I believe it'll work.

# Remove invisible/collinear points

Right before optimization step, there should be an algorithm to remove
collinear/invisible points. This is necessary to ease the work of the optimizer
and produce better results. It is difficult to embed this algorithm in the
optimizer because the optimizer will change the position of the nodes and the
collinearity property will change.

# Move some abstractions to lib2geom

SVG d generator code should be moved to 2geom. Inkscape has one implementation
and libdepixelize has another.

If the alternative optimizer doesn't work and we need to implement harmonic
maps, then we should move the implementation to 2geom.
