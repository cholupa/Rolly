module frame(){
    // frame bottom
    scale([85,110,15])
        cube([1,1,1],center = true);
}
difference(){
    difference(){
        difference(){
            // frame bottom
            scale([85,110,15])
                cube([1,1,1],center = true);
            // frame hole
            scale([80,105,10])
                translate([0,0,0.5])
                cube([1,1,1],center = true);

        }
        cube([1000,1,100],center=true);
    }
    translate([-50,0,-20])
        cube([100,60,50]);
}

//scale([1,1,1])
//    translate([25,40,-14])
//        cylinder(10,5,5);
scale([1,1,1])
    translate([25,-40,-14])
        cylinder(10,5,5);
//scale([1,1,1])
//    translate([-25,40,-14])
//        cylinder(10,5,5);
scale([1,1,1])
    translate([-25,-40,-14])
        cylinder(10,5,5);
rotate([0,90,90])
    scale([0.5,0.5,2])
        translate([7,30,-5])
            cylinder(10,5,5);
rotate([0,90,90])
    scale([0.5,0.5,2])
        translate([7,-30,-5])
            cylinder(10,5,5);
