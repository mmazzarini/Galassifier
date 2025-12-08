package com.galassifier.galassifier.Config;

import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class PythonClassificationConfig {
  
    private final Path mlRoot; 
    private final Path DEBUG_pythonImagePath;
    private final Path scriptPath;
    private final String pythonExecutable;
    
    public PythonClassificationConfig(
    @Value("${python.ml.modelpath}") String mlRootProperty,
    @Value("${python.script.path}") String scriptPathProperty,
    @Value("${python.executable}") String pythonExecutable,
    @Value("${python.debug.image.path}") String debugImagePathProperty
)   {
            this.pythonExecutable = pythonExecutable;
            this.mlRoot = Paths.get(mlRootProperty).toAbsolutePath();
            this.scriptPath = this.mlRoot.resolve(scriptPathProperty).toAbsolutePath();      
            this.DEBUG_pythonImagePath = Paths.get(debugImagePathProperty).toAbsolutePath();      
    }

    public Path getMlRoot(){ return mlRoot;}

    public Path getScriptPath(){ return scriptPath;}

    public String getPythonExe(){return pythonExecutable;}

    public Path DEBUG_getPythonImagePath(){ return DEBUG_pythonImagePath; }
}
