
//difference(){
//
//rotate([90,90,0])
//    translate([-24.5,0,0])
//        scale([56.4,30,5])
//            cube([1,1,1],center=true);
//
//rotate([90,90,0])
//    translate([-24.5,0,2.0])
//        cube([50,25,15],center=true);
//rotate([90,90,0])
//    translate([-24.5,-15,0])
//        scale([20,15,10])
//            cube([1,1,1],center=true);
//}


difference(){
    rotate([90,90,0])
        translate([-24.5,0,5])
            scale([56.4,30,5])
                cube([1,1,1],center=true);
    rotate([90,0,0])
        translate([13.5,0,2])
            cylinder(5,1,1);

    rotate([90,0,0])
        translate([13.5,50,2])
            cylinder(5,1,1);
    rotate([90,90,0])
        translate([-10.5,-5,0])
            scale([10,10,20])
            cube([1,1,1],center=true);
    rotate([90,90,0])
        translate([-37.5,-5,0])
            scale([10,10,20])
                cube([1,1,1],center=true);



}