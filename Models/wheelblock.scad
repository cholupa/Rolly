wheelbox();
rotate([0,90,0])            
    scale([1,1,1])
        translate([0,5,10])
            cylinder(20,2.8,2.8);
rotate([0,90,0])            
    scale([1,1,1])
        translate([0,-5,10])
            cylinder(20,2.8,2.8);
module wheelbox(){
    difference(){
        rotate([0,0,0])
            translate([0,0,-10])
                cube([30,30,40],center=true);
        rotate([0,90,0])
            translate([20,0,-50])
                cylinder(100,2,2);
    }
    
}