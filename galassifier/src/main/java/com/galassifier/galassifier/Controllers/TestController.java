package com.galassifier.galassifier.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@RestController
public class TestController {
    
    @Autowired
    GalaxyClassificationController galaxyController;
    //How dowes this autowired work? how is the instance created? Spring magic? answer: yes
    // ok but...do i need to add other? No, just @Autowired is enough for spring to inject the dependency.
    //ok but if I want to "bouce" /tewstdemo to a method in GalaxyClassificationController? whgat to do? 
    // answer
    
    @GetMapping("/testdemo")
    public String testDemo() {

        System.out.println("[TESTDEMO] Endpoint called!");
        String retString = "";
        if(galaxyController != null) {          
            retString = galaxyController.DEBUG_classifyGalaxy(); // just to test the method call
            
            retString = "TestController: GalaxyClassificationController autowired successfully and method called.";    
        }
        
        return retString;
    }
}