if ( A.connected(B) ) {
    if ( !C.connected(D) ) {
        bool foreign_is_contour = edge(C, D).contour();
 
        // the number of contour edges
        switch ( edge(A, C).contour()
                 + edge(B, D).contour()
                 + foreign_is_contour ) {
        case 2:
            A.smooth = !foreign_is_contour;
            break;
        default:
            assert(("precondition failed", false));
        // the following cases are only for
        // documentation of possible values (they don't
        // change the algorithm)
        case 3: case 1: case 0:
            // {A, B} is the pair with the angle
            // closest to 180 degrees
            A.smooth = true;
        }
    } else {
        // there might be 2-color, then A.smooth = true
 
        // or it might be 1-color and doesn't matter,
        // because the current node will disappear
        A.smooth = true;
    }
} else if ( A.connected(C) ) {
    if ( !B.connected(D) ) {
        bool foreign_is_contour = edge(B, D).contour();
 
        // the number of contour edges
        switch ( edge(A, B).contour()
                 + edge(C, D).contour()
                 + foreign_is_contour ) {
        case 2:
            A.smooth = !foreign_is_contour;
            break;
        default:
            assert(("precondition failed", false));
        // the following cases are only for
        // documentation of possible values (they don't
        // change the algorithm)
        case 3: case 1: case 0:
            // {A, C} is the pair with the angle
            // closest to 180 degrees
            A.smooth = true;
        }
    } else {
        // there might be 2-color, then A.smooth = true
 
        // or it might be 1-color and doesn't matter,
        // because the current node will disappear
        A.smooth = true;
    }
} else if ( B.connected(D) ) {
    bool foreign_is_contour = edge(C, D).contour();
 
    switch ( edge(A, B).contour()
             + edge(A, C).contour()
             + foreign_is_contour ) {
    case 2:
        A.smooth = !foreign_is_contour;
        break;
    default:
        assert(("precondition failed", false));
    case 3: case 1: case 0:
        // {B, D} is the pair with the angle closest to
        // 180 degrees
        A.smooth = false;
    }
} else if ( C.connected(D) ) {
    bool foreign_is_contour = edge(B, D).contour();
 
    switch ( edge(A, C).contour()
             + edge(A, B).contour()
             + foreign_is_contour ) {
    case 2:
        A.smooth = !foreign_is_contour;
        break;
    default:
        assert(("precondition failed", false));
    case 3: case 1: case 0:
        // {C, D} is the pair with the angle closest to
        // 180 degrees
        A.smooth = false;
    }
} else {
    // there is a 4-color pattern, where the current
    // node won't be smooth
    A.smooth = false;
}
