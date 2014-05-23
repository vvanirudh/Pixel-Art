#include "../kopftracer2011.h"
#include <glibmm/init.h>
#include <gdkmm/wrap_init.h>
#include <iostream>
#include "priv/2geom/svg-path-render.h"
#include "render-svg.h"
#include <popt.h>
#include <fstream>
#include <cstdio>
#include <cstdlib>

using namespace std;

namespace {

enum Output {
    VORONOI = 1,
    GROUPED_VORONOI,
    NON_SMOOTH,
    SMOOTH
} output_type = SMOOTH;

const char *output;

double curves_multiplier = Tracer::Kopf2011::Options::CURVES_MULTIPLIER;
int islands_weight = Tracer::Kopf2011::Options::ISLANDS_WEIGHT;
int sparse_pixels_radius = Tracer::Kopf2011::Options::SPARSE_PIXELS_RADIUS;
double sparse_pixels_multiplier
= Tracer::Kopf2011::Options::SPARSE_PIXELS_MULTIPLIER;

int show_version;

poptOption options[] = {
    {"output", 'o',
     POPT_ARG_STRING, &output, 0,
     "Export document to a SVG file",
     "FILENAME"},
    {"curves", 'c',
     POPT_ARG_DOUBLE, &curves_multiplier, 0,
     "Favors connections that are part of a long curve",
     "MULTIPLIER"},
    {"islands", 'i',
     POPT_ARG_INT, &islands_weight, 0,
     "Avoid single disconnected pixels",
     "WEIGHT"},
    {"sparse-pixels", 'm',
     POPT_ARG_DOUBLE, &sparse_pixels_multiplier, 0,
     "Favors connections that are part of foreground color",
     "MULTIPLIER"},
    {"sparse-pixels-radius", 'r',
     POPT_ARG_INT, &sparse_pixels_radius, 0,
     "Favors connections that are part of foreground color",
     "WINDOW-RADIUS"},
    {"voronoi",'v',
     POPT_ARG_VAL, &output_type, VORONOI,
     "Output composed of straight lines",
     NULL},
    {"grouped-voronoi", 'g',
     POPT_ARG_VAL, &output_type, GROUPED_VORONOI,
     "Output composed of straight lines"
     " (grouping neighbours cells sharing the same color)",
     NULL},
    {"no-smooth",'n',
     POPT_ARG_VAL, &output_type, NON_SMOOTH,
     "Preserve staircasing artifacts",
     NULL},
    {"version", '\0',
     POPT_ARG_NONE, &show_version, 0,
     "Displays version and exit",
     NULL},
    POPT_AUTOHELP
    POPT_TABLEEND
};

Tracer::Kopf2011::Options tracingOptions()
{
    Tracer::Kopf2011::Options ret;

    ret.curvesMultiplier = curves_multiplier;
    ret.islandsWeight = islands_weight;
    ret.sparsePixelsMultiplier = sparse_pixels_multiplier;
    ret.sparsePixelsRadius = sparse_pixels_radius;

    ret.optimize = output_type == SMOOTH;

    return ret;
}

} // anonymous namespace

int main(int argc, char const *argv[])
{
    Glib::init();
    Gdk::wrap_init();

    poptContext popt_con = poptGetContext(NULL, argc, argv, options, 0);
    poptGetNextOpt(popt_con);
    char const *input = poptGetArg(popt_con);

    if ( show_version ) {
        std::cout << "0.1" << std::endl;
        return EXIT_SUCCESS;
    }

    if ( !input ) {
        poptPrintUsage(popt_con, stderr, 0);
        poptFreeContext(popt_con);
        return EXIT_FAILURE;
    }

    if ( sparse_pixels_radius < 1 ) {
        std::cerr << "Sparse pixels radius (-r) should be a non-zero positive"
            " number" << std::endl;
        poptFreeContext(popt_con);
        return EXIT_FAILURE;
    }

    if ( sparse_pixels_radius == 1 ) {
        std::cerr << "WARNING: use value of 1 to sparse pixels radius (-r)"
            " doesn't make sense" << std::endl;
    }

    try {
        Tracer::Splines splines;

        if ( output_type == VORONOI ) {
            splines
                = Tracer::Kopf2011::to_voronoi(string(input), tracingOptions());
        } else if ( output_type == GROUPED_VORONOI ) {
            splines = Tracer::Kopf2011::to_grouped_voronoi(string(input),
                                                           tracingOptions());
        } else {
            splines
                = Tracer::Kopf2011::to_splines(string(input), tracingOptions());
        }

        if ( output ) {
            ofstream out(output);
            print_svg(out, splines);
        } else {
            print_svg(cout, splines);
        }
    } catch (const Gdk::PixbufError &e) {
        cerr << "Problem while processing file:\n"
             << e.what().raw() << endl;
        poptFreeContext(popt_con);
        return EXIT_FAILURE;
    } catch (const Glib::FileError &e) {
        cerr << "Problem while accessing file:\n"
             << e.what().raw() << endl;
        poptFreeContext(popt_con);
        return EXIT_FAILURE;
    }

    // Could be freed before, but variable is still acessible...
    poptFreeContext(popt_con);
}

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
