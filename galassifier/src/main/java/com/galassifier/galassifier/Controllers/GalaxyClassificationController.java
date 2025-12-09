package com.galassifier.galassifier.Controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.galassifier.galassifier.Config.PythonClassificationConfig;
import com.galassifier.galassifier.Exceptions.PythonRuntimeException;
import com.galassifier.galassifier.MiscellaneousSandbox.MyClosureObj;
import com.galassifier.galassifier.Models.GalaxyClassificationResponse;
import com.galassifier.galassifier.Utilities.GalassifierProcessLibrary;

import org.springframework.web.bind.annotation.RequestParam;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;

//REST controller for handling galaxy classification requests

@RestController
public class GalaxyClassificationController {

    @Autowired
    private PythonClassificationConfig pythonConfig;

    @PostMapping("/classify")
    public GalaxyClassificationResponse classifyGalaxy(@RequestParam("image") MultipartFile image) {
     
        String GalaxyLabel = ProcessGalaxyPicture(image);
        GalaxyClassificationResponse ClassificationResponse = new GalaxyClassificationResponse(GalaxyLabel);
        return ClassificationResponse;
    }
    
    private String ProcessGalaxyPicture(MultipartFile image) {

        Path tempFile = null;
        
        String originalName = image.getOriginalFilename();
        String suffix = (originalName != null && originalName.contains(".")) ?
            originalName.substring(originalName.lastIndexOf('.')) : null;
        
        try{
            tempFile = Files.createTempFile("GalayTempFile", suffix);
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not create temp file...");
        }

        try {
            image.transferTo(tempFile.toFile());
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not transfer image to temp file...");
        }

        ProcessBuilder pB = new ProcessBuilder(
            pythonConfig.getPythonExe(),
            pythonConfig.getScriptPath().toString(),
            tempFile.toString(),
            pythonConfig.getMlRoot().toString()
        );

        /*
        Process process = GalassifierProcessLibrary.HandleStartProcess(pB);
        BufferedReader stdInput = GalassifierProcessLibrary.HandleStdInput(process);
        int exitCode = GalassifierProcessLibrary.HandleWaitForProcess(process);
        if(exitCode != 0)
        {
            throw new PythonRuntimeException("Python script failed with exit code: " + exitCode);
        }

        String galaxyTypeString = GalassifierProcessLibrary.HandleInputRead(stdInput); 
        GalassifierProcessLibrary.HandleInputClose(stdInput);
 */
        String galaxyTypeString = "";
        return galaxyTypeString;
    }

    // Debug method to classify galaxy without input image. Will use instead some local test image
    public String DEBUG_classifyGalaxy() {
        
        Path testImagePath = Paths.get(pythonConfig.DEBUG_getPythonImagePath().toString());
        ProcessBuilder pB = new ProcessBuilder(
            pythonConfig.getPythonExe(),
            pythonConfig.getScriptPath().toString(),
            testImagePath.toString(),
            pythonConfig.getMlRoot().toString()

        );
    
        System.out.println("COMMAND: " + pB.command());

        try(MyClosureObj myClosure = new MyClosureObj()){
            myClosure.gooGoo();
            // Just to test the AutoCloseable implementation
        }

        pB.redirectErrorStream(true); // merge error output with output
        Process process = GalassifierProcessLibrary.HandleStartProcess(pB);

        StringBuilder output = GalassifierProcessLibrary.HandleStdInput(process);
        int exitCode = GalassifierProcessLibrary.HandleWaitForProcess(process);
        String outText = output.toString().trim();
        //DEBUG 
        System.out.println(outText);
        if (exitCode != 0) {
            throw new PythonRuntimeException("Python script failed with exit code: " + exitCode);
        }
        
        
        
        return outText;
    }
}
