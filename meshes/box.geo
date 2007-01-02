R=4; 
n=20; 

lt=R/n;

Point(1) = {-R/2,-R/2,-R/2,lt};

Extrude {R,0,0} {
  Point{1}; Layers{{n}, {1}, {1}}; 
}
Extrude {0,R,0} {
  Line{1}; Layers{{n}, {0}, {1}}; Recombine;
}
Extrude {0,0,R} {
  Surface{5}; Layers{{n}, {0}, {1}}; Recombine;
}

Physical Surface(1) = {22,5,27,26,14,18};
Physical Volume(100)={1};
