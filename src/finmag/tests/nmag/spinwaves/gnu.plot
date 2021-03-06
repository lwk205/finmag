set lmargin 12
set rmargin 2
set grid

set multiplot title "Agreement of finmag and nmag (overview)"

#
# LOWER GRAPH - Ratios.
#

set origin 0.0, 0.0
set size   1.0, 0.4

set tmargin 0
set bmargin 3

set xlabel "time (s)"
set xrange [0:5e-12]
set xtic 0, 2e-12, 4e-12
set format x "%.0g"

set ylabel "ratio"
set yrange [-4 : 8]
set ytic -3, 3, 7
set format y "%.1f"

set nokey
plot \
    "< paste averages_ref.txt averages.txt" using 1:($2/$6), \
    "< paste averages_ref.txt averages.txt" using 1:($3/$7), \
    "< paste averages_ref.txt averages.txt" using 1:($4/$8)

#
# UPPER GRAPH - Magnetisations.
# 

set origin 0.0, 0.4
set size   1.0, 0.55 # some space on top for the page title.

set tmargin 1
set bmargin 0

set xlabel ""
set format x ""

set ylabel "polarisation"
set yrange [-0.1:1]
set ytic 0, 0.5, 1
set format y "%.1g"

set key
plot \
    "averages_ref.txt" using 1:2 title "m_x (nmag)" with lines lc rgbcolor "red", \
    "averages_ref.txt" using 1:3 title "m_y" with lines lc rgbcolor "blue", \
    "averages_ref.txt" using 1:4 title "m_z" with lines lc rgbcolor "green", \
    "averages.txt" using 1:2 title "m_x (finmag)" with points lc rgbcolor "red", \
    "averages.txt" using 1:3 title "m_y" with points lc rgbcolor "blue", \
    "averages.txt" using 1:4 title "m_z" with points lc rgbcolor "green"

unset multiplot 

pause -1
