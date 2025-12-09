package com.galassifier.galassifier.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;

// This REST controller is for testing purposes.
// It calls a Debug version of GalaxyClassificationController that does the 
// exact same classification process but with a predefined image.

@RestController
public class TestController {
    
    @Autowired
    GalaxyClassificationController galaxyController;
    
    // Test endpoint to classify a galaxy image for debug purposes
    @GetMapping("/testdemo")
    public String testDemo() {

        System.out.println("[TESTDEMO] Endpoint called!");
        String retString = "[TESTDEMO] Empty response from /testdemo. Seomething went wrong!";

        if(galaxyController != null) {          
            retString = galaxyController.DEBUG_classifyGalaxy(); // Test method
        }
        
        return retString;
    }
}