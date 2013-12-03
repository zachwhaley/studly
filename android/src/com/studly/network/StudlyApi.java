package com.studly.network;

import retrofit.http.GET;

import com.studly.model.StudlyMapping;

public interface StudlyApi {

    @GET("/get-mappings.json")
    StudlyMapping.List getMappings();
}
