/*  This file is part of the libdepixelize project
    Copyright (C) 2013 Vinícius dos Santos Oliveira <vini.ipsmaker@gmail.com>

    GNU Lesser General Public License Usage
    This library is free software; you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by the
    Free Software Foundation; either version 2.1 of the License, or (at your
    option) any later version.
    You should have received a copy of the GNU Lesser General Public License
    along with this library.  If not, see <http://www.gnu.org/licenses/>.

    GNU General Public License Usage
    Alternatively, this library may be used under the terms of the GNU General
    Public License as published by the Free Software Foundation, either version
    2 of the License, or (at your option) any later version.
    You should have received a copy of the GNU General Public License along with
    this library.  If not, see <http://www.gnu.org/licenses/>.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
*/

#ifndef DEPIXELIZE_RENDER_SVG_H
#define DEPIXELIZE_RENDER_SVG_H

#include "priv/2geom/svg-path-render.h"
#include "../splines.h"
#include <iostream>
#include <iomanip>
#include <limits>

void print_svg(std::ostream &svg, const Tracer::Splines &splines)
{
    svg << std::setprecision(std::numeric_limits<Geom::Coord>::digits10)
        << "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\""
        << splines.width() << "px\" height=\"" << splines.height() << "px\">\n";

    for ( Tracer::Splines::const_iterator it = splines.begin(),
              end = splines.end() ; it != end ; ++it ) {
        svg << "\t<path d=\"";

        Geom::render_svg_path(svg, it->pathVector);

        std::hex(svg);
        svg << "\" fill=\"#"
            << std::setfill('0')
            << std::setw(2) << int(it->rgba[0])
            << std::setw(2) << int(it->rgba[1])
            << std::setw(2) << int(it->rgba[2])
            << std::setw(0) << std::setfill(' ') << "\" fill-opacity=\""
            << double(it->rgba[3]) / 255.;
        std::dec(svg);

        svg << "\" />\n";
    }

    svg << "</svg>" << std::endl;
}

#endif // DEPIXELIZE_RENDER_SVG_H

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
