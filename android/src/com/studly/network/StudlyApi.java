package com.studly.network;

import retrofit.http.GET;
import retrofit.http.POST;
import retrofit.http.Query;

import com.studly.model.StudlyMapping;

public interface StudlyApi {

    @GET("/get-mappings.json")
    StudlyMapping.List getMappings();
    
    @POST("/get-mappings.json")
    StudlyMapping.List setLatLon(@Query("calendarId") String calendarId,
                                 @Query("lat") long latitude,
                                 @Query("lon") long longitude);
}
