module body(){
        //body dims
    bodyLength = 100;
    bodyHeight = 80;
    bodyDepth = 20;

    //Axles
    axLength = bodyHeight + 40;
    axr1 = 3;
    axr2 = 3;


    bodyArray = [bodyLength,bodyHeight,bodyDepth];


    difference(){

        cube(bodyArray,center=true);
        translate([0,0,5])
            cube([95,75,15],center=true);

    }
    //bottom
    difference(){
        translate([50-0.0001,-40,-10])
            cube([40,80,20]);
        rotate([90,0,0])
            translate([70,0,-60])
                cylinder(axLength,axr1,axr2);
    }
    difference(){
        //axle holes
        translate([-90+0.0001,-40,-10])
            cube([40,80,20]);
        rotate([90,0,0])
            translate([-70,0,-60])
                cylinder(axLength,axr1,axr2);
    }

}



difference(){
    body();
    cube([1,1000,100],center=true);   
    cube([1000,1,100],center=true);
    translate([0,-100,-100])
        cube([100,100,300]);
    translate([-100,0,-100])
        cube([100,100,300]);
    translate([-100,-100,-100])
        cube([100,100,300]);
}






    