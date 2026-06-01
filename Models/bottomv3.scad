module frame(){
    difference(){
        difference(){
            difference(){
                // frame bottom
                scale([100,110,15])
                    cube([1,1,1],center = true);
                // frame hole
    //            scale([80,105,10])
    //                translate([0,0,0.5])
    //                cube([1,1,1],center = true);
                rotate([0,90,0])            
                    scale([1,1,1])
                        translate([0,-50,40])
                            cylinder(20,3,3);
                rotate([0,90,0])
                    scale([1,1,1])
                        translate([0,-50,-60])
                            cylinder(20,3,3);
                rotate([0,90,0])            
                    scale([1,1,1])
                        translate([0,-40,40])
                            cylinder(20,3,3);
                rotate([0,90,0])
                    scale([1,1,1])
                        translate([0,-40,-60])
                            cylinder(20,3,3);
                rotate([0,90,90])
                    scale([0.5,0.5,2])
                        translate([7,30,-5])
                            cylinder(10,5,5);
                rotate([0,90,90])
                    scale([0.5,0.5,2])
                        translate([7,-30,-5])
                            cylinder(10,5,5);


            }
            cube([1000,1,100],center=true);
        }
        translate([-600,0,-20])
            cube([1000,60,50]);
    }
        //scale([1,1,1])
    //    translate([25,40,-14])
    //        cylinder(10,5,5);
    scale([1,1,1])
        translate([25,-10,-14])
            cylinder(10,2,2);
    //scale([1,1,1])
    //    translate([-25,40,-14])
    //        cylinder(10,5,5);
    scale([1,1,1])
        translate([-25,-10,-14])
            cylinder(10,2,2);
}

frame();


module beam(){
    cube([15,110,15]);
    rotate([0,90,0])
        cube([]);
}
beam();