/**
 * \file
 * \brief Renders the contents of a SVG file
 *
 * Copyright 2013 Vinícius dos Santos Oliveira <vini.ipsmaker@gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it either under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * (the "LGPL") or, at your option, under the terms of the Mozilla
 * Public License Version 1.1 (the "MPL"). If you do not alter this
 * notice, a recipient may use your version of this file under either
 * the MPL or the LGPL.
 *
 * You should have received a copy of the LGPL along with this library
 * in the file COPYING-LGPL-2.1; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 * You should have received a copy of the MPL along with this library
 * in the file COPYING-MPL-1.1
 *
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * This software is distributed on an "AS IS" basis, WITHOUT WARRANTY
 * OF ANY KIND, either express or implied. See the LGPL or the MPL for
 * the specific language governing rights and limitations.
 *
 */

#ifndef SEEN_SVG_PATH_RENDER_H
#define SEEN_SVG_PATH_RENDER_H

#include <2geom/pathvector.h>
#include <ostream>

namespace Geom {

inline void render_point(std::ostream &out, Point p)
{
    out << p[X] << ',' << p[Y];
}

inline void render_svg_path(std::ostream &out, PathVector const &source)
{
    bool first = true;
    for ( PathVector::const_iterator it = source.begin(), end = source.end()
              ; it != end ; ++it ) {
        {
            if (first) {
                out << "M ";
                first = false;
            } else {
                out << " M ";
            }

            render_point(out, it->initialPoint());
        }
        for ( Path::const_iterator it2 = it->begin(), end2 = it->end_open()
                  ; it2 != end2 ; ++it2) {
            /*
              The performance could probably be improved by using "Open and
              Efficient Type Switch for C++"
              <http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3449.pdf>.

              TODO: every time a new C++ version is out, check if a type switch
              syntax was added and update the code below.
             */
            if ( BezierCurve<1> const *curve
                 = dynamic_cast<BezierCurve<1> const*>(&*it2) ) {
                // it's a line

                out << " L";

                std::vector<Point> points = curve->points();
                for ( std::vector<Point>::iterator it3 = points.begin() + 1,
                          end3 = points.end() ; it3 != end3 ; ++it3 ) {
                    out << ' ';
                    render_point(out, *it3);
                }
            } else if ( BezierCurve<2> const *curve
                 = dynamic_cast<BezierCurve<2> const*>(&*it2) ) {
                // it's a quadratic Bézier curve

                out << " Q";

                std::vector<Point> points = curve->points();
                for ( std::vector<Point>::iterator it3 = points.begin() + 1,
                          end3 = points.end() ; it3 != end3 ; ++it3 ) {
                    out << ' ';
                    render_point(out, *it3);
                }
            } else if ( BezierCurve<3> const *curve
                 = dynamic_cast<BezierCurve<3> const*>(&*it2) ) {
                // it's a cubic Bézier curve

                out << " C";

                std::vector<Point> points = curve->points();
                for ( std::vector<Point>::iterator it3 = points.begin() + 1,
                          end3 = points.end() ; it3 != end3 ; ++it3 ) {
                    out << ' ';
                    render_point(out, *it3);
                }
            } else {
                // I don't know what it is, so I'll just approximate

                out << " C";

                for ( int i = 0 ; i != 4 ; ++i ) {
                    Point p = (*it2)(Coord(i+1) / 4.);
                    out << ' ';
                    render_point(out, p);
                }
            }
        }
        if ( it->closed() )
            out << " z";
    }
}

}

#endif

/*
  Local Variables:
  mode:c++
  c-file-style:"stroustrup"
  c-file-offsets:((innamespace . 0)(inline-open . 0)(case-label . +))
  indent-tabs-mode:nil
  fill-column:99
  End:
*/
// vim: filetype=cpp:expandtab:shiftwidth=4:tabstop=8:softtabstop=4:encoding=utf-8:textwidth=99 :
