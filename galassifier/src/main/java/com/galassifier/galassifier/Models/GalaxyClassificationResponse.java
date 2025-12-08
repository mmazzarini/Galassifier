package com.galassifier.galassifier.Models;

public class GalaxyClassificationResponse {
    private String galaxyType;
    //We will see if we need other props.

    public GalaxyClassificationResponse(String galaxyType)
    {
        this.galaxyType = galaxyType;
    }

    //Get/Set
    public String getGalaxyType()
    {
        return this.galaxyType;
    }

    public void setGalaxyType(String galaxyType)
    {
        this.galaxyType = galaxyType;
    }
}



